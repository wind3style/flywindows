from pynput import keyboard
import pygetwindow as gw
import subprocess
import ctypes   
import logging
import sys
import getopt

pressed = set()

hotkeys = [
            {'pressed_keys': [keyboard.Key.alt_l], 'press_key': keyboard.KeyCode.from_char('1'),
            'action': 'moveTo',
            'relative_x0': 0,
            'relative_y0': 0,
            'relative_width': 1/4,
            'relative_height': 1/4
            },
            {'pressed_keys': [keyboard.Key.alt_l], 'press_key': keyboard.KeyCode.from_char('2'),
            'action': 'moveTo',
            'relative_x0': 1/4,
            'relative_y0': 0,
            'relative_width': 1/4,
            'relative_height': 1/4
            },            
            {'pressed_keys': [keyboard.Key.alt_l], 'press_key': keyboard.KeyCode.from_char('3'),
            'action': 'moveTo',
            'relative_x0': 2/4,
            'relative_y0': 0,
            'relative_width': 1/4,
            'relative_height': 1/4
            },            
            {'pressed_keys': [keyboard.Key.alt_l], 'press_key': keyboard.KeyCode.from_char('4'),
            'action': 'moveTo',
            'relative_x0': 3/4,
            'relative_y0': 0,
            'relative_width': 1/4,
            'relative_height': 1/4
            },            
            {'pressed_keys': [keyboard.Key.alt_l], 'press_key': keyboard.KeyCode.from_char('`'),
            'action': 'moveTo',
            'relative_x0': 0,
            'relative_y0': 25/100,
            'relative_width': 1/4,
            'relative_height': 72/100
            },            
            {'pressed_keys': [keyboard.Key.alt_l], 'press_key': keyboard.KeyCode.from_char('q'),
            'action': 'moveTo',
            'relative_x0': 1/6,
            'relative_y0': 25/100,
            'relative_width': 4/6,
            'relative_height': 72/100
            },            
            ]

def run(s):
    subprocess.Popen(s)

def on_press(key):
    logging.debug("Press: %s, type: %s"%(str(key), type(key)))
    pressed.add(key)
    
    logging.debug("Pressed: %s"%pressed)
    
    for hkey in hotkeys:
        if check_if_pressed(hkey) and key == hkey['press_key']:
            logging.debug("HotKey triggered")
            user32 = ctypes.windll.user32
            screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
            print("Screen size: %dx%d"%(screensize))
            win = gw.getActiveWindow()
            if win != None:
                if hkey['action'] == 'moveTo':
                    win.moveTo(int(screensize[0]*hkey['relative_x0']), int(screensize[1]*hkey['relative_y0']))
                    win.resizeTo(int(screensize[0]*hkey['relative_width']), int(screensize[1]*hkey['relative_height']))
                
    if check_if_pressed({'pressed_keys': [keyboard.KeyCode.from_char('q'), keyboard.KeyCode.from_char('w'), keyboard.KeyCode.from_char('e')]}):
        logging.info("Quit")
        exit(0)        

def on_release(key):
    logging.debug("Release: %s"%str(key))
    if key in pressed:
        pressed.remove(key)

def check_if_pressed(hkey):
    for key_check in hkey['pressed_keys']:
        if key_check not in pressed:
            return False
    return True
            
def main(argv_all):
    
#    debug_level = "INFO"
    debug_level = "DEBUG"
    
    try:
        argv = argv_all[1:]
        opts, args = getopt.getopt(argv, 'd', ['debug'])
    except getopt.GetoptError:
        logging.debug("Incorrect arguments")
        usage_help(argv_all[0]);
        sys.exit(2)

    for opt, arg in opts:
        print("opt: %s"%opt)
        if opt in ['-d', '--debug']:
            debug_level="DEBUG"    
        
    logging.basicConfig(level=debug_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    logging.info("FlyWindows - Windows position hotkey manager. Writen by Fedorov Alexander <wind3style@gmail.com>")
    
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    
if __name__ == "__main__":
    main(sys.argv)