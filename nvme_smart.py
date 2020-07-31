import subprocess
import json
from random import *
import nvme_simulation as nv_simul

def print_smart_log(json_data):

	print('critical_warning %d' %json_data['critical_warning'])
	print('temperature %d' %json_data['temperature'])
	print('avail_spare %d' %json_data['avail_spare'])
	print('spare_thresh %d' %json_data['spare_thresh'])
	print('percent_used %d' %json_data['percent_used'])
	print('data_units_read %d' %json_data['data_units_read'])
	print('data_units_written %d' %json_data['data_units_written'])
	print('host_read_commands %d' %json_data['host_read_commands'])
	print('host_write_commands %d' %json_data['host_write_commands'])
	print('controller_buys_time %d' %json_data['controller_busy_time'])
	print('power_cycles %d' %json_data['power_cycles'])
	print('power_on_hours %d' %json_data['power_on_hours'])
	print('unsafe_shutdowns %d' %json_data['unsafe_shutdowns'])
	print('media_errors %d' %json_data['media_errors'])
	print('num_err_log_entries %d' %json_data['num_err_log_entries'])
	print('warning_temp_time %d' %json_data['warning_temp_time'])
	print('critical_comp_tim %d' %json_data['critical_comp_time'])
	print('thm_temp1_trans_count %d' %json_data['thm_temp1_trans_count'])
	print('thm_temp2_trans_count %d' %json_data['thm_temp2_trans_count'])
	print('thm_temp1_total_time %d' %json_data['thm_temp1_total_time'])
	print('thm_temp2_total_time %d' %json_data['thm_temp2_total_time'])


def get_smart_log(device_path):
    if nv_simul.NVME_SIMULATION == 0:
        proc = subprocess.Popen("nvme smart-log %s -o json" %device_path,
                                shell=True,
                                stdout=subprocess.PIPE,
                                encoding='utf-8')
        err = proc.wait()

        (stdout, stderr) = proc.communicate()

        json_data = json.loads(stdout)
    else:
        json_data = nv_simul.gen_simulation_smart_log(int(device_path[9:]))

	#print(type(json_data))
	#print(json_data)

    print_smart_log(json_data)

    return json_data

if __name__ == '__main__':
	smart_log_json = get_smart_log("/dev/nvme0")
	print('test critical warning %d' %smart_log_json['critical_warning'])
