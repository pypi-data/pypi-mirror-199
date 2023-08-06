import os
import sys
import psutil
import json
import argparse
from cpuinfo import get_cpu_info

KEY_CLOCK_SPEED = "hz_advertised"
KEY_CLOCK_SPEED_ACTUAL = "hz_actual"

def get_diskinfo():
    disks = psutil.disk_partitions(all=False)

    results = []
    for disk in disks:
        usage = psutil.disk_usage(disk.mountpoint)
        disk_res = {
                        "device": disk.device,
                        "mount_point": disk.mountpoint,
                        "size": usage.total,
                        "used": usage.used,
                        "free": usage.free,
                        "percent_used": usage.percent
        }
        results.append(disk_res)

    return results

def get_clock_speed(key: str, cpu_info):
    """Gets the clock speeds from the CPU Info object. For some reason on ARM platforms this isn't
    available and so needs to be accounted for"""
    
    if key not in cpu_info:
        return 0
    
    return cpu_info[key][0]


def get_sysinfo() -> dict:
    cpu_count = os.cpu_count()
    cpu_info = get_cpu_info()
    core_count = psutil.cpu_count(logical=False)  # This will get the number of physical CPUs regardless of whehter HT/ SMT is enabled or not
    smt_on = cpu_count > core_count
    mem = psutil.virtual_memory()
    cpu_f = psutil.cpu_freq(percpu=False)
    cpu_freq = get_clock_speed(KEY_CLOCK_SPEED, cpu_info)
    cpu_freq_act = get_clock_speed(KEY_CLOCK_SPEED_ACTUAL, cpu_info)
    cpu_freq_min = 0
    cpu_freq_max = 0
    if hasattr(cpu_f, "min"):
        cpu_freq_min = cpu_f.min

    if hasattr(cpu_f, "max"):
        cpu_freq_max = cpu_f.max

    disks = get_diskinfo()


    results = {
        "arch": cpu_info.get("arch", "unknown"),
        "smt_on": smt_on,
        "core_count": core_count,
        "cpu_count": cpu_count,
        "cpu_vendor":  cpu_info.get("vendor_id_raw", "unknown"),
        "cpu_model": cpu_info.get("brand_raw", "unknown"),
        "cpu_frequency": cpu_freq,
        "cpu_frequency_actual": cpu_freq_act,
        "cpu_freq_min": cpu_freq_min,
        "cpu_freq_max": cpu_freq_max,
        "installed_memory":  mem.total,
        "l3_cache_size": cpu_info.get("l3_cache_size", 0),
        "l2_cache_size": cpu_info.get("l2_cache_size", 0),
        "l1_data_cache_size": cpu_info.get("l1_data_cache_size", 0),
        "l1_instruction_cache_size": cpu_info.get("l1_instruction_cache_size", 0),
        "l2_cache_line_size": cpu_info.get("l2_cache_line_size", 0),
        "l2_cache_associativity": cpu_info.get("l2_cache_associativity", 0),
        "cpu_flags": cpu_info.get("flags", []),
        "disks": disks
    }

    return results



def main():
    argparser = argparse.ArgumentParser(description="HPC Mark Benchmarking and Pricing Tool",
                                        epilog="(C) HMx Labs Limited 2023. All Rights Reserved.")
    argparser.add_argument('--file', dest="file", required=False, action="store_true", default=False,
                            help="Specify if the output should be written to file")
    argparser.add_argument('--stdout', dest="stdout", required=False, action="store_true", default=True,
                            help="Specify if the output should be written to file")
    argparser.add_argument('--filename', dest="filename", required=False, default="sysinfo.json",
                            help="Specify if the output should be written to file")
                            
    args = None
    out_file = False
    out_stdouf = True
    filename = "sysinfo.json"
    try:
        args = argparser.parse_args()
        out_file = args.file
        out_stdouf = args.stdout
        filename = args.filename
    except Exception:
        argparser.print_help()
        sys.exit(1)

    try:
        results = get_sysinfo()

        if out_stdouf:
            print(json.dumps(results, indent=4))

        if out_file:
            with open(filename, 'w') as res_file:
                res_file.write(json.dumps(results))

    except Exception as exp:
        print(f"Error obtaining System information {exp}", file=sys.stderr)


if __name__ == "__main__":
    main()