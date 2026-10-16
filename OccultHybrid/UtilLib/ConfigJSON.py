"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
LordPercivalXII's OccultHybrid Mod

> ConfigJSON

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
# ======================================================================================================================
# Module Importation
from pathlib import Path
from OccultHybrid.UtilLib.JSONHandler import JSONHandler, JSON_LIB
from OccultHybrid.UtilLib.JSONParser import json_load
from OccultHybrid.UtilLib.ConfigTemplate import CONFIG_DEFAULT, CONFIG_NAME

# ======================================================================================================================
# JSON Path
#
# CONFIG_PATH = Path(JSON_LIB).resolve().parent
CONFIG_PATH = Path(__file__).resolve().parent.parent.parent.parent

# ======================================================================================================================
# ConfigJSON Class
class ConfigJSON(JSONHandler):
    """
    A Configuration Handler that borrows functions from JSONHandler.
    """
    def __init__(self, cfg_name: str):
        """
        Initialise the ConfigJSON Class & generate the Config file if required.
        """
        super(ConfigJSON, self).__init__(cfg_name, CONFIG_PATH)
        if self.logger is not None:
            self.logger.module_name = f"ConfigJSONHandler Class @ {cfg_name}"
        self.generate_config()

    def generate_config(self):
        """
        Generate the Config JSON. Avoids usage of generate_json().
        :return:
        """
        # Generate Config
        status = self.generate_json(CONFIG_DEFAULT)
        self.getConfigData()

        # Key Check on Existing Config
        if status is False:
            # key_check_list = list(self.json_data.keys())
            missing_keys = []
            for key_def in CONFIG_DEFAULT.keys():
                has_checked = False
                # for key_check in key_check_list:
                if key_def in self.json_data:
                    if self.logger is not None:
                        self.logger.debug(f"DEBUG: CHECK -> {key_def}")
                    # key_check_list.remove(key_check)
                    has_checked = True

                if has_checked is False:
                    missing_keys.append(key_def)

            if self.logger is not None:
                self.logger.debug(f"DEBUG: KEY CHECK MISSING {len(missing_keys)} "
                                  f"KEYS: {missing_keys if len(missing_keys) > 0 else None}")

            # Add missing keys
            if len(missing_keys) > 0:
                if self.logger is not None:
                    self.logger.info(f"Config Check: {len(missing_keys)} keys missing. Appending...\n\n{missing_keys}")

                for key in missing_keys:
                    self.json_data[key] = CONFIG_DEFAULT[key]

                # Update File for future reads
                self.update_json_file()
                if self.logger is not None:
                    self.logger.info(f"Config Check: Updated JSON File {self.json_fp}")
            else:
                if self.logger is not None:
                    self.logger.info(f"Config Check: All keys accounted for. No key appending required.")

    def getConfigData(self):
        """
        Alternate call method to get Config Data.

        :return:
        """
        self.formulate_json()


def setDebugState_Config(state: bool, fp: Path or str = ""):
    """
    Method to set Filepath of Config JSON File.
    :param fp:
    :param state:
    :return:
    """
    if state is False:
        global CONFIG_PATH
        if fp == "":
            CONFIG_PATH = CONFIG_PATH.parent
        else:
            CONFIG_PATH = fp
