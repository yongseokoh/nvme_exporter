from prometheus_client import start_http_server, Summary, Counter, Gauge, Histogram
from prometheus_client import Info
import nvme_smart as ns
import nvme_list as nl
import nvme_ctrl as nc
import nvme_simulation as nv_simul
import random
import time
import json
import os
import argparse

def init_nvme_ctrl_gauge():
    nvme_ctrl_gauge = dict()
    nvme_ctrl_gauge['cc']		= Gauge('nvme_ctrl_cc'		,'nvme_ctrl_configuration'	 , ['device', 'cc'])
    nvme_ctrl_gauge['csts']		= Gauge('nvme_ctrl_csts'	,'nvme_ctrl_status'			 , ['device', 'csts'])
    return nvme_ctrl_gauge

def init_nvme_smart_gauge():
    nvme_smart_gauge = dict()
    nvme_smart_gauge['critical_warning']		= Gauge('nvme_smart_log_critical_warning'		,'nvme_smart_log_critical_warning'		 , ['device', 'devno', 'critical_warning'])
    nvme_smart_gauge['temperature']				= Gauge('nvme_smart_log_temperature'			,'nvme_smart_log_temperature'			 , ['device','devno'])
    nvme_smart_gauge['avail_spare']				= Gauge('nvme_smart_log_avail_spare'			,'nvme_smart_log_avail_spare'			 , ['device', 'devno'])
    nvme_smart_gauge['spare_thresh']			= Gauge('nvme_smart_log_spare_thresh'			,'nvme_smart_log_spare_thresh'			 , ['device', 'devno'])
    nvme_smart_gauge['percent_used']			= Gauge('nvme_smart_log_percent_used'			,'nvme_smart_log_percent_used'			 , ['device', 'devno'])
    nvme_smart_gauge['data_units_read']			= Gauge('nvme_smart_log_data_units_read'		,'nvme_smart_log_data_units_read'		 , ['device', 'devno'])
    nvme_smart_gauge['data_units_written']		= Gauge('nvme_smart_log_data_units_written'		,'nvme_smart_log_data_units_written'	 , ['device', 'devno'])
    nvme_smart_gauge['host_read_commands']		= Gauge('nvme_smart_log_host_read_commands'		,'nvme_smart_log_host_read_commands'	 , ['device', 'devno'])
    nvme_smart_gauge['host_write_commands']		= Gauge('nvme_smart_log_host_write_commands'	,'nvme_smart_log_host_write_commands'	 , ['device', 'devno'])
    nvme_smart_gauge['controller_busy_time']	= Gauge('nvme_smart_log_controller_busy_time'	,'nvme_smart_log_controller_busy_time'	 , ['device', 'devno'])
    nvme_smart_gauge['power_cycles']			= Gauge('nvme_smart_log_power_cycles'			,'nvme_smart_log_power_cycles'			 , ['device', 'devno'])
    nvme_smart_gauge['power_on_hours']			= Gauge('nvme_smart_log_power_on_hours'			,'nvme_smart_log_power_on_hours'		 , ['device', 'devno'])
    nvme_smart_gauge['unsafe_shutdowns']		= Gauge('nvme_smart_log_unsafe_shutdowns'		,'nvme_smart_log_unsafe_shutdowns'		 , ['device', 'devno'])
    nvme_smart_gauge['media_errors']			= Gauge('nvme_smart_log_media_errors'			,'nvme_smart_log_media_errors'			 , ['device', 'devno'])
    nvme_smart_gauge['num_err_log_entries']		= Gauge('nvme_smart_log_num_error_log_entries'	,'nvme_smart_log_num_error_log_entries'	 , ['device', 'devno'])
    nvme_smart_gauge['warning_temp_time']		= Gauge('nvme_smart_warning_temp_time'			,'nvme_smart_warning_temp_time'			 , ['device', 'devno'])
    nvme_smart_gauge['critical_comp_time']		= Gauge('nvme_smart_critical_comp_time'			,'nvme_smart_critical_comp_time'		 , ['device', 'devno'])
    nvme_smart_gauge['thm_temp1_trans_count']	= Gauge('nvme_smart_thm_temp1_trans_count'		,'nvme_smart_thm_temp1_trans_count'		 , ['device', 'devno'])
    nvme_smart_gauge['thm_temp2_trans_count']	= Gauge('nvme_smart_thm_temp2_trans_count'		,'nvme_smart_thm_temp2_trans_count'		 , ['device', 'devno'])
    return nvme_smart_gauge

def gather_nvme_smart_log(nvme_smart_gauge, nvme_list_json):

    for nvme in nvme_list_json['Devices']:

        device = nvme['DevicePath']

        smart_json = ns.get_smart_log(device)
        devno = nvme['DevicePath'][9:11]

        if smart_json['critical_warning'] & 1:
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], devno=devno, critical_warning='avail_spare').set(1)
        else:
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], devno=devno, critical_warning='avail_spare').set(0)

        if smart_json['critical_warning'] & (1 << 1) :
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], devno=devno, critical_warning='temp_threshold').set(1)
        else:
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], devno=devno, critical_warning='temp_threshold').set(0)

        if smart_json['critical_warning'] & (1 << 2) :
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], devno=devno, critical_warning='nvm_subsystem_reliability').set(1)
        else:
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], devno=devno, critical_warning='nvm_subsystem_reliability').set(0)

        if smart_json['critical_warning'] & (1 << 3) :
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], devno=devno, critical_warning='read_only').set(1)
        else:
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], devno=devno, critical_warning='read_only').set(0)

        if smart_json['critical_warning'] & (1 << 4) :
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], devno=devno, critical_warning='volatile_backup_failed').set(1)
        else:
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], devno=devno, critical_warning='volatile_backup_failed').set(0)

        if smart_json['critical_warning'] & (1 << 5) :
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], devno=devno, critical_warning='persistent_memory_read_only').set(1)
        else:
            nvme_smart_gauge['critical_warning'].labels(device=nvme['DevicePath'], devno=devno, critical_warning='persistent_memory_read_only').set(0)

        nvme_smart_gauge['temperature'].labels(device=nvme['DevicePath'], devno=devno).set(smart_json['temperature'])
        nvme_smart_gauge['avail_spare'].labels(device=nvme['DevicePath'], devno=devno).set(smart_json['avail_spare'])
        nvme_smart_gauge['spare_thresh'].labels(device=nvme['DevicePath'], devno=devno).set(smart_json['spare_thresh'])
        nvme_smart_gauge['percent_used'].labels(device=nvme['DevicePath'], devno=devno).set(smart_json['percent_used'])
        nvme_smart_gauge['data_units_read'].labels(device=nvme['DevicePath'], devno=devno).set(smart_json['data_units_read'])
        nvme_smart_gauge['data_units_written'].labels(device=nvme['DevicePath'], devno=devno).set(smart_json['data_units_written'])
        nvme_smart_gauge['host_read_commands'].labels(device=nvme['DevicePath'], devno=devno).set(smart_json['host_read_commands'])
        nvme_smart_gauge['host_write_commands'].labels(device=nvme['DevicePath'], devno=devno).set(smart_json['host_write_commands'])
        nvme_smart_gauge['controller_busy_time'].labels(device=nvme['DevicePath'],devno=devno).set(smart_json['controller_busy_time'])
        nvme_smart_gauge['power_cycles'].labels(device=nvme['DevicePath'], devno=devno).set(smart_json['power_cycles'])
        nvme_smart_gauge['power_on_hours'].labels(device=nvme['DevicePath'], devno=devno).set(smart_json['power_on_hours'])
        nvme_smart_gauge['unsafe_shutdowns'].labels(device=nvme['DevicePath'], devno=devno).set(smart_json['unsafe_shutdowns'])		
        nvme_smart_gauge['media_errors'].labels(device=nvme['DevicePath'], devno=devno).set(smart_json['media_errors'])
        nvme_smart_gauge['num_err_log_entries'].labels(device=nvme['DevicePath'], devno=devno).set(smart_json['num_err_log_entries'])
        nvme_smart_gauge['warning_temp_time'].labels(device=nvme['DevicePath'], devno=devno).set(smart_json['warning_temp_time'])
        nvme_smart_gauge['critical_comp_time'].labels(device=nvme['DevicePath'], devno=devno).set(smart_json['critical_comp_time'])
        nvme_smart_gauge['thm_temp1_trans_count'].labels(device=nvme['DevicePath'], devno=devno).set(smart_json['thm_temp1_trans_count'])
        nvme_smart_gauge['thm_temp2_trans_count'].labels(device=nvme['DevicePath'], devno=devno).set(smart_json['thm_temp2_trans_count'])

def gather_nvme_ctrl_info(nvme_ctrl_gauge, nvme_list_json):

    for nvme in nvme_list_json['Devices']:

        device = nvme['DevicePath']

        ctrl_json = nc.get_ctrl_regs(device)

        if ctrl_json['cc'] & 1:
            nvme_ctrl_gauge['cc'].labels(device=nvme['DevicePath'], cc='en').set(1)
        else:
            nvme_ctrl_gauge['cc'].labels(device=nvme['DevicePath'], cc='en').set(0)

        if ctrl_json['csts'] & 1:
            nvme_ctrl_gauge['csts'].labels(device=nvme['DevicePath'], csts='rdy').set(1)
        else:
            nvme_ctrl_gauge['csts'].labels(device=nvme['DevicePath'], csts='rdy').set(0)

def put_nvme_info(nvme_list_json):

	nvme_info = Info('nvme_info', 'Description of NVMe Info', ['device'])

	for nvme in nvme_list_json['Devices']:
		nvme_info.labels(nvme['DevicePath']).info({'ProduceName': nvme['ProductName']})
		nvme_info.labels(nvme['DevicePath']).info({'ModelNumber': nvme['ModelNumber']})

def parse_args():
    parser = argparse.ArgumentParser(
        description='NVME Export port number and update period time'
    )
    parser.add_argument(
        '-p', '--port',
        required=False,
        type=int,
        help='Port to listen',
        default=int(os.environ.get('PORT', '9900'))
    )
    parser.add_argument(
        '-u', '--update',
        required=False,
        help='export mertic update period in seconds',
        default=os.environ.get('UPDATE_PERIOD', '10')
    )
    parser.add_argument(
        '-s', '--simulation',
        required=False,
        help='making use of NVMe simulation',
        default=os.environ.get('SIMULATION', '0')
    )
    return parser.parse_args()

def main():

    try:
        port = 9998
        simulation = 1
        update_period = 60
        # args = parse_args()
        #print('port = %d' % int(args.port))
        #print('update = %d' % int(args.update))
        #print('simulation = %d' % int(args.simulation))

        nv_simul.NVME_SIMULATION = int(simulation)

        # Start up the server to expose the metrics.
        start_http_server(int(port))
        # Generate some requests.

        if nv_simul.NVME_SIMULATION == 1:
            nv_simul.init_nvme_devices()
            #nv_simul.init_simulation_smart_log()

        nvme_list_json = nl.get_nvme_list()
        put_nvme_info(nvme_list_json)
        nvme_smart_gauge = init_nvme_smart_gauge()
        nvme_ctrl_gauge = init_nvme_ctrl_gauge()

        while True:
            gather_nvme_smart_log(nvme_smart_gauge, nvme_list_json)
            gather_nvme_ctrl_info(nvme_ctrl_gauge, nvme_list_json)
            time.sleep(int(update_period))

    except KeyboardInterrupt:
        print("\nInterrupted")
        exit(0)

if __name__ == '__main__':
    main()
