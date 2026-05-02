"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
LordPercivalXII's OccultHybrid Mod

> Exception Tuning

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
# Importation of MasterApprentice Logger
try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger
    apprentice_logger = ApprenticeLogger('TD1 Exception Watcher', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger
    master_logger = MasterLogger('TD1 Exception Watcher', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False


class DevAccessPanelException(BaseException):
    """
    A custom Exception explicitly for the DevAccessPanel to differentiate errors.
    """
    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def __new__(cls, *args, **kwargs):
        pass


def exception_checker(func):
    """
    The Exception Checker is used to check for any Exceptions in the running code. If tripped, an error
    will be asserted and an LastException will occur. From there, other LE Analyzers will take over to
    scrutinise and debug the issue.

    :param func: The function to be tested. (Can class be used?)
    :return: Exception Error or None
    """
    try:
        func()

    except Exception as e:
        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.error(f"EXCEPTION ERROR:\nPLEASE FORWARD THIS TO TWELFTHDOCTOR1 AND INCLUDE ANY OTHER "
                                    f"LAST EXCEPTIONS WHERE APPLICABLE!\n\n{e}")

        if master_logger is not None and master_logger is not False:
            master_logger.error(f"EXCEPTION ERROR:\n\n{e}")

        raise Exception(f"EXCEPTION ERROR:\nPLEASE FORWARD THIS TO TWELFTHDOCTOR1 AND INCLUDE ANY OTHER LAST "
                        f"EXCEPTIONS WHERE APPLICABLE!\n\n{e}")
