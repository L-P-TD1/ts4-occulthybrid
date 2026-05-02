import services
from OccultHybrid.IC_Hybrid.occult_cache import OccultDataCache
from server_commands.argument_helpers import get_optional_target, OptionalTargetParam, OptionalSimInfoParam, TunableInstanceParam
from services import client_manager
from sims.occult.occult_enums import OccultType
from sims.occult.occult_tracker import OccultTracker
from sims.outfits.outfit_enums import OutfitCategory
from sims4.commands import CommandRestrictionFlags, CommandType, Command, client_cheat, CheatOutput, Output
from sims4.common import Pack
from sims4.resources import Types
from sims4.log import Logger
from OccultHybrid.IC_Hybrid import occult_utils
# from OccultHybrid.Modules.pelt_layer_cache import get_pelt_layers, register_pelt_layers, pelt_layer_exists_in_cache

try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Occult Hybrid Commands', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Occult Hybrid Commands', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False


logger = Logger('TD1 Hybrid Commands', default_owner='TwelfthDoctor1')

occult_memory_traits = {
    OccultType.ALIEN: 16768010466321094980,
    OccultType.VAMPIRE: 11440349392908825663,
    OccultType.MERMAID: 17158874848357145152,
    OccultType.WITCH: 11287859092209813903,
    OccultType.WEREWOLF: 12351341566375713428,
    OccultType.FAIRY: 18197032510434408842
}

FAIRY_ADD_WING_LOOT = 425309

FAIRY_REMOVE_WING_LOOT = 425310

occult_map_cache = dict()

occult_edit_cache = None

VAMPIRE_MANUAL_DARK_FORM_TRAIT = 156397


def remove_conflicting_traits(sim_info, trait_to_check, output=None):
    trait_tracker = sim_info.trait_tracker
    if trait_tracker.is_conflicting(trait_to_check):
        if output:
            output('Sim has conflicting trait!')
        traits_to_remove = []
        for trait in trait_tracker.equipped_traits:
            if trait.is_conflicting(trait_to_check):
                traits_to_remove.append(trait)

        for trait in traits_to_remove:
            sim_info.remove_trait(trait)
            if output:
                output('Removed conflicting trait: {}'.format(trait))


@Command('iced_cream.hybrid.commands.edit_form_in_cas', command_type=(CommandType.Live), command_restrictions=(CommandRestrictionFlags.RESTRICT_SAVE_UNLOCKED))
def edit_form_in_cas(occult_type: OccultType=OccultType.HUMAN, opt_sim: OptionalTargetParam=None, _connection=None):
    if not _connection:
        _connection = client_manager().get_first_client_id()
    output = CheatOutput(_connection)
    sim = get_optional_target(opt_sim, _connection)
    if sim is None:
        output('No valid sim specified for iced_cream.hybrid.commands.edit_form_in_cas')
        return False
    if occult_type != OccultType.HUMAN:
        if occult_type not in OccultTracker.OCCULT_DATA:
            output('invalid occult type specified - ' + str(occult_type))
            return False


    global occult_edit_cache
    occult_edit_cache = occult_type

    def process_sim(sim_info, force_form=False):
        occult_tracker = sim_info.occult_tracker

        # Post Caching Switch to Final Occult
        if occult_tracker.has_occult_type(occult_type):
            previous_occult_types = sim_info.current_occult_types
            if previous_occult_types != occult_type:
                if previous_occult_types != OccultType.HUMAN:
                    occult_tracker.switch_to_occult_type(OccultType.HUMAN)
                if force_form:
                    if occult_utils.sim_valid_for_occult_form(sim_info, occult_type):
                        occult_tracker.switch_to_occult_type(occult_type)
                        sim_info.current_occult_types = occult_type
            occult_tracker.set_pending_occult_type(previous_occult_types)
            sim_info.occult_types = occult_type | OccultType.HUMAN

        # Cache Old Map
        cache_map = occult_tracker._sim_info_map.copy()
        occult_map_cache.update({sim_info.id : cache_map})

        if master_logger is not None and master_logger is not False:
            master_logger.debug(
                f"PROCESS - CACHE SIM OCCULT MAP\n"
                f"Name: {sim_info.first_name} {sim_info.last_name}\n"
                f"\n"
                f"MAP: {cache_map}\n"
            )

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info(
                f"PROCESS - CACHE SIM OCCULT MAP\n"
                f"Name: {sim_info.first_name} {sim_info.last_name}\n"
                f"\n"
                f"MAP: {cache_map}\n"
            )

        # if master_logger is not None and master_logger is not False:
        #     master_logger.info(
        #         f"PROCESS - ARCHIVE & TRANSFER PELT LAYERS\n"
        #         f"Name: {sim_info.first_name} {sim_info.last_name}\n"
        #         f"\n"
        #         f"OCCULT: {occult_type}\n"
        #         f"VALUE: {sim_info.pelt_layers}\n"
        #         f"HAS ATTR: {hasattr(sim_info, 'pelt_layers')}\n"
        #         f"HAS CACHE DATA: {pelt_layer_exists_in_cache(sim_info, occult_type)}\n"
        #     )
        #
        # # Handle Pelt Layers
        # if (occult_type == OccultType.WEREWOLF or occult_type == OccultType.FAIRY) and hasattr(sim_info, "pelt_layers") and pelt_layer_exists_in_cache(sim_info, occult_type):
        #     sim_info.pelt_layers = get_pelt_layers(sim_info, occult_type)
        #     occult_tracker._sim_info_map[OccultType.HUMAN].pelt_layers = get_pelt_layers(sim_info, occult_type)

        # Handle Memory Traits
        for occult, tuning in OccultTracker.OCCULT_DATA.items():
            # Skip Occult to edit or Human Occult
            if occult == occult_type or occult == OccultType.HUMAN:
                continue

            if occult_tracker.has_occult_type(occult):
                for k, v in occult_memory_traits.items():
                    if k == occult:
                        memory_trait = services.get_instance_manager(Types.TRAIT).get(v)
                        sim_info.add_trait(memory_trait)
                        sim_info.remove_trait(tuning.occult_trait)
                        # delete_form(occult, OptionalTargetParam(str(sim_info.id)))

    solo = occult_utils.is_custom_occult(occult_type)
    if solo:
        sim_info = sim.sim_info
        occult_tracker = sim_info.occult_tracker
        process_sim(sim_info, True)
        occult_tracker._occult_form_available = True
    else:
        household = sim.sim_info.household
        for household_sim in household.get_humans_gen():
            process_sim(household_sim.sim_info)

    if not solo:
        client_cheat('sims.exit2caswithhouseholdid {} {} gender'.format(sim.id, sim.household_id), _connection)
    else:
        client_cheat('sims.exit2caswithhouseholdid {} {} disguise'.format(sim.id, sim.household_id), _connection)
    return True


@Command('iced_cream.hybrid.commands.set_occult_type', command_type=(CommandType.Live), command_restrictions=(CommandRestrictionFlags.UNRESTRICTED))
def set_occult_type(occult_type: OccultType=OccultType.HUMAN, opt_sim: OptionalTargetParam=None, _connection=None):
    output = CheatOutput(_connection)
    sim = get_optional_target(opt_sim, _connection)
    if sim is None:
        output('No valid sim specified for iced_cream.hybrid.commands.set_occult_type')
        return False
    sim_info = sim.sim_info
    if not sim_info.occult_tracker.has_occult_type(occult_type):
        output('Sim does not have the specified occult type - {}'.format(str(occult_type)))
        return False
    sim_info.occult_types = int(occult_type) | int(OccultType.HUMAN)
    return True


@Command('iced_cream.hybrid.commands.switch_to_occult', command_type=(CommandType.Live), command_restrictions=(CommandRestrictionFlags.UNRESTRICTED))
def switch_to_occult(occult_type: OccultType=OccultType.HUMAN, opt_sim: OptionalTargetParam=None, _connection=None):
    output = CheatOutput(_connection)
    sim = get_optional_target(opt_sim, _connection)
    if sim is None:
        output('No valid sim specified for iced_cream.hybrid.commands.switch_to_occult')
        return False
    sim_info = sim.sim_info
    occult_tracker = sim_info.occult_tracker
    if occult_type != OccultType.HUMAN:
        occult_data = OccultTracker.OCCULT_DATA.get(occult_type)
        if not occult_data:
            output('Invalid occult type specified. Exiting...')
            return False
        if not occult_data.current_occult_trait:
            output('Occult type has no form... Exiting...')
            return False
        if not sim_info.occult_tracker.has_occult_type(occult_type):
            output('Adding occult')
            occult_tracker.add_occult_type(occult_type)
        if not occult_utils.sim_valid_for_occult_form(sim_info, occult_type):
            output('Sim not valid for form.. Exiting...')
            return False
        output('Switching to occult')
        occult_tracker.switch_to_occult_type(occult_type)
        return True


@Command('iced_cream.hybrid.commands.remove_conflicting_traits_for_occult_type', command_type=(CommandType.Live), command_restrictions=(CommandRestrictionFlags.UNRESTRICTED))
def remove_conflicting_traits_for_occult_type(occult_type: OccultType=OccultType.HUMAN, opt_sim: OptionalTargetParam=None, _connection=None):
    output = CheatOutput(_connection)
    sim = get_optional_target(opt_sim, _connection)
    if sim is None:
        output('No valid sim specified for iced_cream.hybrid.commands.remove_conflicting_traits_for_occult_type')
        return False
    occult_tuning = OccultTracker.OCCULT_DATA.get(occult_type)
    if not occult_tuning:
        output('No tuning found for specified occult')
        return False
    conflicts_to_remove = [occult_tuning.occult_trait]
    sim_info = sim.sim_info
    for trait in conflicts_to_remove:
        remove_conflicting_traits(sim_info, trait, output)

    return True


@Command('iced_cream.hybrid.commands.add_occult_type', command_type=(CommandType.Live), command_restrictions=(CommandRestrictionFlags.UNRESTRICTED))
def add_occult_type(occult_type: OccultType=OccultType.HUMAN, opt_sim: OptionalTargetParam=None, _connection=None):
    output = CheatOutput(_connection)
    sim = get_optional_target(opt_sim, _connection)
    if sim is None:
        output('No valid sim specified for iced_cream.hybrid.commands.remove_conflicting_traits_for_occult_type')
        return False
    remove_conflicting_traits_for_occult_type(occult_type, sim, _connection)
    sim.sim_info.occult_tracker.add_occult_type(occult_type)
    occult_utils.recalc_all(sim.sim_info.occult_tracker)
    return True


@Command('cas.plan_batuu_outfit', pack=(Pack.GP09), command_type=(CommandType.Live), command_restrictions=(CommandRestrictionFlags.RESTRICT_SAVE_UNLOCKED))
def plan_batuu_outfit(opt_sim: OptionalSimInfoParam=None, _connection=None):
    output = CheatOutput(_connection)
    sim = get_optional_target(opt_sim, _connection, target_type=OptionalSimInfoParam)
    if sim is None:
        output('No valid target specified.')
        return False
    if not sim.has_outfit_category(OutfitCategory.BATUU):
        return False
    for sim_info in sim.household.get_humans_gen():
        if sim_info.occult_tracker:
            sim_info.occult_tracker.set_pending_occult_type(sim_info.current_occult_types)
            sim_info.occult_tracker.switch_to_occult_type(OccultType.HUMAN)

    client_cheat('sims.exit2caswithhouseholdid {} {} batuu'.format(sim.id, sim.household_id), _connection)
    return True


@Command('iced_cream.hybrid.commands.force_add_trait', command_type=(CommandType.Live), command_restrictions=(CommandRestrictionFlags.UNRESTRICTED))
def force_add_trait(trait_type: TunableInstanceParam(Types.TRAIT), opt_sim: OptionalTargetParam=None, _connection=None):
    output = CheatOutput(_connection)
    sim = get_optional_target(opt_sim, _connection)
    if sim is None:
        output('No valid sim specified for iced_cream.hybrid.commands.remove_conflicting_traits_for_occult_type')
    if trait_type is None:
        output('no trait id specified')
        return False
    if sim.sim_info.age not in trait_type.ages:
        output('sim is not valid age')
        return False
    for occult, tuning in OccultTracker.OCCULT_DATA.items():
        if tuning.part_occult_trait is not None:
            if tuning.part_occult_trait == trait_type:
                if sim.sim_info.occult_tracker.has_occult_type(occult):
                    sim.sim_info.occult_tracker.remove_occult_type(occult)

    remove_conflicting_traits(sim.sim_info, trait_type, output)
    sim.sim_info.add_trait(trait_type)
    if not sim.sim_info.has_trait(trait_type):
        remove_conflicting_traits(sim.sim_info, trait_type, output)
        sim.sim_info.add_trait(trait_type)
    return True


@Command('iced_cream.hybrid.commands.delete_form', command_type=(CommandType.Live), command_restrictions=(CommandRestrictionFlags.UNRESTRICTED))
def delete_form(occult_type: OccultType=OccultType.VAMPIRE, opt_sim: OptionalTargetParam=None, _connection=None):
    output = CheatOutput(_connection)
    sim = get_optional_target(opt_sim, _connection)
    if sim is None:
        output('No valid sim specified for iced_cream.hybrid.commands.set_occult_type')
        return False
    sim_info = sim.sim_info
    occult_tracker = sim_info.occult_tracker
    if occult_type == OccultType.HUMAN:
        output('Cannot delete the human form')
        return False
    if occult_type in occult_tracker._sim_info_map:
        if occult_utils.is_sim_in_form(sim_info, occult_type):
            trait = occult_utils.get_form_trait(occult_type)
            sim_info.remove_trait(trait)
        del occult_tracker._sim_info_map[occult_type]
        occult_utils.recalc_all(occult_tracker)
    return True


@Command('td1hybrid.commands.restore_occult')
def restore_occult(opt_sim: OptionalTargetParam=None, _connection=None):
    if not _connection:
        _connection = client_manager().get_first_client_id()
    output = CheatOutput(_connection)
    sim = get_optional_target(opt_sim, _connection)
    if sim is None:
        output('No valid sim specified for td1hybrid.commands.restore_occult')
        return False

    def process_sim(sim_info):
        occult_tracker = sim_info.occult_tracker

        # Ref & Use old Map
        new_form_map = occult_tracker._sim_info_map.copy()
        old_cache = occult_map_cache.get(sim_info.id)
        # old_cache[OccultType.HUMAN] = new_form_map[OccultType.HUMAN]
        # old_cache[occult_edit_cache] = new_form_map[occult_map_cache]

        if master_logger is not None and master_logger is not False:
            master_logger.debug(
                f"PROCESS - OLD & NEW SIM OCCULT MAP\n"
                f"Name: {sim_info.first_name} {sim_info.last_name}\n"
                f"\n"
                f"OLD MAP: {old_cache}\n"
                f"MAP TO REPLACE: {new_form_map}\n"
            )

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info(
                f"PROCESS - OLD & NEW SIM OCCULT MAP\n"
                f"Name: {sim_info.first_name} {sim_info.last_name}\n"
                f"\n"
                f"OLD MAP: {old_cache}\n"
                f"MAP TO REPLACE: {new_form_map}\n"
            )

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

        if master_logger is not None and master_logger is not False:
            master_logger.debug(
                f"PROCESS - OLD & NEW SIM OCCULT MAP\n"
                f"Name: {sim_info.first_name} {sim_info.last_name}\n"
                f"\n"
                f"REPLACED MAP: {new_form_map}\n"
            )

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info(
                f"PROCESS - OLD & NEW SIM OCCULT MAP\n"
                f"Name: {sim_info.first_name} {sim_info.last_name}\n"
                f"\n"
                f"REPLACED MAP: {new_form_map}\n"
            )

    household = sim.sim_info.household
    for household_sim in household.get_humans_gen():
        process_sim(household_sim.sim_info)


@Command('td1hybrid.commands.recalc_all')
def cmd_recalc_all(opt_sim: OptionalTargetParam=None, _connection=None):
    output = CheatOutput(_connection)
    sim = get_optional_target(opt_sim, _connection)
    if sim is None:
        output('No valid sim specified for td1hybrid.commands.recalc_all')
        return False
    occult_utils.recalc_all(sim.sim_info.occult_tracker)
    return True


@Command('td1hybrid.view_sim_cached_occults')
def cmd_view_cache_occults(opt_sim: OptionalTargetParam, _connection=None):
    output = Output(_connection)
    sim = get_optional_target(opt_sim, _connection)
    occult_tracker = sim.sim_info.occult_tracker

    cache_map = occult_tracker._sim_info_map.copy()

    output(f"OCCULT CACHE MAP [{sim.sim_info.first_name} {sim.sim_info.last_name}]\n\n")

    for k, v in cache_map.items():
        output(f"CLASS REF: {v} - {OccultType(k)}\n\n")

        if master_logger is not None and master_logger is not False:
            master_logger.info(
                f"OCCULT CACHE MAP [{sim.sim_info.first_name} {sim.sim_info.last_name}] - {k}\n\n"
                f"CLASS REF: {v}\n\n"
                f"NESTED VARS: {vars(v)}\n\n"
            )


@Command('td1hybrid.refresh_motives')
def cmd_refresh_motives(opt_sim: OptionalTargetParam, _connection=None):
    output = Output(_connection)
    sim = get_optional_target(opt_sim, _connection)
    sim.sim_info.trait_tracker.sort_and_send_commodity_list()
    output(f"Motive List updated.")


@Command("td1occulthandler.switch_occult", command_type=CommandType.Live)
def cmd_switch_occult(opt_sim: OptionalTargetParam, occult: str, _connection=None):
    output = Output(_connection)
    sim = get_optional_target(opt_sim, _connection)
    occult_tracker = sim.sim_info.occult_tracker
    trait_tracker = sim.sim_info.trait_tracker
    manual_dark_form_trait = services.get_instance_manager(Types.TRAIT).get(VAMPIRE_MANUAL_DARK_FORM_TRAIT)

    # add_wing_loot = services.get_instance_manager(Types.ACTION).get(FAIRY_ADD_WING_LOOT)
    # remove_wing_loot = services.get_instance_manager(Types.ACTION).get(FAIRY_REMOVE_WING_LOOT)
    # resolver = SingleSimResolver(sim.sim_info)

    try:
        occult = OccultType(occult)

    except ValueError:
        output(f"The specified occult type does not exist.\nAllowed OccultTypes: {OccultType.names}")

    if sim is None:
        output('No valid target specified.')

    if occult != OccultType.HUMAN:
        occult_data = OccultTracker.OCCULT_DATA.get(occult)

        if not occult_data:
            output(f"OccultTracker lacks data for specified occult.")
            return

        if not occult_data.current_occult_trait:
            output("The specified occult does not have a secondary form.")
            return

        if not occult_tracker.has_occult_type(occult):
            output("The specified sim does not have the specified occult.")
            return

        # if occult == OccultType.FAIRY:
        #     remove_wing_loot.apply_to_resolver(resolver)
        # else:
        #     add_wing_loot.apply_to_resolver(resolver)

    # if occult != OccultType.VAMPIRE:
    #     if trait_tracker.has_trait(manual_dark_form_trait):
    #         sim.sim_info.remove_trait(manual_dark_form_trait)
    #
    # else:
    #     if not trait_tracker.has_trait(manual_dark_form_trait):
    #         sim.sim_info.add_trait(manual_dark_form_trait)

    # occult_tracker.set_pending_occult_type(sim.sim_info.current_occult_types)
    # if occult != OccultType.HUMAN:
    #     occult_tracker.switch_to_occult_type(OccultType.HUMAN)
    occult_tracker.switch_to_occult_type(occult)

    output(f"Sim: {sim.sim_info.first_name} {sim.sim_info.last_name} | Switched to Occult: {occult}")


@Command('td1hybrid.view_global_cached_occults')
def cmd_view_global_cache_occults(_connection=None):
    output = Output(_connection)

    msg = (
        f"OCCULTDATACACHE CLASS\n\n"
        f"EXIT TRAITS: {OccultDataCache.occult_exit_traits}\n\n"
        f"REMOVAL TRAITS: {OccultDataCache.occult_removal_traits}\n\n"
        f"ADD ACTIONS: {OccultDataCache.occult_add_actions}\n\n"
        f"CUSTOM OCCULTS: {OccultDataCache.custom_occults}\n\n"
    )

    output(msg)

    if master_logger is not None and master_logger is not False:
        master_logger.info(msg)


@Command('td1hybrid.view_cas_cached_sims')
def cmd_view_cas_cached_sims(_connection=None):
    output = Output(_connection)

    msg = f"CAS OCCULT MAP CACHE\n\n"
    output(msg)

    for k, v in occult_map_cache.items():
        sim = get_optional_target(OptionalTargetParam(str(k)))
        sim_name = f"{sim.sim_info.first_name} {sim.sim_info.last_name}" if sim is not None else f"{k}"
        conv_v = {OccultType(nk): nv for nk, nv in v.items()}
        ext = f"SIM: {sim_name}\n\nOCCULT MAP: {conv_v}\n\n"
        msg += ext
        output(ext)


    if master_logger is not None and master_logger is not False:
        master_logger.info(msg)


@Command("td1occulthybrid.help")
def cmd_view_help(_connection=None):
    output = Output(_connection)
    output('============================================================================')
    output("iced_cream.hybrid.commands.edit_form_in_cas {occult_type} {opt_sim}")
    output("iced_cream.hybrid.commands.set_occult_type {occult_type} {opt_sim}")
    output("iced_cream.hybrid.commands.switch_to_occult {occult_type} {opt_sim}")
    output("iced_cream.hybrid.commands.remove_conflicting_traits_for_occult_type {occult_type} {opt_sim}")
    output("iced_cream.hybrid.commands.add_occult_type {occult_type} {opt_sim}")
    output("cas.plan_batuu_outfit {opt_sim}")
    output("iced_cream.hybrid.commands.force_add_trait {trait} {opt_sim}")
    output("iced_cream.hybrid.commands.delete_form {occult_type} {opt_sim}")
    output("td1hybrid.commands.restore_occult {opt_sim}")
    output("td1hybrid.commands.recalc_all {opt_sim}")
    output("td1hybrid.view_sim_cached_occults {opt_sim}")
    output("td1hybrid.refresh_motives {opt_sim}")
    output("td1occulthandler.switch_occult {opt_sim}")
    output("td1hybrid.view_global_cached_occults")
    output("td1hybrid.view_cas_cached_sims")
    output("\noccult_type (OccultType -> int/IntFlag): \n1: HUMAN\n2: ALIEN\n4: VAMPIRE\n8: MERMAID\n16: WITCH\n32: WEREWOLF\n64: FAIRY")
    output("\nopt_sim: Use sims.get_sim_id_by_name {first_name} {last_name} command")
