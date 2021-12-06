import time
import pyautogui
import random


def random_move(x, y):
    # Choose a random amount of segments to move to x, y
    randomSteps = random.randrange(3, 9)
    # Loop through all the random moves of mouse to get closer to x, y
    while randomSteps < 12:
        currentMouseX, currentMouseY = pyautogui.position()
        # Choose a random destination to move the mouse closer to x, y
        if x < currentMouseX:
            stepDistanceX = (currentMouseX - x) / (12 - randomSteps)
            randomDestinationX = random.randrange(currentMouseX, currentMouseX - stepDistanceX)
        else:
            stepDistanceX = (x - currentMouseX) / (12 - randomSteps)
            randomDestinationX = random.randrange(currentMouseX, currentMouseX + stepDistanceX)
        if y < currentMouseY:
            stepDistanceY = (currentMouseY - y) / (12 - randomSteps)
            randomDestinationY = random.randrange(currentMouseY, currentMouseY - stepDistanceY)
        else:
            stepDistanceY = (x - currentMouseY) / (12 - randomSteps)
            randomDestinationY = random.randrange(currentMouseY, currentMouseY + stepDistanceY)

        randMoveDuration = (random.randrange(0, 500, 6)) / 1000
        pyautogui.moveTo(randomDestinationX, randomDestinationY, randMoveDuration)
        randomSteps += 1

    # Finish by moving mouse to x, y
    pyautogui.moveTo(x, y)


def random_click(x, y, mouse_button):
    randX = x + random.randrange(-3, 3)
    randY = y + random.randrange(-3, 3)
    randDuration = (random.randrange(150, 450, 6)) / 1000
    pyautogui.moveTo(randX, randY)
    pyautogui.mouseDown(button=mouse_button)
    time.sleep(randDuration)
    pyautogui.mouseUp(button=mouse_button)


def mouse_drift():
    # Function to make the user seem more human with slightly moving mouse on accident/boredom
    randRepeat = random.randrange(0, 6)
    while randRepeat < 3:
        currentMouseX, currentMouseY = pyautogui.position()
        rand = random.randrange(0, 15)
        randomDestinationX = random.randrange(-rand, rand)
        rand = random.randrange(0, 15)
        randomDestinationY = random.randrange(-rand, rand)
        randMoveDuration = (random.randrange(0, 500, 6)) / 1000
        pyautogui.moveTo(randomDestinationX, randomDestinationY, randMoveDuration)
        randRepeat += 1
