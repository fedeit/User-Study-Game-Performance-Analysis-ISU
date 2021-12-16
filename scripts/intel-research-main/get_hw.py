import GPUtil
import platform
import win32api
import wmi

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
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        name = gpu.name
        id = gpu.id
        uuid = gpu.uuid
        info = {
            'name': name,
            'id': id,
            'uuid': uuid
        }
        gpus_list.append(info)
    return gpus_list

def getCPUInfo():
    hw = platform.uname()
    config = {
        'platform': hw,
        'cpu': platform.processor()
    }
    return config


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