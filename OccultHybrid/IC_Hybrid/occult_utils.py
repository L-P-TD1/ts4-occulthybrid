from bucks.bucks_commands import lock_all_perks_for_bucks_type
from bucks.bucks_enums import BucksType
from event_testing.resolver import SingleSimResolver
from sims.occult.occult_enums import OccultType
from sims.occult.occult_tracker import OccultTracker
from sims.sim_info_base_wrapper import SimInfoBaseWrapper
from OccultHybrid.IC_Hybrid.occult_cache import OccultDataCache
from OccultHybrid.IC_Hybrid import settings
from OccultHybrid.CoreLib.TD1_OccultHybrid_Config import get_option_value
from sims4.log import Logger

# Importation of MasterApprentice Logger
try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Occult Utils', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Occult Utils', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger("TD1 Occult Utils", default_owner="TwelfthDoctor1")

occult_list = [
    OccultType.HUMAN,
    OccultType.ALIEN,
    OccultType.ALIEN | OccultType.HUMAN,
    OccultType.VAMPIRE,
    OccultType.VAMPIRE | OccultType.HUMAN,
    OccultType.MERMAID,
    OccultType.MERMAID | OccultType.HUMAN,
    OccultType.WITCH,
    OccultType.WITCH | OccultType.HUMAN,
    OccultType.WEREWOLF,
    OccultType.WEREWOLF | OccultType.HUMAN
]


def is_sim_hybrid_occult(sim_info):
    occult_count = 0
    for occult in OccultTracker.OCCULT_DATA:
        if occult != OccultType.HUMAN and sim_has_occult_trait(sim_info, occult):
            occult_count += 1

    return occult_count > 1


def sim_valid_for_occult_form(sim_info, occult_type):
    if occult_type == OccultType.HUMAN:
        return True
    try:
        trait = get_form_trait(occult_type)
        trait_tracker = sim_info.trait_tracker
        return trait is not None and sim_info.has_trait(trait) or (trait.is_valid_trait(sim_info) and (not trait_tracker.is_conflicting(trait)))
    except:
        return False


def is_required_occult_form(occult_type, tuning=None):
    if tuning is None:
        try:
            tuning = OccultTracker.OCCULT_DATA[occult_type]
        except KeyError:
            return False

    if is_custom_occult(occult_type):
        return True
    return tuning.current_occult_trait is not None and not tuning.cas_can_delete_alternative_form


def required_occult_forms_gen():
    for occult_type, tuning in OccultTracker.OCCULT_DATA.items():
        if is_required_occult_form(occult_type, tuning=tuning):
            yield occult_type


def has_required_occult_form(occult_tracker):
    for occult_type in required_occult_forms_gen():
        if sim_valid_for_occult_form(occult_tracker._sim_info, occult_type) and occult_tracker.has_occult_type(
                occult_type):
            return True

    return False


def sim_has_occult_trait(sim_info, occult_type):
    trait = get_occult_trait(occult_type)
    if trait and sim_info.has_trait(trait):
        return True
    return False


def get_occult_trait(occult_type):
    try:
        trait = OccultTracker.OCCULT_DATA[occult_type].occult_trait
        return trait
    except:
        return None


def get_form_trait(occult_type):
    try:
        trait = OccultTracker.OCCULT_DATA[occult_type].current_occult_trait
        return trait
    except:
        return None


def get_human_form_occult_types(sim_info):
    found_xp_stat = False
    final_occult_type = OccultType.HUMAN
    for occult_type, tuning in OccultTracker.OCCULT_DATA.items():
        if sim_has_occult_trait(sim_info, occult_type):
            if final_occult_type == OccultType.HUMAN or not found_xp_stat or (
                    not tuning.current_occult_trait and tuning.experience_statistic):
                final_occult_type = OccultType.HUMAN | occult_type
                found_xp_stat = tuning.experience_statistic is not None

    return final_occult_type


def recalc_occult_types(occult_tracker):
    sim_info = occult_tracker._sim_info
    final_occult_type = sim_info.current_occult_types

    occult_tuning = OccultTracker.OCCULT_DATA.get(final_occult_type)

    logger.info(f"SIM INFO: {sim_info}\nFINAL OCCULT TYPE: {final_occult_type}\nOCCULT TUNING: {occult_tuning}")

    if final_occult_type == OccultType.HUMAN:
        final_occult_type = get_human_form_occult_types(sim_info)
        logger.info(f"FINAL OCC TYPE HUMAN: {final_occult_type}")

    elif not occult_tuning or not occult_tuning.experience_statistic:
        new_occult_type = OccultType.HUMAN
        for occult, tuning in OccultTracker.OCCULT_DATA.items():
            if not sim_info.occult_tracker.has_occult_type(occult):
                logger.info(f"OCCULT ({occult}) != FINAL_OCCULT")
                continue
            if tuning.experience_statistic:
                new_occult_type = occult
                logger.info(f"OCCULT {occult} HAS XP STAT")
                break
                continue
            if new_occult_type == OccultType.HUMAN:
                new_occult_type = occult
        final_occult_type = new_occult_type

    sim_info.occult_types = final_occult_type | OccultType.HUMAN
    logger.info(f"FINAL RESULT: {final_occult_type}\nSIM INFO OCCULT TYPES: {sim_info.occult_types}\n")


def recalc_occult_form_availability(occult_tracker, saving=False):
    sim_info = occult_tracker.sim_info
    logger.info(f"RECALC OCCULT FORM AVAILABILITY -> SAVING: {saving}")
    if saving:
        if sim_info.occult_types == OccultType.HUMAN:
            occult_tracker._occult_form_available = False
            logger.info("SIM IS ONLY HUMAN OCCULT.")
            return
        for occult, tuning in OccultTracker.OCCULT_DATA.items():
            if sim_info.occult_types == OccultType.HUMAN | occult or sim_info.occult_types == occult:
                if tuning.current_occult_trait is not None:
                    occult_tracker._occult_form_available = occult_tracker.get_occult_sim_info(occult) is not None
                else:
                    occult_tracker._occult_form_available = False
                logger.info(f"UPDATE OCCULT FORM AVAILABLE: {occult_tracker._occult_form_available}")
                break
            return None

    else:
        occult_tracker._occult_form_available = False
        has_optional_occult = False
        for occult, tuning in OccultTracker.OCCULT_DATA.items():
            if not occult_tracker.has_occult_type(occult) or is_custom_occult(occult):
                continue
            if tuning.current_occult_trait is not None and tuning.cas_can_delete_alternative_form:
                logger.info(f"CURRENT OCCULT TRAIT NOT NONE [{tuning.current_occult_trait}] & CAN DELETE ALT FORM [{tuning.cas_can_delete_alternative_form}] -> HAS OPTIONAL OCCULT")
                has_optional_occult = True
                if not occult_tracker._occult_form_available:
                    occult_tracker._occult_form_available = occult_tracker.get_occult_sim_info(occult) is not None
                    logger.info(f"UPDATE OCCULT FORM AVAILABLE: {occult_tracker._occult_form_available}")
                else:
                    logger.info(f"OCCULT FORM AVAILABLE FAILURE")
                    break

        if not occult_tracker._occult_form_available and (not has_optional_occult) and (not saving):
            occult_tracker._occult_form_available = has_required_occult_form(occult_tracker)


def recalc_all(occult_tracker):
    if not exit_invalid_forms(occult_tracker):
        cleanup_occult_exit_traits(occult_tracker)
        recalc_occult_types(occult_tracker)
        recalc_occult_form_availability(occult_tracker)
        remove_traits(occult_tracker)
        # handle_occult_reprocess(occult_tracker)


def remove_traits(occult_tracker):
    sim_info = occult_tracker._sim_info
    for occult in OccultTracker.OCCULT_DATA:
        if occult == OccultType.HUMAN:
            continue
        if not occult_tracker.has_occult_type(occult):
            traits_to_remove = OccultDataCache.occult_removal_traits.get(occult, [])
            for trait in traits_to_remove:
                if sim_info.has_trait(trait):
                    sim_info.remove_trait(trait)


def get_occult_types_for_save(occult_tracker):
    sim_info = occult_tracker.sim_info
    occult_types = occult_tracker.sim_info.occult_types
    if sim_info.current_occult_types != OccultType.HUMAN:
        occult_types = OccultType.HUMAN | sim_info.current_occult_types
    else:
        for occult in OccultTracker.OCCULT_DATA:
            if occult_types == occult or occult_types & occult:
                if not is_custom_occult(occult) or get_custom_occult_info(occult).menu_allow_modify_in_cas_picker:
                    occult_types = occult | OccultType.HUMAN

    return occult_types


def cleanup_occult_exit_traits(occult_tracker):
    sim_info = occult_tracker._sim_info
    for occult, traits in OccultDataCache.occult_exit_traits.items():
        if occult == sim_info.current_occult_types:
            continue
        try:
            for trait in traits:
                sim_info.remove_trait(trait)

        except:
            pass


def validate_occult_type(occult_type):
    if occult_type != OccultType.HUMAN and occult_type not in OccultTracker.OCCULT_DATA:
        return False
    return True


def get_all_active_occult_types(occult_tracker):
    result = OccultType.HUMAN
    for occult_type in OccultTracker.OCCULT_DATA:
        if sim_has_occult_trait(occult_tracker._sim_info, occult_type):
            result |= occult_type

    return result


def remove_occult_type(original_function, occult_tracker, occult_type):
    sim_info = occult_tracker._sim_info
    all_occults = get_all_active_occult_types(occult_tracker) | occult_type
    occults_to_keep = all_occults & ~occult_type
    sim_info.occult_types = occults_to_keep
    current_occult = sim_info.current_occult_types
    if current_occult != OccultType.HUMAN:
        occult_tracker.switch_to_occult_type(OccultType.HUMAN)
    old_map = {}
    if settings.OCCULT_FORM_MEMORY and get_option_value("occult_form_memory"):
        old_map = occult_tracker._sim_info_map.copy()
        occult_tracker._generate_sim_info(OccultType.HUMAN, generate_new=False)
    try:
        sim_info.occult_types = all_occults | occult_type
        original_function(occult_tracker, occult_type)
    except:
        pass
    if settings.OCCULT_FORM_MEMORY and get_option_value("occult_form_memory"):
        occult_tracker._sim_info_map.update(old_map)
        if OccultType.HUMAN in old_map:
            human_form = old_map[OccultType.HUMAN]
            SimInfoBaseWrapper.copy_physical_attributes(sim_info._base, human_form)
            sim_info.load_outfits(human_form.save_outfits())
            sim_info.appearance_tracker.evaluate_appearance_modifiers()
            sim_info.resend_physical_attributes()
            sim_info.resend_current_outfit()
            sim_info.force_resend_suntan_data()
    if sim_info.current_occult_types != current_occult and occult_tracker.has_occult_type(current_occult) and (
            occult_tracker.get_occult_sim_info(current_occult) is not None) and (current_occult != OccultType.HUMAN):
        occult_tracker.switch_to_occult_type(current_occult)
    tuning = OccultTracker.OCCULT_DATA.get(occult_type)
    if tuning:
        try:
            if tuning.primary_buck_type is not BucksType.INVALID:
                lock_all_perks_for_bucks_type(tuning.primary_buck_type, sim_info.id, True)
        except:
            pass
        try:
            if tuning.secondary_buck_type is not BucksType.INVALID:
                lock_all_perks_for_bucks_type(tuning.secondary_buck_type, sim_info.id, True)
        except:
            pass
    recalc_all(occult_tracker)


def exit_invalid_forms(occult_tracker):
    sim_info = occult_tracker._sim_info
    for occult, tuning in OccultTracker.OCCULT_DATA.items():
        if is_sim_in_form(sim_info, occult):
            if not sim_valid_for_occult_form(sim_info, occult):
                trait = get_form_trait(occult)
                sim_info.remove_trait(trait)
                return True

    return False


def on_add_occult(occult_type, sim_info):
    if occult_type in OccultDataCache.occult_add_actions:
        try:
            resolver = SingleSimResolver(sim_info)
            for action in OccultDataCache.occult_add_actions[occult_type]:
                action.apply_to_resolver(resolver)

        except:
            pass


def is_custom_occult(occult_type):
    return occult_type != OccultType.HUMAN and occult_type in OccultDataCache.custom_occults


def get_custom_occult_info(occult_type) -> OccultDataCache.CustomOccultData:
    return OccultDataCache.custom_occults.get(occult_type)


def is_sim_in_form(sim_info, occult_type):
    if occult_type == OccultType.HUMAN:
        for occult, tuning in OccultTracker.OCCULT_DATA.items():
            if tuning.current_occult_trait is not None:
                if sim_info.has_trait(tuning.current_occult_trait):
                    return False
        return True
    else:
        trait = get_form_trait(occult_type)
        if trait is None:
            return False
        return sim_info.has_trait(trait)
