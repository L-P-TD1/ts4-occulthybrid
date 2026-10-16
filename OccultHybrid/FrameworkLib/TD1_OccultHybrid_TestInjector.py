"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
LordPercivalXII's OccultHybrid Mod

> TestInjector Tuning

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
from event_testing.tests import TunableGlobalTestSet, TunableTestSet
from sims4.common import Pack, is_available_pack
from sims4.log import Logger
from sims4.resources import Types
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import TunableMapping, TunableList, TunableReference, TunableTuple, \
    Tunable, TunableEnumEntry

# Importation of MasterApprentice Logger

try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Tests Injector & Replacer', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Tests Injector & Replacer', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger('TD1 Tests Injector & Replacer', default_owner='TwelfthDoctor1')


class TD1OccultHybridTestsInjector(metaclass=HashedTunedInstanceMetaclass,
                                   manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'test_globals': TunableMapping(
            description='Test Globals data to be injected into an Interaction.',
            key_name='interaction_instance',
            key_type=TunableList(
                description='The list of interactions to be injected.',
                tunable=TunableReference(
                    description='The instance of the Interaction.',
                    manager=services.get_instance_manager(Types.INTERACTION)
                )
            ),
            value_name='test_data',
            value_type=TunableTuple(
                description='The data that holds the test data.',
                test_globals=TunableGlobalTestSet(
                    description='A set of global tests that are always run before other tests. All tests must pass in order for the interaction to run.',
                ),
                replace_test_globals=Tunable(
                    description='Modifier to determine whether the Global TestSet should be overridden.',
                    tunable_type=bool,
                    default=False
                ),
                pack=TunableEnumEntry(
                    description='The pack to test for.',
                    tunable_type=Pack,
                    default=Pack.BASE_GAME
                )
            )
        ),
        'interaction_tests': TunableMapping(
            description='Tests data to be injected into an Interaction.',
            key_name='interaction_instance',
            key_type=TunableList(
                description='The list of interactions to be injected.',
                tunable=TunableReference(
                    description='The instance of the Interaction.',
                    manager=services.get_instance_manager(Types.INTERACTION)
                )
            ),
            value_name='test_data',
            value_type=TunableTuple(
                description='The data that holds the test data.',
                tests=TunableTestSet(
                    description='A list of tests groups.  At least one must pass all its sub-tests to pass the TestSet. ORs of ANDs',
                ),
                replace_test=Tunable(
                    description='Modifier to determine whether the TestSet should be overridden.',
                    tunable_type=bool,
                    default=False
                ),
                pack=TunableEnumEntry(
                    description='The pack to test for.',
                    tunable_type=Pack,
                    default=Pack.BASE_GAME
                )
            )
        ),
        'test_set_instance_tests': TunableMapping(
            description='Tests data to be injected into an TestSetInstance.',
            key_name='test_set_instance',
            key_type=TunableList(
                description='The list of TestSetInstances to be injected.',
                tunable=TunableReference(
                    description='The instance of the TestSetInstance.',
                    manager=services.get_instance_manager(Types.SNIPPET)
                )
            ),
            value_name='test_data',
            value_type=TunableTuple(
                description='The data that holds the test data.',
                tests=TunableTestSet(
                    description='A list of tests groups.  At least one must pass all its sub-tests to pass the TestSet. ORs of ANDs',
                ),
                replace_test=Tunable(
                    description='Modifier to determine whether the TestSet should be overridden.',
                    tunable_type=bool,
                    default=False
                ),
                pack=TunableEnumEntry(
                    description='The pack to test for.',
                    tunable_type=Pack,
                    default=Pack.BASE_GAME
                )
            )
        ),
        'test_autonomous': TunableMapping(
            description='Test Autonomous data to be injected into an Interaction.',
            key_name='interaction_instance',
            key_type=TunableList(
                description='The list of interactions to be injected.',
                tunable=TunableReference(
                    description='The instance of the Interaction.',
                    manager=services.get_instance_manager(Types.INTERACTION)
                )
            ),
            value_name='test_data',
            value_type=TunableTuple(
                description='The data that holds the test data.',
                test_autonomous=TunableTestSet(
                    description='A set of tests that are only run for interactions being considered by autonomy.',
                ),
                replace_test_autonomous=Tunable(
                    description='Modifier to determine whether the Autonomous TestSet should be overridden.',
                    tunable_type=bool,
                    default=False
                ),
                pack=TunableEnumEntry(
                    description='The pack to test for.',
                    tunable_type=Pack,
                    default=Pack.BASE_GAME
                )
            )
        ),
    }

    __slots__ = ('test_globals', 'interaction_tests', 'test_set_instance_tests', 'test_autonomous')

    @classmethod
    def _tuning_loaded_callback(cls):
        if cls.test_globals is not None:
            for (interaction_instance, test_data) in cls.test_globals.items():
                if is_available_pack(test_data.pack):
                    if interaction_instance is None:
                        message1 = 'No Interaction Instances inside Global TestSet Injector. Injection cannot continue.'

                        if apprentice_logger is not None and apprentice_logger is not False:
                            apprentice_logger.error(message1, owner="TwelfthDoctor1")

                        if master_logger is not None and master_logger is not False:
                            master_logger.error(message1, owner="TwelfthDoctor1")

                        logger.info(message1, owner="TwelfthDoctor1")

                        return

                    if test_data is None or test_data.test_globals is None:
                        message2 = 'No Test Data inside Global TestSet Injector. Injection cannot continue.'

                        if apprentice_logger is not None and apprentice_logger is not False:
                            apprentice_logger.error(message2, owner="TwelfthDoctor1")

                        if master_logger is not None and master_logger is not False:
                            master_logger.error(message2, owner="TwelfthDoctor1")

                        logger.info(message2, owner="TwelfthDoctor1")

                        return

                    for interaction in interaction_instance:
                        if hasattr(test_data, "test_globals"):
                            cls.inject_testset_globals_into_interaction(interaction, test_data.test_globals, test_data.replace_test_globals)

        if cls.interaction_tests is not None:
            for (interaction_instance, test_data) in cls.interaction_tests.items():
                if is_available_pack(test_data.pack):
                    if interaction_instance is None:
                        message1 = 'No Interaction Instances inside Global TestSet Injector. Injection cannot continue.'

                        if apprentice_logger is not None and apprentice_logger is not False:
                            apprentice_logger.error(message1, owner="TwelfthDoctor1")

                        if master_logger is not None and master_logger is not False:
                            master_logger.error(message1, owner="TwelfthDoctor1")

                        logger.info(message1, owner="TwelfthDoctor1")

                        return

                    if test_data is None or test_data.tests is None:
                        message2 = 'No Test Data inside Global TestSet Injector. Injection cannot continue.'

                        if apprentice_logger is not None and apprentice_logger is not False:
                            apprentice_logger.error(message2, owner="TwelfthDoctor1")

                        if master_logger is not None and master_logger is not False:
                            master_logger.error(message2, owner="TwelfthDoctor1")

                        logger.info(message2, owner="TwelfthDoctor1")

                        return

                    for interaction in interaction_instance:
                        if hasattr(test_data, "tests"):
                            cls.inject_tests_int_into_interaction(interaction, test_data.tests, test_data.replace_test)

        if cls.test_set_instance_tests is not None:
            for (test_set_instance, test_data) in cls.test_set_instance_tests.items():
                if is_available_pack(test_data.pack):
                    if test_set_instance is None:
                        message1 = 'No Interaction Instances inside Global TestSet Injector. Injection cannot continue.'

                        if apprentice_logger is not None and apprentice_logger is not False:
                            apprentice_logger.error(message1, owner="TwelfthDoctor1")

                        if master_logger is not None and master_logger is not False:
                            master_logger.error(message1, owner="TwelfthDoctor1")

                        logger.info(message1, owner="TwelfthDoctor1")

                        return

                    if test_data is None or test_data.tests is None:
                        message2 = 'No Test Data inside Global TestSet Injector. Injection cannot continue.'

                        if apprentice_logger is not None and apprentice_logger is not False:
                            apprentice_logger.error(message2, owner="TwelfthDoctor1")

                        if master_logger is not None and master_logger is not False:
                            master_logger.error(message2, owner="TwelfthDoctor1")

                        logger.info(message2, owner="TwelfthDoctor1")

                        return

                    for test_set in test_set_instance:
                        if hasattr(test_data, "tests"):
                            cls.inject_tests_ts_into_test_set(test_set, test_data.tests, test_data.replace_test)

        if cls.test_autonomous is not None:
            for (interaction_instance, test_data) in cls.test_autonomous.items():
                if is_available_pack(test_data.pack):
                    if interaction_instance is None:
                        message1 = 'No Interaction Instances inside Global TestSet Injector. Injection cannot continue.'

                        if apprentice_logger is not None and apprentice_logger is not False:
                            apprentice_logger.error(message1, owner="TwelfthDoctor1")

                        if master_logger is not None and master_logger is not False:
                            master_logger.error(message1, owner="TwelfthDoctor1")

                        logger.info(message1, owner="TwelfthDoctor1")

                        return

                    if test_data is None or test_data.test_autonomous is None:
                        message2 = 'No Test Data inside Global TestSet Injector. Injection cannot continue.'

                        if apprentice_logger is not None and apprentice_logger is not False:
                            apprentice_logger.error(message2, owner="TwelfthDoctor1")

                        if master_logger is not None and master_logger is not False:
                            master_logger.error(message2, owner="TwelfthDoctor1")

                        logger.info(message2, owner="TwelfthDoctor1")

                        return

                    for interaction in interaction_instance:
                        if hasattr(test_data, "test_autonomous"):
                            cls.inject_test_autonomous_into_interaction(interaction, test_data.test_autonomous, test_data.replace_test_autonomous)

    @staticmethod
    def inject_testset_globals_into_interaction(interaction, test, replace):
        if replace is False:
            message4 = f'Interaction TestSet Globals {interaction.test_globals} \nbeing injected with {test}.'

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info(message4, owner="TwelfthDoctor1")

            if master_logger is not None and master_logger is not False:
                master_logger.info(message4, owner="TwelfthDoctor1")

            logger.info(message4, owner="TwelfthDoctor1")

            interaction.test_globals += test

        elif replace is True:
            message5 = f'Interaction TestSet Globals {interaction.test_globals} \nbeing replaced with {test}.'

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info(message5, owner="TwelfthDoctor1")

            if master_logger is not None and master_logger is not False:
                master_logger.info(message5, owner="TwelfthDoctor1")

            logger.info(message5, owner="TwelfthDoctor1")

            interaction.test_globals = test

    @staticmethod
    def inject_tests_int_into_interaction(interaction, test, replace):
        if replace is False:
            message6 = f'Interaction Tests {interaction.tests} \nbeing injected with {test}.'

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info(message6, owner="TwelfthDoctor1")

            if master_logger is not None and master_logger is not False:
                master_logger.info(message6, owner="TwelfthDoctor1")

            logger.info(message6, owner="TwelfthDoctor1")

            interaction.tests += test

        elif replace is True:
            message7 = f'Interaction Tests {interaction.tests} \nbeing replaced with {test}.'

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info(message7, owner="TwelfthDoctor1")

            if master_logger is not None and master_logger is not False:
                master_logger.info(message7, owner="TwelfthDoctor1")

            logger.info(message7, owner="TwelfthDoctor1")

            interaction.tests = test

    @staticmethod
    def inject_tests_ts_into_test_set(test_set, test, replace):
        if replace is False:
            message8 = f'TestSet Instance {test_set.test} \nbeing injected with {test}.'

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info(message8, owner="TwelfthDoctor1")

            if master_logger is not None and master_logger is not False:
                master_logger.info(message8, owner="TwelfthDoctor1")

            logger.info(message8, owner="TwelfthDoctor1")

            test_set.test += test

        elif replace is True:
            message9 = f'TestSet Instance {test_set.test} \nbeing replaced with {test}.'

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info(message9, owner="TwelfthDoctor1")

            if master_logger is not None and master_logger is not False:
                master_logger.info(message9, owner="TwelfthDoctor1")

            logger.info(message9, owner="TwelfthDoctor1")

    @staticmethod
    def inject_test_autonomous_into_interaction(interaction, test, replace):
        if replace is False:
            message10 = f'Interaction Autonomous Tests {interaction.tests} \nbeing injected with {test}.'

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info(message10, owner="TwelfthDoctor1")

            if master_logger is not None and master_logger is not False:
                master_logger.info(message10, owner="TwelfthDoctor1")

            logger.info(message10, owner="TwelfthDoctor1")

            interaction.test_autonomous += test

        elif replace is True:
            message11 = f'Interaction Autonomous Tests {interaction.tests} \nbeing replaced with {test}.'

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info(message11, owner="TwelfthDoctor1")

            if master_logger is not None and master_logger is not False:
                master_logger.info(message11, owner="TwelfthDoctor1")

            logger.info(message11, owner="TwelfthDoctor1")

            interaction.test_autonomous = test
