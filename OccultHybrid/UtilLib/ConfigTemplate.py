"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
LordPercivalXII's OccultHybrid Mod

> ConfigTemplate

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
# DEFAULT CONFIGURATION FILE
# This is the default settings for the config file (in .json)
#
# JSON Methodology make use of Python Dictionaries, thereby simplifying
# addition, deletion, and modification processes.
#
# Ensure that the keys are UNIQUE. Also ensure that the keys in code FULLY MATCH
# those written here, or else an error will occur inferring that the key does not exist.
#
# Default values can either be set from here for in UI via value. However, it is recommended to do it here instead.

CONFIG_NAME = "TD1_OccultHybrid_Settings"  # Name of Config File
CONFIG_DEFAULT = {
    "override_motive_panel": True,
    "occult_form_memory": True,
    "allow_hybrid_babies": True,
    "post_cas_occult_autoadd": False,
    "werewolf_stabilization": False,
    "debug_log_commodity": False,
    "cheat_debug_pie_menu": False
    # "show_autoadd_dialog": True,
    # "last_played_version": "1.xx",
    # "perm_no_show_autoadd_dialog": False
}

CONFIG_CHANGE_SHOW = {
    "override_motive_panel": False,
    "occult_form_memory": True,
    "allow_hybrid_babies": True,
    "post_cas_occult_autoadd": False,
    "werewolf_stabilization": True,
    "debug_log_commodity": False,
    "cheat_debug_pie_menu": False
    # "show_autoadd_dialog": False, # Will never show change dialog unless via command
    # "last_played_version": False,
    # "perm_no_show_autoadd_dialog": False
}
# ======================================================================================================================
