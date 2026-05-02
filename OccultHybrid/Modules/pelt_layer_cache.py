from OccultHybrid.UtilLib.JSONHandler import JSONHandler
from sims.occult.occult_enums import OccultType

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Pelt Layer Cache', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

# pelt_layer_cache = JSONHandler("pelt_layer_cache")
# # pelt_layer_cache.generate_json(dict())
# # pelt_layer_cache.formulate_json()
#
#
# def register_pelt_layers(sim_info, occult):
#     if not (occult == OccultType.WEREWOLF or occult == OccultType.FAIRY):
#         return
#
#     if sim_info.id in pelt_layer_cache.return_json():
#         sim_pelt_layers = pelt_layer_cache.return_specific_json(sim_info.id)
#     else:
#         sim_pelt_layers = dict()
#
#     if master_logger is not None and master_logger is not False:
#         master_logger.info(
#             f"CURRENT PELT LAYER CACHE: {sim_pelt_layers}\n"
#             f"TO REPLACE/ADD: {sim_info.pelt_layers.decode('cp437')}\n"
#         )
#
#     sim_pelt_layers[occult] = sim_info.pelt_layers.decode("cp437")
#
#     pelt_layer_cache.update_specific_json(sim_info.id, sim_pelt_layers)
#
#     if master_logger is not None and master_logger is not False:
#         master_logger.info(
#             f"PELT LAYER CACHE: {pelt_layer_cache.return_json()[sim_info.id]}"
#         )
#
#     pelt_layer_cache.update_json_file()
#
#
# def get_pelt_layers(sim_info, occult):
#     if not (occult == OccultType.WEREWOLF or occult == OccultType.FAIRY):
#         return None
#
#     return pelt_layer_cache.return_specific_json(sim_info.id)[occult].encode("cp437")
#
#
# def pelt_layer_exists_in_cache(sim_info, occult):
#     if not (occult == OccultType.WEREWOLF or occult == OccultType.FAIRY):
#         return False
#
#     if sim_info.id in pelt_layer_cache.return_json():
#         if occult in pelt_layer_cache.return_specific_json(sim_info.id):
#             return True
#         else:
#             return False
#     else:
#         return False