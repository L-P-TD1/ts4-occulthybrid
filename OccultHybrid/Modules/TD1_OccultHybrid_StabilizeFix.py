"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
LordPercivalXII's OccultHybrid Mod

> Stabilize Fix Module

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
from OccultHybrid.CoreLib.TD1_OccultHybrid_Decorator import to_decorate
from sims.sim_info_manager import SimInfoManager
from sims.occult.occult_tracker import OccultTracker
from sims.occult.occult_enums import OccultType
from sims4.common import is_available_pack, Pack
from sims4.resources import Types
from traits.trait_tracker import TraitTracker

# Importation of MasterApprentice Logger

try:
    from MasterApprenticeLib.TD1_Lib_ApprenticeLogger import ApprenticeLogger

    apprentice_logger = ApprenticeLogger('TD1 Occult Hybrid Fix Handler', main_owner='TwelfthDoctor1')

except ImportError:
    apprentice_logger = False

try:
    from MasterApprenticeLib.TD1_Lib_MasterLogger import MasterLogger

    master_logger = MasterLogger('TD1 Occult Hybrid Fix Handler', main_owner='TwelfthDoctor1')

except ImportError:
    master_logger = False

# No longer required.
RUN_SECONDARY_FORM_FIX = False
RAN_FIX = False

TIMEOUT_TRAIT = 9260118828366424873
VAMPIRE_MANUAL_DARK_FORM_TRAIT = 156397


@to_decorate(SimInfoManager, 'on_loading_screen_animation_finished')
def administer_secondary_form_fix_on_load(original, self, *args, **kwargs):
    result = original(self, *args, **kwargs)

    if RUN_SECONDARY_FORM_FIX is False or get_option_value("werewolf_stabilization") is False:
        return

    if RAN_FIX is True:
        return

    if not is_available_pack(Pack.GP12):
        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.info("Pack: GP12 not found. Fix not required.")

        if master_logger is not None and master_logger is not False:
            master_logger.info("Pack: GP12 not found. Fix will not initiate.")
        return

    try:
        timeout_trait = services.get_instance_manager(Types.TRAIT).get(TIMEOUT_TRAIT)
        for sim_info in services.sim_info_manager().get_all():
            trait_tracker: TraitTracker = sim_info.trait_tracker
            occult_tracker: OccultTracker = sim_info.occult_tracker
            manual_dark_form_trait = services.get_instance_manager(Types.TRAIT).get(VAMPIRE_MANUAL_DARK_FORM_TRAIT)

            for occult in OccultType:
                current_occult_trait = get_current_occult_trait(occult, occult_tracker)

                # Disallow Werewolf Occult
                if occult == OccultType.WEREWOLF:
                    continue

                # If Have Occult Data
                if current_occult_trait is not None:
                    # If Have Secondary Form Trait (currently in Secondary Form)
                    if sim_info.has_trait(current_occult_trait):
                        # sim_info.add_trait(timeout_trait)

                        # Initiate Switch to Secondary Form
                        if occult != OccultType.VAMPIRE:
                            if trait_tracker.has_trait(manual_dark_form_trait):
                                sim_info.remove_trait(manual_dark_form_trait)

                        else:
                            if not trait_tracker.has_trait(manual_dark_form_trait):
                                sim_info.add_trait(manual_dark_form_trait)

                        occult_tracker.set_pending_occult_type(sim_info.current_occult_types)
                        occult_tracker.switch_to_occult_type(occult)

                    # If not in Secondary Form
                    else:
                        # Initiate Switch to Into Primary Form
                        occult_tracker.set_pending_occult_type(sim_info.current_occult_types)
                        occult_tracker.switch_to_occult_type(OccultType.HUMAN)

                # No Occult Data - HUMAN
                else:
                    pass

        global RAN_FIX
        RAN_FIX = True

    except Exception as e:
        if apprentice_logger is not None and apprentice_logger is not False:
            apprentice_logger.error(
                f"SECONDARY FORM FIX FAILURE:\n{e}"
            )

        if master_logger is not None and master_logger is not False:
            master_logger.error(
                f"SECONDARY FORM FIX FAILURE:\n{e}"
            )


def get_current_occult_trait(occult: OccultType, occult_tracker: OccultTracker):
    if occult_tracker.has_occult_type(occult):
        occult_data = OccultTracker.OCCULT_DATA.get(occult)

        current_occult_trait = occult_data.current_occult_trait

        return current_occult_trait
    else:
        return None
