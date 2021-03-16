"""
Monitoring views
"""
import os

from django.conf import settings
from django.views.generic import TemplateView
from django.http import JsonResponse

# TODO: move to settings
RECALBOX_THERMAL_BASEDIR = '/sys/class/thermal'
# Assume 'thermal_zone0' is the CPU thermal infos on Raspberry
RECALBOX_THERMAL_DEVICE_CPU_DIR = 'thermal_zone0'
RECALBOX_THERMAL_CURRENT_TEMP_FILE = 'temp'
#RECALBOX_THERMAL_MAXTEMP_LIMIT_FILE = 'trip_point_0_temp'


# Compatibility support for Recalbox versions from 3.2.x to 3.3.x
# (psutil package only available since 3.3.0 beta 5)
try:
    import psutil
except ImportError:
    class RecalboxSystemInfosMixin(object):
        psutil_available = False
else:
    class RecalboxSystemInfosMixin(object):
        """
        Mixin to get all system infos using 'psutil' library
        """
        psutil_available = True
        mining_cpu_interval = settings.RECALBOX_PSUTIL_CPU_INTERVAL
        
        def get_thermal_infos(self, device_dir):
            """
            Watch for thermal infos using ACPI thermal API:
            
            http://lwn.net/Articles/268958/
            
            This is a naive implementation for the Raspberry2 which have only 
            one "trip_point" that is the "hot" type (should be critical)
            """
            #critical_limit = float(open(os.path.join(device_dir, RECALBOX_THERMAL_MAXTEMP_LIMIT_FILE), 'r').read().strip())
            current_temp = float(open(os.path.join(device_dir, RECALBOX_THERMAL_CURRENT_TEMP_FILE), 'r').read().strip())
            critical_limit = 75000
            
            # Divide per 1000 to have temperature in degrees Celsius
            current_temp = current_temp/1000
            critical_limit = critical_limit/1000
            percent_usage = (current_temp/critical_limit)*100
            
            return {
                'max': round(critical_limit, 2),
                'current': round(current_temp, 2),
                'percent_usage': round(percent_usage, 2),
            }
        
        def get_cpu_infos(self):
            return {
                'count': psutil.cpu_count(),
                'usage': psutil.cpu_percent(interval=self.mining_cpu_interval, percpu=True),
            }
        
        def get_memory_infos(self):
            virtual_mem = psutil.virtual_memory()
            return {
                'usage_percent': virtual_mem.percent,
                'usage_bytes': virtual_mem.used,
                'free_unified': virtual_mem.available,
                'total': virtual_mem.total,
            }
        
        def get_filesystem_infos(self):
            context = []
            
            for disk_part in psutil.disk_partitions():
                usage = psutil.disk_usage(disk_part.mountpoint)
                context.append({
                    'device': disk_part.device,
                    'mountpoint': disk_part.mountpoint,
                    'fstype': disk_part.fstype,
                    'total': usage.total,
                    'free': usage.free,
                    'used_bytes': usage.used,
                    'used_percent': usage.percent,
                })
            
            return context

class MonitoringView(RecalboxSystemInfosMixin, TemplateView):
    """
    Monitoring view to display system informations
    """
    template_name = "manager_frontend/monitoring.html"
    
    def get_context_data(self, **kwargs):
        context = super(MonitoringView, self).get_context_data(**kwargs)
        context['PSUTIL_AVAILABLE'] = self.psutil_available
        
        if self.psutil_available:
            context.update({
                'cpu_infos': self.get_cpu_infos(),
                'memory_infos': self.get_memory_infos(),
                'filesystem_infos': self.get_filesystem_infos(),
                'cpu_thermal_infos': self.get_thermal_infos(os.path.join(RECALBOX_THERMAL_BASEDIR, RECALBOX_THERMAL_DEVICE_CPU_DIR)),
            })
        return context


def update_context(request, *args, **kwargs):
    monitor = MonitoringView()
    data = {
        'cpu_infos': monitor.get_cpu_infos(),
        'memory_infos': monitor.get_memory_infos(),
        'filesystem_infos': monitor.get_filesystem_infos(),
        'cpu_thermal_infos': monitor.get_thermal_infos(os.path.join(RECALBOX_THERMAL_BASEDIR, RECALBOX_THERMAL_DEVICE_CPU_DIR)),
    }
    return JsonResponse(data)
