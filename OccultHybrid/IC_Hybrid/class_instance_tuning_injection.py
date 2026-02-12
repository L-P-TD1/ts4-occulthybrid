from sims.occult.occult_enums import OccultType
from sims.occult.occult_tracker import OccultTracker
from sims.sim_info_types import Age
from sims4.resources import Types
from OccultHybrid.IC_Hybrid.occult_cache import OccultDataCache
from OccultHybrid.IC_Hybrid.tuning_utils import get_resource_of_type_from_id, get_resources_of_type_from_ids, remove_all_occult_conflicts_from_trait, remove_specific_occult_conflict_from_trait, add_ages_to_trait, remove_ages_from_trait

class ClassInstanceTuningInjection:

    @staticmethod
    def _process_mermaid_traits():
        if not OccultTracker.OCCULT_DATA or OccultType.MERMAID not in OccultTracker.OCCULT_DATA:
            return
        trait_mermaid_of_age = get_resource_of_type_from_id(211545, Types.TRAIT)
        restricted_ages = {Age.BABY, Age.TODDLER, Age.CHILD}
        remove_ages_from_trait(trait_mermaid_of_age, restricted_ages)
        mermaid_tuning = OccultTracker.OCCULT_DATA.get(OccultType.MERMAID)
        if not mermaid_tuning.additional_occult_traits:
            new_mermaid_tuning = mermaid_tuning.clone_with_overrides(additional_occult_traits=(frozenset([trait_mermaid_of_age])))
            new_dict = dict(OccultTracker.OCCULT_DATA)
            new_dict[OccultType.MERMAID] = new_mermaid_tuning
            OccultTracker.OCCULT_DATA = OccultTracker.OCCULT_DATA.__class__(new_dict)
        trait_mermaid_discovered = get_resource_of_type_from_id(215252, Types.TRAIT)
        remove_ages_from_trait(trait_mermaid_discovered, restricted_ages)
        trait_mermaid_discovered_temporary = get_resource_of_type_from_id(215414, Types.TRAIT)
        remove_ages_from_trait(trait_mermaid_discovered_temporary, restricted_ages)
        traits_to_remove = [
         trait_mermaid_discovered, trait_mermaid_discovered_temporary]
        OccultDataCache.cache_removal_traits(OccultType.MERMAID, traits_to_remove)

    @staticmethod
    def _process_servo_traits():
        robot_trait_tuning = get_resource_of_type_from_id(218444, Types.TRAIT)
        if robot_trait_tuning is not None:
            robot_occult_conflicts_to_remove = {
             OccultType.ALIEN,
             OccultType.VAMPIRE,
             OccultType.WITCH}
            for occult_type in robot_occult_conflicts_to_remove:
                remove_specific_occult_conflict_from_trait(occult_type, robot_trait_tuning)

            add_ages_to_trait(robot_trait_tuning, {Age.TEEN, Age.ADULT, Age.ELDER})

    @staticmethod
    def _process_bloodline_traits():
        spellcaster_bloodline_trait_ids = {
         218027,
         218026,
         218025}

        bloodline_traits = get_resources_of_type_from_ids(spellcaster_bloodline_trait_ids, Types.TRAIT)
        if bloodline_traits:
            for trait in bloodline_traits:
                remove_all_occult_conflicts_from_trait(trait)

    @staticmethod
    def _cache_vampire_manual_dark_form_trait():
        trait_vampire_manual_dark_form = get_resource_of_type_from_id(156397, Types.TRAIT)
        if trait_vampire_manual_dark_form:
            OccultDataCache.cache_exit_traits(OccultType.VAMPIRE, [trait_vampire_manual_dark_form])
            OccultDataCache.cache_removal_traits(OccultType.VAMPIRE, [trait_vampire_manual_dark_form])
            remove_ages_from_trait(trait_vampire_manual_dark_form, {Age.BABY, Age.TODDLER, Age.CHILD})

    @staticmethod
    def _process_plantsim_trait():
        trait_plantsim = get_resource_of_type_from_id(162668, Types.TRAIT)
        if trait_plantsim:
            trait_plantsim.is_npc_only = False
            trait_plantsim.persistable = True
            trait_plantsim.allow_from_gallery = True
            remove_all_occult_conflicts_from_trait(trait_plantsim)
            buff_plantsim = get_resource_of_type_from_id(162844, Types.BUFF)
            if buff_plantsim:
                if not trait_plantsim.display_name:
                    trait_plantsim.display_name = buff_plantsim.buff_name
                    trait_plantsim.display_name_gender_neutral = buff_plantsim.buff_name
                    trait_plantsim.trait_description = buff_plantsim.buff_name
                    trait_plantsim.icon = buff_plantsim.icon

    @staticmethod
    def _process_traits():
        ClassInstanceTuningInjection._process_mermaid_traits()
        ClassInstanceTuningInjection._process_servo_traits()
        ClassInstanceTuningInjection._process_bloodline_traits()
        ClassInstanceTuningInjection._cache_vampire_manual_dark_form_trait()
        ClassInstanceTuningInjection._process_plantsim_trait()
        for occult, tuning in OccultTracker.OCCULT_DATA.items():
            occult_trait = tuning.occult_trait
            if not occult_trait:
                continue
            if tuning.current_occult_trait:
                current_occult_trait = tuning.current_occult_trait
                try:
                    invalid_ages = {age for age in Age if age < tuning.min_age_for_occult_ui}
                    remove_ages_from_trait(current_occult_trait, invalid_ages)
                except:
                    pass

                if tuning.additional_occult_traits:
                    for trait in tuning.additional_occult_traits:
                        if not trait.display_name:
                            trait.display_name = occult_trait.display_name
                            trait.display_name_gender_neutral = occult_trait.display_name_gender_neutral
                            trait.trait_description = occult_trait.display_name

                if tuning.part_occult_trait:
                    part_occult_trait = tuning.part_occult_trait
                    if not part_occult_trait.display_name:
                        part_occult_trait.display_name = occult_trait.display_name
                        part_occult_trait.display_name_gender_neutral = occult_trait.display_name_gender_neutral
                        part_occult_trait.trait_description = occult_trait.display_name

    @staticmethod
    def _process_interactions():
        alien_trait = get_resource_of_type_from_id(102785, Types.TRAIT)
        if alien_trait:
            alien_self_interaction_ids = {116078,
             103336,
             157440,
             103335,
             103337,
             157442}
            alien_pie_menu_id = 14984329746562603234
            pie_menu = get_resource_of_type_from_id(alien_pie_menu_id, Types.PIE_MENU_CATEGORY)
            if pie_menu:
                interactions = get_resources_of_type_from_ids(alien_self_interaction_ids, Types.INTERACTION)
                for tuning in interactions:
                    if not tuning.category:
                        tuning.category = pie_menu

    @staticmethod
    def _process_actions():
        loot_mermaid_discovery_check = get_resource_of_type_from_id(215254, Types.ACTION)
        if loot_mermaid_discovery_check:
            OccultDataCache.cache_add_actions(OccultType.MERMAID, [loot_mermaid_discovery_check])

    @staticmethod
    def _process_statistics():
        pass

    @staticmethod
    def _process_buffs():
        buff_plantsim = get_resource_of_type_from_id(162844, Types.BUFF)
        if buff_plantsim:
            buff_plantsim.is_npc_only = False

    @classmethod
    def load_data_into_class_instances(cls, instance_manager):
        _instance_manager_process_map = {Types.TRAIT: cls._process_traits, 
         Types.INTERACTION: cls._process_interactions, 
         Types.ACTION: cls._process_actions, 
         Types.STATISTIC: cls._process_statistics(), 
         Types.BUFF: cls._process_buffs()}
        func = _instance_manager_process_map.get(instance_manager.TYPE)
        if func:
            func()