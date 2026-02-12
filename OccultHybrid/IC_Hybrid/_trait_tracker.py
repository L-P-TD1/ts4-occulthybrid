import operator, services
from sims.occult.occult_tracker import OccultTracker, OccultType
from sims4.resources import Types
from statistics.commodity import MotiveUIStyle
from traits.trait_tracker import TraitTracker
from OccultHybrid.CoreLib.TD1_OccultHybrid_Decorator import to_decorate as inject_to
from OccultHybrid.IC_Hybrid import settings, occult_utils
from OccultHybrid.CoreLib.TD1_OccultHybrid_Config import get_option_value
from sims4.log import Logger

# Importation of MasterApprentice Logger
try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 OccultHybrid Trait Tracker', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

logger = Logger('TD1 OccultHybrid Trait Tracker', default_owner='TwelfthDoctor1')

MOTIVE_MAXIMUMS = {
    MotiveUIStyle.LONG: 2,
    MotiveUIStyle.ORB: 1
}

ORB_MOTIVE_MAPPING = {
    OccultType.WITCH: 213024,
    OccultType.WEREWOLF: 276223
}

LONG_BAR_MOTIVE = {
    OccultType.VAMPIRE: 150238,
    OccultType.FAIRY: 420035
}

BLACKLIST_MOTIVES = {
    384632,  # Ghost Stamina
    427050,  # Balance & Imbalance
    226814,  # commodity_CollegeOrganization_SecretSociety_SpriteVisitor_Timer
    16653,  # commodity_Motive_Comfort
    181210,  # commodity_sim_BodyTemperature
    10020,  # commodity_Motive_Thirst
    401759,  # commodity_FamilyRecipes_MotivatingTracker
    39470,  # commodity_object_burning
    219291,  # commodity_CollegeOrganization_SecretSociety_SpriteFavor
    272961,  # commodity_Sim_Fulfillment
    33350,  # commodity_SimInfo_TimeSinceLastSlept
    306749,  # commodity_Burnout_MentalTracker
    304271,  # commodity_Burnout_CreativeTracker
    33351,  # commodity_SimInfo_TimeSinceLastSocial
    190848  # commodity_sim_Overheating
}

BLACKLIST_OVERRIDE_MOTIVES = {
    OccultType.FAIRY: 150238
}


def get_commodity_list(trait_tracker_instance):
    if not trait_tracker_instance._sim_info.is_selectable:
        return
    final_list = []
    commodities = trait_tracker_instance._sim_info.get_initial_commodities()
    override_dict = dict()
    occult_motives_dict = dict()
    occult_traits = []
    if OccultTracker.OCCULT_DATA:
        for occult, tuning in OccultTracker.OCCULT_DATA.items():
            if tuning.occult_trait:
                occult_traits.append(tuning.occult_trait)
            if tuning.current_occult_trait:
                occult_traits.append(tuning.current_occult_trait)
            if tuning.additional_occult_traits:
                occult_traits.extend(tuning.additional_occult_traits)

    for trait in occult_traits:
        if trait.initial_commodities:
            for override_commodity in trait.initial_commodities:
                render_style = override_commodity.ui_render_style
                occult_motives = occult_motives_dict.get(render_style, [])
                if override_commodity not in occult_motives:
                    occult_motives.append(override_commodity)
                else:
                    occult_motives_dict[render_style] = occult_motives

    for trait in trait_tracker_instance._equipped_traits:
        if trait.ui_commodity_sort_override:
            for override_commodity in trait.ui_commodity_sort_override:
                if override_commodity in commodities:
                    render_style = override_commodity.ui_render_style
                    motives = override_dict.get(render_style, [])
                    if override_commodity not in motives:
                        motives.append(override_commodity)
                        override_dict[render_style] = motives

    if master_logger is not None and master_logger is not False:
        master_logger.debug(
            f"OVERRIDE COMMODITY DICT VIEW\n"
            f"\n"
            f"{override_dict}"
        )

    logger.info(
        f"OVERRIDE COMMODITY DICT VIEW\n"
        f"\n"
        f"{override_dict}"
    )

    motive_dict = {}
    current_occult = trait_tracker_instance._sim_info.occult_types
    for motive in commodities:
        if master_logger is not None and master_logger is not False:
            master_logger.debug(
                f"COMMODITY FOR TEST: {motive}"
            )

        logger.info(
            f"COMMODITY FOR TEST: {motive}"
        )

        blacklist = False
        for blacklist_motive in BLACKLIST_MOTIVES:
            if motive == services.get_instance_manager(Types.STATISTIC).get(blacklist_motive):
                if master_logger is not None and master_logger is not False:
                    master_logger.debug(
                        f"Commodity {motive} matches Commodity {services.get_instance_manager(Types.STATISTIC).get(blacklist_motive)}"
                    )
                blacklist = True
                break

        # Long Motive Blacklist Handling
        if current_occult == OccultType.FAIRY or current_occult == OccultType.HUMAN | OccultType.FAIRY or occult_utils.is_sim_in_form(
                trait_tracker_instance._sim_info, OccultType.FAIRY):
            # Blacklist Vampire Power - Fairy Form
            if motive == services.get_instance_manager(Types.STATISTIC).get(LONG_BAR_MOTIVE[OccultType.VAMPIRE]):
                blacklist = True

                if master_logger is not None and master_logger is not False:
                    master_logger.debug(
                        f"Sim is Fairy\n"
                        f"\n"
                        f"Disable: {motive}"
                    )

                logger.debug(
                    f"Sim is Fairy\n"
                    f"\n"
                    f"Disable: {motive}"
                )
        elif current_occult == OccultType.VAMPIRE or current_occult == OccultType.HUMAN | OccultType.VAMPIRE or occult_utils.is_sim_in_form(
                trait_tracker_instance._sim_info, OccultType.VAMPIRE) or current_occult == OccultType.HUMAN:
            # Blacklist Emotional Power - Vampire Form
            if motive == services.get_instance_manager(Types.STATISTIC).get(LONG_BAR_MOTIVE[OccultType.FAIRY]):
                blacklist = True

                if master_logger is not None and master_logger is not False:
                    master_logger.debug(
                        f"Sim is not Fairy\n"
                        f"\n"
                        f"Disable: {motive}"
                    )

                logger.debug(
                    f"Sim is not Fairy\n"
                    f"\n"
                    f"Disable: {motive}"
                )

        # Orb Motive Blacklist Handling
        if current_occult == OccultType.WEREWOLF or current_occult == OccultType.HUMAN | OccultType.WEREWOLF or occult_utils.is_sim_in_form(
                trait_tracker_instance._sim_info, OccultType.WEREWOLF):
            # Blacklist Fury Orb - Spellcaster Form
            if motive == services.get_instance_manager(Types.STATISTIC).get(ORB_MOTIVE_MAPPING[OccultType.WITCH]):
                blacklist = True

                if master_logger is not None and master_logger is not False:
                    master_logger.debug(
                        f"Sim is Werewolf\n"
                        f"\n"
                        f"Disable: {motive}"
                    )

                logger.debug(
                    f"Sim is Werewolf\n"
                    f"\n"
                    f"Disable: {motive}"
                )
        else:
            # Blacklist Spellcaster Orb - Werewolf Form
            if motive == services.get_instance_manager(Types.STATISTIC).get(ORB_MOTIVE_MAPPING[OccultType.WEREWOLF]):
                blacklist = True

                if master_logger is not None and master_logger is not False:
                    master_logger.debug(
                        f"Sim is not Werewolf\n"
                        f"\n"
                        f"Disable: {motive}"
                    )

                logger.debug(
                    f"Sim is not Werewolf\n"
                    f"\n"
                    f"Disable: {motive}"
                )

        if blacklist is True:
            continue

        if motive.ui_render_style not in motive_dict:
            motive_dict[motive.ui_render_style] = []
        if motive.visible:
            motive_dict[motive.ui_render_style].append(motive)

    if master_logger is not None and master_logger is not False:
        master_logger.debug(
            f"MOTIVE DICT VIEW\n"
            f"\n"
            f"{motive_dict}"
        )

    logger.debug(
        f"MOTIVE DICT VIEW\n"
        f"\n"
        f"{motive_dict}"
    )

    for ui_style in MotiveUIStyle:
        if ui_style in motive_dict:
            sorted_motives = sorted((motive_dict[ui_style]), key=(operator.attrgetter('ui_sort_order')))
        else:
            sorted_motives = []
        override_motives = override_dict.get(ui_style, [])

        for override_motive in override_motives:
            if current_occult == OccultType.FAIRY or current_occult == OccultType.HUMAN | OccultType.FAIRY or occult_utils.is_sim_in_form(
                    trait_tracker_instance._sim_info, OccultType.FAIRY):
                if override_motive == services.get_instance_manager(Types.STATISTIC).get(BLACKLIST_OVERRIDE_MOTIVES[OccultType.FAIRY]):
                    if master_logger is not None and master_logger is not False:
                        master_logger.debug(
                            f"OVERRIDE MOTIVE REMOVAL\n"
                            f"\n"
                            f"{override_motive}"
                        )

                    logger.debug(
                        f"OVERRIDE MOTIVE REMOVAL\n"
                        f"\n"
                        f"{override_motive}"
                    )

                    override_motives.remove(services.get_instance_manager(Types.STATISTIC).get(BLACKLIST_OVERRIDE_MOTIVES[OccultType.FAIRY]))

        temp_list = override_motives + sorted_motives
        temp_list = list(dict.fromkeys(temp_list).keys())
        if ui_style in MOTIVE_MAXIMUMS:
            max_motives = MOTIVE_MAXIMUMS[ui_style]
            if len(temp_list) > max_motives:
                for motive in occult_motives_dict.get(ui_style, []):
                    if len(temp_list) > max_motives:
                        if motive in temp_list:
                            temp_list.remove(motive)
                    else:
                        break

                temp_list = temp_list[:max_motives]
        temp_list = sorted(temp_list, key=(operator.attrgetter('ui_sort_order')))

        if master_logger is not None and master_logger is not False:
            master_logger.debug(
                f"SORTING MOTIVE DICT : {ui_style}\n"
                f"\n"
                f"[1] SORTED MOTIVES: {sorted_motives}\n"
                f"[2] OVERRIDE MOTIVES: {override_motives}\n\n"
                f"FINAL {ui_style}: {temp_list}"
            )

        logger.debug(
            f"SORTING MOTIVE DICT : {ui_style}\n"
            f"\n"
            f"[1] SORTED MOTIVES: {sorted_motives}\n"
            f"[2] OVERRIDE MOTIVES: {override_motives}\n\n"
            f"FINAL {ui_style}: {temp_list}"
        )

        if ui_style == MotiveUIStyle.DEFAULT:
            final_list.extend(temp_list)
        else:
            final_list = temp_list + final_list

    if master_logger is not None and master_logger is not False:
        master_logger.debug(
            f"FINAL LIST VIEW\n"
            f"\n"
            f"{final_list}"
        )

    logger.debug(
        f"FINAL LIST VIEW\n"
        f"\n"
        f"{final_list}"
    )

    return final_list


@inject_to(TraitTracker, '_send_commodity_list_msg')
def send_commodity_list_msg(original, self, commodity_list: list, *args, **kwargs):
    if settings.OVERRIDE_MOTIVES_PANEL and get_option_value("override_motive_panel"):
        return original(self, get_commodity_list(self), *args, **kwargs)
    return original(self, commodity_list, *args, **kwargs)