import psutil

def get_hardware_info():

    hardware_info = {}

    hardware_info['cpu_cores'] = psutil.cpu_count(logical=False)

    hardware_info['ram_info'] = round(psutil.virtual_memory().total/(1024 ** 3),2)

    partitions = psutil.disk_partitions(all=True) 
    hardware_info['partition'] = {}
    for partition in partitions:
        partition_name = psutil.disk_usage(partition.mountpoint)
        hardware_info['partition'][partition.device] = round(partition_name.total / (1024 ** 3),2)

    return hardware_info

print(get_hardware_info())