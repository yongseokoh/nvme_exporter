import subprocess
import json
import nvme_simulation as nv_simul

def print_nvme_list(json_data):

	for device in json_data['Devices']:
		print('DevicePath %s' %device['DevicePath'])
		print('Firmware %s' %device['Firmware'])
		print('Index %s' %device['Index'])
		print('ModelNumber %s' %device['ModelNumber'])
		print('ProductName %s' %device['ProductName'])
		print('SerialNumber %s' %device['SerialNumber'])
		print('UsedBytes %s' %device['UsedBytes'])
		print('MaximumLBA %s' %device['MaximumLBA'])
		print('PhysicalSize %s' %device['PhysicalSize'])
		print('SectorSize %s' %device['SectorSize'])

def get_nvme_list():
    if nv_simul.NVME_SIMULATION == 0:

        proc = subprocess.Popen("nvme list %s -o json",
                                shell=True,
                                stdout=subprocess.PIPE,
                                encoding='utf-8')
        err = proc.wait()

        (stdout, stderr) = proc.communicate()

        json_data = json.loads(stdout)

    else:
        json_data = nv_simul.gen_simulation_nvme_list()


	#print(type(json_data))
	#print(json_data)

    print_nvme_list(json_data)

    return json_data

if __name__ == '__main__':
	nvme_list_json = get_nvme_list("/dev/nvme0")
	print(nvme_list_json)
