from sims4.tuning.instance_manager import InstanceManager
from OccultHybrid.IC_Hybrid.class_instance_tuning_injection import ClassInstanceTuningInjection
from OccultHybrid.CoreLib.TD1_OccultHybrid_Decorator import to_decorate as inject_to


@inject_to(InstanceManager, 'load_data_into_class_instances')
def load_data_into_class_instances(original, self, *args, **kwargs):
    original(self, *args, **kwargs)
    ClassInstanceTuningInjection.load_data_into_class_instances(self)
