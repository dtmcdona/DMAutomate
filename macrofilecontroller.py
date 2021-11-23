import time
import random
import pyautogui
import dm_macro
import shutil
import os
from sys import platform
from pynput import keyboard
from pynput import mouse
from pynput.mouse import Button as mouseButton
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
        # Used to calc delta time
        self.lastTimestamp = round(time.perf_counter(), 3)
        self.deltaTime = 0
        # Randomize for less detection but less efficiency
        random.seed()
        self.randomEnabled = False
        self.randomTime = (random.randrange(0, 1000, 1))/1000
        # Check which os
        if platform == "linux" or platform == "linux2":
            self.currentdir = os.path.dirname(os.path.abspath(__file__)) + '/'
        elif platform == "win32":
            self.currentdir = os.path.dirname(os.path.abspath(__file__)) + '\\'

    def on_move(self, x, y):
        # Get mouse position
        self.currentMouseX, self.currentMouseY = pyautogui.position()
        mousedistance = ((self.currentMouseX-self.prevMouseX)+(self.currentMouseY-self.prevMouseY))
        # Check to see mouse has moved far enough
        if mousedistance > 10:
            macroFile = open(self.filename, "a")
            # Calc delta time to save to macro
            self.delta_time()
            if self.deltaTime > 0.0001:
                macroFile.write(self.currentIndent + "pyautogui.moveTo(" + str(self.currentMouseX) + ", " + str(self.currentMouseY) + ", duration="+str(self.deltaTime)+")\n")
            else:
                macroFile.write(self.currentIndent + "pyautogui.moveTo(" + str(self.currentMouseX) + ", " + str(
                    self.currentMouseY) + ")\n")
            macroFile.close()
            self.prevMouseX = self.currentMouseX
            self.prevMouseY = self.currentMouseY
            print('Mouse moved to {0}'.format((x, y)))

    def on_click(self, x, y, button, pressed):
        if pressed:
            # Get mouse position
            self.currentMouseX, self.currentMouseY = pyautogui.position()
            macroFile = open(self.filename, "a")
            # Calc delta time to save to macro
            self.delta_time()
            if self.deltaTime > 0.01:
                macroFile.write(self.currentIndent + "time.sleep({0})\n".format(self.deltaTime))
            if button == mouseButton.left:
                macroFile.write(self.currentIndent + "pyautogui.click(" + str(self.currentMouseX) + ", " + str(self.currentMouseY) + ", button='left')\n")
                macroFile.close()
            if button == mouseButton.right:
                macroFile.write(self.currentIndent + "pyautogui.click(" + str(self.currentMouseX) + ", " + str(self.currentMouseY) + ", button='right')\n")
                macroFile.close()
        print('Mouse '+str(button)+' {0} at {1}'.format('pressed' if pressed else 'released', (x, y)))
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
            macroFile = open(self.filename, "a")
            # Calc delta time to save to macro
            self.delta_time()
            if self.deltaTime > 0.01:
                macroFile.write(self.currentIndent + "time.sleep({0})\n".format(self.deltaTime))
            macroFile.write(self.currentIndent + "keyboard.press({0})\n".format(key))
            macroFile.close()
        except AttributeError:
            print('Unique key {0} pressed'.format(
                key))

    def on_release(self, key):
        print('{0} released'.format(key))
        macroFile = open(self.filename, "a")
        # Calc delta time to save to macro
        self.delta_time()
        if self.deltaTime > 0.01:
            macroFile.write(self.currentIndent + "time.sleep({0})\n".format(self.deltaTime))
        macroFile.write(self.currentIndent + "keyboard.release({0})\n".format(key))
        macroFile.close()
        if key == keyboard.Key.esc:
            self.running = False
            # Stop listener
            return False

    def delta_time(self):
        # Calc delta time to save to macro
        self.deltaTime = round((time.perf_counter()-self.lastTimestamp), 1)
        self.lastTimestamp = round(time.perf_counter(), 3)
        if self.randomEnabled:
            self.randomTime = (random.randrange(0, 1000, 1)) / 1000
            self.deltaTime += self.randomTime
            self.lastTimestamp += self.randomTime
        print(self.deltaTime)

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
        # Reset deltatime
        self.delta_time()

    def play_macro(self):
        print("Playing")
        # Reload the macro script since it probably has been updated
        reload(dm_macro)
        dm_macro.macro_func()
        time.sleep(1)

    def save_macro(self, filename):
        print("Saving...")
        src = r''+self.currentdir+'dm_macro.py'
        dst = r''+self.currentdir+filename
        shutil.copyfile(src, dst)
        print("Saved macro as: "+filename)

    def load_macro(self, filename):
        print("Loading...")
        src = r'' + self.currentdir + filename
        dst = r'' + self.currentdir + 'dm_macro.py'
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
#recorder.create_macro()
#recorder.activate_listeners()
recorder.save_macro("dm_macro2.py")
# recorder.play_macro()
recorder.running = True

# src = r''+self.currentdir+'main.py'
# dst = r''+self.currentdir+'macrofilecontroller.py'
# shutil.copyfile(src, dst)

counter = 0
while recorder.running:
    counter += 1
print("Done!")