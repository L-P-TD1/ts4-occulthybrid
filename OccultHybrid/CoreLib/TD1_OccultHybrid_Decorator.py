"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
TwelfthDoctor1's Occult Hybrid Handler

> Decorator Tuning

(C) Copyright TD1 & TWoCC 2020 - 2022
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Licensed under CC-BY-NC-ND 4.0

https://creativecommons.org/licenses/by-nc-nd/4.0/

Codes from other parties are not part of the License and Copyright.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
from functools import wraps

# Importation of Master Logger

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Py3 Decorator', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False


def decorator(target_func, new_func):

    @wraps(target_func)
    def _decorator(*args, **kwargs):
        # Code to Run Before Func
        # if master_logger is not None and master_logger is not False:
        #     master_logger.info(f"[DECORATOR PROCESS - HANDLER] Decorating: {target_func} | {new_func}")

        return new_func(target_func, *args, **kwargs)

    # Returner
    return _decorator


def to_decorate(target_obj, target_func_name):
    """
    Decorator to Inject Function to Specified Class Object and Function Subset.
    :param target_obj: Class Object
    :param target_func_name: Function Subject of Class Object
    :return:
    """

    def _to_decorate(new_func):
        # if master_logger is not None and master_logger is not False:
        #     master_logger.info(f"[DECORATOR PROCESS - 2] Target Function Name: {target_func_name}")

        target_func = getattr(target_obj, target_func_name)

        # if master_logger is not None and master_logger is not False:
        #     master_logger.info(f"[DECORATOR PROCESS - 3] Target Function: {target_func}")

        setattr(target_obj, target_func_name, decorator(target_func, new_func))

        return new_func

    # if master_logger is not None and master_logger is not False:
    #     master_logger.info(f"[DECORATOR PROCESS - 1] Inject: {target_func_name}")

    # Returner
    return _to_decorate
