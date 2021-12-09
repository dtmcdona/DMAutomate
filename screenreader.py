import time

import pyautogui
import cv2
import numpy as np
import os
import random
from pynput import keyboard
from pynput import mouse
from pynput.mouse import Button as mouseButton
from sys import platform

class Reader:
    def __init__(self):
        self.status = "idle"
        self.running = False
        self.listeners = False
        self.start_button = '`'
        self.object_on_mouse = 'Test'
        if platform == "linux" or platform == "linux2":
            self.imagedir = os.path.dirname(os.path.abspath(__file__)) + '/images'
        elif platform == "win32":
            self.imagedir = os.path.dirname(os.path.abspath(__file__)) + '\\images\\'
        self.object_directory = ''
        self.currentMouseX, self.currentMouseY = pyautogui.position()
        self.prevMouseX = 0
        self.prevMouseY = 0
        self.crop_size = 32
        self.image_index = 0
        self.lastTimestamp = round(time.perf_counter(), 3)
        self.deltaTime = round((time.perf_counter() - self.lastTimestamp), 1)

    def image_search(self, needle_filename, haystack_filename):
        needle = cv2.imread(self.imagedir+needle_filename, cv2.IMREAD_UNCHANGED)
        grayscale_needle = cv2.cvtColor(needle, cv2.COLOR_BGR2GRAY)
        haystack = cv2.imread(self.imagedir+haystack_filename, cv2.IMREAD_UNCHANGED)
        grayscale_haystack = cv2.cvtColor(haystack, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(grayscale_haystack, grayscale_needle, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # Max location has the best match with max_val to be % accuracy
        width = needle.shape[1]
        height = needle.shape[0]
        bottom_right = (max_loc[0] + width, max_loc[1] + height)
        # Threshold is the % accuracy compared to original needle
        threshold = .80
        yloc, xloc = np.where(result >= threshold)
        # Keep track of all matches and identify unique cases
        matches = []
        if len(xloc) > 0:
            print("There are {0} total matches in the haystack.".format(len(xloc)))
            for (x, y) in zip(xloc, yloc):
                # Twice to ensure singles are kept after picking unique cases
                matches.append([int(x), int(y), int(width), int(height)])
                matches.append([int(x), int(y), int(width), int(height)])
            # Grouping function
            matches, weights = cv2.groupRectangles(matches, 1, 0.2)
            print("There are {0} unique matches in the haystack.".format(len(matches)))
            # Display image with rectangle
            for (x, y, width, height) in matches:
                cv2.rectangle(haystack, (x, y), (x + width, y + height), (255, 255, 0), 2)
            # cv2.imshow('Haystack', haystack)
            # cv2.waitKey()
            # cv2.destroyAllWindows()
        else:
            print("There are no matches.")
        return matches

    def object_search(self, object_name, haystack_filename):
        self.object_directory = os.path.join(self.imagedir, object_name)
        # Keep track of all matches and identify unique cases
        objects = []
        if os.path.exists(self.object_directory):
            files = os.listdir(self.object_directory)
            # Threshold is the % accuracy compared to original needle
            threshold = .95
            self.image_index = 1
            haystack = cv2.imread(self.imagedir + haystack_filename, cv2.IMREAD_UNCHANGED)
            grayscale_haystack = cv2.cvtColor(haystack, cv2.COLOR_BGR2GRAY)
            for f in files:
                if '.png' in f:
                    matches = []
                    image_path = os.path.join(self.object_directory, object_name+str(self.image_index)+'.png')
                    needle = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
                    grayscale_needle = cv2.cvtColor(needle, cv2.COLOR_BGR2GRAY)
                    result = cv2.matchTemplate(grayscale_haystack, grayscale_needle, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                    # Max location has the best match with max_val to be % accuracy
                    width = needle.shape[1]
                    height = needle.shape[0]
                    bottom_right = (max_loc[0] + width, max_loc[1] + height)
                    yloc, xloc = np.where(result >= threshold)
                    if len(xloc) > 0:
                        print("There are {0} total matches in the haystack.".format(len(xloc)))
                        for (x, y) in zip(xloc, yloc):
                            # Twice to ensure singles are kept after picking unique cases
                            matches.append([int(x), int(y), int(width), int(height)])
                            matches.append([int(x), int(y), int(width), int(height)])
                        # Grouping function
                        matches, weights = cv2.groupRectangles(matches, 1, 0.2)
                        print("There are {0} unique matches in the haystack.".format(len(matches)))
                        # Display image with rectangle
                        for (x, y, width, height) in matches:
                            if (x, y, width, height) not in objects:
                                objects.append([int(x), int(y), int(width), int(height)])
                            cv2.rectangle(haystack, (x, y), (x + width, y + height), (255, 255, 0), 2)
                        # cv2.imshow('Haystack', haystack)
                        # cv2.waitKey()
                        # cv2.destroyAllWindows()
                    else:
                        print("There are no matches.")
                    self.image_index += 1
                    print("Found " + str(len(objects)) + " of " + object_name + " in " + haystack_filename)
        else:
            print("Object does not exist in image files.")
        return matches

    def pick_random(self, match_list):
        if len(match_list) > 0:
            rand = random.randrange(0, len(match_list))
            return match_list[rand]
        else:
            return None

    def center_pos(self, single_match):
        if single_match is not None:
            left = int(single_match[0] + (single_match[2]*3/8))
            right = int(single_match[0] + (single_match[2]*5/8))
            top = int(single_match[1] + (single_match[3]*3/8))
            bottom = int(single_match[1] + (single_match[3]*5/8))
            randX = random.randrange(left, right)
            randY = random.randrange(top, bottom)
            return (randX, randY)

    def on_move(self, x, y):
        if self.running:
            # Get mouse position
            self.currentMouseX, self.currentMouseY = pyautogui.position()
            mousedistance = ((self.currentMouseX - self.prevMouseX) + (self.currentMouseY - self.prevMouseY))
            # Check to see mouse has moved far enough and also only goes at most every second
            self.delta_time(False)
            if mousedistance > 20 and self.deltaTime > 1:
                # Set previous time
                self.delta_time(True)
                # Takes screenshot, crops it to specified size, and saves under object_directory
                screenshot = pyautogui.screenshot()
                image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                x = int(self.currentMouseX - (self.crop_size / 2))
                y = int(self.currentMouseY - (self.crop_size / 2))
                w = x+int(self.crop_size)
                h = y+int(self.crop_size)
                cropped_image = image[x:w, y:h]
                # cv2.imshow('Cropped', cropped_image)
                if platform == "linux" or platform == "linux2":
                    cv2.imwrite(self.object_directory+'/'+self.object_on_mouse+str(self.image_index)+'.png', cropped_image)
                elif platform == "win32":
                    cv2.imwrite(self.object_directory+'\\'+self.object_on_mouse+str(self.image_index)+'.png', cropped_image)
                self.image_index += 1
                print('There are '+str(self.image_index)+' images of '+self.object_on_mouse)
                # print('Mouse moved to {0}'.format((x, y)))

    def delta_time(self, set_last):
        # Calc delta time to save to macro
        self.deltaTime = round((time.perf_counter()-self.lastTimestamp), 1)
        if set_last:
            self.lastTimestamp = round(time.perf_counter(), 3)

    def on_click(self, x, y, button, pressed):
        if self.running:
            if pressed:
                # Get mouse position
                self.currentMouseX, self.currentMouseY = pyautogui.position()
            print('Mouse '+str(button)+' {0} at {1}'.format('pressed' if pressed else 'released', (x, y)))
            if not pressed:
                # Stop listener
                return False

    def on_release(self, key):
        try:
            if key.char == self.start_button and self.running:
                self.running = False
                print("Stopped watching {0}".format(self.object_on_mouse))
            elif key.char == self.start_button:
                print("What object are you showing me under the mouse cursor?")
                # self.object_on_mouse = input()
                print("How big is it?")
                # Just crops box of this size from screenshot
                # self.crop_size = input()
                print("Watching {0}".format(self.object_on_mouse))
                self.object_directory = os.path.join(self.imagedir, self.object_on_mouse)
                if not os.path.exists(self.object_directory):
                    os.mkdir(self.object_directory)
                files = os.listdir(self.object_directory)
                self.image_index = 1
                for f in files:
                    if '.png' in f:
                        self.image_index += 1
                self.running = True
        except AttributeError:
            print('Unique key {0} pressed'.format(key))

    def on_press(self, key):
        if self.running:
            print('{0} pressed'.format(key))

    def activate_listeners(self):
        self.listeners = True
        # Listeners are responsible for mouse/keyboard input
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        listener.start()

        listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click)
        listener.start()


reader = Reader()
reader.activate_listeners()
screenshot = pyautogui.screenshot(reader.imagedir+'screenshot.png')
match_list = reader.object_search('Test', 'screenshot.png')
match_list2 = reader.image_search('Capture.PNG', 'screenshot.png')
rand_match = reader.pick_random(match_list2)
pyautogui.moveTo(reader.center_pos(rand_match))
print("Picked: "+str(rand_match))
while True:
    continue
