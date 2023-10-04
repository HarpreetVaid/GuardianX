import psutil

def get_live_info():
    live_info = {}
    live_info['cpu_info'] = {}

    live_info['cpu_info']['cpu_freq'] = psutil.cpu_freq().current / 1e3
    live_info['cpu_info']['cpu_usage'] = psutil.cpu_percent(interval=1)

    live_info['used_ram'] = round(psutil.virtual_memory().used / (1024 ** 3), 2)
    partitions = psutil.disk_partitions(all=True)
    live_info['partition'] = {}
    for partition in partitions:
        partition_name = psutil.disk_usage(partition.mountpoint)
        live_info['partition'][partition.device] = round(partition_name.used / (1024 ** 3), 2)

    return live_info

live_info_data = get_live_info()  # Corrected variable name

print(live_info_data)
