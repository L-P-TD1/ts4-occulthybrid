"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
LordPercivalXII's OccultHybrid Mod

> Config Tuning

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
from pathlib import Path
import services
from sims4.commands import Command, CommandType, Output
from sims4.localization import LocalizationHelperTuning
from sims4.tuning.tunable import TunableMapping, Tunable, TunableTuple
from ui.ui_dialog import UiDialogOkCancel
from ui.ui_dialog_generic import UiDialogTextInputOkCancel
from ui.ui_dialog_notification import UiDialogNotification
from OccultHybrid.UtilLib.ConfigJSON import ConfigJSON
from OccultHybrid.UtilLib.ConfigTemplate import CONFIG_NAME, CONFIG_DEFAULT, CONFIG_CHANGE_SHOW

# Importation of MasterApprentice Logger

try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Developer/Debug Access Panel Config', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 OccultHybrid Config', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False


class TD1OccultHybridConfigHandlerUI:
    CONFIG_UI_TEXT_INPUT = 'config_value'
    CONFIG_UI_TEXT_DISPLAY = TunableMapping(
        description='List to hold the UI Text for each option.',
        key_name='option_type',
        key_type=Tunable(
            description='The option type for the UI to be associated with.',
            tunable_type=str,
            default=''
        ),
        value_name='ui_data',
        value_type=TunableTuple(
            ok_cancel=UiDialogOkCancel.TunableFactory(
                description='Meant for Boolean Options.',
            ),
            text_input=UiDialogTextInputOkCancel.TunableFactory(
                description='Meant for String, Integer and Float Options. For 1 Text Input.',
                text_inputs=(CONFIG_UI_TEXT_INPUT),
            ),
        )
    )


main_dir = Path(__file__).resolve().parent.parent.parent.parent

config = ConfigJSON(CONFIG_NAME)
config.generate_config()
config.getConfigData()

main_header = 'TD1 Occult Hybrid Config Settings'


@Command('td1occulthybrid.list_config', command_type=CommandType.Live)
def print_config_values(_connection=None):
    output = Output(_connection)
    config.getConfigData()

    for k,v in config.return_json().items():
        output(f"{k}: {v}")


@Command('td1occulthybrid.list_config_notif', command_type=CommandType.Live)
def print_config_values_notif(_connection=None):
    client = services.client_manager().get_first_client()
    output = Output(_connection)
    config.getConfigData()
    text_final = ""
    for k, v in config.return_json().items():
        output(f"{k}: {v}")
        text_final += f'[{k}]: {v}\n\n'
    text_final += 'These modifier tunings can be found inside the TD1_OccultHybrid_Settings.cfg file. Use the Settings Panel to modify settings.'
    message_title = lambda **_: LocalizationHelperTuning.get_raw_text('TD1 Occult Hybrid Mod Configurations')
    message_text = lambda **_: LocalizationHelperTuning.get_raw_text(text_final)
    notification = UiDialogNotification.TunableFactory().default(
        client.active_sim,
        text=message_text,
        title=message_title,
        information_level=UiDialogNotification.UiDialogNotificationLevel.SIM,
        expand_behavior=UiDialogNotification.UiDialogNotificationExpandBehavior.FORCE_EXPAND,
        visual_type=UiDialogNotification.UiDialogNotificationVisualType.SPECIAL_MOMENT
    )
    notification.show_dialog()


@Command('td1occulthybrid.list_config_all', command_type=CommandType.Live)
def print_all_config_values(_connection=None):
    output = Output(_connection)
    config.getConfigData()

    for k, v in config.return_json().items():
        output(f"{k}: {v}")

    for (option_type, dialog_data) in TD1OccultHybridConfigHandlerUI.CONFIG_UI_TEXT_DISPLAY.items():
        output(f"{option_type}")


@Command('td1occulthybrid.set_option', command_type=CommandType.Live)
def config_set_option(option, _connection=None):
    output = Output(_connection)
    config.getConfigData()

    if option in config.return_json():
        for (option_type, dialog_data) in TD1OccultHybridConfigHandlerUI.CONFIG_UI_TEXT_DISPLAY.items():
            if option_type == option:
                client = services.client_manager().get_first_client()
                if type(CONFIG_DEFAULT[option]) == bool:
                    def on_response(dialog):
                        if dialog.accepted:
                            option_toggle(option)

                    dialog = dialog_data.ok_cancel(None)
                    dialog.add_listener(on_response)
                    dialog.show_dialog()
                else:
                    def on_response(dialog):
                        if dialog.accepted:
                            option_toggle(option, str(dialog.text_input_responses.get("config_value")))

                    dialog = dialog_data.text_input(None)
                    dialog.add_listener(on_response)
                    dialog.show_dialog()

    else:
        output("Wrong Option Specified. Please refer to config list and try again.")


def option_toggle(config_key, to_set:str=""):
    client = services.client_manager().get_first_client()

    cfg_value = config.return_specific_json(config_key)

    if type(cfg_value) == bool:
        config.update_specific_json(config_key, not cfg_value)

        to_set = not cfg_value

    elif type(cfg_value) == int or type(cfg_value) == float:
        if to_set.isdigit():
            config.update_specific_json(config_key, int(to_set))
        else:
            config.update_specific_json(config_key, float(to_set))

    else:
        config.update_specific_json(config_key, str(to_set))

    config.update_json_file()

    if apprentice_logger is not None and apprentice_logger is not False:
        apprentice_logger.info(
            f"Option: {config_key} has been set to {to_set}. (Formerly {cfg_value})",
            owner="TwelfthDoctor1")

    if master_logger is not None and master_logger is not False:
        master_logger.info(f"Option: {config_key} has been set to {to_set}. (Formerly {cfg_value})",
                           owner="TwelfthDoctor1")

    if CONFIG_CHANGE_SHOW[config_key] is True:
        dialog_message = f"The option: {config_key} has been changed from {cfg_value} to {to_set}.\n\nA restart may be required for changes to take effect."

    else:
        dialog_message = f"The option: {config_key} has been changed from {cfg_value} to {to_set}."

    message_title_config_change = lambda **_: LocalizationHelperTuning.get_raw_text("Access Panel Option Change")
    message_text_config_change = lambda **_: LocalizationHelperTuning.get_raw_text(dialog_message)

    notification_config_change = UiDialogNotification.TunableFactory().default(
        client.active_sim,
        text=message_text_config_change,
        title=message_title_config_change,
        expand_behavior=UiDialogNotification.UiDialogNotificationExpandBehavior.FORCE_EXPAND,
        urgency=UiDialogNotification.UiDialogNotificationUrgency.URGENT
    )
    notification_config_change.show_dialog()


def get_option_value(option):
    """
    Gets the value from the option (key) in the Config List.
    :param option:
    :return:
    """
    config.getConfigData()
    return config.return_specific_json(option)


def config_exist(option: str):
    config.getConfigData()
    if option in config.json_data:
        return True
    else:
        return False
