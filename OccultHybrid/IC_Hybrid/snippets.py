import services
from objects.definition_manager import DefinitionManager
from sims.occult.occult_enums import OccultType
from sims4.localization import TunableLocalizedStringFactory
from sims4.resources import Types, CompoundTypes
from sims4.tuning.instances import HashedTunedInstanceMetaclass
from sims4.tuning.tunable import TunableReference, TunableMapping, TunableTuple, TunableSet, TunableResourceKey, Tunable, TunableRange, TunableEnumEntry
from sims4.tuning.tunable_base import ExportModes, GroupNames
from statistics.base_statistic import GalleryLoadBehavior
from statistics.statistic_categories import StatisticCategory
from OccultHybrid.IC_Hybrid import tuning_utils
from OccultHybrid.IC_Hybrid import occult_cache


class TraitInjectionSnippet(metaclass=HashedTunedInstanceMetaclass,
                            manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'data': TunableMapping(
            key_type=TunableReference(
                manager=services.get_instance_manager(Types.TRAIT),
                pack_safe=True
            ),
            value_type=TunableTuple(
                super_affordances=TunableSet(
                    tunable=TunableReference(
                        manager=(services.get_instance_manager(Types.INTERACTION)),
                       class_restrictions=('SuperInteraction', ),
                       pack_safe=True
                    )
                ),
                icon=TunableResourceKey(
                    allow_none=True,
                    resource_types=(CompoundTypes.IMAGE),
                    export_modes=(ExportModes.All),
                    tuning_group=(GroupNames.APPEARANCE)
                ),
                trait_description=TunableLocalizedStringFactory(
                    allow_none=True,
                    export_modes=(ExportModes.All),
                    tuning_group=(GroupNames.APPEARANCE),
                    default=None
                ),
                initial_commodities_blacklist=TunableSet(
                    tunable=TunableReference(
                        manager=services.get_instance_manager(Types.STATISTIC),
                        class_restrictions=('Commodity',),
                        pack_safe=True
                    )
                ),
                force_playable=Tunable(
                    tunable_type=bool,
                    default=False
                ),
                force_allow_from_gallery=Tunable(
                    tunable_type=bool,
                    default=False
                ),
                force_persistable=Tunable(
                    tunable_type=bool,
                    default=True
                )
            )
        )
    }

    @classmethod
    def _tuning_loaded_callback(cls):
        for trait, tuning in cls.data.items():
            tuning_utils.add_interactions_to_trait(tuning.super_affordances, trait)
            try:
                if tuning.icon:
                    trait.icon = tuning.icon
            except:
                pass

            try:
                if tuning.trait_description:
                    trait.trait_description = tuning.trait_description
            except:
                pass

            try:
                if tuning.initial_commodities_blacklist:
                    tuning_utils.add_motives_to_trait_blacklist(tuning.initial_commodities_blacklist, trait)
            except:
                pass

            if tuning.force_playable:
                trait.is_npc_only = False
            if tuning.force_allow_from_gallery:
                trait.allow_from_gallery = True
            if tuning.force_persistable:
                trait.persistable = True


class PhoneInjectionSnippet(metaclass=HashedTunedInstanceMetaclass,
                            manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        '_phone_affordances': TunableSet(
            tunable=TunableReference(
                manager=(services.get_instance_manager(Types.INTERACTION)),
                class_restrictions=('SuperInteraction', ),
                pack_safe=True
            )
        )
    }

    @classmethod
    def _tuning_loaded_callback(cls):
        OBJECT_SIM = 14965
        definition_manager = services.definition_manager()
        object_sim = super(DefinitionManager, definition_manager).get(OBJECT_SIM)
        affordances = set(object_sim._phone_affordances)
        affordances.update(cls._phone_affordances)
        object_sim._phone_affordances = tuple(affordances)


class PackSafeTraitInjectionSnippet(metaclass=HashedTunedInstanceMetaclass,
                                    manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'trait': TunableReference(
            manager=services.get_instance_manager(Types.TRAIT),
            pack_safe=True
        ),
        'required_trait_map': TunableMapping(
            key_type=TunableReference(
                manager=services.get_instance_manager(Types.TRAIT),
                pack_safe=True
            ),
            value_type=TunableTuple(
                super_affordances=TunableSet(
                    tunable=TunableReference(
                        manager=(services.get_instance_manager(Types.INTERACTION)),
                        class_restrictions=('SuperInteraction', ),
                        pack_safe=True
                    )
                )
            )
        )
    }

    @classmethod
    def _tuning_loaded_callback(cls):
        try:
            for trait, data in cls.required_trait_map.items():
                try:
                    tuning_utils.add_interactions_to_trait(data.super_affordances, cls.trait)
                except:
                    pass

        except:
            pass


class CheatInteractionSnippet(metaclass=HashedTunedInstanceMetaclass,
                              manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'cheat_interactions': TunableSet(
            tunable=TunableReference(
                manager=(services.get_instance_manager(Types.INTERACTION)),
                class_restrictions=('SuperInteraction', ),
                pack_safe=True
            )
        )
    }

    @classmethod
    def _tuning_loaded_callback(cls):
        for interaction in cls.cheat_interactions:
            try:
                interaction.cheat = True
            except:
                pass


class BuffInjectionSnippet(metaclass=HashedTunedInstanceMetaclass,
                           manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'data': TunableMapping(
            key_type=TunableReference(
                manager=services.get_instance_manager(Types.BUFF),
                pack_safe=True
            ),
            value_type=TunableTuple(
                force_playable=Tunable(
                    tunable_type=bool,
                    default=False
                ),
                change_timeout=Tunable(
                    tunable_type=bool,
                    default=False
                ),
                show_timeout=Tunable(
                    tunable_type=bool,
                    default=True
                ),
                mood_type=TunableReference(
                    manager=(services.mood_manager()),
                allow_none=True,
                export_modes=(ExportModes.All)),
                force_mood_weight=Tunable(
                    tunable_type=bool,
                    default=False
                ),
                mood_weight=TunableRange(
                    tunable_type=int,
                    default=0,
                    minimum=0,
                    export_modes=(ExportModes.All)
                )
            )
        )
    }

    @classmethod
    def _tuning_loaded_callback(cls):
        for buff, tuning in cls.data.items():
            if tuning.force_playable:
                buff.persists = True
                buff.is_npc_only = False
            else:
                if tuning.mood_type:
                    buff.mood_type = tuning.mood_type
                if tuning.force_mood_weight:
                    buff.mood_weight = tuning.mood_weight
            if tuning.change_timeout:
                buff.show_timeout = tuning.show_timeout


class CommodityInjectionSnippet(metaclass=HashedTunedInstanceMetaclass,
                                manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'data': TunableMapping(
            key_type=TunableReference(
                manager=services.get_instance_manager(Types.STATISTIC),
                class_restrictions=('Commodity',),
                pack_safe=True),
            value_type=TunableTuple(
                replace_categories=Tunable(
                    tunable_type=bool,
                    default=False
                ),
                _categories=TunableSet(tunable=StatisticCategory),
                replace_gallery_load_behavior=Tunable(
                    tunable_type=bool,
                    default=False
                ),
                gallery_load_behavior=TunableEnumEntry(
                    tunable_type=GalleryLoadBehavior,
                    default=(GalleryLoadBehavior.LOAD_ONLY_FOR_SIM),
                    tuning_group=(GroupNames.SPECIAL_CASES)
                ),
                replace_decay_rate=Tunable(
                    tunable_type=bool,
                    default=False
                ),
                decay_rate=TunableRange(
                    tunable_type=float,
                    default=0.001,
                    minimum=0.0,
                    tuning_group=(GroupNames.CORE)
                )
            )
        )
    }

    @classmethod
    def _tuning_loaded_callback(cls):
        for motive, tuning in cls.data.items():
            if tuning._categories:
                if tuning.replace_categories:
                    motive._categories = tuning._categories
                else:
                    motive._categories.update(tuning._categories)
            if tuning.replace_gallery_load_behavior:
                motive.gallery_load_behavior = tuning.gallery_load_behavior
            if tuning.replace_decay_rate:
                motive.decay_rate = tuning.decay_rate


class CustomOccultCacheSnippet(metaclass=HashedTunedInstanceMetaclass,
                               manager=services.get_instance_manager(Types.SNIPPET)):
    INSTANCE_TUNABLES = {
        'data': TunableMapping(
            key_type=TunableEnumEntry(
                tunable_type=OccultType,
                default=(OccultType.HUMAN)
            ),
            value_type=TunableTuple(
                menu_allow_add_remove_picker=Tunable(
                    tunable_type=bool,
                    default=True
                ),
                menu_allow_modify_in_cas_picker=Tunable(
                    tunable_type=bool,
                    default=True
                ),
                menu_allow_delete_picker=Tunable(
                    tunable_type=bool,
                    default=True
                ),
                form_clone_human=Tunable(
                    tunable_type=bool,
                    default=True
                )
            )
        )
    }

    @classmethod
    def _tuning_loaded_callback(cls):
        for occult, tuning in cls.data.items():
            if occult == OccultType.HUMAN:
                continue
            else:
                occult_info = occult_cache.OccultDataCache.CustomOccultData(menu_allow_add_remove_picker=(tuning.menu_allow_add_remove_picker),
                  menu_allow_modify_in_cas_picker=(tuning.menu_allow_modify_in_cas_picker),
                  form_clone_human=(tuning.form_clone_human))
                occult_cache.OccultDataCache.cache_custom_occult(occult, occult_info)