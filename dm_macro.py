import time
import pyautogui

def macro_func():
	pyautogui.FAILSAFE = False
	pyautogui.moveTo(802, 386)
	time.sleep(.5)
	pyautogui.moveTo(802, 386)
	time.sleep(.5)
	time.sleep(.5)
	pyautogui.moveTo(760, 388)
	time.sleep(.5)
	pyautogui.moveTo(738, 370)
	time.sleep(.5)
	pyautogui.moveTo(704, 392)
	time.sleep(.5)
	pyautogui.moveTo(728, 402)
	time.sleep(.5)
	pyautogui.moveTo(714, 392)
	time.sleep(.5)
	pyautogui.moveTo(724, 402)
	time.sleep(.5)
	time.sleep(.5)
	pyautogui.moveTo(730, 410)
	time.sleep(.5)
	print('Done playing')