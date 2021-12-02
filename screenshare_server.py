# Lets import the libraries
import socket, cv2, pickle, struct, imutils
import numpy as np
from sys import platform
import pyautogui

screen_width, screen_height = pyautogui.size()
if platform == "win32":
    from PIL import ImageGrab
    from mss import mss
    bounding_box = {'top': 0, 'left': 0, 'width': screen_width, 'height': screen_height}
    sct = mss()
    
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host_name = socket.gethostname()
host_ip = '127.0.0.1'
port = 8080
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen(5)
print("Server:", socket_address)
running = True

while running:
    client_socket, addr = server_socket.accept()
    print('Screen sharing with:', addr)
    if client_socket:
        client_connected = True
        while client_connected:
            if platform == "linux" or platform == "linux2":
                screenshot = pyautogui.screenshot(region=(0, 0, screen_width, screen_height))
            elif platform == "win32":
                screenshot = sct.grab(bounding_box)
            scale_percent = 100
            scaled_width = int(screen_width * scale_percent / 100)
            scaled_height = int(screen_height * scale_percent / 100)
            scaled_tuple = (scaled_width, scaled_height)
            frame = cv2.resize(np.array(screenshot), scaled_tuple)
            pickled_frame = pickle.dumps(frame)
            newtork_packet = struct.pack("Q", len(pickled_frame)) + pickled_frame
            client_socket.sendall(newtork_packet)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                client_socket.close()
                break
cv2.destroyAllWindows()

