import time

import win32gui
import re

class WindowController():

    def __init__(self):
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """Finds a window by its class name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, handle_window, wildcard):
        if re.match(wildcard, str(win32gui.GetWindowText(handle_window))) is not None:
            self._handle = handle_window

    def find_window_wildcard(self, wildcard):
        """Find window which matches wildcard"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """Set window to foreground"""
        win32gui.SetForegroundWindow(self._handle)

    def delayed_find_window(self, wait_time, class_name, window_name=None):
        time.sleep(wait_time)
        self.find_window(class_name, window_name)

    def delayed_find_window_wildcard(self, wait_time, wildcard):
        time.sleep(wait_time)
        self.find_window_wildcard(wildcard)



