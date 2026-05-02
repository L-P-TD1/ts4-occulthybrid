from sims.occult.occult_enums import OccultType


# enter_cas = False
# occult_swap_temp_blacklist = None
# sim_physical_attr_cache = dict()
# sim_outfit_cache = dict()


class OccultDataCache:

    class CustomOccultData:

        def __init__(self, menu_allow_add_remove_picker: bool=False, menu_allow_modify_in_cas_picker: bool=False, menu_allow_delete_picker: bool=False, form_clone_human: bool=False):
            self.menu_allow_add_remove_picker = menu_allow_add_remove_picker
            self.menu_allow_delete_picker = menu_allow_delete_picker
            self.menu_allow_modify_in_cas_picker = menu_allow_modify_in_cas_picker
            self.form_clone_human = form_clone_human

    occult_exit_traits = dict()
    occult_removal_traits = dict()
    occult_add_actions = dict()
    custom_occults = dict()
    # occult_forms_cache = dict()
    # sim_physical_attr_cache = dict()
    # sim_outfit_cache = dict()
    _processed_custom_occults = False
    # occult_swap_temp_blacklist = None
    # enter_cas = False

    @classmethod
    def cache_exit_traits(cls, occult_type: OccultType, traits: list):
        if occult_type not in cls.occult_exit_traits:
            cls.occult_exit_traits[occult_type] = traits
        else:
            cls.occult_exit_traits[occult_type].extend(traits)

    @classmethod
    def cache_removal_traits(cls, occult_type: OccultType, traits: list):
        if occult_type not in cls.occult_removal_traits:
            cls.occult_removal_traits[occult_type] = traits
        else:
            cls.occult_removal_traits[occult_type].extend(traits)

    @classmethod
    def cache_add_actions(cls, occult_type: OccultType, actions: list):
        if occult_type not in cls.occult_add_actions:
            cls.occult_add_actions[occult_type] = actions
        else:
            cls.occult_add_actions[occult_type].extend(actions)

    @classmethod
    def cache_custom_occult(cls, occult_type: OccultType, custom_occult: CustomOccultData):
        if occult_type != OccultType.HUMAN:
            data = {occult_type: custom_occult}
            cls.custom_occults.update(data)

    @classmethod
    def process_custom_occults(cls):
        if not cls._processed_custom_occults:
            cls._processed_custom_occults = True
            for occult in OccultType:
                if occult >= 1024 and occult not in cls.custom_occults:
                    cls.cache_custom_occult(occult, cls.CustomOccultData())

    # @classmethod
    # def process_outfit_data(cls, sim_id, occult_type, outfit_data):
    #     if occult_type not in cls.sim_outfit_cache:
    #         cls.sim_outfit_cache[sim_id] = {occult_type: outfit_data}
    #     else:
    #         cls.sim_outfit_cache[sim_id][occult_type].extend(outfit_data)
    #
    # @classmethod
    # def process_sim_attributes(cls, sim_id, occult_type, sim_attr):
    #     if sim_id not in cls.sim_physical_attr_cache:
    #         cls.sim_physical_attr_cache[sim_id] = {occult_type: sim_attr}
    #     else:
    #         cls.sim_physical_attr_cache[sim_id][occult_type].extend(sim_attr)
    #
    # @classmethod
    # def update_blacklisted_occult_for_cas(cls, occult_type):
    #     cls.occult_swap_temp_blacklist = occult_type
    #
    # @classmethod
    # def update_enter_cas(cls, cas_update=False):
    #     cls.enter_cas = cas_update


# def process_outfit_data(sim_id, outfit_data: dict):
#     if sim_id not in sim_outfit_cache:
#         sim_outfit_cache[sim_id] = outfit_data
#     else:
#         sim_outfit_cache[sim_id].extend(outfit_data)
#
#
# def process_sim_attributes(sim_id, sim_attr: dict):
#     if sim_id not in sim_physical_attr_cache:
#         sim_physical_attr_cache[sim_id] = sim_attr
#     else:
#         sim_physical_attr_cache[sim_id].extend(sim_attr)
