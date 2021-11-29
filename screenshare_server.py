# Lets import the libraries
import socket, cv2, pickle, struct, imutils
import numpy as np
from PIL import ImageGrab
from mss import mss
import pyautogui

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
port = 8080
socket_address = (host_ip, port)
server_socket.bind(socket_address)
server_socket.listen(5)
print("Server:", socket_address)
screen_width, screen_height = pyautogui.size()
bounding_box = {'top': 0, 'left': 0, 'width': screen_width, 'height': screen_height}
sct = mss()
running = True

while running:
    client_socket, addr = server_socket.accept()
    print('Screen sharing with:', addr)
    if client_socket:
        client_connected = True
        while client_connected:
            screenshot = sct.grab(bounding_box)
            scale_percent = 75
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

