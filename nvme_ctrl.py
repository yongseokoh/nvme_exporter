import subprocess
import json
from random import *
import nvme_simulation as nv_simul

def get_ctrl_regs(device_path):
    if nv_simul.NVME_SIMULATION == 0:
        proc = subprocess.Popen("nvme show-regs %s -o json" %device_path,
                                shell=True,
                                stdout=subprocess.PIPE,
                                encoding='utf-8')
        err = proc.wait()

        (stdout, stderr) = proc.communicate()

        json_data = json.loads(stdout)
    else:
        json_data = nv_simul.gen_simulation_ctrl(int(device_path[9:]))

    return json_data
