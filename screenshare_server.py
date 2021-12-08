# Lets import the libraries
import socket, cv2, pickle, struct, imutils
import numpy as np
from sys import platform
import pyautogui
from pynput.keyboard import Key, Controller


class Server:
    def __init__(self):
        self.keyboard = Controller()
        self.running = True
        self.screen_width, self.screen_height = pyautogui.size()
        if platform == "win32":
            from PIL import ImageGrab
            from mss import mss
            self.bounding_box = {'top': 0, 'left': 0, 'width': self.screen_width, 'height': self.screen_height}
            self.sct = mss()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host_name = socket.gethostname()
        host_ip = '127.0.0.1'
        port = 8080
        socket_address = (host_ip, port)
        self.server_socket.bind(socket_address)
        self.server_socket.listen(5)
        self.data = b""
        self.payload_size = struct.calcsize("Q")
        print("Server:", socket_address)

    def server_logic(self):
        newX = 0
        newY = 0
        while self.running:
            client_socket, addr = self.server_socket.accept()
            print('Screen sharing with:', addr)
            if client_socket:
                client_connected = True
                while client_connected:
                    if platform == "linux" or platform == "linux2":
                        screenshot = pyautogui.screenshot(region=(0, 0, self.screen_width, self.screen_height))
                    elif platform == "win32":
                        screenshot = self.sct.grab(self.bounding_box)
                    scale_percent = 100
                    scaled_width = int(self.screen_width * scale_percent / 100)
                    scaled_height = int(self.screen_height * scale_percent / 100)
                    scaled_tuple = (scaled_width, scaled_height)
                    frame = cv2.resize(np.array(screenshot), scaled_tuple)
                    pickled_frame = pickle.dumps(frame)
                    network_packet = struct.pack("Q", len(pickled_frame)) + pickled_frame
                    # Prints optimal packet recv size for max fps
                    # print(len(network_packet))
                    client_socket.sendall(network_packet)
                    # Receive data
                    while len(self.data) < self.payload_size:
                        packet = client_socket.recv(256)
                        if not packet:
                            break
                        self.data += packet
                    packed_msg_size = self.data[:self.payload_size]
                    self.data = self.data[self.payload_size:]
                    msg_size = struct.unpack("Q", packed_msg_size)[0]
                    while len(self.data) < msg_size:
                        self.data += client_socket.recv(256)
                    message_data = self.data[:msg_size]
                    self.data = self.data[msg_size:]
                    message = pickle.loads(message_data)
                    print(message)
                    split_message = message.split()
                    if len(split_message) == 2:
                        # This is for relative x, y coordinates for mouse movement
                        newX = float(split_message[0])
                        newY = float(split_message[1])
                        destX = int(round(newX * self.screen_width, 0))
                        destY = int(round(newY * self.screen_height, 0))
                        print("pyautogui.moveTo("+str(destX)+", "+str(destY)+")")
                    elif len(split_message) == 3:
                        # This is for relative x, y coordinates for mouse click
                        newX = float(split_message[0])
                        newY = float(split_message[1])
                        button = split_message[2]
                        print("pyautogui.click(" + str(destX) + ", " + str(destY) +", button='"+button+"')")
                    elif len(split_message) == 4:
                        key_type = split_message[0]
                        key_pressed = split_message[2]
                        action = split_message[3]
                        if key_type == "Unique":
                            if action == "pressed":
                                print("keyboard.pressed({0})\n".format(key_pressed))
                            else:
                                print("keyboard.released({0})\n".format(key_pressed))
                        elif key_type == "Letter":
                            if action == "pressed":
                                print("keyboard.pressed({0})\n".format(key_pressed))
                            else:
                                print("keyboard.released({0})\n".format(key_pressed))

                    # Exit key
                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        client_socket.close()
                        break
                    # Receive data from client

        cv2.destroyAllWindows()


myServer = Server()
myServer.server_logic()
