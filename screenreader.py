import time
import string
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
        self.running = False
        self.listeners = False
        self.start_button = '`'
        self.object_on_mouse = 'Test'
        if platform == "linux" or platform == "linux2":
            self.imagedir = os.path.dirname(os.path.abspath(__file__)) + '/images'
        elif platform == "win32":
            self.imagedir = os.path.dirname(os.path.abspath(__file__)) + '\\images\\'
        self.object_directory = ''
        self.number_directory = os.path.join(self.imagedir, 'Numbers')
        self.character_directory = os.path.join(self.imagedir, 'Characters')
        self.currentMouseX, self.currentMouseY = pyautogui.position()
        self.prevMouseX = 0
        self.prevMouseY = 0
        self.crop_size = 32
        self.image_index = 0
        self.lastTimestamp = round(time.perf_counter(), 3)
        self.deltaTime = round((time.perf_counter() - self.lastTimestamp), 1)

    def image_search(self, needle_filename, haystack_filename):
        # Search for needle in a haystack
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

    def number_search(self, threshold, haystack_filename):
        # Keep track of all matches and identify unique cases
        numbers = []
        if os.path.exists(self.number_directory):
            files = os.listdir(self.number_directory)
            self.image_index = 1
            haystack = cv2.imread(self.imagedir + haystack_filename, cv2.IMREAD_UNCHANGED)
            grayscale_haystack = cv2.cvtColor(haystack, cv2.COLOR_BGR2GRAY)
            match_number = 0
            while match_number < 10:
                for f in files:
                    if '.png' in f:
                        matches = []
                        image_path = os.path.join(self.number_directory, str(match_number) + '_' + str(self.image_index) + '.png')
                        print(image_path)
                        if not os.path.exists(image_path):
                            break
                        needle = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
                        grayscale_needle = cv2.cvtColor(needle, cv2.COLOR_BGR2GRAY)
                        result = cv2.matchTemplate(grayscale_haystack, grayscale_needle, cv2.TM_CCOEFF_NORMED)
                        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                        # Max location has the best match with max_val to be % accuracy
                        width = needle.shape[1]
                        height = needle.shape[0]
                        bottom_right = (max_loc[0] + width, max_loc[1] + height)
                        # Threshold is the % accuracy compared to original needle
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
                                if (x, y, width, height) not in numbers:
                                    numbers.append([int(x), int(y), int(width), int(height), int(match_number)])
                                cv2.rectangle(haystack, (x, y), (x + width, y + height), (255, 255, 0), 2)
                            # cv2.imshow('Haystack', haystack)
                            # cv2.waitKey()
                            # cv2.destroyAllWindows()
                        else:
                            print("There are no matches.")
                        self.image_index += 1
                        print("Found " + str(len(numbers)) + " of numbers in " + haystack_filename)
                match_number += 1
                self.image_index = 1
        else:
            print("Numbers do not exist in screenshot.")
        print(numbers)
        return numbers

    def sort_matches(self, sort_index, threshold,  match_list):
        # Bubble sort algo
        match_len = len(match_list)
        for y1 in range(match_len-1):
            for y2 in range(0, match_len - y1 - 1):
                # If index is greater than next index
                if match_list[y2][sort_index] > match_list[y2+1][sort_index]:
                    # If difference of index values is greater than the threshold
                    if abs(match_list[y2][sort_index] - match_list[y2+1][sort_index]) > threshold:
                        match_list[y2], match_list[y2+1] = match_list[y2+1], match_list[y2]

    def number_concat(self, threshold, price, matches):
        # Concat data together to form usable numbers
        match_len = len(matches)
        temp_array = matches[0]
        result_array = []
        for index in range(0, match_len-1):
            print(index)
            if abs(matches[index][1] - matches[index+1][1]) < threshold:
                print(temp_array)
                # Sum width of each character
                temp_array[2] = temp_array[2] + matches[index+1][2]
                # Multiply index value by 10 and add index+1
                temp_array[4] = (temp_array[4]*10) + matches[index+1][4]
                print(temp_array)
                if index == match_len - 2:
                    result_array.append(temp_array)
                    temp_array = matches[index + 1]
            else:
                result_array.append(temp_array)
                temp_array = matches[index+1]
        if price:
            for number in result_array:
                number[4] = number[4]/100
        print(result_array)

    def set_selection(self, x1, y1, x2, y2):
        # Selection is used to only search for objects in an area
        self.selection = [x1, y1, x2, y2]

    def get_selection(self, x1, y1, x2, y2):
        # Selection is used to only search for objects in an area
        return self.selection

    def split_image(self, directory, filename, width_split, height_split):
        # Split image is used to split an image into smaller images
        image_path = os.path.join(directory, filename)
        filenames_list = []
        if not os.path.exists(image_path):
            print("Filepath does not exist for split_image method.")
            return filenames_list
        img = cv2.imread(image_path)
        width = int(img.shape[0])
        height = int(img.shape[1])
        if width_split > width:
            print("Width is too large.")
            return filenames_list
        if height_split > height:
            print("Height is too large.")
            return filenames_list
        for index_a in range(0, width, int(width_split)):
            for index_b in range(0, height, int(height_split)):
                x = index_a
                y = index_b
                image_path = os.path.join(directory, f"{filename.replace('.png', '')}_{index_a}_{index_b}.png")
                cv2.imwrite(image_path, img[index_a:index_a + int(width_split), index_b:index_b + int(height_split), :])
                filenames_list.append([int(x), int(y), int(width), int(height), f"{filename.replace('.png', '')}_{index_a}_{index_b}.png"])
        print(filenames_list)
        return filenames_list

    def image_difference(self, threshold, needle_directory, needle_filename, haystack_directory, haystack_filename, iterations):
        # Recursive function to find differences with remaining iterations
        # representing how many times it will be cut into four parts
        remaining_iterations = iterations - 1
        # Record similarities and differences between two first images
        similarities = []
        differences = []
        # Load haystack image
        haystack_image_path = os.path.join(haystack_directory, haystack_filename)
        if not os.path.exists(haystack_image_path):
            print("Haystack file does not exist.")
            return differences
        img = cv2.imread(haystack_image_path)
        section_width = img.shape[0] / 2
        section_height = img.shape[1] / 2
        # Cut haystack image into 4 sections
        haystack_images = self.split_image(haystack_directory, haystack_filename, section_width, section_height)
        # Load needle image
        needle_image_path = os.path.join(needle_directory, needle_filename)
        if not os.path.exists(needle_image_path):
            print("Needle file does not exist.")
            return differences
        img = cv2.imread(needle_image_path)
        # Cut needle image into 4 sections
        section_width = img.shape[0] / 2
        section_height = img.shape[1] / 2
        needle_images = self.split_image(needle_directory, needle_filename, section_width, section_height)
        # Loop through each needle section and haystack section and compare
        for haystack_section in haystack_images:
            for needle_section in needle_images:
                # Format for needle/haystack section [x, y, width, height, filename]
                # Only do loop if the x, y positions match
                if not haystack_section[0] == needle_section[0]:
                    continue
                if not haystack_section[1] == needle_section[1]:
                    continue
                haystack_path = os.path.join(haystack_directory, haystack_section[4])
                if not os.path.exists(haystack_path):
                    print("Split haystack files do not exist.")
                    return differences
                needle_path = os.path.join(needle_directory, needle_section[4])
                if not os.path.exists(needle_path):
                    print("Split needle files do not exist.")
                    return differences
                # Turn both images to grayscale to speed up process
                haystack = cv2.imread(haystack_path, cv2.IMREAD_UNCHANGED)
                grayscale_haystack = cv2.cvtColor(haystack, cv2.COLOR_BGR2GRAY)
                needle = cv2.imread(needle_path, cv2.IMREAD_UNCHANGED)
                grayscale_needle = cv2.cvtColor(needle, cv2.COLOR_BGR2GRAY)
                # Match the results
                matches = []
                result = cv2.matchTemplate(grayscale_haystack, grayscale_needle, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                # Max location has the best match with max_val to be % accuracy
                width = needle.shape[1]
                height = needle.shape[0]
                bottom_right = (max_loc[0] + width, max_loc[1] + height)
                # Threshold is the % accuracy compared to original needle
                yloc, xloc = np.where(result >= threshold)
                if len(xloc) > 0:
                    # Similarity found
                    print("There are {0} total matches in the haystack.".format(len(xloc)))
                    for (x, y) in zip(xloc, yloc):
                        # Twice to ensure singles are kept after picking unique cases
                        matches.append([needle_section[0], needle_section[1], needle_section[2], needle_section[3]])
                        matches.append([needle_section[0], needle_section[1], needle_section[2], needle_section[3]])
                    # Grouping function
                    matches, weights = cv2.groupRectangles(matches, 1, 0.2)
                    print("There are {0} unique matches in the haystack.".format(len(matches)))
                    if remaining_iterations == 0:
                        # Display image with rectangle
                        for (x, y, width, height) in matches:
                            print("Similarity found:" + str(needle_section))
                            similarities.append(needle_section)
                            # cv2.rectangle(haystack, (x, y), (x + width, y + height), (255, 255, 0), 2)
                        # cv2.imshow('Haystack', haystack)
                        # cv2.waitKey()
                        # cv2.destroyAllWindows()
                elif remaining_iterations == 0:
                    # Differences found in the last iteration
                    print("Difference found:" + str(needle_section))
                    differences.append(needle_section)
                elif remaining_iterations > 0:
                    # If there are differences then iterate this section for efficiency
                    same_parts, different_parts = self.image_difference(threshold, needle_directory, needle_section[4], haystack_directory, haystack_section[4], remaining_iterations)
                    similarities.append(same_parts)
                    differences.append(different_parts)
                else:
                    print("There are no matches.")
        return similarities, differences

    def character_concat(self, threshold, multiboxes, matches):
        # Concat data together to form usable words
        match_len = len(matches)
        temp_array = matches[0]
        result_array = []
        if multiboxes:
            skip_next = False
        for index in range(1, match_len):
            if abs(matches[index-1][1] - matches[index][1]) < threshold:
                print(temp_array)
                # Sum width of each character
                temp_array[2] = temp_array[2] + (matches[index][0]-matches[index-1][0])
                # Add character to the end
                if multiboxes:
                    if not skip_next:
                        temp_array[4] = temp_array[4] + matches[index][4]
                    else:
                        skip_next = False
                else:
                    temp_array[4] = temp_array[4] + matches[index][4]
                print(temp_array)
                if index < match_len-1 and abs((matches[index][0]+matches[index][2]) - matches[index+1][0]) > threshold and len(temp_array[4]) > 1:
                    if multiboxes:
                        skip_next = True
                        temp_array[2] = matches[index][2] + matches[index][0] - temp_array[0]
                        result_array.append(temp_array)
                        temp_array = matches[index+1]
                        index += 2
                    else:
                        temp_array[4] = temp_array[4] + ' '
                if index == match_len - 1 and len(temp_array[4]) > 1:
                    result_array.append(temp_array)
                    temp_array = matches[index]
            elif len(temp_array[4]) > 1:
                result_array.append(temp_array)
                temp_array = matches[index]
        # Clean up results
        print(result_array[0][4])
        result_len = len(result_array)
        for index in range(0, result_len-2):
            if multiboxes:
                temp_str = result_array[index][4]
                result_array[index][4] = temp_str.replace("o8", "8").replace("co", "c").replace("og", "g")
                if index > 0 and result_array[index][4] == 'rg':
                    result_array.pop(index)
                    result_array[index-1][4] = result_array[index-1][4] + 'g'
                if result_array[index][4] == 'lng':
                    result_array.pop(index)
                    result_array[index-1][4] = result_array[index-1][4] + 'ng'
            elif not multiboxes:
                result_array[index][4] = result_array[index][4].replace("n r g", "ng").replace("c o", "c").replace("i l", "i").replace("n r ", "n")
        return result_array

    def proximity_combine(self, list_a, list_b):
        # Combine elements in lists to form combinations
        list_a_len = len(list_a)
        list_b_len = len(list_b)
        combined_list = []
        for index_a in range(0, list_a_len):
            for index_b in range(0, list_b_len):
                distance_x = abs(list_a[index_a][0] - list_b[index_b][0])
                distance_y = abs(list_a[index_a][1] - list_b[index_b][1])
                # Finds smallest width
                padding = (min(list_a[index_a][2], list_b[index_b][2]))*2
                if distance_x < padding and distance_y < padding:
                    if list_a[index_a][0] < list_b[index_b][0]:
                        combined_str = str(list_a[index_a][4])+str(list_b[index_b][4])
                        new_x = list_a[index_a][0]
                        new_y = list_a[index_a][1]
                    else:
                        combined_str = str(list_b[index_b][4]) + str(list_a[index_a][4])
                        new_x = list_a[index_b][0]
                        new_y = list_a[index_b][1]
                    if combined_str not in combined_list:
                        combined_width = list_a[index_a][2]+list_b[index_b][2]
                        new_height = list_a[index_a][3]
                        combined_list.append([new_x, new_y, combined_width, new_height, combined_str])
        return combined_list

    def character_search(self, threshold, letters, haystack_filename):
        # Keep track of all matches and identify unique cases
        chars = []
        chars_list = []
        if letters:
            chars_list = ['A', 'B', 'C', 'D', 'E',
                          'F', 'G', 'H', 'I', 'J',
                          'K', 'L', 'M', 'N', 'O',
                          'P', 'Q', 'R', 'S', 'T',
                          'U', 'V', 'W', 'X', 'Y',
                          'Z', '0', '1', '2', '3',
                          '4', '5', '6', '7', '8',
                          '9']
        else:
            chars_list = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=']
        chars_list_len = len(chars_list)
        if os.path.exists(self.character_directory):
            files = os.listdir(self.character_directory)
            self.image_index = 1
            haystack = cv2.imread(self.imagedir + haystack_filename, cv2.IMREAD_UNCHANGED)
            grayscale_haystack = cv2.cvtColor(haystack, cv2.COLOR_BGR2GRAY)
            match_number = 0
            while match_number < chars_list_len:
                for f in files:
                    if '.png' in f:
                        matches = []
                        image_path = os.path.join(self.character_directory,
                                                  chars_list[match_number] + '_' + str(self.image_index) + '.png')
                        print(image_path)
                        if not os.path.exists(image_path):
                            break
                        needle = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
                        grayscale_needle = cv2.cvtColor(needle, cv2.COLOR_BGR2GRAY)
                        result = cv2.matchTemplate(grayscale_haystack, grayscale_needle, cv2.TM_CCOEFF_NORMED)
                        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                        # Max location has the best match with max_val to be % accuracy
                        width = needle.shape[1]
                        height = needle.shape[0]
                        bottom_right = (max_loc[0] + width, max_loc[1] + height)
                        # Threshold is the % accuracy compared to original needle
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
                                if (x, y, width, height) not in chars:
                                    chars.append([int(x), int(y), int(width), int(height), str(chars_list[match_number]).lower()])
                                # cv2.rectangle(haystack, (x, y), (x + width, y + height), (255, 255, 0), 2)
                            # cv2.imshow('Haystack', haystack)
                            # cv2.waitKey()
                            # cv2.destroyAllWindows()
                        else:
                            print("There are no matches.")
                        self.image_index += 1
                        print("Found " + str(len(chars)) + " of numbers in " + haystack_filename)
                match_number += 1
                self.image_index = 1
            else:
                print("Characters do not exist in screenshot.")
            print(chars)
            return chars

    def draw_info(self, matches, haystack_filename):
        # Draw the matches on the original image
        boxes = []
        haystack = cv2.imread(self.imagedir + haystack_filename, cv2.IMREAD_UNCHANGED)
        for (x, y, width, height, name) in matches:
            if (x, y, width, height) not in boxes:
                boxes.append([int(x), int(y), int(width), int(height)])
            cv2.rectangle(haystack, (x, y), (x + width, y + height), (255, 255, 0), 2)
        cv2.imshow('Haystack', haystack)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def object_search(self, object_name, threshold, haystack_filename):
        # Keep track of all matches and identify unique cases
        self.object_directory = os.path.join(self.imagedir, object_name)
        objects = []
        if os.path.exists(self.object_directory):
            files = os.listdir(self.object_directory)
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
                    # Threshold is the % accuracy compared to original needle
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
        return objects

    def pick_random(self, matches):
        # Pick random element in the matches list
        if len(matches) > 0:
            rand = random.randrange(0, len(matches))
            return matches[rand]
        else:
            return None

    def center_pos(self, single_match):
        # Return center x, y coordinates of a match
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
        # Mouse press action
        if self.running:
            if pressed:
                # Get mouse position
                self.currentMouseX, self.currentMouseY = pyautogui.position()
            print('Mouse '+str(button)+' {0} at {1}'.format('pressed' if pressed else 'released', (x, y)))
            if not pressed:
                # Stop listener
                return False

    def on_release(self, key):
        # Watch an object
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
        # Key press
        if self.running:
            print('{0} pressed'.format(key))

    def activate_listeners(self):
        # Listeners are responsible for mouse/keyboard input
        self.listeners = True
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        listener.start()

        listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click)
        listener.start()


reader = Reader()
# reader.activate_listeners()
# screenshot = pyautogui.screenshot(reader.imagedir+'screenshot.png')
# char_list = reader.character_search(.85, False, 'price_screenshot.png')
# reader.sort_matches(0, 0, char_list)
# reader.sort_matches(1, 5, char_list)
# num_list = reader.number_search(.85, 'price_screenshot.png')
# reader.sort_matches(0, 0, num_list)
# reader.sort_matches(1, 5, num_list)
# print(num_list)
# reader.draw_info(num_list, 'price_screenshot.png')
# reader.number_concat(5, True, num_list)
# print(char_list)
# prices = reader.proximity_combine(char_list, num_list)
# print(prices)
# reader.draw_info(prices, 'price_screenshot.png')
# letter_list = reader.character_search(.94, True, 'price_screenshot.png')
# reader.sort_matches(0, 0, letter_list)
# reader.sort_matches(1, 5, letter_list)
# print(letter_list)
# reader.draw_info(letter_list, 'price_screenshot.png')
# words = reader.character_concat(5, True, letter_list)
# print(words)
# reader.draw_info(words, 'price_screenshot.png')
# match_list2 = reader.image_search('Capture.PNG', .85, 'screenshot.png')
# rand_match = reader.pick_random(match_list2)
# pyautogui.moveTo(reader.center_pos(rand_match))
# print("Picked: "+str(rand_match))
# Image difference tests
similar, difference = reader.image_difference(.85, reader.imagedir, 'Image_diff_1.png', reader.imagedir, 'Image_diff_2.png', 2)
print(similar)
print(difference)
while True:
    continue
