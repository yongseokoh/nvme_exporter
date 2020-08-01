# nvme_exporter for Prometheus
:cyclone: **nvme_exporter** provides useful metrics of NVMe SSDs (e.g., lifetime, device status, and read/write operations that are described in NVME specifications [https://nvmexpress.org/](https://nvmexpress.org/)).  The information is obtained from NVMe Admin Commands using the NVMe CLI tool.  

nvme_exporter is written based on the python prometheus client ([https://github.com/prometheus/client_python](https://github.com/prometheus/client_python)) and the NVMe CLI tool ([https://github.com/linux-nvme/nvme-cli](https://github.com/linux-nvme/nvme-cli)).

## Dependencies
- `python3.6`
- `nvme-cli` 
- `python prometheous-client`

## Installation 
```
git clone git@github.com:yongseokoh/nvme_exporter.git
cd nvme_exporter

# Install prometheus-client
pip install requirements.txt

# Install nvme-cli tool
git submodule init
git submodule update
cd nvme-cli
make
make install
```

### Usage
```
usage: nvme_exporter.py [-h] [-p PORT] [-u UPDATE] [-s SIMULATION]

NVME Export port number and update period time

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Port to listen
  -u UPDATE, --update UPDATE
                        export mertic update period in seconds
  -s SIMULATION, --simulation SIMULATION
                        making use of NVMe simulation
```

### Example
```
sudo python nvme_exporter.py -p 9243 -u 10
```

## Grafana Sample
<img src="https://github.com/yongseokoh/nvme_exporter/blob/dev-0.1/sample/grafana_nvme_export.png?raw=true" target="_blank" width="800">

## NVMe Health & Monitoring Metrics

**Command**: `nvme smart-log /dev/nvme0 -o json`

| Name                                               | type     | impl. state |
| -------------------------------------------------- | -------- | ------------|
| critical_warning                                   | Gauge    | implemented |
| temperature                                        | Gauge    | implemented |
| avail_sapre                                        | Gauge    | implemented |
| spare_thresh                                       | Gauge    | implemented |
| percent_used                                       | Gauge    | implemented |
| data_units_read                                    | Gauge    | implemented |
| data_units_written                                 | Gauge    | implemented |
| host_read_commands                                 | Gauge    | implemented |
| host_write_commands                                | Gauge    | implemented |
| controller_busy_time                               | Gauge    | implemented |
| power_cycles                                       | Gauge    | implemented |
| power_on_hours                                     | Gauge    | implemented |
| unsafe_shutdowns                                   | Gauge    | implemented |
| media_errors                                       | Gauge    | implemented |
| num_err_log_entries                                | Gauge    | implemented |
| warning_temp_time                                  | Gauge    | implemented |
| critical_comp_time                                 | Gauge    | implemented |
| thm_temp1_trans_count                              | Gauge    | implemented |
| tmp_temp2_trans_count                              | Gauge    | implemented |

**Command**: `nvme show-regs /dev/nvme0 -o json`

| Name                                               | type     | impl. state |
| -------------------------------------------------- | -------- | ------------|
| controller configuration                           | Gauge    | implemented |
| controller status                                  | Gauge    | implemented |
| other metrics                                      | Gauge    | pending     |
