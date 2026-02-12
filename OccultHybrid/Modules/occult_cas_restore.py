import services
from OccultHybrid.IC_Hybrid.injector import inject_to
from OccultHybrid.IC_Hybrid.commands import occult_map_cache
from OccultHybrid.CoreLib.TD1_OccultHybrid_Config import get_option_value
# from OccultHybrid.Modules.pelt_layer_cache import register_pelt_layers
from sims.occult.occult_enums import OccultType
from sims.occult.occult_tracker import OccultTracker
from sims.sim_info_manager import SimInfoManager
from sims4.resources import Types
# from sims4.log import Logger
#
# logger = Logger('TD1 Occult Hybrid CAS Restorer Handler', default_owner='TwelfthDoctor1')

# Importation of MasterApprentice Logger
# try:
#     from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger
#
#     apprentice_logger = ApprenticeLogger('TD1 Occult Hybrid CAS Restorer Handler', main_owner='TwelfthDoctor1')
#
# except ImportError:
#     apprentice_logger = False
#
# try:
#     from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger
#
#     master_logger = MasterLogger('TD1 Occult Hybrid CAS Restorer Handler', main_owner='TwelfthDoctor1')
#
# except ImportError:
#     master_logger = False

occult_memory_traits = {
    OccultType.ALIEN: 16768010466321094980,
    OccultType.VAMPIRE: 11440349392908825663,
    OccultType.MERMAID: 17158874848357145152,
    OccultType.WITCH: 11287859092209813903,
    OccultType.WEREWOLF: 12351341566375713428,
    OccultType.FAIRY: 18197032510434408842
}


def process_sim(sim_info):
    occult_tracker = sim_info.occult_tracker

    # Ref & Use old Map
    new_form_map = occult_tracker._sim_info_map.copy()
    old_cache = occult_map_cache.get(sim_info.id)
    # old_cache[OccultType.HUMAN] = new_form_map[OccultType.HUMAN]
    # old_cache[occult_edit_cache] = new_form_map[occult_map_cache]

    # if master_logger is not None and master_logger is not False:
    #     master_logger.debug(
    #         f"PROCESS - OLD & NEW SIM OCCULT MAP\n"
    #         f"Name: {sim_info.first_name} {sim_info.last_name}\n"
    #         f"\n"
    #         f"OLD MAP: {old_cache}\n"
    #         f"MAP TO REPLACE: {new_form_map}\n"
    #     )
    #
    # if apprentice_logger is not None and apprentice_logger is not False:
    #     apprentice_logger.info(
    #         f"PROCESS - OLD & NEW SIM OCCULT MAP\n"
    #         f"Name: {sim_info.first_name} {sim_info.last_name}\n"
    #         f"\n"
    #         f"OLD MAP: {old_cache}\n"
    #         f"MAP TO REPLACE: {new_form_map}\n"
    #     )

    # logger.info(
    #     f"PROCESS - OLD & NEW SIM OCCULT MAP\n"
    #     f"Name: {sim_info.first_name} {sim_info.last_name}\n"
    #     f"\n"
    #     f"OLD MAP: {old_cache}\n"
    #     f"MAP TO REPLACE: {new_form_map}\n"
    # )

    # Handle Memory Traits
    for occult, tuning in OccultTracker.OCCULT_DATA.items():
        # Skip Occult to edit or Human Occult
        if occult == OccultType.HUMAN or occult_tracker.has_occult_type(occult):
            continue

        for k, v in occult_memory_traits.items():
            if k == occult:
                memory_trait = services.get_instance_manager(Types.TRAIT).get(v)
                if sim_info.has_trait(memory_trait):
                    sim_info.remove_trait(memory_trait)
                    sim_info.add_trait(tuning.occult_trait)
                    # add_occult_type(occult, OptionalTargetParam(str(sim_info.id)))
                    if k == OccultType.WITCH:
                        continue
                    else:
                        new_form_map[occult] = old_cache[occult]
                # else:
                #     if occult == OccultType.WEREWOLF or occult == OccultType.FAIRY and hasattr(sim_info, "pelt_layers"):
                #         register_pelt_layers(sim_info, occult)

    occult_tracker._sim_info_map.update(new_form_map)

    # if master_logger is not None and master_logger is not False:
    #     master_logger.debug(
    #         f"PROCESS - OLD & NEW SIM OCCULT MAP\n"
    #         f"Name: {sim_info.first_name} {sim_info.last_name}\n"
    #         f"\n"
    #         f"REPLACED MAP: {new_form_map}\n"
    #     )
    #
    # if apprentice_logger is not None and apprentice_logger is not False:
    #     apprentice_logger.info(
    #         f"PROCESS - OLD & NEW SIM OCCULT MAP\n"
    #         f"Name: {sim_info.first_name} {sim_info.last_name}\n"
    #         f"\n"
    #         f"REPLACED MAP: {new_form_map}\n"
    #     )

    # logger.info(
    #     f"PROCESS - OLD & NEW SIM OCCULT MAP\n"
    #     f"Name: {sim_info.first_name} {sim_info.last_name}\n"
    #     f"\n"
    #     f"REPLACED MAP: {new_form_map}\n"
    # )


@inject_to(SimInfoManager, 'on_loading_screen_animation_finished')
def cas_restore_occult_to_sim_on_load(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)

    try:
        if get_option_value("post_cas_occult_autoadd"):
            for sim_info in services.sim_info_manager().get_all():
                if sim_info.sim_id in occult_map_cache:
                    process_sim(sim_info)

    except Exception as e:
        # logger.info(f"Error found with Occult CAS Restorer Process by TwelfthDoctor1: {str(e)}")
        raise Exception(f"Error found with Occult CAS Restorer Process by TwelfthDoctor1: {str(e)}")

    return result
