from glob import glob
from sys import argv
import pyautogui
import time
import win32gui
import win32con
import wmi
from os.path import basename, splitext

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
        pyautogui.keyDown('alt')
        pyautogui.keyDown('f4')
        # Wait 0.5 seconds
        time.sleep(0.5)
        # Release the alt+f4 keypress
        pyautogui.keyUp('f4')
        pyautogui.keyUp('alt')
        time.sleep(0.5)
    
def waitAndLocate(btn_img, params):
    """
    Function to locate a button in the window

    :param btn_img: path to the image of the button to look for
    :return: coordinates + dimensions of the button
    """ 
    while True:
         # Find window and maximize
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
        whnd = win32gui.FindWindow(None, name)
        win32gui.ShowWindow(whnd, win32con.SW_MAXIMIZE)

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
    first_click = True
    times = []
    init_time = time.time()
    # Get each image in the directory called with the Game name
    for action in sorted(glob(game + '/*.*'), key=intIndexSort):
        print('[INFO] Looking for ' + action)
        if (splitext(action)[1] == '.txt'):
            file = open(action, 'r')
            strings = file.readlines()
            keyboard_string = strings[iteration]
            pyautogui.write(keyboard_string, 0.05)
            file.close()
            continue
        btn_img = action
        # Locate the button using the image in the folder, wait until found
        res = waitAndLocate(btn_img, params)
        # Record the timestamp of when the button was found
        times.append(time.time() - init_time)
        # Get the center point of the button
        point = pyautogui.center(res)
        # If this is the first click, click twice to focus on the window
        if first_click:
            pyautogui.click(point[0], point[1])
            first_click = False
        # Move to the location of the button - duration of move defined in params['move_time']
        pyautogui.moveTo(point[0], point[1], params['move_time'] + 0.2, pyautogui.easeInOutQuad)
        # If image name contains ONECLICK click once, otherwise normal double click
        if 'ONECLICK' in btn_img: 
            pyautogui.click(point[0], point[1])
        else:
            pyautogui.doubleClick(point[0], point[1])
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
