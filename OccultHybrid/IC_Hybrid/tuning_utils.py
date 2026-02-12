from server_commands.argument_helpers import get_tunable_instance
from sims.occult.occult_tracker import OccultTracker
from sims4.resources import Types

def get_resource_of_type_from_id(res_id, res_type: Types):
    try:
        result = get_tunable_instance(res_type, res_id, exact_match=True)
        return result
    except:
        return


def get_resources_of_type_from_ids(ids_set, res_type):
    result_set = set()
    for item_id in ids_set:
        cls = get_resource_of_type_from_id(item_id, res_type)
        if cls:
            result_set.add(cls)

    return result_set


def remove_conflicts_from_trait(trait, conflicting_traits: set, recursive=True):
    if not (trait and conflicting_traits):
        return
    conflicts = set(trait.conflicting_traits)
    trait.conflicting_traits = frozenset(conflicts.difference(conflicting_traits))
    if recursive:
        for conflict_trait in conflicting_traits:
            remove_conflicts_from_trait(conflict_trait, {trait}, recursive=False)


def remove_all_occult_conflicts_from_trait(trait):
    if not trait:
        return
    occult_traits = []
    for tuning in OccultTracker.OCCULT_DATA.values():
        if tuning.occult_trait:
            occult_traits.append(tuning.occult_trait)
        else:
            if tuning.current_occult_trait:
                occult_traits.append(tuning.current_occult_trait)
            if tuning.additional_occult_traits:
                occult_traits.extend(tuning.additional_occult_traits)
        if tuning.part_occult_trait:
            occult_traits.append(tuning.part_occult_trait)

    remove_conflicts_from_trait(trait, set(occult_traits))


def remove_specific_occult_conflict_from_trait(occult_type, trait):
    if not trait:
        return
    tuning = OccultTracker.OCCULT_DATA.get(occult_type)
    if not tuning:
        return
    occult_traits = []
    if tuning.occult_trait:
        occult_traits.append(tuning.occult_trait)
    if tuning.current_occult_trait:
        occult_traits.append(tuning.current_occult_trait)
    if tuning.additional_occult_traits:
        occult_traits.extend(tuning.additional_occult_traits)
    if tuning.part_occult_trait:
        occult_traits.append(tuning.part_occult_trait)
    remove_conflicts_from_trait(trait, set(occult_traits))


def remove_trait_blacklist_for_interactions(interactions):
    if interactions:
        for interaction in interactions:
            if not hasattr(interaction, 'test_globals'):
                continue
            else:
                for test in interaction.test_globals:
                    if getattr(test, 'blacklist_traits', ()) is not ():
                        test.blacklist_traits = ()


def add_interactions_to_trait(interactions, trait):
    if not (interactions and trait):
        return
    super_affordances = set(trait.super_affordances)
    super_affordances.update(interactions)
    trait.super_affordances = frozenset(super_affordances)


def remove_ages_from_trait(trait, ages: set):
    if not (trait and ages):
        return
    new_ages = set(trait.ages)
    new_ages.difference_update(ages)
    trait.ages = frozenset(new_ages)


def add_ages_to_trait(trait, ages: set):
    if not (trait and ages):
        return
    new_ages = set(trait.ages)
    new_ages.update(ages)
    trait.ages = frozenset(new_ages)


def add_motives_to_trait_blacklist(motives: set, trait):
    if motives is not None:
        if trait is not None:
            blacklist = set(trait.initial_commodities_blacklist)
            blacklist.update(motives)
            trait.initial_commodities_blacklist = frozenset(blacklist)


def remove_motives_from_trait_blacklist(motives: set, trait):
    if motives is not None:
        if trait is not None:
            blacklist = set(trait.initial_commodities_blacklist)
            blacklist.difference_update(motives)
            trait.initial_commodities_blacklist = frozenset(blacklist)