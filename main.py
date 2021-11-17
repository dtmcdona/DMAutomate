import kivy
import time
import dm_macro
import os
import keyboard
import pyautogui
from importlib import reload
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

kivy.require('1.9.0')

class MyRoot(BoxLayout):

    def __init__(self):
        super(MyRoot, self).__init__()

    def record_macro(self):

        self.status.text = "Recording..."
        pyautogui.FAILSAFE = False
        newMacroFile = open("dm_macro.py", "w")
        time.sleep(.5)
        # Setup initial file
        newMacroFile.write("import time\nimport pyautogui\n\n")
        newMacroFile.write("def macro_func():\n")
        # Current indent will be used to format python file
        currentIndent = "\t"
        newMacroFile.write(currentIndent+"pyautogui.FAILSAFE = False\n")
        # Record all actions from the user
        previousMouseX = 0
        previousMouseY = 0
        # Get mouse position
        currentMouseX, currentMouseY = pyautogui.position()
        newMacroFile.write(currentIndent+"pyautogui.moveTo(" + str(currentMouseX) + ", " + str(currentMouseY) + ")\n")
        newMacroFile.write(currentIndent+"time.sleep(.5)\n")
        time.sleep(.5)
        running = True
        # Counter will exit the loop after 2.5 seconds
        counter = 10
        while running is True:
            # Get mouse position
            currentMouseX, currentMouseY = pyautogui.position()
            if previousMouseX != currentMouseX and previousMouseY != currentMouseY:
                newMacroFile.write(currentIndent+"pyautogui.moveTo("+str(currentMouseX)+", "+str(currentMouseY)+")\n")

            # Set previous mouse position
            previousMouseX = currentMouseX
            previousMouseY = currentMouseY
            newMacroFile.write(currentIndent+"time.sleep(.5)\n")
            time.sleep(.5)
            counter -= 1
            if counter < 1:
                running = False

        newMacroFile.write(currentIndent+"print('Done playing')")
        newMacroFile.close()
        self.status.text = "-"
        print('Done recording')

    def play_macro(self):
        self.status.text = "Playing"
        # Reload the dm_macro.py script since it probably has been updated
        reload(dm_macro)
        dm_macro.macro_func()
        time.sleep(1)
        self.status.text = "-"

    def load_macro(self):
        # Possibily load/save macros under different names in file system
        self.status.text = "Loading"

class DMAutomate(App):

    def build(self):
        return MyRoot()

dmAutomate = DMAutomate()
dmAutomate.run()