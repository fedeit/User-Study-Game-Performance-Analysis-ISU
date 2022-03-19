import wmi
from cpuinfo import get_cpu_info
import json

def getDrives():
    c = wmi.WMI()
    drives = []
    for drive in c.Win32_DiskDrive():
        info = {
            'interface': drive.InterfaceType.strip(),
            'description': drive.Description.strip(),
            'mediatype': drive.MediaType.strip(),
            'model': drive.Model.strip(),
            'serial': drive.SerialNumber.strip()
        }
        drives.append(info)
    return drives

def getGPUs():
    gpus_list = []
    c = wmi.WMI()
    for gpu in c.Win32_VideoController():
        if ('Intel Corporation' == gpu.AdapterCompatibility):
            continue
        name = gpu.Caption
        id = gpu.DeviceID
        uuid = gpu.PNPDeviceID
        info = {
            'name': name,
            'id': id,
            'uuid': uuid
        }
        gpus_list.append(info)
    return gpus_list

def getCPUInfo():
    return get_cpu_info()


def getHardwareInfo():
    info = {
        'drives': getDrives(),
        'GPUs': getGPUs(),
        'CPU': getCPUInfo()
    }
    return info

if __name__ == '__main__':
    info = getHardwareInfo()
    print(info)
    with open('./hw_conf.json', 'w+') as f:
        json.dump(info, f)