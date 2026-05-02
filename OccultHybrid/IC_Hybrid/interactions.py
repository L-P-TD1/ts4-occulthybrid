import operator, event_testing, services
from bucks.bucks_commands import lock_all_perks_for_bucks_type
from bucks.bucks_enums import BucksType
from event_testing.results import TestResult
from interactions import ParticipantTypeSim
from interactions.base.picker_interaction import PickerSuperInteraction
from interactions.utils.tunable import TunableContinuation
from server_commands.argument_helpers import OptionalTargetParam
from server_commands.interaction_commands import push_interaction
from sims.occult.occult_enums import OccultType
from sims.occult.occult_tracker import OccultTracker
from sims4.localization import LocalizationHelperTuning, TunableLocalizedStringFactory
from sims4.resources import CompoundTypes, Types
from sims4.tuning.tunable import TunableResourceKey, Tunable, TunableEnumEntry, TunableReference
from sims4.tuning.tunable_base import ExportModes, GroupNames
from sims4.utils import flexmethod
from automation.constants import Constants
from ui.ui_dialog_picker import ObjectPickerRow
from OccultHybrid.IC_Hybrid.commands import edit_form_in_cas, delete_form, cmd_switch_occult
from OccultHybrid.IC_Hybrid import occult_utils


OCCULT_DATA_REF = {
    "vampire": {
        "type": OccultType.VAMPIRE,
        "primary_buck": 40961,
        "secondary_buck": 40962
    },
    "witch": {
        "type": OccultType.WITCH,
        "primary_buck": 49153,
        "secondary_buck": None
    },
    "werewolf": {
        "type": OccultType.WEREWOLF,
        "primary_buck": 135169,
        "secondary_buck": None
    },
    "fairy": {
        "type": OccultType.FAIRY,
        "primary_buck": 129025,
        "secondary_buck": None
    }
}

OCCULT_TRAIT_TO_TYPE = {
    102785: OccultType.ALIEN,
    149527: OccultType.VAMPIRE,
    199043: OccultType.MERMAID,
    213050: OccultType.WITCH,
    289780: OccultType.WEREWOLF,
    433287: OccultType.FAIRY
}

HUMAN_FORM_TRAIT = 151039
HUMAN_REF_TRAIT = 14136328463489586342

ADD_WING_INT = 17193300801246196753
REMOVE_WING_INT = 18257506431549589720


class HybridOccultPickerSuperInteraction(PickerSuperInteraction):
    INSTANCE_TUNABLES = {'picker_target': TunableEnumEntry(tunable_type=ParticipantTypeSim,
                        default=(ParticipantTypeSim.TargetSim),
                        tuning_group=(GroupNames.PICKERTUNING))}

    @classmethod
    def _test(cls, *args, picked_row=None, **kwargs):
        if OccultTracker.OCCULT_DATA:
            for occult in OccultTracker.OCCULT_DATA:
                if not occult_utils.is_custom_occult(occult):
                    return event_testing.results.TestResult.TRUE
                if occult_utils.get_custom_occult_info(occult).menu_allow_add_remove_picker:
                    return event_testing.results.TestResult.TRUE

            return TestResult(False)
        return TestResult(False)

    def _run_interaction_gen(self, timeline):
        trait_target = self.get_participant(self.picker_target)
        self._show_picker_dialog(trait_target, target_sim=trait_target)
        return True


class OccultTraitPickerSuperInteraction(HybridOccultPickerSuperInteraction):
    INSTANCE_TUNABLES = {'is_add':Tunable(description='\n                If this interaction is trying to add a trait to the sim or to\n                remove a trait from the sim.\n                ',
       tunable_type=bool,
       default=True,
       tuning_group=GroupNames.PICKERTUNING), 
     'icon_trait_already_equipped':TunableResourceKey(description='The icon to display over traits the sim already has.',
       allow_none=True,
       resource_types=CompoundTypes.IMAGE,
       export_modes=ExportModes.All,
       tuning_group=GroupNames.APPEARANCE), 
     'icon_part_trait_already_equipped':TunableResourceKey(description='The icon to display over traits the sim already has.',
       allow_none=True,
       resource_types=CompoundTypes.IMAGE,
       export_modes=ExportModes.All,
       tuning_group=GroupNames.APPEARANCE), 
     'icon_part_trait':TunableResourceKey(description='The icon to display over traits the sim already has.',
       allow_none=True,
       resource_types=CompoundTypes.IMAGE,
       export_modes=ExportModes.All,
       tuning_group=GroupNames.APPEARANCE), 
     'picker_target':TunableEnumEntry(tunable_type=ParticipantTypeSim,
       default=ParticipantTypeSim.TargetSim,
       tuning_group=GroupNames.PICKERTUNING)}

    def _run_interaction_gen(self, timeline):
        trait_target = self.get_participant(self.picker_target)
        self._show_picker_dialog(trait_target, target_sim=trait_target)
        return True

    @flexmethod
    def picker_rows_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        trait_target = (inst_or_cls.get_participant)(cls.picker_target, target=target, context=context, **kwargs)
        trait_tracker = trait_target.sim_info.trait_tracker
        half_text = LocalizationHelperTuning.get_raw_text('1/2')
        for trait, is_occult in cls._trait_gen():
            if trait.display_name:
                display_name = trait.display_name(trait_target)
            else:
                display_name = LocalizationHelperTuning.get_raw_text(str(trait.__name__))
            if not is_occult:
                display_name = LocalizationHelperTuning.get_name_value_pair(display_name, half_text)
            if not is_occult:
                if cls.icon_part_trait is not None:
                    row_icon = cls.icon_part_trait
                else:
                    row_icon = None
                    if trait.icon:
                        row_icon = trait.icon
                row_tooltip = None
                has_trait = trait_tracker.has_trait(trait)
                conflict = trait_tracker.is_conflicting(trait)
                is_valid = trait.is_valid_trait(trait_target.sim_info)
                if cls.is_add:
                    if has_trait:
                        is_enabled = False
            else:
                is_enabled = is_valid and not conflict
            if not is_enabled:
                if is_valid:
                    if conflict:
                        row_tooltip = cls._generate_conflicting_trait_tooltip(trait, trait_tracker, trait_target)
                    else:
                        is_enabled = has_trait
                if has_trait:
                    row_icon = cls._get_trait_equipped_icon_override(is_occult, row_icon)
                row = ObjectPickerRow(name=display_name,
                  icon=row_icon,
                  tag=trait,
                  is_enable=is_enabled,
                  row_tooltip=row_tooltip)
                yield row

    def on_choice_selected(self, choice_tag, **kwargs):
        trait = choice_tag
        if trait is not None:
            trait_target = self.get_participant(self.picker_target)
            if self.is_add:
                trait_target.sim_info.add_trait(trait)
            else:
                trait_target.sim_info.remove_trait(trait)
            display_again = kwargs.get('display_again', True)
            if display_again:
                if choice_tag:
                    self._show_picker_dialog(trait_target, target_sim=trait_target)

    def on_multi_choice_selected(self, picked_choice, **kwargs):
        for choice in picked_choice:
            self.on_choice_selected(choice, display_again=False)

        if picked_choice:
            trait_target = self.get_participant(self.picker_target)
            self._show_picker_dialog(trait_target, target_sim=trait_target)

    @classmethod
    def _trait_gen(cls, occult_only=False):
        for occult, tuning in OccultTracker.OCCULT_DATA.items():
            if occult_utils.is_custom_occult(occult):
                if not occult_utils.get_custom_occult_info(occult).menu_allow_add_remove_picker:
                    continue
            if tuning.occult_trait:
                yield (
                 tuning.occult_trait, True)
            if occult_only or tuning.part_occult_trait:
                yield (
                 tuning.part_occult_trait, False)

    @classmethod
    def _get_trait_equipped_icon_override(cls, is_occult=True, fallback_icon=None):
        if is_occult:
            if cls.icon_trait_already_equipped is not None:
                return cls.icon_trait_already_equipped
        if not is_occult:
            if cls.icon_part_trait_already_equipped is not None:
                return cls.icon_part_trait_already_equipped
        return fallback_icon

    @classmethod
    def _generate_conflicting_trait_tooltip(cls, trait, trait_tracker, trait_target):
        display_name = None
        for equipped_trait in trait_tracker.equipped_traits:
            if equipped_trait is not trait and trait.is_conflicting(equipped_trait) and equipped_trait.display_name is not None:
                display_name = equipped_trait.display_name
                break

        return display_name

    @classmethod
    def _get_occult_type_from_trait(cls, occult_trait):
        for occult, tuning in OccultTracker.OCCULT_DATA.items():
            if occult_utils.is_custom_occult(occult):
                return None
            if tuning.occult_trait == occult_trait:
                return occult
        return None


class OccultTogglePickerSuperInteraction(OccultTraitPickerSuperInteraction):

    @flexmethod
    def picker_rows_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        trait_target = (inst_or_cls.get_participant)(cls.picker_target, target=target, context=context, **kwargs)
        trait_tracker = trait_target.sim_info.trait_tracker
        half_text = LocalizationHelperTuning.get_raw_text('1/2')
        for trait, is_occult in cls._trait_gen():
            if trait.display_name:
                display_name = trait.display_name(trait_target)
            else:
                display_name = LocalizationHelperTuning.get_raw_text(str(trait.__name__))
            if not is_occult:
                display_name = LocalizationHelperTuning.get_name_value_pair(display_name, half_text)

                if cls.icon_part_trait is not None:
                    row_icon = cls.icon_part_trait
                else:
                    row_icon = None

                row_tooltip = None

            else:
                if trait.icon:
                    row_icon = trait.icon
                    row_tooltip = None
                else:
                    row_tooltip = None

            has_trait = trait_tracker.has_trait(trait)
            conflict = trait_tracker.is_conflicting(trait)
            is_valid = trait.is_valid_trait(trait_target.sim_info)

            if has_trait:
                is_enabled = True
            else:
                is_enabled = is_valid and not conflict
                if is_valid:
                    if conflict:
                        row_tooltip = cls._generate_conflicting_trait_tooltip(trait, trait_tracker, trait_target)

            if has_trait:
                row_icon = cls._get_trait_equipped_icon_override(is_occult, row_icon)

            row = ObjectPickerRow(
                name=display_name,
                icon=row_icon,
                tag=trait,
                is_enable=is_enabled,
                row_tooltip=row_tooltip
            )
            yield row

    def on_choice_selected(self, choice_tag, **kwargs):
        trait = choice_tag
        if trait is not None:
            trait_target = self.get_participant(self.picker_target)
            trait_tracker = trait_target.sim_info.trait_tracker
            if not trait_tracker.has_trait(trait):
                if self._get_occult_type_from_trait(trait) is not None:
                    trait_target.sim_info.occult_tracker.add_occult_type(self._get_occult_type_from_trait(trait))
                    trait_target.sim_info.occult_tracker.switch_to_occult_type(self._get_occult_type_from_trait(trait))
                    trait_target.sim_info.occult_tracker.switch_to_occult_type(OccultType.HUMAN)
                else:
                    trait_target.sim_info.add_trait(trait)
            else:
                trait_target.sim_info.remove_trait(trait)
            display_again = kwargs.get('display_again', True)
            if display_again:
                if choice_tag:
                    self._show_picker_dialog(trait_target, target_sim=trait_target)

    def on_multi_choice_selected(self, picked_choice, **kwargs):
        for choice in picked_choice:
            self.on_choice_selected(choice, display_again=False)

        if picked_choice:
            sim = self.get_participant(self.picker_target)
            self._show_picker_dialog(sim, target_sim=sim)


class OccultCASPickerSuperInteraction(HybridOccultPickerSuperInteraction):
    INSTANCE_TUNABLES = {'picker_target': TunableEnumEntry(tunable_type=ParticipantTypeSim,
                        default=(ParticipantTypeSim.TargetSim),
                        tuning_group=(GroupNames.PICKERTUNING))}

    @classmethod
    def _test(cls, *args, picked_row=None, **kwargs):
        if OccultTracker.OCCULT_DATA:
            for occult in OccultTracker.OCCULT_DATA:
                if not occult_utils.is_custom_occult(occult):
                    return event_testing.results.TestResult.TRUE
                if occult_utils.get_custom_occult_info(occult).menu_allow_modify_in_cas_picker:
                    return event_testing.results.TestResult.TRUE

            return TestResult(False)
        return TestResult(False)

    def _run_interaction_gen(self, timeline):
        trait_target = self.get_participant(self.picker_target)
        self._show_picker_dialog(trait_target, target_sim=trait_target)
        return True

    @flexmethod
    def picker_rows_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        sim = (inst_or_cls.get_participant)(cls.picker_target, target=target, context=context, **kwargs)
        for occult_type, trait_info, is_enabled in cls._occult_gen(sim):
            if trait_info.display_name:
                display_name = trait_info.display_name(target)
            else:
                display_name = LocalizationHelperTuning.get_raw_text(str(trait_info.__name__))
            row = ObjectPickerRow(name=display_name,
              icon=(trait_info.icon),
              tag=occult_type,
              is_enable=is_enabled)
            yield row

    def on_choice_selected(self, choice_tag, **kwargs):
        sim = self.get_participant(self.picker_target)
        edit_form_in_cas(choice_tag, OptionalTargetParam(str(sim.id)))

    @classmethod
    def _occult_gen(cls, participant):
        for occult, tuning in OccultTracker.OCCULT_DATA.items():
            if occult_utils.is_custom_occult(occult):
                if not occult_utils.get_custom_occult_info(occult).menu_allow_modify_in_cas_picker:
                    continue
            if tuning.occult_trait is not None:
                yield (
                 occult, tuning.occult_trait, participant.sim_info.occult_tracker.has_occult_type(occult))


class OccultFormDeletePickerSuperInteraction(HybridOccultPickerSuperInteraction):
    INSTANCE_TUNABLES = {'picker_target': TunableEnumEntry(tunable_type=ParticipantTypeSim,
                        default=(ParticipantTypeSim.TargetSim),
                        tuning_group=(GroupNames.PICKERTUNING))}

    @classmethod
    def _test(cls, *args, picked_row=None, **kwargs):
        if OccultTracker.OCCULT_DATA:
            for occult, tuning in OccultTracker.OCCULT_DATA.items():
                if tuning.current_occult_trait is not None:
                    return TestResult.TRUE

            return TestResult(False)
        return TestResult(False)

    def _run_interaction_gen(self, timeline):
        trait_target = self.get_participant(self.picker_target)
        self._show_picker_dialog(trait_target, target_sim=trait_target)
        return True

    @flexmethod
    def picker_rows_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        sim = (inst_or_cls.get_participant)(cls.picker_target, target=target, context=context, **kwargs)
        for occult_type, trait_info, is_enabled, form_tooltip in cls._occult_gen(sim):
            if trait_info.display_name:
                display_name = trait_info.display_name(target)
            else:
                display_name = LocalizationHelperTuning.get_raw_text(str(trait_info.__name__))
            row_description = None
            if form_tooltip:
                try:
                    fact = TunableLocalizedStringFactory._Wrapper(string_id=(form_tooltip.hash))
                    row_description = fact(target)
                except:
                    pass

            row = ObjectPickerRow(name=display_name,
              icon=(trait_info.icon),
              tag=occult_type,
              is_enable=is_enabled,
              row_description=row_description)
            yield row

    def on_choice_selected(self, choice_tag, show_again=True, **kwargs):
        sim = self.get_participant(self.picker_target)
        delete_form(choice_tag, OptionalTargetParam(str(sim.id)))
        if choice_tag:
            if show_again:
                self._show_picker_dialog(sim, target_sim=sim)

    def on_multi_choice_selected(self, picked_choice, **kwargs):
        for choice in picked_choice:
            self.on_choice_selected(choice, show_again=False)

        if picked_choice:
            target = self.get_participant(self.picker_target)
            self._show_picker_dialog(target, target_sim=target)

    @classmethod
    def _occult_gen(cls, participant):
        for occult, tuning in OccultTracker.OCCULT_DATA.items():
            if occult_utils.is_custom_occult(occult):
                if not occult_utils.get_custom_occult_info(occult).menu_allow_delete_picker:
                    continue
            if tuning.current_occult_trait is not None:
                is_enabled = participant.sim_info.occult_tracker.get_occult_sim_info(occult) is not None
                yield (occult, tuning.occult_trait, is_enabled, tuning.cas_alternative_form_sim_name_tooltip)


class OccultTypePickerSuperInteraction(HybridOccultPickerSuperInteraction):
    INSTANCE_TUNABLES = {'icon_trait_already_equipped':TunableResourceKey(description='The icon to display over traits the sim already has.',
       allow_none=True,
       resource_types=CompoundTypes.IMAGE,
       export_modes=ExportModes.All,
       tuning_group=GroupNames.APPEARANCE), 
     'picker_target':TunableEnumEntry(tunable_type=ParticipantTypeSim,
       default=ParticipantTypeSim.TargetSim,
       tuning_group=GroupNames.PICKERTUNING)}

    @classmethod
    def _test(cls, *args, picked_row=None, **kwargs):
        if OccultTracker.OCCULT_DATA:
            for occult, tuning in OccultTracker.OCCULT_DATA.items():
                if tuning.experience_statistic is not None:
                    return event_testing.results.TestResult.TRUE

            return TestResult(False)
        return TestResult(False)

    def _run_interaction_gen(self, timeline):
        trait_target = self.get_participant(self.picker_target)
        self._show_picker_dialog(trait_target, target_sim=trait_target)
        return True

    @flexmethod
    def picker_rows_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        sim = (inst_or_cls.get_participant)(cls.picker_target, target=target, context=context, **kwargs)
        current_types = sim.sim_info.occult_types
        for occult_type, trait_info, is_enabled in cls._occult_gen(sim):
            if trait_info.display_name:
                display_name = trait_info.display_name(target)
            else:
                display_name = LocalizationHelperTuning.get_raw_text(str(trait_info.__name__))
            row_icon = trait_info.icon
            if not current_types == occult_type:
                if current_types == occult_type | OccultType.HUMAN:
                    if cls.icon_trait_already_equipped:
                        row_icon = cls.icon_trait_already_equipped
                        is_enabled = True
                row = ObjectPickerRow(name=display_name,
                  icon=row_icon,
                  tag=occult_type,
                  is_enable=is_enabled)
                if inst_or_cls.use_pie_menu():
                    row.row_tooltip = trait_info.trait_description
                yield row

    def on_choice_selected(self, choice_tag, **kwargs):
        sim = self.get_participant(self.picker_target)
        sim.sim_info.occult_types = OccultType.HUMAN | choice_tag
        sim.sim_info.trait_tracker.sort_and_send_commodity_list()
        if choice_tag:
            self._show_picker_dialog(sim, target_sim=sim)

    def on_multi_choice_selected(self, picked_choice, **kwargs):
        for choice in picked_choice:
            self.on_choice_selected(choice, show_again=False)

        if picked_choice:
            target = self.get_participant(self.picker_target)
            self._show_picker_dialog(target, target_sim=target)

    @classmethod
    def _occult_gen(cls, participant):
        for occult, tuning in OccultTracker.OCCULT_DATA.items():
            if tuning.occult_trait is not None and tuning.experience_statistic is not None:
                is_enabled = participant.sim_info.occult_tracker.has_occult_type(occult)
                yield (occult, tuning.occult_trait, is_enabled)


class OccultPerkResetPickerSuperInteraction(HybridOccultPickerSuperInteraction):
    INSTANCE_TUNABLES = {'picker_target': TunableEnumEntry(tunable_type=ParticipantTypeSim,
                        default=(ParticipantTypeSim.TargetSim),
                        tuning_group=(GroupNames.PICKERTUNING))}

    @classmethod
    def _test(cls, *args, picked_row=None, **kwargs):
        if OccultTracker.OCCULT_DATA:
            for occult, tuning in OccultTracker.OCCULT_DATA.items():
                for occult_str, tuning_dict in OCCULT_DATA_REF.items():
                    if tuning_dict["type"] != occult:
                        continue

                    if tuning_dict["primary_buck"] != BucksType.INVALID:
                        return event_testing.results.TestResult.TRUE

            return TestResult(False)
        return TestResult(False)

    def _run_interaction_gen(self, timeline):
        trait_target = self.get_participant(self.picker_target)
        self._show_picker_dialog(trait_target, target_sim=trait_target)
        return True

    @flexmethod
    def picker_rows_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        sim = (inst_or_cls.get_participant)(cls.picker_target, target=target, context=context, **kwargs)
        for occult_type, trait_info, is_enabled, primary_bucks, secondary_bucks in cls._occult_gen(sim):
            if trait_info.display_name:
                display_name = trait_info.display_name(target)
            else:
                display_name = LocalizationHelperTuning.get_raw_text(str(trait_info.__name__))
            row = ObjectPickerRow(name=display_name,
              icon=(trait_info.icon),
              tag=(
             primary_bucks, secondary_bucks),
              is_enable=is_enabled)
            if inst_or_cls.use_pie_menu():
                row.row_tooltip = trait_info.trait_description
            yield row

    def on_choice_selected(self, choice_tag, show_again=True, **kwargs):
        sim = self.get_participant(self.picker_target)
        primary_bucks, secondary_bucks = choice_tag
        if primary_bucks:
            if primary_bucks is not BucksType.INVALID:
                lock_all_perks_for_bucks_type(primary_bucks, sim.id, True)
        if secondary_bucks:
            if secondary_bucks is not BucksType.INVALID:
                lock_all_perks_for_bucks_type(secondary_bucks, sim.id, True)
        if choice_tag:
            if show_again:
                self._show_picker_dialog(sim, target_sim=sim)

    def on_multi_choice_selected(self, picked_choice, **kwargs):
        for choice in picked_choice:
            self.on_choice_selected(choice, show_again=False)

        if picked_choice:
            target = self.get_participant(self.picker_target)
            self._show_picker_dialog(target, target_sim=target)

    @classmethod
    def _occult_gen(cls, participant):
        for occult, tuning in OccultTracker.OCCULT_DATA.items():
            for occult_str, tuning_dict in OCCULT_DATA_REF.items():
                if tuning_dict["type"] != occult:
                    continue

                if tuning_dict["primary_buck"] is not None and tuning_dict["primary_buck"] is not BucksType.INVALID:
                    primary_buck_type = tuning_dict["primary_buck"]
                    secondary_buck_type = tuning_dict["secondary_buck"] if tuning_dict["secondary_buck"] is not None else BucksType.INVALID
                    has_occult = participant.sim_info.occult_tracker.has_occult_type(occult)
                    yield (occult, tuning.occult_trait, has_occult, primary_buck_type, secondary_buck_type)


class HybridOccultNeedsDisplaySuperInteraction(PickerSuperInteraction):
    INSTANCE_TUNABLES = {'picker_target': TunableEnumEntry(tunable_type=ParticipantTypeSim,
                        default=(ParticipantTypeSim.TargetSim),
                        tuning_group=(GroupNames.PICKERTUNING))}

    def _run_interaction_gen(self, timeline):
        trait_target = self.get_participant(self.picker_target)
        self._show_picker_dialog(trait_target, target_sim=trait_target)
        return True

    @flexmethod
    def picker_rows_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        sim = (inst_or_cls.get_participant)(cls.picker_target, target=target, context=context, **kwargs)
        for motive_info in cls._needs_gen(sim):
            icon = None
            try:
                icon = motive_info.states[(-1)].icon
            except:
                pass

            if motive_info.stat_name:
                if motive_info.is_visible:
                    display_name = motive_info.stat_name
                else:
                    continue
                progress = motive_info.get_value()
                progress -= motive_info.min_value
                pct = progress / (motive_info.max_value - motive_info.min_value)
                pct *= 100
                description = LocalizationHelperTuning.get_raw_text('{:.2f}%'.format(pct))
                row = ObjectPickerRow(name=display_name,
                  icon=icon,
                  tag=motive_info,
                  row_description=description,
                  is_enable=False)
                yield row

    @classmethod
    def _needs_gen(cls, participant):
        needs_tracker = participant.sim_info.commodity_tracker
        stats = needs_tracker.get_all_commodities()
        needs = []
        for stat in stats:
            if stat.is_commodity:
                needs.append(stat)

        needs = sorted(needs, key=(operator.attrgetter('ui_sort_order')))
        needs = sorted(needs, key=(operator.attrgetter('ui_render_style')), reverse=True)
        for need in needs:
            yield need

    def on_choice_selected(self, choice_tag, show_again=True, **kwargs):
        pass

    def on_multi_choice_selected(self, picked_choice, **kwargs):
        pass


class OccultSecondaryFormPickerSuperInteraction(HybridOccultPickerSuperInteraction):
    INSTANCE_TUNABLES = {
        'icon_trait_already_equipped':TunableResourceKey(
            description='The icon to display over traits the sim already has.',
            allow_none=True,
            resource_types=CompoundTypes.IMAGE,
            export_modes=ExportModes.All,
            tuning_group=GroupNames.APPEARANCE
        ),
        'picker_target':TunableEnumEntry(
            tunable_type=ParticipantTypeSim,
            default=ParticipantTypeSim.TargetSim,
            tuning_group=GroupNames.PICKERTUNING
        ),
        "add_wing_int": TunableContinuation(
            description="Interaction to run to add fairy wings."
        ),
        "remove_wing_int": TunableContinuation(
            description="Interaction to run to remove fairy wings."
        )
    }

    @classmethod
    def _test(cls, *args, picked_row=None, **kwargs):
        if OccultTracker.OCCULT_DATA:
            for occult, tuning in OccultTracker.OCCULT_DATA.items():
                if tuning.current_occult_trait is not None:
                    return event_testing.results.TestResult.TRUE

            return TestResult(False)
        return TestResult(False)

    def _run_interaction_gen(self, timeline):
        trait_target = self.get_participant(self.picker_target)
        self._show_picker_dialog(trait_target, target_sim=trait_target)
        return True

    @flexmethod
    def picker_rows_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = inst if inst is not None else cls
        sim = (inst_or_cls.get_participant)(cls.picker_target, target=target, context=context, **kwargs)
        current_types = sim.sim_info.occult_types
        for occult_type, trait_info, is_enabled in cls._occult_gen(sim):
            if trait_info.display_name:
                display_name = trait_info.display_name(target)
            else:
                display_name = LocalizationHelperTuning.get_raw_text(str(trait_info.__name__))
            row_icon = trait_info.icon
            if not current_types == occult_type:
                if occult_type == OccultType.WITCH:
                    continue
                if current_types == occult_type | OccultType.HUMAN:
                    if cls.icon_trait_already_equipped:
                        row_icon = cls.icon_trait_already_equipped
                        is_enabled = True
                row = ObjectPickerRow(name=display_name,
                  icon=row_icon,
                  tag=occult_type,
                  is_enable=is_enabled)
                if inst_or_cls.use_pie_menu():
                    row.row_tooltip = trait_info.trait_description
                yield row

    def on_choice_selected(self, choice_tag, **kwargs):
        sim = self.get_participant(self.picker_target)
        cmd_switch_occult(OptionalTargetParam(str(sim.id)), choice_tag)

        # if sim.sim_info.occult_tracker.has_occult_type(OccultType.FAIRY):
        #     if choice_tag == OccultType.FAIRY:
        #         push_interaction(affordance=self.add_wing_int, opt_sim=OptionalTargetParam(str(sim.id)))
        #         push_interaction(affordance=Constants.Interactions.CHANGE_TO_FAIRY_FORM, opt_sim=OptionalTargetParam(str(sim.id)))
        #     else:
        #         push_interaction(affordance=self.remove_wing_int, opt_sim=OptionalTargetParam(str(sim.id)))
        #         push_interaction(affordance=Constants.Interactions.CHANGE_FROM_FAIRY_FORM, opt_sim=OptionalTargetParam(str(sim.id)))

        sim.sim_info.trait_tracker.sort_and_send_commodity_list()

        if choice_tag:
            self._show_picker_dialog(sim, target_sim=sim)

    @classmethod
    def _occult_gen(cls, participant):
        for occult, tuning in OccultTracker.OCCULT_DATA.items():
            if tuning.occult_trait is not None and tuning.current_occult_trait is not None:
                is_enabled = (participant.sim_info.occult_tracker.has_occult_type(occult) or
                              participant.sim_info.occult_tracker.has_occult_type(occult | OccultType.HUMAN))
                yield (occult, tuning.occult_trait, is_enabled)

        # Human Trait
        yield (OccultType.HUMAN, services.get_instance_manager(Types.TRAIT).get(HUMAN_REF_TRAIT), True)
