import random
from sims.occult.occult_enums import OccultType
from sims.occult.occult_tracker import OccultTracker
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from OccultHybrid.IC_Hybrid import occult_cache
from OccultHybrid.IC_Hybrid import occult_utils
from OccultHybrid.IC_Hybrid import settings
from OccultHybrid.CoreLib.TD1_OccultHybrid_Decorator import to_decorate as inject_to
from OccultHybrid.CoreLib.TD1_OccultHybrid_Config import get_option_value
# from OccultHybrid.Modules.pelt_layer_cache import register_pelt_layers, get_pelt_layers, pelt_layer_exists_in_cache

# Importation of MasterApprentice Logger
try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Occult Tracker', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

from sims4.log import Logger

logger = Logger('TD1 Occult Tracker', default_owner='TwelfthDoctor1')


@inject_to(OccultTracker, 'has_occult_type')
def has_occult_type(original, self, occult_type):
    return occult_type == OccultType.HUMAN or original(self, occult_type) or occult_utils.sim_has_occult_trait(self.sim_info, occult_type)


@inject_to(OccultTracker, 'validate_appropriate_occult')
def validate_appropriate_occult(original, self, sim, occult_form_before_reset):
    original(self, sim, occult_form_before_reset)
    occult_utils.recalc_all(self)


@inject_to(OccultTracker, '_generate_sim_info')
def _generate_sim_info(original, self, occult_type, generate_new=True, *args, **kwargs):
    appearance_tracker = self.sim_info.appearance_tracker
    active_appearance_mods = appearance_tracker.active_displayed_appearance_modifiers()
    gen = generate_new

    logger.info(f"OCCULT TYPE: {occult_type}\nOCCULT SIM INFO: {self.get_occult_sim_info(OccultType.HUMAN)}")

    if occult_type == OccultType.HUMAN:
        gen = False

    elif self.get_occult_sim_info(OccultType.HUMAN) is None:
        original(self, OccultType.HUMAN, *args, generate_new=False, **kwargs)

    occult_types = self.sim_info.occult_types
    self.sim_info.occult_types = OccultType.HUMAN | occult_type

    logger.info(f"OCCULT TYPES: {occult_types}\nSIM INFO OCCULT TYPES: {self.sim_info.occult_types}")

    for mod in active_appearance_mods:
        mod.should_display = False

    appearance_tracker.evaluate_appearance_modifiers()
    sim_info = original(self, occult_type, *args, generate_new=gen, **kwargs)

    logger.info(f"GENERATED SIM INFO: {sim_info}")

    should_replace = False

    if occult_utils.is_custom_occult(occult_type):
        should_replace = occult_utils.get_custom_occult_info(occult_type).form_clone_human

    elif occult_utils.get_form_trait(occult_type) is None:
        should_replace = True

    if occult_type == OccultType.HUMAN:
        try:
            SimInfoBaseWrapper.copy_physical_attributes(sim_info, self.sim_info._base)
            sim_info.load_outfits(self.sim_info.save_outfits())
            sim_info.resend_physical_attributes()
            sim_info.resend_current_outfit()
        except Exception as e:
            pass

    elif gen and should_replace:
        try:
            human_form = self.get_occult_sim_info(OccultType.HUMAN)
            SimInfoBaseWrapper.copy_physical_attributes(sim_info._base, human_form)
            sim_info.load_outfits(human_form.save_outfits())
            sim_info.resend_physical_attributes()
            sim_info.resend_current_outfit()
        except Exception as e:
            pass

    for mod in active_appearance_mods:
        mod.should_display = True

    appearance_tracker.evaluate_appearance_modifiers()
    self.sim_info.occult_types = occult_types

    # if occult_type == OccultType.WEREWOLF or occult_type == OccultType.FAIRY:
    #     if master_logger is not None and master_logger is not False:
    #         master_logger.debug(
    #             f"PROCESS CHECK - PELT LAYER DATA\n"
    #             f"\n"
    #             f"{sim_info.pelt_layers}"
    #         )
    #
    #
    #     register_pelt_layers(sim_info, occult_type)
    #     self._sim_info_map[OccultType.HUMAN].pelt_layers = sim_info.pelt_layers

    return sim_info


@inject_to(OccultTracker, 'add_occult_type')
def add_occult_type(original, self: OccultTracker, occult_type):
    if occult_type == OccultType.HUMAN:
        return
    if occult_type not in OccultTracker.OCCULT_DATA:
        for occult in OccultTracker.OCCULT_DATA:
            if occult_type & occult:
                self.add_occult_type(occult)

        self.sim_info.occult_types |= OccultType.HUMAN
        return
    else:
        occult_types = self.sim_info.occult_types
        if occult_types & occult_type:
            self.sim_info.occult_types &= ~occult_type
        original(self, occult_type)
        self.sim_info.occult_types = occult_types | occult_type
        tuning = OccultTracker.OCCULT_DATA.get(occult_type)
        if tuning:
            additional_occult_traits = tuning.additional_occult_traits or []
            occult_trait = tuning.occult_trait

            if occult_trait and (not self.sim_info.has_trait(occult_trait)):
                self.sim_info.add_trait(occult_trait)
            for trait in additional_occult_traits:
                self.sim_info.add_trait(trait)

    occult_utils.on_add_occult(occult_type, self.sim_info)
    occult_utils.recalc_occult_types(self)


@inject_to(OccultTracker, 'remove_occult_type')
def remove_occult_type(original, self, occult_type):
    if occult_type == OccultType.HUMAN:
        return
    if occult_type not in OccultTracker.OCCULT_DATA:
        for occult in OccultTracker.OCCULT_DATA:
            try:
                if occult_type & occult:
                    self.remove_occult_type(occult)
            except:
                pass

        return
    else:
        sim_info = self.sim_info
        occult_trait = occult_utils.get_occult_trait(occult_type)
        if occult_trait:
            if sim_info.has_trait(occult_trait):
                sim_info.remove_trait(occult_trait)
                return
        occult_utils.remove_occult_type(original, self, occult_type)


@inject_to(OccultTracker, 'save')
def save(original, self):
    sim_info = self.sim_info
    original_occult_types = sim_info.occult_types
    original_has_form = self._occult_form_available
    sim_info.occult_types = occult_utils.get_occult_types_for_save(self)
    occult_utils.recalc_occult_form_availability(self, saving=True)
    data = original(self)
    sim_info.occult_types = original_occult_types
    self._occult_form_available = original_has_form
    return data


@inject_to(OccultTracker, 'switch_to_occult_type')
def switch_to_occult_type(original, self, occult_type):
    current_occult = self.sim_info.current_occult_types

    # if (current_occult == OccultType.WEREWOLF or current_occult == OccultType.FAIRY) and hasattr(self.sim_info, "pelt_layers"):
    #     register_pelt_layers(self.sim_info, current_occult)
    #
    # if occult_type == OccultType.WEREWOLF or occult_type == OccultType.FAIRY:
    #     if pelt_layer_exists_in_cache(self.sim_info, occult_type):
    #         self.sim_info.pelt_layers = get_pelt_layers(self.sim_info, occult_type)
    #         self.sim_info.occult_tracker._sim_info_map[occult_type] = get_pelt_layers(self.sim_info, occult_type)
    #     else:
    #         self.sim_info.pelt_layers = b""
    #         self.sim_info.occult_tracker._sim_info_map[occult_type] = b""

    if current_occult != occult_type and occult_type != OccultType.HUMAN and (current_occult != OccultType.HUMAN):
        self.sim_info.occult_types = self.sim_info.current_occult_types | OccultType.HUMAN
        original(self, OccultType.HUMAN)

    if not self.has_occult_type(occult_type):
        self.add_occult_type(occult_type)

    self.sim_info.occult_types = OccultType.HUMAN | occult_type

    if not self.get_occult_sim_info(occult_type):
        self._generate_sim_info(occult_type)

    original(self, occult_type)
    occult_utils.recalc_occult_types(self)


@inject_to(OccultTracker, '_switch_to_occult_type_internal')
def _switch_to_occult_type_internal(original, self, occult_type):
    try:
        occult_type = OccultType(occult_type)
        logger.info(f"OCCULT TYPE [{occult_type}]")
    except:
        return

    if not self.get_occult_sim_info(occult_type):
        self._generate_sim_info(occult_type)

    try:
        original(self, occult_type)
    except:
        pass

    self.sim_info.current_occult_types = occult_type

@inject_to(OccultTracker, 'apply_occult_age')
def apply_occult_age(original, self, age):
    original(self, age)
    self._update_occult_traits()
    occult_utils.recalc_all(self)


@inject_to(OccultTracker, 'post_load')
def post_load(original, self):
    if self._pending_occult_type and (not self.has_occult_type(self._pending_occult_type) or self.get_occult_sim_info(
            self._pending_occult_type) is None or (not occult_utils.sim_valid_for_occult_form(self.sim_info,
                                                                                              self._pending_occult_type))):
        self._pending_occult_type = OccultType.HUMAN

    occult_utils.recalc_all(self)
    return original(self)


@inject_to(OccultTracker, 'load')
def load(original, self, data):
    occult_cache.OccultDataCache.process_custom_occults()
    self._sim_info.occult_types = data.occult_types or OccultType.HUMAN
    self._sim_info.current_occult_types = data.current_occult_types or OccultType.HUMAN
    self._pending_occult_type = data.pending_occult_type
    self._occult_form_available = data.occult_form_available
    occult_data_map = {}
    for sim_info_data in data.occult_sim_infos:
        occult_data_map[sim_info_data.occult_type] = sim_info_data

    for occult_type in OccultType:
        if occult_type != OccultType.HUMAN and occult_type not in self.OCCULT_DATA:
            self._sim_info.occult_types &= ~occult_type
            self._sim_info.occult_types &= ~occult_type
            if self._sim_info.current_occult_types == occult_type:
                self._sim_info.current_occult_types = OccultType.HUMAN
            elif self._pending_occult_type == occult_type:
                self._pending_occult_type = None
            logger.info(f"SIM INFO OCCULT TYPES: {self._sim_info.occult_types}\nCURRENT OCCULT TYPES: {self._sim_info.current_occult_types}\nPENDING: {self._pending_occult_type}")
        else:
            if occult_type in occult_data_map:
                sim_info_data = occult_data_map[occult_type]
                sim_info = self._generate_sim_info((sim_info_data.occult_type), generate_new=False)

                logger.info(f"SIM INFO: {sim_info}\\nOCCULT TYPE: {sim_info_data.occult_type}\nBASE: {self._sim_info._base}")

                if occult_type == self._sim_info.current_occult_types:
                    SimInfoBaseWrapper.copy_physical_attributes(sim_info_data, self._sim_info._base)
                else:
                    sim_info.load_outfits(sim_info_data.outfits)
                    SimInfoBaseWrapper.copy_physical_attributes(sim_info._base, sim_info_data)
            if occult_type != OccultType.HUMAN:
                if self.has_occult_type(occult_type):
                    if occult_type == self._sim_info.current_occult_types:
                        self._generate_sim_info(occult_type, generate_new=False)

    return original(self, data)


def add_occult(occult_tracker: OccultTracker, occult_type, occult_tuning=None):
    if not occult_tuning:
        occult_tuning = OccultTracker.OCCULT_DATA.get(occult_type)
    if not occult_tuning or (occult_tuning.part_occult_trait is not None and occult_tracker.sim_info.has_trait(occult_tuning.part_occult_trait)):
        if occult_tuning.part_occult_trait is not None:
            if occult_tracker.sim_info.has_trait(occult_tuning.part_occult_trait):
                occult_tracker.sim_info.remove_trait(occult_tuning.part_occult_trait)
        occult_tracker.add_occult_type(occult_type)


def add_part_occult(occult_tracker: OccultTracker, occult_type, occult_tuning=None):
    if occult_tracker.has_occult_type(occult_type):
        return
    if not occult_tuning:
        occult_tuning = OccultTracker.OCCULT_DATA.get(occult_type)

    if occult_tuning and occult_tuning.part_occult_trait is not None:
        occult_tracker.sim_info.add_trait(occult_tuning.part_occult_trait)


@inject_to(OccultTracker, 'apply_occult_genetics')
def apply_occult_genetics(original, self: OccultTracker, parent_a, parent_b, seed, **kwargs):
    if settings.ALLOW_HYBRID_BABIES and self.has_any_occult_or_part_occult_trait() and get_option_value("allow_hybrid_babies"):
        rng = random.Random(seed)
        for occult, tuning in OccultTracker.OCCULT_DATA.items():
            if self.has_occult_type(occult):
                continue
            occult_count = 0
            part_occult_count = 0
            for parent in [parent_a, parent_b]:
                if parent.occult_tracker.has_occult_type(occult):
                    occult_count += 1
                    part_occult_count = 2
                elif tuning.part_occult_trait is not None and parent.has_trait(tuning.part_occult_trait):
                    part_occult_count += 1
            occult_result = rng.randint(0, 99)
            part_result = rng.randint(0, 99)
            occult_chance = 50 * occult_count
            part_occult_chance = 50 * part_occult_count
            if occult_result < occult_chance:
                add_occult(self, occult, tuning)
            elif part_result < part_occult_chance:
                add_part_occult(self, occult, tuning)
    return original(self, parent_a, parent_b, seed, **kwargs)
