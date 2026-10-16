"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
LordPercivalXII's OccultHybrid Mod

> MenuUI Tuning [Origins from InteractionPicker]

(C) Copyright L.P. XII - TD1 & TWoCC 2020 - 2026
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Licensed under MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Codes from other parties are not part of the License and Copyright.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import enum
from OccultHybrid.CoreLib.TD1_OccultHybrid_Config import config_exist, get_option_value
from event_testing.tests import TunableTestSet
from interactions.base.picker_interaction import PickerSuperInteraction
from interactions.context import InteractionSource
from interactions.utils.localization_tokens import LocalizationTokens
from interactions.utils.tunable import TunableContinuation
from interactions.utils.tunable_icon import TunableIconVariant
from sims4.commands import execute
from sims4.localization import TunableLocalizedStringFactory
from sims4.tuning.tunable import TunableList, OptionalTunable, HasTunableSingletonFactory, AutoFactoryInit, Tunable, \
    TunableEnumEntry
from sims4.tuning.tunable_base import GroupNames
from sims4.utils import flexmethod
from snippets import define_snippet
from ui.ui_dialog_picker import BasePickerRow, UiItemPicker, ObjectPickerRow, UiObjectPicker
from sims4.log import Logger

# Importation of MasterApprentice Logger

try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Menu UI 2.0', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Menu UI 2.0', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger('TD1 Menu UI 2.0', default_owner="TwelfthDoctor1")


class MenuUIBaseIcons:
    """
    The MenuUIBaseIcons are base icons for the Menu and Settings UI to rely upon if certain tunings are in place and
    certain icons are not tuned.
    """
    UI_ICON_SETTINGS_ENABLED = TunableIconVariant()
    UI_ICON_SETTINGS_DISABLED = TunableIconVariant()
    UI_ICON_SETTINGS_DISALLOW = TunableIconVariant()
    UI_ICON_MENU_LOCKED = TunableIconVariant()
    UI_ICON_MENU_MISSING = TunableIconVariant()
    UI_ICON_MENU_UNKNOWN = TunableIconVariant()
    UI_ICON_MENU_BACK = TunableIconVariant()
    UI_ICON_MENU_EXIT = TunableIconVariant()
    UI_ICON_MENU_PLACEHOLDER = TunableIconVariant()
    UI_ICON_SETTINGS_VARIATION = TunableIconVariant()
    UI_ICON_SETTINGS_MISSING = TunableIconVariant()
    UI_ICON_SETTINGS_UNKNOWN = TunableIconVariant()


class MenuUIBaseIconsEnums(enum.Int):
    """
    The MenuUIBaseIconsEnums are used to translate the chosen enum from a tunable into its Icon Tunable Data equivalent
    that is contained inside the MenuUIBaseIcons class.
    """
    NONE = 0
    SETTINGS_ENABLED = 1
    SETTINGS_DISABLED = 2
    SETTINGS_DISALLOW = 3
    MENU_LOCKED = 4
    MENU_MISSING = 5
    MENU_UNKNOWN = 6
    MENU_BACK = 7
    MENU_EXIT = 8
    MENU_PLACEHOLDER = 9
    SETTINGS_VARIATION = 10
    SETTINGS_MISSING = 11
    SETTINGS_UNKNOWN = 12


def parse_ui_icon_enum_to_data(icon_enum):
    """
    This function translated the specified icon into the equivalent Icon Data stored in the MenuUIBaseIcon class.
    :param icon_enum: MenuUIBaseIconsEnums
    :return: Icon Data for Picker to resolve (TunableIconVariant)
    """
    if icon_enum == MenuUIBaseIconsEnums.NONE:
        return None

    elif icon_enum == MenuUIBaseIconsEnums.SETTINGS_ENABLED:
        return MenuUIBaseIcons.UI_ICON_SETTINGS_ENABLED

    elif icon_enum == MenuUIBaseIconsEnums.SETTINGS_DISABLED:
        return MenuUIBaseIcons.UI_ICON_SETTINGS_DISABLED

    elif icon_enum == MenuUIBaseIconsEnums.SETTINGS_DISALLOW:
        return MenuUIBaseIcons.UI_ICON_SETTINGS_DISALLOW

    elif icon_enum == MenuUIBaseIconsEnums.MENU_LOCKED:
        return MenuUIBaseIcons.UI_ICON_MENU_LOCKED

    elif icon_enum == MenuUIBaseIconsEnums.MENU_MISSING:
        return MenuUIBaseIcons.UI_ICON_MENU_MISSING

    elif icon_enum == MenuUIBaseIconsEnums.MENU_UNKNOWN:
        return MenuUIBaseIcons.UI_ICON_MENU_UNKNOWN

    elif icon_enum == MenuUIBaseIconsEnums.MENU_BACK:
        return MenuUIBaseIcons.UI_ICON_MENU_BACK

    elif icon_enum == MenuUIBaseIconsEnums.MENU_EXIT:
        return MenuUIBaseIcons.UI_ICON_MENU_EXIT

    elif icon_enum == MenuUIBaseIconsEnums.MENU_PLACEHOLDER:
        return MenuUIBaseIcons.UI_ICON_MENU_PLACEHOLDER

    elif icon_enum == MenuUIBaseIconsEnums.SETTINGS_VARIATION:
        return MenuUIBaseIcons.UI_ICON_SETTINGS_VARIATION

    return None


class OccultHybridMenuUIStructure(HasTunableSingletonFactory, AutoFactoryInit):
    """
    Menu UI Structure for Interaction and Snippet.
    """
    FACTORY_TUNABLES = {
        'icon_enabled': OptionalTunable(
            description='If enabled, specify the icon to be displayed in UI for enabled state.',
            tunable=TunableIconVariant()
        ),
        'icon_disabled': OptionalTunable(
            description='If enabled, specify the icon to be displayed in UI for disabled state.',
            tunable=TunableIconVariant()
        ),
        'name': OptionalTunable(
            description='If enabled, display this name in the UI. Otherwise the display name of the first affordance in the continuation will be used as the name.',
            tunable=TunableLocalizedStringFactory()
        ),
        'item_description': OptionalTunable(
            description='When enabled, the tuned string will be shown as a description.',
            tunable=TunableLocalizedStringFactory()
        ),
        'item_tooltip': OptionalTunable(
            description='When enabled, the tuned string will be shown as a tooltip.',
            tunable=TunableLocalizedStringFactory()
        ),
        'disable_tooltip': OptionalTunable(
            description='When tuned, and the item is disabled, the tuned string will be shown as a tooltip. Otherwise it will try to grab a tooltip off a failed test.',
            tunable=TunableLocalizedStringFactory()
        ),
        'continuation': TunableContinuation(
            description='The continuation to push when this item is selected.',
            minlength=1
        ),
        'enable_tests': OptionalTunable(
            description='Tests which would dictate if this option is enabled in the pie menu.  ORs of ANDs. If disabled, it will default to the tests for the first affordance in the continuation chain.',
            tunable=TunableTestSet()
        ),
        'localization_tokens': OptionalTunable(
            description="Additional localization tokens for this item to use in the name/description. This is in addition to the display name tokens tuned in the continuation's first affordance.",
            tunable=LocalizationTokens.TunableFactory()
        ),
        'visibility_tests': OptionalTunable(
            description='Tests which would dictate if this option is visible in the pie menu.  ORs of ANDs. If disabled, this item will always be visible.',
            tunable=TunableTestSet()
        ),
        'base_icon_enabled': TunableEnumEntry(
            description="The base icon to use for enabled state if icon_enabled is unused.",
            tunable_type=MenuUIBaseIconsEnums,
            default=MenuUIBaseIconsEnums.MENU_MISSING
        ),
        'base_icon_disabled': TunableEnumEntry(
            description="The base icon to use for disabled state if icon_disabled is unused.",
            tunable_type=MenuUIBaseIconsEnums,
            default=MenuUIBaseIconsEnums.NONE
        ),
        'base_icon_locked': TunableEnumEntry(
            description="The base icon to use if the interaction is locked (failed test).",
            tunable_type=MenuUIBaseIconsEnums,
            default=MenuUIBaseIconsEnums.MENU_LOCKED
        ),
        'icon_state_change_tests': OptionalTunable(
            description="Tests to determine whether the enabled or disabled state should be chosen.",
            tunable=TunableTestSet()
        )
    }


class OccultHybridSettingsUIStructure(HasTunableSingletonFactory, AutoFactoryInit):
    FACTORY_TUNABLES = {
        'icon_enabled': OptionalTunable(
            description='If enabled, specify the icon to be displayed in UI.',
            tunable=TunableIconVariant()
        ),
        'icon_disabled': OptionalTunable(
            description='If enabled, specify the icon to be displayed in UI.',
            tunable=TunableIconVariant()
        ),
        'name': OptionalTunable(
            description='If enabled, display this name in the UI. Otherwise the display name of the first affordance in the continuation will be used as the name.',
            tunable=TunableLocalizedStringFactory()
        ),
        'item_description': OptionalTunable(
            description='When enabled, the tuned string will be shown as a description.',
            tunable=TunableLocalizedStringFactory()
        ),
        'item_tooltip': OptionalTunable(
            description='When enabled, the tuned string will be shown as a tooltip.',
            tunable=TunableLocalizedStringFactory()
        ),
        'disable_tooltip': OptionalTunable(
            description='When tuned, and the item is disabled, the tuned string will be shown as a tooltip. Otherwise it will try to grab a tooltip off a failed test.',
            tunable=TunableLocalizedStringFactory()
        ),
        'continuation': TunableContinuation(
            description='The continuation to push when this item is selected.',
            minlength=1
        ),
        'enable_tests': OptionalTunable(
            description='Tests which would dictate if this option is enabled in the pie menu.  ORs of ANDs. If disabled, it will default to the tests for the first affordance in the continuation chain.',
            tunable=TunableTestSet()
        ),
        'localization_tokens': OptionalTunable(
            description="Additional localization tokens for this item to use in the name/description. This is in addition to the display name tokens tuned in the continuation's first affordance.",
            tunable=LocalizationTokens.TunableFactory()
        ),
        'visibility_tests': OptionalTunable(
            description='Tests which would dictate if this option is visible in the pie menu.  ORs of ANDs. If disabled, this item will always be visible.',
            tunable=TunableTestSet()
        ),
        'config_option': Tunable(
            description="The config option to be called upon.",
            tunable_type=str,
            default=""
        ),
        'base_icon_enabled': TunableEnumEntry(
            description="The base icon to use for enabled state if icon_enabled is unused.",
            tunable_type=MenuUIBaseIconsEnums,
            default=MenuUIBaseIconsEnums.SETTINGS_ENABLED
        ),
        'base_icon_disabled': TunableEnumEntry(
            description="The base icon to use for disabled state if icon_disabled is unused.",
            tunable_type=MenuUIBaseIconsEnums,
            default=MenuUIBaseIconsEnums.SETTINGS_DISABLED
        ),
        'base_icon_disallow': TunableEnumEntry(
            description="The base icon to use if the option is disallowed to be chosen (failed enable_tests).",
            tunable_type=MenuUIBaseIconsEnums,
            default=MenuUIBaseIconsEnums.SETTINGS_DISALLOW
        )
    }


# Snippet Definer
(_, TunableOccultHybridMenuUIStructureSnippet) = define_snippet('occulthybrid_menu_ui',
                                                                  OccultHybridMenuUIStructure.TunableFactory())
(_, TunableOccultHybridSettingsUIStructureSnippet) = define_snippet("occulthybrid_settings_ui",
                                                                      OccultHybridSettingsUIStructure.TunableFactory())


def handle_menu_icon(is_enable, state_test, resolver, choice):
    if is_enable:
        if state_test:
            test_result = bool(state_test.run_tests(resolver))
        else:
            test_result = True

        if test_result is True:
            return choice.icon_enabled if choice.icon_enabled is not None else \
                parse_ui_icon_enum_to_data(choice.base_icon_enabled)
        else:
            return choice.icon_disabled if choice.icon_disabled is not None else \
                parse_ui_icon_enum_to_data(choice.base_icon_disabled)

    else:
        return MenuUIBaseIcons.UI_ICON_MENU_LOCKED if choice.base_icon_locked == MenuUIBaseIconsEnums.NONE else \
            parse_ui_icon_enum_to_data(choice.base_icon_locked)


def handle_settings_icon(config_option, is_enable, version_type, choice):
    if config_option == "":
        """
        This test is specifically to allow options without a config option (blank).
        """
        return choice.icon_enabled if choice.icon_enabled is not None else \
            parse_ui_icon_enum_to_data(choice.base_icon_enabled)

    if config_exist(config_option) is False:
        """
        Test for Non-Existence options.
        Returns Unknown Icon State.
        """
        return MenuUIBaseIcons.UI_ICON_SETTINGS_UNKNOWN

    if is_enable:
        if get_option_value(config_option) is True:
            if choice.icon_enabled is not None:
                return choice.icon_enabled
            else:
                return parse_ui_icon_enum_to_data(choice.base_icon_enabled)

        elif get_option_value(config_option) is False:
            if choice.icon_disabled is not None:
                return choice.icon_disabled
            else:
                return parse_ui_icon_enum_to_data(choice.base_icon_disabled)
        else:
            """
            For Configs that are Int, Str, Float data types, they should use the Variation Icon State.
            """
            return MenuUIBaseIcons.UI_ICON_SETTINGS_VARIATION if choice.icon_enabled is None else choice.icon_enabled
    else:
        """
        If Version Type is invalid based from is_enable, return Disallowed Icon State.
        """
        return MenuUIBaseIcons.UI_ICON_SETTINGS_DISALLOW if choice.base_icon_disallow is None else parse_ui_icon_enum_to_data(choice.base_icon_disallow)


class TD1OccultHybridMenuUIPicker(PickerSuperInteraction):
    """
    A deviation of the InteractionPicker to accommodate for requirements for the Menu UI.

    The Menu UI is used for most Menus that are using InteractionPickers.
    """
    INSTANCE_TUNABLES = {
        'picker_dialog': UiItemPicker.TunableFactory(
            description='The item picker dialog.',
            tuning_group=GroupNames.PICKERTUNING
        ),
        'possible_actions': TunableList(
            description='A list of the interactions that will show up in the dialog picker.',
            tunable=TunableOccultHybridMenuUIStructureSnippet(),
            minlength=1,
            tuning_group=GroupNames.PICKERTUNING
        ),
        'return_menu': TunableContinuation(
            description="The Menu UI to return to if no option is selected.",
        )
    }

    def _run_interaction_gen(self, timeline):
        self._show_picker_dialog(self.sim, target_sim=self.sim)
        return True

    @flexmethod
    def picker_rows_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = cls if inst is None else inst
        cloned_context = context.clone_for_insert_next(source=InteractionSource.SCRIPT_WITH_USER_INTENT)
        for choice in inst_or_cls.possible_actions:
            first_continuation = next(iter(choice.continuation), None)

            if master_logger is not None and master_logger is not False:
                master_logger.debug(
                    f"Current Choice:\n{choice}\n\nFirst Continuation:\n{first_continuation}\n\nFull Context:"
                    f"\n{inst_or_cls.possible_actions}"
                )

            if first_continuation is None:

                if master_logger is not None and master_logger is not False:
                    master_logger.debug(
                        f"First Continuation is unexpectedly None. Skipping....."
                    )

            else:
                affordance = first_continuation.affordance
                resolver = affordance.get_resolver(target=target, context=cloned_context, **kwargs)

                if choice.visibility_tests is None or choice.visibility_tests.run_tests(resolver) is not None:
                    tokens = tuple() if choice.localization_tokens is None else choice.localization_tokens.get_tokens(
                        resolver)

                    display_name = affordance.get_name(
                        target=target,
                        context=cloned_context
                    ) if choice.name is None else affordance.create_localized_string(
                        choice.name,
                        tokens,
                        target=target,
                        context=cloned_context,
                        **kwargs
                    )

                    display_description = None if choice.item_description is None else \
                        affordance.create_localized_string(
                            choice.item_description, tokens, target=target, context=cloned_context, **kwargs
                        )
                    # row_tooltip = None # No Tooltip to satisfy interactions without tooltips
                    tag = choice
                    if choice.enable_tests:
                        test_result = choice.enable_tests.run_tests(resolver)
                    else:
                        test_result = affordance.test(target=target, context=cloned_context)
                    # row_tooltip = choice.item_tooltip  # item_tooltip
                    # row_tooltip = test_result.tooltip  # affordance failed test tooltip
                    is_enabled = bool(test_result)
                    # row_tooltip = choice.disable_tooltip  # disable_tooltip

                    row_tooltip = choice.disable_tooltip if is_enabled is False and choice.disable_tooltip is not None \
                        else test_result.tooltip if test_result.tooltip is not None and is_enabled is False else \
                        choice.item_tooltip

                    icon_state = handle_menu_icon(is_enabled, choice.icon_state_change_tests, resolver, choice)

                    icon_info = None if icon_state is None else icon_state(resolver)

                    if master_logger is not None and master_logger is not False:
                        master_logger.debug(
                            f"ICON: {icon_info}\n\n"
                            f"SPECIFIC RESULT: {icon_state}\n\n"
                            f"ROW ENABLED: {is_enabled}"
                        )

                    row = BasePickerRow(
                        is_enable=is_enabled,
                        name=display_name,
                        icon_info=icon_info,
                        row_description=display_description,
                        tag=tag,
                        row_tooltip=row_tooltip
                    )

                    if master_logger is not None and master_logger is not False:
                        master_logger.debug(row)

                    yield row

                else:
                    if master_logger is not None and master_logger is not False:
                        master_logger.debug(
                            f"Affordance Choice [{affordance}] tuned to not be visible due to Test Failure. "
                            f"Skipping....."
                        )

                        master_logger.info(
                            f"[VISIBILITY TESTS DATA]\n{choice.visibility_tests}\n\n"
                            f"{choice.visibility_tests.run_tests(resolver) if choice.visibility_tests is not None else 'Test returns NoneType. Cannot run test.....'}"
                        )

    def on_choice_selected(self, choice, **kwargs):
        if choice is not None:
            self.push_tunable_continuation(choice.continuation)
        else:
            if self.return_menu is not None:
                self.push_tunable_continuation(self.return_menu)


class TD1OccultHybridMenuUIObjectBasedPicker(PickerSuperInteraction):
    """
    A deviation of the InteractionPicker to accommodate for requirements for the Menu UI.

    The Menu UI is used for most Menus that are using InteractionPickers.

    This Menu is configured to use the UIObjectPicker instead.
    """
    INSTANCE_TUNABLES = {
        'picker_dialog': UiObjectPicker.TunableFactory(
            description='The item picker dialog.',
            tuning_group=GroupNames.PICKERTUNING
        ),
        'possible_actions': TunableList(
            description='A list of the interactions that will show up in the dialog picker.',
            tunable=TunableOccultHybridMenuUIStructureSnippet(),
            minlength=1,
            tuning_group=GroupNames.PICKERTUNING
        ),
        'return_menu': TunableContinuation(
            description="The Menu UI to return to if no option is selected.",
        )
    }

    def _run_interaction_gen(self, timeline):
        self._show_picker_dialog(self.sim, target_sim=self.sim)
        return True

    @flexmethod
    def picker_rows_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = cls if inst is None else inst
        cloned_context = context.clone_for_insert_next(source=InteractionSource.SCRIPT_WITH_USER_INTENT)
        for choice in inst_or_cls.possible_actions:
            first_continuation = next(iter(choice.continuation), None)

            if master_logger is not None and master_logger is not False:
                master_logger.debug(
                    f"Current Choice:\n{choice}\n\nFirst Continuation:\n{first_continuation}\n\nFull Context:"
                    f"\n{inst_or_cls.possible_actions}"
                )

            if first_continuation is None:

                if master_logger is not None and master_logger is not False:
                    master_logger.debug(
                        f"First Continuation is unexpectedly None. Skipping....."
                    )

            else:
                affordance = first_continuation.affordance
                resolver = affordance.get_resolver(target=target, context=cloned_context, **kwargs)

                if choice.visibility_tests is None or choice.visibility_tests.run_tests(resolver) is not None:
                    tokens = tuple() if choice.localization_tokens is None else choice.localization_tokens.get_tokens(
                        resolver)

                    display_name = affordance.get_name(
                        target=target,
                        context=cloned_context
                    ) if choice.name is None else affordance.create_localized_string(
                        choice.name,
                        tokens,
                        target=target,
                        context=cloned_context,
                        **kwargs
                    )

                    display_description = None if choice.item_description is None else \
                        affordance.create_localized_string(
                            choice.item_description, tokens, target=target, context=cloned_context, **kwargs
                        )
                    # row_tooltip = None  # No Tooltip to satisfy interactions without tooltips
                    tag = choice
                    if choice.enable_tests:
                        test_result = choice.enable_tests.run_tests(resolver)
                    else:
                        test_result = affordance.test(target=target, context=cloned_context)
                    # row_tooltip = choice.item_tooltip  # item_tooltip
                    # row_tooltip = test_result.tooltip  # affordance failed test tooltip
                    is_enabled = bool(test_result)
                    # row_tooltip = choice.disable_tooltip  # disable_tooltip

                    row_tooltip = choice.disable_tooltip if is_enabled is False and choice.disable_tooltip is not None \
                        else test_result.tooltip if test_result.tooltip is not None and is_enabled is False else \
                        choice.item_tooltip

                    icon_state = handle_menu_icon(is_enabled, choice.icon_state_change_tests, resolver, choice)

                    icon_info = None if icon_state is None else icon_state(resolver)

                    if master_logger is not None and master_logger is not False:
                        master_logger.debug(
                            f"ICON: {icon_info}\n\n"
                            f"SPECIFIC RESULT: {icon_state}\n\n"
                            f"ROW ENABLED: {is_enabled}"
                        )

                    row = ObjectPickerRow(
                        is_enable=is_enabled,
                        name=display_name,
                        icon_info=icon_info,
                        row_description=display_description,
                        tag=tag,
                        row_tooltip=row_tooltip
                    )

                    if master_logger is not None and master_logger is not False:
                        master_logger.debug(row)

                    yield row

                else:
                    if master_logger is not None and master_logger is not False:
                        master_logger.debug(
                            f"Affordance Choice [{affordance}] tuned to not be visible due to Test Failure. "
                            f"Skipping....."
                        )

                        master_logger.info(
                            f"[VISIBILITY TESTS DATA]\n{choice.visibility_tests}\n\n"
                            f"{choice.visibility_tests.run_tests(resolver) if choice.visibility_tests is not None else 'Test returns NoneType. Cannot run test.....'}"
                        )

    def on_choice_selected(self, choice, **kwargs):
        if choice is not None:
            self.push_tunable_continuation(choice.continuation)
        else:
            if self.return_menu is not None:
                self.push_tunable_continuation(self.return_menu)


class TD1OccultHybridSettingsUIPicker(PickerSuperInteraction):
    """
    A deviation of the InteractionPicker to accommodate for requirements for the Settings UI.

    The Settings UI is used specifically for Config Options to handle enabled/disabled states and lessen the need
    for Interactions to call upon the change config option command.
    """
    INSTANCE_TUNABLES = {
        'picker_dialog': UiItemPicker.TunableFactory(
            description='The item picker dialog.',
            tuning_group=GroupNames.PICKERTUNING
        ),
        'possible_actions': TunableList(
            description='A list of the interactions that will show up in the dialog picker.',
            tunable=TunableOccultHybridSettingsUIStructureSnippet(),
            minlength=1,
            tuning_group=GroupNames.PICKERTUNING
        ),
        'return_menu': TunableContinuation(
            description="The Menu UI to return to if no option is selected.",
        )
    }

    def _run_interaction_gen(self, timeline):
        self._show_picker_dialog(self.sim, target_sim=self.sim)
        return True

    @flexmethod
    def picker_rows_gen(cls, inst, target, context, **kwargs):
        inst_or_cls = cls if inst is None else inst
        cloned_context = context.clone_for_insert_next(source=InteractionSource.SCRIPT_WITH_USER_INTENT)
        for choice in inst_or_cls.possible_actions:
            first_continuation = next(iter(choice.continuation), None)

            if master_logger is not None and master_logger is not False:
                master_logger.debug(
                    f"Current Choice:\n{choice}\n\nFirst Continuation:\n{first_continuation}\n\nFull Context:"
                    f"\n{inst_or_cls.possible_actions}"
                )

            if first_continuation is None:

                if master_logger is not None and master_logger is not False:
                    master_logger.debug(
                        f"First Continuation is unexpectedly None. Skipping....."
                    )
            else:
                affordance = first_continuation.affordance
                resolver = affordance.get_resolver(target=target, context=cloned_context, **kwargs)

                if choice.visibility_tests is None or choice.visibility_tests.run_tests(resolver) is not None:
                    tokens = tuple() if choice.localization_tokens is None else choice.localization_tokens.get_tokens(
                        resolver)

                    display_name = affordance.get_name(
                        target=target,
                        context=cloned_context
                    ) if choice.name is None else affordance.create_localized_string(
                        choice.name,
                        tokens,
                        target=target,
                        context=cloned_context,
                        **kwargs
                    )

                    display_description = None if choice.item_description is None else \
                        affordance.create_localized_string(
                            choice.item_description, tokens, target=target, context=cloned_context, **kwargs
                        )
                    # row_tooltip = None # No Tooltip to satisfy interactions without tooltips
                    tag = choice
                    if choice.enable_tests:
                        test_result = choice.enable_tests.run_tests(resolver)
                    else:
                        test_result = affordance.test(target=target, context=cloned_context)
                    # row_tooltip = choice.item_tooltip  # item_tooltip
                    # row_tooltip = test_result.tooltip  # affordance failed test tooltip
                    is_enabled = bool(test_result)
                    # row_tooltip = choice.disable_tooltip  # disable_tooltip

                    row_tooltip = choice.disable_tooltip if is_enabled is False and choice.disable_tooltip is not None \
                        else test_result.tooltip if test_result.tooltip is not None and is_enabled is False else \
                        choice.item_tooltip

                    icon_state = handle_settings_icon(choice.config_option, is_enabled, None, choice)

                    icon_info = None if icon_state is None else icon_state(resolver)

                    if master_logger is not None and master_logger is not False:
                        master_logger.debug(
                            f"ICON: {icon_info}\n\n"
                            f"SPECIFIC RESULT: {icon_state}\n\n"
                            f"VERSION TYPE: {None}\n\n"
                            f"CONFIG OPTION: {choice.config_option}\n\n"
                            f"CONFIG TEST EXISTENCE: {config_exist(choice.config_option)}\n\n"
                            f"CONFIG VALUE: {get_option_value(choice.config_option) if choice.config_option is not '' else 'NO SPECIFIED OPTION'}\n\n"
                            f"ROW ENABLED: {is_enabled}"
                        )

                    row = BasePickerRow(
                        is_enable=is_enabled,
                        name=display_name,
                        icon_info=icon_info,
                        row_description=display_description,
                        tag=tag,
                        row_tooltip=row_tooltip
                    )

                    if master_logger is not None and master_logger is not False:
                        master_logger.debug(row)

                    yield row

                else:
                    if master_logger is not None and master_logger is not False:
                        master_logger.debug(
                            f"Affordance Choice [{affordance}] tuned to not be visible due to Test Failure. "
                            f"Skipping....."
                        )

                        master_logger.info(
                            f"[VISIBILITY TESTS DATA]\n{choice.visibility_tests}\n\n"
                            f"{choice.visibility_tests.run_tests(resolver) if choice.visibility_tests is not None else 'Test returns NoneType. Cannot run test.....'}"
                        )

    def on_choice_selected(self, choice, **kwargs):
        if choice is not None:
            if choice.config_option is not "":
                master_logger.info(
                    f"[OPTION SELECTED]\n{choice.config_option}"
                )
                execute(f'td1occulthybrid.set_option {choice.config_option}', None)
                # set_option(choice.config_option, None)
            self.push_tunable_continuation(choice.continuation)
        else:
            if self.return_menu is not None:
                self.push_tunable_continuation(self.return_menu)
