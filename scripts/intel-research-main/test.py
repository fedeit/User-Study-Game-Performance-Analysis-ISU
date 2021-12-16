# import wmi
# ti = 0
# name = 'League'
# f = wmi.WMI()
# for process in f.Win32_Process():
#     if name in process.name:
#         process.Terminate()
#         ti += 1

# if ti == 0:
#     print("Process not found!!!")


import pandas as pd
import datetime
import win32gui
import win32con
#df = pd.DataFrame(columns=['init_time', 'total_time', 'times'])
#df.to_csv('./metrics_' + datetime.datetime.utcnow().strftime("%m-%d-%y_%H-%M-%S") + '.csv')

import wmi
c = wmi.WMI()
for gpu in c.Win32_VideoController():
    print(gpu)