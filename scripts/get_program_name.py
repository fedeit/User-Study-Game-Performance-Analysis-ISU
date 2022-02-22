import win32gui
import win32con
import win32api
import win32process as wproc

def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        print (hex(hwnd), win32gui.GetWindowText( hwnd ))

win32gui.EnumWindows( winEnumHandler, None )

def maximizeWindows(name): 
    try:
        whnd = win32gui.FindWindow(None, name)
        win32gui.ShowWindow(whnd, win32con.SW_MAXIMIZE)
        remote_thread, _ = wproc.GetWindowThreadProcessId(whnd)
        wproc.AttachThreadInput(win32api.GetCurrentThreadId(), remote_thread, True)
        win32gui.SetFocus(whnd)
    except:
        return

maximizeWindows('Rainbow Six')