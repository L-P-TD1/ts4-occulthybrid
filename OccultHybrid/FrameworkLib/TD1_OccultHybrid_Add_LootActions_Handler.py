"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
LordPercivalXII's OccultHybrid Mod

> LootAction Injector Tuning

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
from event_testing.tests import TunableTestSet
from interactions.utils.loot import LootActionVariant
from sims4.common import Pack, is_available_pack
from sims4.log import Logger
from sims4.resources import Types
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import TunableReference, TunableList, Tunable, TunableTuple, TunableEnumEntry

# Importation of MasterApprentice Logger
try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 LootAction Injector', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 LootAction Injector', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger('TD1 LootAction Injector', default_owner='TwelfthDoctor1')


class TD1OccultHybridLootActionInjector(metaclass=HashedTunedInstanceMetaclass,
                                        manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'loot_instance': TunableReference(
            description='The LootAction to be injected',
            manager=services.get_instance_manager(Types.ACTION),
            allow_none=False,
            pack_safe=True
        ),
        'loot_actions': TunableList(
            description='List of loots operations that will be awarded.',
            tunable=LootActionVariant(statistic_pack_safe=True)
        ),
        'tests': TunableTestSet(
            description='Tests to run before applying any of the loot actions. These are run before run_test_first is evaluated so it will not affect these tests.'
        ),
        'replace_loot_actions': Tunable(
            description='Modifier to determine should the loot_actions be overridden.',
            tunable_type=bool,
            default=False
        ),
        'replace_tests': Tunable(
            description='Modifier to determine should the tests be overridden.',
            tunable_type=bool,
            default=False
        ),
        'pack': TunableEnumEntry(
            description='The pack to test for.',
            tunable_type=Pack,
            default=Pack.BASE_GAME
        )
    }

    __slots__ = ['loot_instance', 'loot_actions', 'tests', 'replace_loot_actions', 'replace_tests', 'pack']

    @classmethod
    def _tuning_loaded_callback(cls):
        if is_available_pack(cls.pack) and cls.loot_instance is not None:
            if cls.loot_actions is not None:
                if cls.replace_loot_actions is False:
                    cls.loot_instance.loot_actions += cls.loot_actions

                    logger.info('Injecting LootActions in {} with {}.'.format(cls.loot_instance, cls.loot_actions))

                    if apprentice_logger is not None and apprentice_logger is not False:
                        apprentice_logger.info('Injecting LootActions in {} with {}.'.format(cls.loot_instance, cls.loot_actions))

                    if master_logger is not None and master_logger is not False:
                        master_logger.info('Injecting LootActions in {} with {}.'.format(cls.loot_instance, cls.loot_actions))

                else:
                    cls.loot_instance.loot_actions = cls.loot_actions

                    logger.info('Replaced LootActions {} into {}'.format(cls.loot_instance, cls.loot_actions))

                    if apprentice_logger is not None and apprentice_logger is not False:
                        apprentice_logger.info('Replaced LootActions {} into {}'.format(cls.loot_instance, cls.loot_actions))

                    if master_logger is not None and master_logger is not False:
                        master_logger.info('Replaced LootActions {} into {}'.format(cls.loot_instance, cls.loot_actions))

            if cls.tests is not None:
                if cls.replace_tests is False:
                    cls.loot_instance.tests += cls.tests

                    logger.info('Injecting tests in {} with {}.'.format(cls.loot_instance, cls.tests))

                    if apprentice_logger is not None and apprentice_logger is not False:
                        apprentice_logger.info('Injecting tests in {} with {}.'.format(cls.loot_instance, cls.tests))

                    if master_logger is not None and master_logger is not False:
                        master_logger.info('Injecting tests in {} with {}.'.format(cls.loot_instance, cls.tests))

                else:
                    cls.loot_instance.tests = cls.tests

                    logger.info('Replaced tests {} into {}'.format(cls.loot_instance, cls.tests))

                    if apprentice_logger is not None and apprentice_logger is not False:
                        apprentice_logger.info('Replaced tests {} into {}'.format(cls.loot_instance, cls.tests))

                    if master_logger is not None and master_logger is not False:
                        master_logger.info('Replaced tests {} into {}'.format(cls.loot_instance, cls.tests))


class TD1OccultHybridLootActionInjectorV2(metaclass=HashedTunedInstanceMetaclass,
                                          manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'lootaction_injector': TunableList(
            description='Lists of LootActions to be injected.',
            tunable=TunableTuple(
                description='Data to be injected into the specified interaction.',
                loot_instance=TunableList(
                    description='A lists of LootActions to be injected.',
                    tunable=TunableReference(
                        description='The LootAction to be injected',
                        manager=services.get_instance_manager(Types.ACTION),
                        allow_none=False,
                        pack_safe=True
                    ),
                ),
                loot_actions=TunableList(
                    description='List of loots operations that will be awarded.',
                    tunable=LootActionVariant(statistic_pack_safe=True)
                ),
                tests=TunableTestSet(
                    description='Tests to run before applying any of the loot actions. These are run before run_test_first is evaluated so it will not affect these tests.'
                ),
                replace_loot_actions=Tunable(
                    description='Modifier to determine should the loot_actions be overridden.',
                    tunable_type=bool,
                    default=False
                ),
                replace_tests=Tunable(
                    description='Modifier to determine should the tests be overridden.',
                    tunable_type=bool,
                    default=False
                ),
                pack=TunableEnumEntry(
                    description='The pack to test for.',
                    tunable_type=Pack,
                    default=Pack.BASE_GAME
                )
            ),
        )
    }

    __slots__ = 'lootaction_injector'

    @classmethod
    def _tuning_loaded_callback(cls):
        if cls.lootaction_injector is not None:
            for injector_data in cls.lootaction_injector:
                if is_available_pack(injector_data.pack):
                    if injector_data.loot_instance is not None:
                        for loot_action in injector_data.loot_instance:
                            if injector_data.loot_actions is not None:
                                if injector_data.replace_loot_actions is False:
                                    loot_action.loot_actions += injector_data.loot_actions

                                    logger.info('Injecting LootActions in {} with {}.'.format(loot_action,
                                                                                              injector_data.loot_actions))

                                    if apprentice_logger is not None and apprentice_logger is not False:
                                        apprentice_logger.info(
                                            'Injecting LootActions in {} with {}.'.format(loot_action,
                                                                                          injector_data.loot_actions))

                                    if master_logger is not None and master_logger is not False:
                                        master_logger.info(
                                            'Injecting LootActions in {} with {}.'.format(loot_action,
                                                                                          injector_data.loot_actions))

                                else:
                                    loot_action.loot_actions = injector_data.loot_actions

                                    logger.info(
                                        'Replaced LootActions {} into {}'.format(injector_data.loot_actions, loot_action))

                                    if apprentice_logger is not None and apprentice_logger is not False:
                                        apprentice_logger.info(
                                            'Replaced LootActions {} into {}'.format(injector_data.loot_actions, loot_action))

                                    if master_logger is not None and master_logger is not False:
                                        master_logger.info('Replaced LootActions {} into {}'.format(injector_data.loot_actions, loot_action))

                            if injector_data.tests is not None:
                                if injector_data.replace_tests is False:
                                    loot_action.tests += injector_data.tests

                                    logger.info('Injecting tests in {} with {}.'.format(loot_action, injector_data.tests))

                                    if apprentice_logger is not None and apprentice_logger is not False:
                                        apprentice_logger.info(
                                            'Injecting tests in {} with {}.'.format(loot_action, injector_data.tests))

                                    if master_logger is not None and master_logger is not False:
                                        master_logger.info(
                                            'Injecting tests in {} with {}.'.format(loot_action, injector_data.tests))

                                else:
                                    loot_action.tests = injector_data.tests

                                    logger.info('Replaced tests {} into {}'.format(injector_data.tests, loot_action))

                                    if apprentice_logger is not None and apprentice_logger is not False:
                                        apprentice_logger.info(
                                            'Replaced tests {} into {}'.format(injector_data.tests, loot_action))

                                    if master_logger is not None and master_logger is not False:
                                        master_logger.info(
                                            'Replaced tests {} into {}'.format(injector_data.tests, loot_action))
