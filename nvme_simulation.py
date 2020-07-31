import subprocess
import json
from random import *

NVME_SIMULATION = 1

nvme_devices = []
nvme_list = dict()
nvme_list['Devices'] = []
NUM_NVME = 24

def init_nvme_devices():
    for devno in range(0, NUM_NVME):
        nvme_device = dict()
        nvme_device['info'] = dict()
        nvme_device['smart'] = dict()
        nvme_device['ctrl'] = dict()

        nvme_devices.insert(devno, nvme_device)

    for devno in range(0, NUM_NVME):
        print('init_nvme_devices() %d' %devno)
        init_simulation_smart_log(devno)
        init_simulation_device_info(devno)
        init_simulation_ctrl(devno)

def get_nvme_device_info(devno):
    nvme_device = nvme_devices[devno]
    return nvme_device['info']

def get_nvme_device_smart_log(devno):
    nvme_device = nvme_devices[devno]
    return nvme_device['smart']

def get_nvme_device_ctrl(devno):
    nvme_device = nvme_devices[devno]
    return nvme_device['ctrl']

def init_simulation_ctrl(devno):
    ctrl_json_data = get_nvme_device_ctrl(devno)
    ctrl_json_data['cap'] = 137606795263
    ctrl_json_data['vs'] = 66048
    ctrl_json_data['intms'] = 0
    ctrl_json_data['intmc'] = 0
    ctrl_json_data['cc'] = 4587520
    ctrl_json_data['csts'] = 0
    ctrl_json_data['nssr'] = 0
    ctrl_json_data['aqa'] = 2031647
    ctrl_json_data['asq'] = 8368267264
    ctrl_json_data['acq'] = 8370688000
    ctrl_json_data['cmbloc'] = 3
    ctrl_json_data['cmbsz'] = 3
    ctrl_json_data['bpinfo'] = 5242883
    ctrl_json_data['bprsel'] = 4294967295
    ctrl_json_data['bpmbl'] = 18446744073709551615

def gen_simulation_ctrl(devno):
    ctrl_json_data = get_nvme_device_ctrl(devno)

    cc_en = randint(0, 1)

    ctrl_json_data['cc'] = 4587520 + cc_en
    if cc_en == 0:
        ctrl_json_data['csts'] = 0
    else:
        ctrl_json_data['csts'] = randint(0, 1)

    return ctrl_json_data

def init_simulation_smart_log(devno):

    smart_json_data = get_nvme_device_smart_log(devno)

    smart_json_data['critical_warning'] = 0
    smart_json_data['temperature'] = 308 + randint(1, 10)
    smart_json_data['avail_spare'] = 0 + randint(1, 10)
    smart_json_data['spare_thresh'] = 0 + randint(1, 10)
    smart_json_data['percent_used'] = 0 + randint(1, 10)
    smart_json_data['data_units_read'] = 0 + randint(1, 10000)
    smart_json_data['data_units_written'] = 0 + randint(1, 100000)
    smart_json_data['host_read_commands'] = 0 + randint(1, 10000)
    smart_json_data['host_write_commands'] = 0 + randint(1, 10000)
    smart_json_data['controller_busy_time'] = 0 + randint(1, 10000)
    smart_json_data['power_cycles'] = 0 + randint(1, 100)
    smart_json_data['power_on_hours'] = 0 + randint(1, 1000)
    smart_json_data['unsafe_shutdowns'] = 0 + randint(1, 100)
    smart_json_data['media_errors'] = 0 + randint(1, 10)
    smart_json_data['num_err_log_entries'] = 0 + randint(1, 10)
    smart_json_data['warning_temp_time'] = 0 + randint(1, 10)
    smart_json_data['critical_comp_time'] = 0 + randint(1, 10)
    smart_json_data['thm_temp1_trans_count'] = 0 + randint(1, 10)
    smart_json_data['thm_temp2_trans_count'] = 0 + randint(1, 10)
    smart_json_data['thm_temp1_total_time'] = 0 + randint(1, 100)
    smart_json_data['thm_temp2_total_time'] = 0 + randint(1, 100)

def gen_simulation_smart_log(devno):

    smart_json_data = get_nvme_device_smart_log(devno)

    avail_spare = randint(0, 1)
    temp_threshold = randint(0, 1)
    nvm_sub_reliability = randint(0, 1)
    read_only = randint(0, 1)
    volatile_backup_failed = randint(0, 1)
    persistent_mem_ro = randint(0, 1)

    critical_warning = (avail_spare)  + (temp_threshold << 1) + (nvm_sub_reliability << 2) + (read_only << 3) + (volatile_backup_failed << 4) + (persistent_mem_ro << 5)

    smart_json_data['critical_warning'] = critical_warning
    smart_json_data['temperature'] = 308 + randint(1, 40) - 15
    smart_json_data['avail_spare'] = (0.01 + randint(1, 100)) % 101
    smart_json_data['spare_thresh'] = (0.01 + randint(1, 100)) % 101
    smart_json_data['percent_used'] = (0.01 + randint(1, 100)) % 101
    smart_json_data['data_units_read'] += randint(1, 100000)
    smart_json_data['data_units_written'] += randint(1, 100000)
    smart_json_data['host_read_commands'] += randint(1, 1000)
    smart_json_data['host_write_commands'] += randint(1, 1000)
    smart_json_data['controller_busy_time'] += randint(1, 10)
    smart_json_data['power_cycles'] += randint(1, 10)
    smart_json_data['power_on_hours'] += randint(1, 10)
    smart_json_data['unsafe_shutdowns'] += randint(1, 10)
    smart_json_data['media_errors'] += randint(1, 10)
    smart_json_data['num_err_log_entries'] += randint(1, 10)
    smart_json_data['warning_temp_time'] += randint(1, 10)
    smart_json_data['critical_comp_time'] += randint(1, 10)
    smart_json_data['thm_temp1_trans_count'] += randint(1, 10)
    smart_json_data['thm_temp2_trans_count'] += randint(1, 10)
    smart_json_data['thm_temp1_total_time'] += randint(1, 10)
    smart_json_data['thm_temp2_total_time'] += randint(1, 10)

    return smart_json_data

def init_simulation_device_info(devno):

    device = get_nvme_device_info(devno)

    device['DevicePath'] = '/dev/nvme%d' % devno
    device['Firmware'] = 'fw%d.0' % devno
    device['Index'] = devno
    device['ModelNumber'] = 'NVME-HIGH-DC-ZBDX-%d' % devno
    device['ProductName'] = 'Non-Volatile Memory Controller'
    device['SerialNumber'] = 'ABC-EBC-HBD-FAC'
    device['UsedBytes'] = 102030030 * devno + 10890808
    device['MaximumLBA'] = 1000000000 + 10000 * devno
    device['PhysicalSize'] = 9939399394 + 93949 * devno
    device['SectorSize'] = 512

def gen_simulation_nvme_list():
    array = []
    for devno in range(0, NUM_NVME):
        device = get_nvme_device_info(devno)
        nvme_list['Devices'].insert(devno, device) 

    return nvme_list
