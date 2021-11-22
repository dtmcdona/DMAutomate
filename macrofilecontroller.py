import time
import pyautogui
import dm_macro
import shutil
import os
from pynput import keyboard
from pynput import mouse
from importlib import reload

class MacroFileController:
    def __init__(self):
        # The current file will always be named "dm_macro.py" and
        # users will be able to save/load under other names
        self.filename = "dm_macro.py"
        # Variable that conveys if the recorder is running
        self.running = False
        # Current indent is used to create new file structure
        self.currentIndent = ""
        # Possibly use status in future to make sure there is no overlapping of events
        self.status = "-"
        # PreviousMouse X and Y are used to limit number of writes to new file
        self.prevMouseX = 0
        self.prevMouseY = 0
        self.currentMouseX = 0
        self.currentMouseY = 0
        # Possibly use last key press for hotkeys/combos in future
        self.lastKeyPress = ""
        self.lastKeyRelease = ""

    def on_move(self, x, y):
        # Get mouse position
        self.currentMouseX, self.currentMouseY = pyautogui.position()
        mousedistance = ((self.currentMouseX-self.prevMouseX)+(self.currentMouseY-self.prevMouseY))
        # Check to see mouse has moved far enough
        if mousedistance > 10:
            macrofile = open(self.filename, "a")
            macrofile.write(self.currentIndent + "pyautogui.moveTo(" + str(self.currentMouseX) + ", " + str(self.currentMouseY) + ")\n")
            macrofile.close()
            self.prevMouseX = self.currentMouseX
            self.prevMouseY = self.currentMouseY
            print('Pointer moved to {0}'.format(
                (x, y)))

    def on_click(self, x, y, button, pressed):
        if pressed:
            # Get mouse position
            self.currentMouseX, self.currentMouseY = pyautogui.position()
            macroFile = open(self.filename, "a")
            macroFile.write(self.currentIndent + "pyautogui.click(" + str(self.currentMouseX) + ", " + str(self.currentMouseY) + ")\n")
            macroFile.close()
        print('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
        if not pressed:
            # Stop listener
            return False

    def on_scroll(self, x, y, dx, dy):
        print('Mouse scrolled {0} at {1}'.format(
            'down' if dy < 0 else 'up',
            (x, y)))

    def on_press(self, key):
        try:
            print('Letter key {0} pressed'.format(key.char))
            macrofile = open(self.filename, "a")
            macrofile.write(self.currentIndent + "keyboard.press({0})\n".format(key))
            macrofile.close()
        except AttributeError:
            print('Unique key {0} pressed'.format(
                key))

    def on_release(self, key):
        print('{0} released'.format(key))
        macrofile = open(self.filename, "a")
        macrofile.write(self.currentIndent + "keyboard.release({0})\n".format(key))
        macrofile.close()
        if key == keyboard.Key.esc:
            self.running = False
            # Stop listener
            return False

    def create_macro(self):
        print("Recording...")
        pyautogui.FAILSAFE = False
        newMacroFile = open(self.filename, "w")
        time.sleep(.5)
        # Setup initial file
        newMacroFile.write("import time\nimport pyautogui\n")
        newMacroFile.write("from pynput.keyboard import Key, Controller\n\n")
        newMacroFile.write("def macro_func():\n\tkeyboard = Controller()\n")
        self.currentIndent = "\t"
        newMacroFile.write(self.currentIndent + "# pyautogui.FAILSAFE = False\n")
        newMacroFile.close()

    def play_macro(self):
        print("Playing")
        # Reload the macro script since it probably has been updated
        reload(dm_macro)
        dm_macro.macro_func()
        time.sleep(1)

    def save_macro(self, filename):
        print("Saving...")
        filepath = os.path.dirname(os.path.abspath(__file__))+'\\'
        src = r''+filepath+'dm_macro.py'
        dst = r''+filepath+filename
        shutil.copyfile(src, dst)
        print("Saved macro as: "+filename)

    def load_macro(self, filename):
        print("Loading...")
        filepath = os.path.dirname(os.path.abspath(__file__)) + '\\'
        src = r'' + filepath + filename
        dst = r'' + filepath + 'dm_macro.py'
        shutil.copyfile(src, dst)
        print("Loaded macro: " + filename)

    def activate_listeners(self):
        # Listeners are responsible for mouse/keyboard input
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        listener.start()

        listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)
        listener.start()


recorder = MacroFileController()
recorder.create_macro()
recorder.activate_listeners()
# recorder.play_macro()
recorder.running = True

filepath = os.path.dirname(os.path.abspath(__file__))+'\\'
src = r''+filepath+'main.py'
dst = r''+filepath+'macrofilecontroller.py'
shutil.copyfile(src, dst)

while recorder.running:
    time.sleep(1)
print("Done!")