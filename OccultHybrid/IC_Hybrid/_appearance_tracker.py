from buffs.appearance_modifier.appearance_modifier_type import AppearanceModifierType
from buffs.appearance_modifier.appearance_tracker import AppearanceTracker
from cas.cas import get_caspart_bodytype
from sims.occult.occult_enums import OccultType
from sims.outfits.outfit_enums import BodyTypeFlag, BodyType
from OccultHybrid.CoreLib.TD1_OccultHybrid_Decorator import to_decorate as inject_to
from sims4.log import Logger

# Importation of MasterApprentice Logger
try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Appearance Tracker', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger("TD1 Appearance Tracker", default_owner="TwelfthDoctor1")


@inject_to(AppearanceTracker, 'evaluate_appearance_modifiers')
def evaluate_appearance_modifiers(original, self):
    try:
        # Get current occult types
        current_occult_types = getattr(self._sim_info, 'current_occult_types', OccultType.HUMAN)

        # if either current occult type equals human OR sim has occult types then INVERSE
        if current_occult_types == OccultType.HUMAN or not hasattr(self._sim_info, 'occult_types'):
            logger.info(f"FAIL: OCCULT IS HUMAN OR HAS NO OCCULT TYPES")
            return original(self)

        occults = self._sim_info.occult_types
        self._sim_info.occult_types = OccultType.HUMAN | current_occult_types

        logger.info(f"SIM INFO: {self._sim_info}\nOCCULT [1]: {self._sim_info.occult_types}\nOCCULT [2]: {occults}\n")

        original(self)
        self._sim_info.occult_types = occults
    except Exception as e:
        logger.error(f"ERROR: {e}")


@inject_to(AppearanceTracker, 'apply_appearance_modifiers')
def apply_appearance_modifiers(original, self, modifiers_to_apply: list, sim_info, is_permanent_modification=False, should_refresh_thumbnail=False):
    current_occult_types = getattr(sim_info, 'current_occult_types', OccultType.HUMAN)
    modifiers_to_remove = []
    logger.info(f"APPLY APPEARANCE MODS -> IS MERMAID [{current_occult_types == OccultType.MERMAID}]")
    if current_occult_types == OccultType.MERMAID:
        try:
            restricted_modifier_types = {
             AppearanceModifierType.SET_CAS_PART,
             AppearanceModifierType.RANDOMIZE_CAS_PART
            }
            restricted_cas_flags = {
             BodyType.SHOES,
             BodyType.SOCKS,
             BodyType.FULL_BODY
            }
            for mod in modifiers_to_apply:
                if mod.modifier.modifier_type in restricted_modifier_types:
                    part_flags = BodyTypeFlag.make_body_type_flag(get_caspart_bodytype(mod.modifier.cas_part))
                    for flag in restricted_cas_flags:
                        if part_flags & flag:
                            modifiers_to_remove.append(mod)
                            break

        except:
            pass

        for mod in modifiers_to_remove:
            try:
                if mod in modifiers_to_apply:
                    modifiers_to_apply.remove(mod)
            except:
                pass

    try:
        logger.info(f"TRY PASS TO ORIG FUNC:\nMODS TO APPLY: {modifiers_to_apply}\nSIM INFO: {sim_info}\nIS PERM MOD: {is_permanent_modification}\nSHOULD REF: {should_refresh_thumbnail}\n")
        return original(self, modifiers_to_apply, sim_info, is_permanent_modification, should_refresh_thumbnail)
    except:
        pass
