"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
LordPercivalXII's OccultHybrid Mod

> CheatSetter Tuning

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
import services
from OccultHybrid.CoreLib.TD1_OccultHybrid_Config import get_option_value
from sims4.log import Logger
from sims4.resources import Types
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import TunableList, TunableTuple, Tunable, TunableReference

# Importation of MasterApprentice Logger
try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger
    apprentice_logger = ApprenticeLogger('TD1 Cheat Setter Injector', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger
    master_logger = MasterLogger('TD1 Cheat Setter Injector', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger('TD1 Cheat Setter Injector', default_owner='TwelfthDoctor1')


class TD1DevAccessPanelCheatSetter(metaclass=HashedTunedInstanceMetaclass,
                                   manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'config_option': Tunable(
            description='The configuration option that relies on this system.',
            tunable_type=str,
            default=''
        ),
        'cheat_setter': TunableList(
            tunable=TunableTuple(
                cheat=Tunable(
                    description='Modifier if the Cheat Tunable should ultimately be True or False',
                    tunable_type=bool,
                    default=False
                ),
                debug=Tunable(
                    description='Modifier if the Debug Tunable should ultimately be True or False',
                    tunable_type=bool,
                    default=False
                ),
                affordances=TunableList(
                    description='The List of affordance to be tuned.',
                    tunable=TunableReference(
                        description='The Affordance to be tuned.',
                        manager=services.get_instance_manager(Types.INTERACTION),
                        pack_safe=True
                    )
                )
            )
        )
    }

    __slots__ = ('config_option', 'cheat_setter')

    @classmethod
    def _tuning_loaded_callback(cls):
        if get_option_value(cls.config_option) is True:
            for (affordances, cheat, debug) in cls.cheat_setter:

                if affordances is None:

                    message0 = f"No Affordance List to tune Cheat & Debug Tunables."

                    logger.warn(message0, owner="TwelfthDoctor1")

                    if apprentice_logger is not None and apprentice_logger is not False:
                        apprentice_logger.warn(message0, owner="TwelfthDoctor1")

                    if master_logger is not None and master_logger is not False:
                        master_logger.warn(message0, owner="TwelfthDoctor1")

                    return

                # apprentice_logger.info(
                #     f"NOTICE: THIS IS A DEBUG INFORMATION TO DEBUG CHEATSETTER.\n\nConfig Option: {cls.config_option}\nCheatSetter: {cls.cheat_setter}\n\nCheat: {cheat}\nDebug: {debug}\nAffordances:{affordances}"
                # )
                # master_logger.info(
                #     f"NOTICE: THIS IS A DEBUG INFORMATION TO DEBUG CHEATSETTER.\n\nConfig Option: {cls.config_option}\nCheatSetter: {cls.cheat_setter}\n\nCheat: {cheat}\nDebug: {debug}\nAffordances:{affordances}"
                # )

                for affordance in affordances:
                    if affordance is not "affordances":
                        for af in affordance:
                            TD1DevAccessPanelCheatSetter.set_cheat_interaction(af, bool(cheat[1]))
                            TD1DevAccessPanelCheatSetter.set_debug_interaction(af, bool(debug[1]))

    @staticmethod
    def set_cheat_interaction(affordance, cheat):
        if cheat is not None:

            if cheat is True:

                message1 = f"Changing Affordance: {affordance} Cheat Tunable into {cheat}"

                logger.info(message1, owner="TwelfthDoctor1")

                if apprentice_logger is not None and apprentice_logger is not False:
                    apprentice_logger.info(message1, owner="TwelfthDoctor1")

                if master_logger is not None and master_logger is not False:
                    master_logger.info(message1, owner="TwelfthDoctor1")

                affordance.cheat = True

            elif cheat is False:

                message1 = f"Changing Affordance: {affordance} Cheat Tunable into {cheat}"

                logger.info(message1, owner="TwelfthDoctor1")

                if apprentice_logger is not None and apprentice_logger is not False:
                    apprentice_logger.info(message1, owner="TwelfthDoctor1")

                if master_logger is not None and master_logger is not False:
                    master_logger.info(message1, owner="TwelfthDoctor1")

                affordance.cheat = False

            else:

                message2 = f"Affordance: {affordance} does not require Injection Change as Cheat Tunable is {cheat}"

                logger.info(message2, owner="TwelfthDoctor1")

                if apprentice_logger is not None and apprentice_logger is not False:
                    apprentice_logger.info(message2, owner="TwelfthDoctor1")

                if master_logger is not None and master_logger is not False:
                    master_logger.info(message2, owner="TwelfthDoctor1")

    @staticmethod
    def set_debug_interaction(affordance, debug):
        if debug is not None:
            if debug is True:
                message3 = f"Changing Affordance: {affordance} Cheat Tunable into {debug}"

                logger.info(message3, owner="TwelfthDoctor1")

                if apprentice_logger is not None and apprentice_logger is not False:
                    apprentice_logger.info(message3, owner="TwelfthDoctor1")

                if master_logger is not None and master_logger is not False:
                    master_logger.info(message3, owner="TwelfthDoctor1")

                affordance.debug = True

            elif debug is False:
                message3 = f"Changing Affordance: {affordance} Cheat Tunable into {debug}"

                logger.info(message3, owner="TwelfthDoctor1")

                if apprentice_logger is not None and apprentice_logger is not False:
                    apprentice_logger.info(message3, owner="TwelfthDoctor1")

                if master_logger is not None and master_logger is not False:
                    master_logger.info(message3, owner="TwelfthDoctor1")

                affordance.debug = False

            else:

                message4 = f"Affordance: {affordance} does not require Injection Change as Cheat Tunable is {debug}"

                logger.info(message4, owner="TwelfthDoctor1")

                if apprentice_logger is not None and apprentice_logger is not False:
                    apprentice_logger.info(message4, owner="TwelfthDoctor1")

                if master_logger is not None and master_logger is not False:
                    master_logger.info(message4, owner="TwelfthDoctor1")
