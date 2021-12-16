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
    c = wmi.WMI()
    gpus_list = []
    for gpu in c.Win32_VideoController():
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