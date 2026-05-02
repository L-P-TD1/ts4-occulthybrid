"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
LordPercivalXII's OccultHybrid Mod

> Decorator Tuning

(C) Copyright L.P. XII - TD1 & TWoCC 2020 - 2026
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Licensed under MIT License

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
