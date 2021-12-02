import socket
import cv2
import pickle
import struct
import pyautogui
import numpy as np

print('Connecting to server...')
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host_ip = socket.gethostname()
port = 8080
client_socket.connect((host_ip, port))
print('Connected!')
data = b""
payload_size = struct.calcsize("Q")
screen_width, screen_height = pyautogui.size()
running = True


while running:
    while len(data) < payload_size:
        packet = client_socket.recv(4*1024)
        if not packet:
            break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]
    while len(data) < msg_size:
        data += client_socket.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)
    scale_tuple = (screen_width, screen_height)
    scaled_frame = cv2.resize(np.array(frame), scale_tuple)
    cv2.imshow("Screen share", scaled_frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
client_socket.close()
cv2.destroyAllWindows()
