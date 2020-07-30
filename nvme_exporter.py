from prometheus_client import start_http_server, Summary, Counter, Gauge, Histogram
from prometheus_client import Info
import nvme_smart as ns
import nvme_list as nl
import nvme_simulation as nv_simul
import random
import time
import json

def init_nvme_smart_gauge():
    nvme_smart_gauge = dict()
    nvme_smart_gauge['critical_warning']		= Gauge('nvme_smart_log_critical_warning'		,'nvme_smart_log_critical_warning'		 , ['device', 'critical_warning'])
    nvme_smart_gauge['temperature']				= Gauge('nvme_smart_log_temperature'			,'nvme_smart_log_temperature'			 , ['device'])
    nvme_smart_gauge['avail_spare']				= Gauge('nvme_smart_log_avail_spare'			,'nvme_smart_log_avail_spare'			 , ['device'])
    nvme_smart_gauge['spare_thresh']			= Gauge('nvme_smart_log_spare_thresh'			,'nvme_smart_log_spare_thresh'			 , ['device'])
    nvme_smart_gauge['percent_used']			= Gauge('nvme_smart_log_percent_used'			,'nvme_smart_log_percent_used'			 , ['device'])
    nvme_smart_gauge['data_units_read']			= Gauge('nvme_smart_log_data_units_read'		,'nvme_smart_log_data_units_read'		 , ['device'])
    nvme_smart_gauge['data_units_written']		= Gauge('nvme_smart_log_data_units_written'		,'nvme_smart_log_data_units_written'	 , ['device'])
    nvme_smart_gauge['host_read_commands']		= Gauge('nvme_smart_log_host_read_commands'		,'nvme_smart_log_host_read_commands'	 , ['device'])
    nvme_smart_gauge['host_write_commands']		= Gauge('nvme_smart_log_host_write_commands'	,'nvme_smart_log_host_write_commands'	 , ['device'])
    nvme_smart_gauge['controller_busy_time']	= Gauge('nvme_smart_log_controller_busy_time'	,'nvme_smart_log_controller_busy_time'	 , ['device'])
    nvme_smart_gauge['power_cycles']			= Gauge('nvme_smart_log_power_cycles'			,'nvme_smart_log_power_cycles'			 , ['device'])
    nvme_smart_gauge['power_on_hours']			= Gauge('nvme_smart_log_power_on_hours'			,'nvme_smart_log_power_on_hours'		 , ['device'])
    nvme_smart_gauge['unsafe_shutdowns']		= Gauge('nvme_smart_log_unsafe_shutdowns'		,'nvme_smart_log_unsafe_shutdowns'		 , ['device'])
    nvme_smart_gauge['media_errors']			= Gauge('nvme_smart_log_media_errors'			,'nvme_smart_log_media_errors'			 , ['device'])
    nvme_smart_gauge['num_err_log_entries']		= Gauge('nvme_smart_log_num_error_log_entries'	,'nvme_smart_log_num_error_log_entries'	 , ['device'])
    nvme_smart_gauge['warning_temp_time']		= Gauge('nvme_smart_warning_temp_time'			,'nvme_smart_warning_temp_time'			 , ['device'])
    nvme_smart_gauge['critical_comp_time']		= Gauge('nvme_smart_critical_comp_time'			,'nvme_smart_critical_comp_time'		 , ['device'])
    nvme_smart_gauge['thm_temp1_trans_count']	= Gauge('nvme_smart_thm_temp1_trans_count'		,'nvme_smart_thm_temp1_trans_count'		 , ['device'])
    nvme_smart_gauge['thm_temp2_trans_count']	= Gauge('nvme_smart_thm_temp2_trans_count'		,'nvme_smart_thm_temp2_trans_count'		 , ['device'])
    return nvme_smart_gauge

def gather_nvme_smart_log(nvme_smart_gauge):

    for nvme in nvme_list_json['Devices']:

        device = nvme['DevicePath']

        print('\nDevice %s' %device)

        smart_json = ns.get_smart_log(device)

        if smart_json['critical_warning'] & 1:
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], critical_warning='avail_spare').set(1)
        else:
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], critical_warning='avail_spare').set(0)

        if smart_json['critical_warning'] & (1 << 1) :
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], critical_warning='temp_threshold').set(1)
        else:
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], critical_warning='temp_threshold').set(0)

        if smart_json['critical_warning'] & (1 << 2) :
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], critical_warning='nvm_subsystem_reliability').set(1)
        else:
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], critical_warning='nvm_subsystem_reliability').set(0)

        if smart_json['critical_warning'] & (1 << 3) :
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], critical_warning='read_only').set(1)
        else:
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], critical_warning='read_only').set(0)

        if smart_json['critical_warning'] & (1 << 4) :
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], critical_warning='volatile_backup_failed').set(1)
        else:
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], critical_warning='volatile_backup_failed').set(0)

        if smart_json['critical_warning'] & (1 << 5) :
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], critical_warning='persistent_memory_read_only').set(1)
        else:
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], critical_warning='persistent_memory_read_only').set(0)

        #nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], critical_warning='test').set(smart_json['critical_warning'])

        nvme_smart_gauge['temperature'].labels(nvme['DevicePath']).set(smart_json['temperature'])
        nvme_smart_gauge['avail_spare'].labels(nvme['DevicePath']).set(smart_json['avail_spare'])
        nvme_smart_gauge['spare_thresh'].labels(nvme['DevicePath']).set(smart_json['spare_thresh'])
        nvme_smart_gauge['percent_used'].labels(nvme['DevicePath']).set(smart_json['percent_used'])
        nvme_smart_gauge['data_units_read'].labels(nvme['DevicePath']).set(smart_json['data_units_read'])
        nvme_smart_gauge['data_units_written'].labels(nvme['DevicePath']).set(smart_json['data_units_written'])
        nvme_smart_gauge['host_read_commands'].labels(nvme['DevicePath']).set(smart_json['host_read_commands'])
        nvme_smart_gauge['host_write_commands'].labels(nvme['DevicePath']).set(smart_json['host_write_commands'])
        nvme_smart_gauge['controller_busy_time'].labels(nvme['DevicePath']).set(smart_json['controller_busy_time'])
        nvme_smart_gauge['power_cycles'].labels(nvme['DevicePath']).set(smart_json['power_cycles'])
        nvme_smart_gauge['power_on_hours'].labels(nvme['DevicePath']).set(smart_json['power_on_hours'])
        nvme_smart_gauge['unsafe_shutdowns'].labels(nvme['DevicePath']).set(smart_json['unsafe_shutdowns'])		
        nvme_smart_gauge['media_errors'].labels(nvme['DevicePath']).set(smart_json['media_errors'])
        nvme_smart_gauge['num_err_log_entries'].labels(nvme['DevicePath']).set(smart_json['num_err_log_entries'])
        nvme_smart_gauge['warning_temp_time'].labels(nvme['DevicePath']).set(smart_json['warning_temp_time'])
        nvme_smart_gauge['critical_comp_time'].labels(nvme['DevicePath']).set(smart_json['critical_comp_time'])
        nvme_smart_gauge['thm_temp1_trans_count'].labels(nvme['DevicePath']).set(smart_json['thm_temp1_trans_count'])
        nvme_smart_gauge['thm_temp2_trans_count'].labels(nvme['DevicePath']).set(smart_json['thm_temp2_trans_count'])

def put_nvme_info():

	nvme_info = Info('nvme_info', 'Description of NVMe Info', ['device'])

	for nvme in nvme_list_json['Devices']:
		nvme_info.labels(nvme['DevicePath']).info({'ProduceName': nvme['ProductName']})
		nvme_info.labels(nvme['DevicePath']).info({'ModelNumber': nvme['ModelNumber']})

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.

    if nv_simul.NVME_SIMULATION == 1:
        nv_simul.init_nvme_devices()
        #nv_simul.init_simulation_smart_log()

    nvme_list_json = nl.get_nvme_list()
    put_nvme_info()
    nvme_smart_gauge = init_nvme_smart_gauge()

    while True:
        gather_nvme_smart_log(nvme_smart_gauge)
        time.sleep(10)
