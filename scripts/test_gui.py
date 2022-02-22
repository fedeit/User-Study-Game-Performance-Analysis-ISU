from glob import glob
from sys import argv
import pyautogui
import pydirectinput as mdev, pydirectinput
import time
import win32gui
import win32con
import win32api
import win32process as wproc
import wmi
import hardware as hw
from os.path import basename, splitext, isdir

def killWindow(params):
    """
    Function to close the window at the end of a test iteration

    :param params: game specific object containing a 'kill_mode' and optional a 'process_name'
    :return: None
    """ 
    # Check kill_mode (win32gui, os, keyboard)
    if params['kill_mode'] == 'win32gui':
        # Close the window using the win32gui WM_CLOSE function
        win32gui.PostMessage(win32gui.GetForegroundWindow(), win32con.WM_CLOSE, 0, 0)
    elif params['kill_mode'] == 'os':
        # Get all running process
        ti = 0
        f = wmi.WMI()
        processes = f.Win32_Process()
        # Get each process name to kill
        for target in params['process_name']:
            # Check if any running process contains the target name
            for process in processes:
                if target in process.name:
                    # If need to kill the process, try to terminate
                    try:
                        process.Terminate()
                    except:
                        # Sometimes the process is already killed
                        # because closing the game will close the launcher
                        print("Process already killed")
                    ti += 1
    elif params['kill_mode'] == 'keyboard':
        # Press alt+f4
        pydirectinput.keyDown('alt')
        pydirectinput.keyDown('f4')

        #hardware.keyDown(130)
        #hardware.keyDown(197)

        # Wait 0.5 seconds
        time.sleep(0.5)
        # Release the alt+f4 keypress
        pydirectinput.keyUp('f4')
        pydirectinput.keyUp('alt')

        #hardware.keyDown(197)
        #hardware.keyDown(130)

        time.sleep(0.5)
    
def waitAndLocate(btn_img, params):
    """
    Function to locate a button in the window

    :param btn_img: path to the image of the button to look for
    :return: coordinates + dimensions of the button
    """ 
    start = time.time()
    while True:
        if time.time() - start > (5*60):
            print("Timeout Error")
            raise TimeoutError(f"wait and locate exceeded {str(time.time()-start)}")
 
         # Find window and maximize
        if 'no_fullscreen' not in params or params['no_fullscreen'] == False:
            maximizeWindows(params)
        # Make foreground window full screen - replaced with exact window name lookup
        # win32gui.ShowWindow(win32gui.GetForegroundWindow(), win32con.SW_MAXIMIZE)
        # Look for the button on the screen
        res = pyautogui.locateOnScreen(btn_img, confidence=0.75)
        # If button is found, return the location
        if (res):
            return res
        # Wait 0.5 seconds before retrying to keep CPU usage low
        time.sleep(0.5)

def maximizeWindows(params): 
    for name in params['window_names']:
        try:
            whnd = win32gui.FindWindow(None, name)
            win32gui.ShowWindow(whnd, win32con.SW_MAXIMIZE)
            # remote_thread, _ = wproc.GetWindowThreadProcessId(whnd)
            # wproc.AttachThreadInput(win32api.GetCurrentThreadId(), remote_thread, True)
            # win32gui.SetFocus(whnd)
        except:
            print('Could not focus window')
            return

def intIndexSort(a):
    filename = splitext(basename(a))[0]
    return float(filename.split('_')[0])

def test(game, params, iteration):
    """
    Function to test the game load time and the level load time for any game.

    :param game: path to the image of the button to look for
    :param params: game specific object containing a 'kill_mode' and optional a 'process_name'
    :return: metrics for the specific game
    """ 
    times = []
    init_time = time.time()
    if (not isdir(game)):
        raise NameError("Game folder does not exist!")
    # Get each image in the directory called with the Game name
    for action in sorted(glob(game + '/*.*'), key=intIndexSort):
        time.sleep(1.5)
        print('[INFO] Looking for ' + action)
        filetype = splitext(action)[1]
        if (filetype == '.txt'):
            file = open(action, 'r')
            strings = file.readlines()
            keyboard_string = strings[iteration]
            pydirectinput.write(keyboard_string, 0.05)
            file.close()
            continue
        elif filetype == '.action':
            file = open(action, 'r')
            strings = file.read().splitlines()
            for key in strings:
                print(f'[INFO]...waiting 1 sec and pressing {key}')
                time.sleep(1)
                pydirectinput.press(key)
            # Record the timestamp of when the button was found
            times.append(time.time() - init_time)
            continue
        elif filetype == '.wait':
            file = open(action, 'r')
            strings = file.readlines()
            time.sleep(int(strings[0]))
            # Record the timestamp of when the button was found
            times.append(time.time() - init_time)
            continue
        # If not text, it's an image
        btn_img = action
        # Locate the button using the image in the folder, wait until found
        res = waitAndLocate(btn_img, params)
        # Record the timestamp of when the button was found
        times.append(time.time() - init_time)
        # Get the center point of the button
        point = pyautogui.center(res)
        mdev.moveTo(point[0], point[1])
        # If NO_CLICK option, skip click sequence
        if 'NO_CLICK' in btn_img:
            continue
        # If image name contains ONECLICK click once, otherwise normal double click
        if 'ONECLICK' in btn_img: 
            print('...one click')
            hw.click(point[0], point[1])
        elif 'MULTI' in btn_img:
            for _ in range(10):
                hw.doubleClick(point[0], point[1])
        else:
            print('...double click')
            hw.doubleClick(point[0], point[1])
            hw.doubleClick(point[0], point[1])
    # Compute total run time
    total_time = time.time() - init_time
    # Close the window once finished 
    killWindow(params)
    # Compute and return metrics
    metrics =  {
        'init_time': init_time,
        'total_time' : total_time,
        'times': times
    }
    return metrics

if '__main__' == __name__:
    test(argv[1])
