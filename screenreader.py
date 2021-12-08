import pyautogui
import cv2
import numpy as np
import os
import random
from sys import platform

class Reader:
    def __init__(self):
        self.status = "idle"
        if platform == "linux" or platform == "linux2":
            self.imagedir = os.path.dirname(os.path.abspath(__file__)) + '/images'
        elif platform == "win32":
            self.imagedir = os.path.dirname(os.path.abspath(__file__)) + '\\images\\'

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
        print("There are {0} total matches in the haystack.".format(len(xloc)))
        # Keep track of all matches and identify unique cases
        matches = []
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
        return matches
        cv2.imshow('Haystack', haystack)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def pick_random(self, match_list):
        rand = random.randrange(0, len(match_list))
        return match_list[rand]

    def center_pos(self, single_match):
        left = int(single_match[0] + (single_match[2]*3/8))
        right = int(single_match[0] + (single_match[2]*5/8))
        top = int(single_match[1] + (single_match[3]*3/8))
        bottom = int(single_match[1] + (single_match[3]*5/8))
        randX = random.randrange(left, right)
        randY = random.randrange(top, bottom)
        return (randX, randY)


reader = Reader()
screenshot = pyautogui.screenshot(reader.imagedir+'screenshot.png')
match_list = reader.image_search('Capture.PNG', 'screenshot.png')
rand_match = reader.pick_random(match_list)
pyautogui.moveTo(reader.center_pos(rand_match))
print("Picked : "+str(rand_match))
