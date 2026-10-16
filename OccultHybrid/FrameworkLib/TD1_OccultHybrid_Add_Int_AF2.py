"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
LordPercivalXII's OccultHybrid Mod

> Affordance Injector 2/3 [AF2/AF3] Tuning

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
from objects.definition_manager import DefinitionManager
from sims4.resources import Types
from sims4.common import Pack, is_available_pack
from sims4.log import Logger
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import TunableList, Tunable, TunableReference, TunableEnumEntry, TunableTuple

# Importation of MasterApprentice Logger
try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Affordance Injector Version 2', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Affordance Injector Version 2', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger('TD1 Affordance Injector Version 2', default_owner='TwelfthDoctor1')

# Object List [Sim Objects]
OBJECT_SIM = 14965
TERRAIN = 14982
OBJECT_CAT = 120621
OBJECT_DOG = 120620
OBJECT_SMALLDOG = 174619
OBJECT_FOX = 256694
OBJECT_HORSE = 120619


class TD1OccultHybridAffordanceInjector(metaclass=HashedTunedInstanceMetaclass,
                                        manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'object_list': TunableList(
            description='List of objects that are to be injected.',
            tunable=Tunable(
                description='Object Instance ID of the Object.',
                tunable_type=int,
                default=None
            )
        ),
        'pack': TunableEnumEntry(
            description='The pack used to test.',
            tunable_type=Pack,
            default=Pack.BASE_GAME
        ),
        'affordances': TunableList(
            description='List of interactions that are to be injected into the Object List.',
            tunable=TunableReference(
                description='Affordance Instance ID of the affordance.',
                manager=services.get_instance_manager(Types.INTERACTION),
                pack_safe=True,
                allow_none=True
            )
        ),
        'affordance_reference': TunableReference(
            description='The affordance used to find the object lists should the object super affordances have that affordance.',
            manager=services.get_instance_manager(Types.INTERACTION),
            pack_safe=True,
            allow_none=True
        ),
        'sim_affordances': TunableList(
            description='List of sim interactions that are to be injected into the Object List.',
            tunable=TunableReference(
                description='Affordance Instance ID of the affordance.',
                manager=services.get_instance_manager(Types.INTERACTION),
                pack_safe=True,
                allow_none=True
            )
        ),
        'phone_affordances': TunableList(
            description='List of phone interactions that are to be injected into the Object List.',
            tunable=TunableReference(
                description='Affordance Instance ID of the affordance.',
                manager=services.get_instance_manager(Types.INTERACTION),
                pack_safe=True,
                allow_none=True
            )
        ),
        'terrain_affordances': TunableList(
            description='List of terrain interactions that are to be injected into the Object List.',
            tunable=TunableReference(
                description='Affordance Instance ID of the affordance.',
                manager=services.get_instance_manager(Types.INTERACTION),
                pack_safe=True,
                allow_none=True
            )
        ),
        'affordances_to_snippet': TunableList(
            description='List of mixer interactions that are to be added onto the Sim. Requires snippet_reference to function.',
            tunable=TunableReference(
                description='The mixer interaction to be injected.',
                manager=services.get_instance_manager(Types.INTERACTION),
                pack_safe=True,
                allow_none=True
            )
        ),
        'snippet_reference': TunableReference(
            description='The mixer snippet for mixer interactions to be injected into.',
            manager=services.get_instance_manager(Types.SNIPPET),
            pack_safe=True,
            allow_none=True
        ),
        'lock_aware_affordances': TunableList(
            description='List of lock aware interactions that are to be injected into the Object List.',
            tunable=TunableReference(
                description='Affordance Instance ID of the affordance.',
                manager=services.get_instance_manager(Types.INTERACTION),
                pack_safe=True,
                allow_none=True
            )
        ),
        'to_sim_object': Tunable(
            description='Modifier to determine if sim_affordances and phone_affordances should be targeted to the Sim Object (14965).',
            tunable_type=bool,
            default=True
        ),
        'to_cat_object': Tunable(
            description='Modifier to determine if sim_affordances and phone_affordances should be targeted to the Cat Object (120621).',
            tunable_type=bool,
            default=False
        ),
        'to_dog_object': Tunable(
            description='Modifier to determine if sim_affordances and phone_affordances should be targeted to the Dog Object (120620).',
            tunable_type=bool,
            default=False
        ),
        'to_smalldog_object': Tunable(
            description='Modifier to determine if sim_affordances and phone_affordances should be targeted to the smallDog Object (174619).',
            tunable_type=bool,
            default=False
        ),
        'to_fox_object': Tunable(
            description='Modifier to determine if sim_affordances and phone_affordances should be targeted to the fox Object (256694).',
            tunable_type=bool,
            default=False
        ),
        'to_horse_object': Tunable(
            description='Modifier to determine if sim_affordances and phone_affordances should be targeted to the Horse Object (120619).',
            tunable_type=bool,
            default=False
        ),
        'lock_aware_to_sa': Tunable(
            description='Modifier to determine if lock_aware_affordances should be targeted to the _super_affordances of the object.',
            tunable_type=bool,
            default=False
        ),
    }

    __slots__ = ['object_list', 'pack', 'affordances', 'affordance_reference', 'phone_affordances',
                 'terrain_affordances', 'sim_affordances', 'affordances_to_snippet', 'snippet_reference',
                 'lock_aware_affordances', 'to_sim_object', 'to_cat_object', 'to_dog_object', 'to_smalldog_object',
                 'to_fox_object', 'lock_aware_to_sa', 'to_horse_object']

    @classmethod
    def _tuning_loaded_callback(cls):
        if is_available_pack(cls.pack):
            if len(cls.sim_affordances) > 0:
                if cls.to_sim_object is True:
                    inject_sa_into_sim(OBJECT_SIM, cls.sim_affordances)

                if cls.to_cat_object is True and is_available_pack(Pack.EP04):
                    inject_sa_into_sim(OBJECT_CAT, cls.sim_affordances)

                if cls.to_dog_object is True and is_available_pack(Pack.EP04):
                    inject_sa_into_sim(OBJECT_DOG, cls.sim_affordances)

                if cls.to_smalldog_object is True and is_available_pack(Pack.EP04):
                    inject_sa_into_sim(OBJECT_SMALLDOG, cls.sim_affordances)

                if cls.to_fox_object is True and is_available_pack(Pack.EP11):
                    inject_sa_into_sim(OBJECT_FOX, cls.sim_affordances)

                if cls.to_horse_object is True and is_available_pack(Pack.EP13):
                    inject_sa_into_sim(OBJECT_HORSE, cls.sim_affordances)

            if len(cls.phone_affordances) > 0:
                if cls.to_sim_object is True:
                    inject_sa_into_phone_sa(OBJECT_SIM, cls.phone_affordances)

                if cls.to_cat_object is True and is_available_pack(Pack.EP04):
                    inject_sa_into_phone_sa(OBJECT_CAT, cls.phone_affordances)

                if cls.to_dog_object is True and is_available_pack(Pack.EP04):
                    inject_sa_into_phone_sa(OBJECT_DOG, cls.phone_affordances)

                if cls.to_smalldog_object is True and is_available_pack(Pack.EP04):
                    inject_sa_into_phone_sa(OBJECT_SMALLDOG, cls.phone_affordances)

                if cls.to_fox_object is True and is_available_pack(Pack.EP11):
                    inject_sa_into_phone_sa(OBJECT_FOX, cls.phone_affordances)

                if cls.to_horse_object is True and is_available_pack(Pack.EP13):
                    inject_sa_into_phone_sa(OBJECT_HORSE, cls.phone_affordances)

            if len(cls.terrain_affordances) > 0:
                inject_sa_into_terrain(cls.terrain_affordances)

            if len(cls.object_list) > 0:
                for object_id in cls.object_list:
                    inject_sa_into_object(object_id, cls.affordances)

            if cls.affordance_reference is not None:
                if len(cls.affordances) > 0:
                    inject_sa_through_sa_reference(cls.affordance_reference, cls.affordances)

                if len(cls.lock_aware_affordances) > 0:
                    inject_lock_components_sa_through_sa_reference(cls.affordance_reference, cls.lock_aware_affordances, cls.lock_aware_to_sa)

            if len(cls.affordances_to_snippet) > 0 and cls.snippet_reference is not None:
                inject_mixer_int_through_mixer_snippet(cls.snippet_reference, cls.affordances_to_snippet)

            else:
                logger.warn('TD1 Affordance Injector V2: No Affordances to inject in tuning.',
                            owner='TwelfthDoctor1')

                if apprentice_logger is not None and apprentice_logger is not False:
                    apprentice_logger.warn('TD1 Affordance Injector V2: No Affordances to inject in tuning.',
                                           owner='TwelfthDoctor1')

                if master_logger is not None and master_logger is not False:
                    master_logger.warn('TD1 Affordance Injector V2: No Affordances to inject in tuning.',
                                       owner='TwelfthDoctor1')
        else:
            logger.info('Pack not found within pack list. Affordance Injection will be ignored.',
                        owner='TwelfthDoctor1')

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info('Pack not found within pack list. Affordance Injection will be ignored.',
                                       owner='TwelfthDoctor1')

            if master_logger is not None and master_logger is not False:
                master_logger.info('Pack not found within pack list. Affordance Injection will be ignored.',
                                   owner='TwelfthDoctor1')


class TD1OccultHybridAffordanceInjectorV3(metaclass=HashedTunedInstanceMetaclass,
                                          manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'affordance_injector': TunableList(
            description='Lists of affordances to be injected.',
            tunable=TunableTuple(
                description='The data to be injected.',
                object_list=TunableList(
                    description='List of objects that are to be injected.',
                    tunable=Tunable(
                        description='Object Instance ID of the Object.',
                        tunable_type=int,
                        default=None
                    )
                ),
                affordances=TunableList(
                    description='List of interactions that are to be injected into the Object List.',
                    tunable=TunableReference(
                        description='Affordance Instance ID of the affordance.',
                        manager=services.get_instance_manager(Types.INTERACTION),
                        pack_safe=True,
                        allow_none=True
                    )
                ),
                affordance_reference=TunableReference(
                    description='The affordance used to find the object lists should the object super affordances have that affordance.',
                    manager=services.get_instance_manager(Types.INTERACTION),
                    pack_safe=True,
                    allow_none=True
                ),
                sim_affordances=TunableList(
                    description='List of sim interactions that are to be injected into the Object List.',
                    tunable=TunableReference(
                        description='Affordance Instance ID of the affordance.',
                        manager=services.get_instance_manager(Types.INTERACTION),
                        pack_safe=True,
                        allow_none=True
                    )
                ),
                phone_affordances=TunableList(
                    description='List of phone interactions that are to be injected into the Object List.',
                    tunable=TunableReference(
                        description='Affordance Instance ID of the affordance.',
                        manager=services.get_instance_manager(Types.INTERACTION),
                        pack_safe=True,
                        allow_none=True
                    )
                ),
                terrain_affordances=TunableList(
                    description='List of terrain interactions that are to be injected into the Object List.',
                    tunable=TunableReference(
                        description='Affordance Instance ID of the affordance.',
                        manager=services.get_instance_manager(Types.INTERACTION),
                        pack_safe=True,
                        allow_none=True
                    )
                ),
                snippet_reference=TunableReference(
                    description='The snippet for interactions to be injected into. Applicable to MixerInteractions and Mixer Snippets.',
                    manager=services.get_instance_manager(Types.SNIPPET),
                    pack_safe=True,
                    allow_none=True
                ),
                affordances_to_snippet=TunableList(
                    description='List of mixer interactions that are to be added onto the Sim. Requires snippet_reference to function.',
                    tunable=TunableReference(
                        description='The mixer interaction to be injected.',
                        manager=services.get_instance_manager(Types.INTERACTION),
                        pack_safe=True,
                        allow_none=True
                    )
                ),
                lock_aware_affordances=TunableList(
                    description='List of lock aware interactions that are to be injected into the Object List.',
                    tunable=TunableReference(
                        description='Affordance Instance ID of the affordance.',
                        manager=services.get_instance_manager(Types.INTERACTION),
                        pack_safe=True,
                        allow_none=True
                    )
                ),
                blacklist_objects=TunableList(
                    description="A list of objects to be blacklisted when picked the AF3 under Inject by Reference or Inject by Tag. [NOT YET IMPLEMENTED]",
                    tunable=TunableReference(
                        description="Object Instance ID to be blacklisted.",
                        manager=services.definition_manager()
                    )
                ),
                pack=TunableEnumEntry(
                    description='The pack used to test.',
                    tunable_type=Pack,
                    default=Pack.BASE_GAME
                ),
                to_sim_object=Tunable(
                    description='Modifier to determine if sim_affordances and phone_affordances should be targeted to the Sim Object (14965).',
                    tunable_type=bool,
                    default=True
                ),
                to_cat_object=Tunable(
                    description='Modifier to determine if sim_affordances and phone_affordances should be targeted to the Cat Object (120621).',
                    tunable_type=bool,
                    default=False
                ),
                to_dog_object=Tunable(
                    description='Modifier to determine if sim_affordances and phone_affordances should be targeted to the Dog Object (120620).',
                    tunable_type=bool,
                    default=False
                ),
                to_smalldog_object=Tunable(
                    description='Modifier to determine if sim_affordances and phone_affordances should be targeted to the smallDog Object (174619).',
                    tunable_type=bool,
                    default=False
                ),
                to_fox_object=Tunable(
                    description='Modifier to determine if sim_affordances and phone_affordances should be targeted to the fox Object (256694).',
                    tunable_type=bool,
                    default=False
                ),
                to_horse_object=Tunable(
                    description='Modifier to determine if sim_affordances and phone_affordances should be targeted to the Horse Object (120619).',
                    tunable_type=bool,
                    default=False
                ),
                lock_aware_to_sa=Tunable(
                    description='Modifier to determine if lock_aware_affordances should be targeted to the _super_affordances of the object.',
                    tunable_type=bool,
                    default=False
                ),
            )
        )
    }

    __slots__ = 'affordance_injector'

    @classmethod
    def _tuning_loaded_callback(cls):
        if cls.affordance_injector is not None:
            for injector_data in cls.affordance_injector:
                has_data = False
                if is_available_pack(injector_data.pack):
                    # Inject to Sim Objects
                    if len(injector_data.sim_affordances) > 0:
                        if injector_data.to_sim_object is True:
                            inject_sa_into_sim(OBJECT_SIM, injector_data.sim_affordances)

                        if injector_data.to_cat_object is True and is_available_pack(Pack.EP04):
                            inject_sa_into_sim(OBJECT_CAT, injector_data.sim_affordances)

                        if injector_data.to_dog_object is True and is_available_pack(Pack.EP04):
                            inject_sa_into_sim(OBJECT_DOG, injector_data.sim_affordances)

                        if injector_data.to_smalldog_object is True and is_available_pack(Pack.EP04):
                            inject_sa_into_sim(OBJECT_SMALLDOG, injector_data.sim_affordances)

                        if injector_data.to_fox_object is True and is_available_pack(Pack.EP11):
                            inject_sa_into_sim(OBJECT_FOX, injector_data.sim_affordances)

                        if injector_data.to_horse_object is True and is_available_pack(Pack.EP13):
                            inject_sa_into_sim(OBJECT_HORSE, injector_data.sim_affordances)

                        has_data = True

                    # Inject to Phone Affordances
                    if len(injector_data.phone_affordances) > 0:
                        if injector_data.to_sim_object is True:
                            inject_sa_into_phone_sa(OBJECT_SIM, injector_data.phone_affordances)

                        if injector_data.to_cat_object is True and is_available_pack(Pack.EP04):
                            inject_sa_into_phone_sa(OBJECT_CAT, injector_data.phone_affordances)

                        if injector_data.to_dog_object is True and is_available_pack(Pack.EP04):
                            inject_sa_into_phone_sa(OBJECT_DOG, injector_data.phone_affordances)

                        if injector_data.to_smalldog_object is True and is_available_pack(Pack.EP04):
                            inject_sa_into_phone_sa(OBJECT_SMALLDOG, injector_data.phone_affordances)

                        if injector_data.to_fox_object is True and is_available_pack(Pack.EP11):
                            inject_sa_into_phone_sa(OBJECT_FOX, injector_data.phone_affordances)

                        if injector_data.to_horse_object is True and is_available_pack(Pack.EP13):
                            inject_sa_into_phone_sa(OBJECT_HORSE, injector_data.phone_affordances)

                        has_data = True

                    # Inject to Terrain Object
                    if len(injector_data.terrain_affordances) > 0:
                        inject_sa_into_terrain(injector_data.terrain_affordances)

                        has_data = True

                    # Inject to Objects in List
                    if len(injector_data.object_list) > 0:
                        for object_id in injector_data.object_list:
                            if len(injector_data.affordances) > 0:
                                inject_sa_into_object(object_id, injector_data.affordances)

                            if len(injector_data.lock_aware_affordances) > 0:
                                inject_lock_components_sa_into_object(object_id, injector_data.lock_aware_affordances)

                        has_data = True

                    # Inject to Object(s) with Referenced Affordance
                    if injector_data.affordance_reference is not None:
                        if len(injector_data.affordances) > 0:
                            inject_sa_through_sa_reference(injector_data.affordance_reference,
                                                           injector_data.affordances)

                        if len(injector_data.lock_aware_affordances) > 0:
                            inject_lock_components_sa_through_sa_reference(injector_data.affordance_reference,
                                                                           injector_data.lock_aware_affordances,
                                                                           injector_data.lock_aware_to_sa)

                        has_data = True

                    # Inject to Affordance Snippet
                    if len(injector_data.affordances_to_snippet) > 0 and injector_data.snippet_reference is not None:
                        inject_mixer_int_through_mixer_snippet(injector_data.snippet_reference,
                                                               injector_data.affordances_to_snippet)

                        has_data = True

                    # No Data Error
                    if has_data is False:
                        logger.warn('TD1 Affordance Injector V2: No Affordances to inject in tuning.',
                                    owner='TwelfthDoctor1')

                        if apprentice_logger is not None and apprentice_logger is not False:
                            apprentice_logger.warn('TD1 Affordance Injector V2: No Affordances to inject in tuning.',
                                                   owner='TwelfthDoctor1')

                        if master_logger is not None and master_logger is not False:
                            master_logger.warn('TD1 Affordance Injector V2: No Affordances to inject in tuning.',
                                               owner='TwelfthDoctor1')

                else:
                    logger.info('Pack not found within pack list. Affordance Injection will be ignored.',
                                owner='TwelfthDoctor1')

                    if apprentice_logger is not None and apprentice_logger is not False:
                        apprentice_logger.info('Pack not found within pack list. Affordance Injection will be ignored.',
                                               owner='TwelfthDoctor1')

                    if master_logger is not None and master_logger is not False:
                        master_logger.info('Pack not found within pack list. Affordance Injection will be ignored.',
                                           owner='TwelfthDoctor1')


def inject_sa_into_object(object_id, sa_tuning_list):
    """
    Injects Affordances into the Object ID inside the Object List.
    :param object_id:
    :param sa_tuning_list:
    :return:
    """
    sa_list = []
    definition_manager = services.definition_manager()
    object_sim = super(DefinitionManager, definition_manager).get(object_id)
    for affordance in sa_tuning_list:
        if not affordance in object_sim._super_affordances:
            sa_list.append(affordance)

    if len(sa_list) > 0:
        logger.info('{}: Injecting Super Affordances\n{}'.format(object_sim, sa_list))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info('{}: Injecting Super Affordances\n{}'.format(object_sim, sa_list))

        if master_logger is not None and master_logger is not False:
            master_logger.info('{}: Injecting Super Affordances\n{}'.format(object_sim, sa_list))

        object_sim._super_affordances += tuple(sa_list)


def inject_sa_into_sim(sim_object, sa_tuning_list):
    """
    Injects Affordances into the Sim Object (14965).
    :param sa_tuning_list:
    :return:
    """
    sa_list = []
    definition_manager = services.definition_manager()
    object_sim = super(DefinitionManager, definition_manager).get(sim_object)
    for affordance in sa_tuning_list:
        if not affordance in object_sim._super_affordances:
            sa_list.append(affordance)

    if len(sa_list) > 0:
        logger.info('{}: Injecting Super Affordances\n{}'.format(object_sim, sa_list))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info('{}: Injecting Super Affordances\n{}'.format(object_sim, sa_list))

        if master_logger is not None and master_logger is not False:
            master_logger.info('{}: Injecting Super Affordances\n{}'.format(object_sim, sa_list))

        object_sim._super_affordances += tuple(sa_list)


def inject_sa_into_phone_sa(sim_object, sa_tuning_list):
    """
    Injects Affordances into the phone located inside the Sim Object (14965).
    :param sa_tuning_list:
    :return:
    """
    sa_list = []
    definition_manager = services.definition_manager()
    object_sim = super(DefinitionManager, definition_manager).get(sim_object)
    for affordance in sa_tuning_list:
        if not affordance in object_sim._phone_affordances:
            sa_list.append(affordance)

    if len(sa_list) > 0:
        logger.info('{}: Injecting Super Affordances\n{}'.format(object_sim, sa_list))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info('{}: Injecting Super Affordances\n{}'.format(object_sim, sa_list))

        if master_logger is not None and master_logger is not False:
            master_logger.info('{}: Injecting Super Affordances\n{}'.format(object_sim, sa_list))

        object_sim._phone_affordances += tuple(sa_list)


def inject_sa_into_terrain(sa_tuning_list):
    """
    Injects Affordances into Terrain Object (14982).
    :param sa_tuning_list:
    :return:
    """
    sa_list = []
    definition_manager = services.definition_manager()
    obj_terrain = super(DefinitionManager, definition_manager).get(TERRAIN)
    for affordance in sa_tuning_list:
        if not affordance in obj_terrain._super_affordances:
            sa_list.append(affordance)

    if len(sa_list) > 0:
        logger.info('{}: Injecting Super Affordances\n{}'.format(obj_terrain, sa_list))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info('{}: Injecting Super Affordances\n{}'.format(obj_terrain, sa_list))

        if master_logger is not None and master_logger is not False:
            master_logger.info('{}: Injecting Super Affordances\n{}'.format(obj_terrain, sa_list))

        obj_terrain._super_affordances += tuple(sa_list)


def inject_sa_through_sa_reference(sa_ref, sa_tuning_list):
    """
    Injects Affordances into any object that has the specified affordance to refer to search.
    :param sa_ref:
    :param sa_tuning_list:
    :return:
    """
    sa_list = []
    obj_list = []
    definition_manager = services.definition_manager()
    for tuning in definition_manager._tuned_classes.values():
        if hasattr(tuning, '_super_affordances') and sa_ref in tuning._super_affordances:
            obj_list.append(tuning)

    for affordance in sa_tuning_list:
        sa_list.append(affordance)

    if len(sa_list) > 0:
        for object_id in obj_list:
            logger.info('{}: Injecting Super Affordances\n{}'.format(object_id, sa_list))

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info('{}: Injecting Super Affordances\n{}'.format(object_id, sa_list))

            if master_logger is not None and master_logger is not False:
                master_logger.info('{}: Injecting Super Affordances\n{}'.format(object_id, sa_list))

            object_id._super_affordances += tuple(sa_list)


def inject_mixer_int_through_mixer_snippet(mixer_reference, mixer_list):
    """
    Injects Affordances into a Snippet.
    Note: This can also be used on non-mixer affordances.
    :param mixer_reference:
    :param mixer_list:
    :return:
    """
    sa_list = []

    for affordance in mixer_list:
        if not affordance in mixer_reference.value:
            sa_list.append(affordance)

    if len(sa_list) > 0:
        logger.info('{}: Injecting Super Affordances\n{}'.format(mixer_reference, sa_list))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info('{}: Injecting Super Affordances\n{}'.format(mixer_reference, sa_list))

        if master_logger is not None and master_logger is not False:
            master_logger.info('{}: Injecting Super Affordances\n{}'.format(mixer_reference, sa_list))

        mixer_reference.value += tuple(sa_list)


def inject_lock_components_sa_into_object(object_id, sa_tuning_list):
    """
    Injects Lock Aware Affordances into the Object ID inside the Object List.
    :param object_id:
    :param sa_tuning_list:
    :return:
    """
    sa_list = []
    final_sa_list = []
    definition_manager = services.definition_manager()
    object = super(DefinitionManager, definition_manager).get(object_id)
    for affordance in sa_tuning_list:
        if not affordance in object._components.object_locking_component.super_affordances:
            sa_list.append(affordance)

    if len(sa_list) > 0:
        logger.info('{}: Injecting Super Affordances\n{}'.format(object, sa_list))

        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info('{}: Injecting Super Affordances\n{}'.format(object, sa_list))

        if master_logger is not None and master_logger is not False:
            master_logger.info('{}: Injecting Super Affordances\n{}'.format(object, sa_list))

        object._components.object_locking_component.super_affordances.union(tuple(frozenset(sa_list)))


def inject_lock_components_sa_through_sa_reference(sa_ref, sa_tuning_list, inj_state):
    """
    Injects Lock Aware Affordances into any object that has the specified affordance to refer to search.
    :param sa_ref:
    :param sa_tuning_list:
    :param inj_state:
    :return:
    """
    sa_list = []
    obj_list = []
    final_sa_list = []
    definition_manager = services.definition_manager()
    for tuning in definition_manager._tuned_classes.values():
        if hasattr(tuning, '_components') and hasattr(tuning._components, 'object_locking_component') and hasattr(tuning._components.object_locking_component, 'super_affordances') and tuning._components.object_locking_component.super_affordances is not None and sa_ref in tuning._components.object_locking_component.super_affordances:
            obj_list.append(tuning)

    for affordance in sa_tuning_list:
        sa_list.append(affordance)

    if len(sa_list) > 0:
        for object_id in obj_list:
            for affordance in object_id._components.object_locking_component.super_affordances:
                final_sa_list.append(affordance)

            logger.info('{}: Injecting Super Affordances\n{}'.format(object_id, sa_list))

            if apprentice_logger is not None and apprentice_logger is not False:
                apprentice_logger.info('{}: Injecting Super Affordances\n{}'.format(object_id, sa_list))

            if master_logger is not None and master_logger is not False:
                master_logger.info('{}: Injecting Super Affordances\n{}'.format(object_id, sa_list))

            if inj_state is False:
                object_id._components.object_locking_component.super_affordances.union(tuple(frozenset(sa_list)))
            else:
                object_id._super_affordances += tuple(sa_list)
