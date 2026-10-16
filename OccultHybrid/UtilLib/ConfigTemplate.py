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
