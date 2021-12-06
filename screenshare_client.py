import socket
import cv2
import pickle
import struct
import pyautogui
import numpy as np
import pygame
import time
from pynput import keyboard
from pynput import mouse
from pynput.mouse import Button as mouseButton


class Client:
    def __init__(self):
        self.running = True
        self.activate_listeners()
        self.screen_width, self.screen_height = pyautogui.size()
        self.currentMouseX, self.currentMouseY = pyautogui.position()
        self.prevMouseX = self.currentMouseX
        self.prevMouseY = self.currentMouseY
        self.absoluteMousePosX = round(self.currentMouseX / self.screen_width, 4)
        self.absoluteMousePosY = round(self.currentMouseY / self.screen_height, 4)
        # Initiate server connection
        print('Connecting to server...')
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host_ip = '192.168.1.8'
        port = 8080
        self.client_socket.connect((host_ip, port))
        print('Connected!')
        self.data = b""
        self.payload_size = struct.calcsize("Q")
        # Delta time to measure connection speed
        self.lastTimestamp = round(time.perf_counter(), 3)
        self.deltaTime = round((time.perf_counter() - self.lastTimestamp), 1)

    def client_logic(self):
        # GUI code
        pygame.init()
        display = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Screen share')
        black = (0, 0, 0)
        white = (255, 255, 255)
        while self.running:
            while len(self.data) < self.payload_size:
                packet = self.client_socket.recv(6220973)
                if not packet:
                    break
                self.data += packet
            packed_msg_size = self.data[:self.payload_size]
            self.data = self.data[self.payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(self.data) < msg_size:
                self.data += self.client_socket.recv(6220973)
            frame_data = self.data[:msg_size]
            self.data = self.data[msg_size:]
            frame = pickle.loads(frame_data)
            scale_tuple = (self.screen_width, self.screen_height)
            scaled_frame = cv2.resize(np.array(frame), scale_tuple)
            cv2.imwrite("screenshare.png", scaled_frame)
            img = pygame.image.load("screenshare.png")
            self.deltaTime = round((time.perf_counter() - self.lastTimestamp), 1)
            self.lastTimestamp = round(time.perf_counter(), 3)
            # Prints how much time is inbetween the client recv data
            print("Deltatime: {0}".format(self.deltaTime))
            display.blit(img, (0, 0))
            pygame.display.update()
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
        self.client_socket.close()
        cv2.destroyAllWindows()

    def activate_listeners(self):
        self.listeners = True
        # Listeners are responsible for mouse/keyboard input
        listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        listener.start()

        listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)
        listener.start()

    def on_move(self, x, y):
        if self.running:
            # Get mouse position
            self.currentMouseX, self.currentMouseY = pyautogui.position()
            mousedistance = ((self.currentMouseX-self.prevMouseX)+(self.currentMouseY-self.prevMouseY))
            # Check to see mouse has moved far enough
            if mousedistance > 20:
                # Send to the server
                self.absoluteMousePosX = round(self.currentMouseX / self.screen_width, 6)
                self.absoluteMousePosY = round(self.currentMouseY / self.screen_height, 6)
                message = str(self.absoluteMousePosX)+" "+str(self.absoluteMousePosY)
                # print(message)
                pickled_message = pickle.dumps(message)
                network_packet = struct.pack("Q", len(pickled_message)) + pickled_message
                # Prints optimal packet recv size for max fps
                print(len(network_packet))
                self.client_socket.sendall(network_packet)
                self.prevMouseX = self.currentMouseX
                self.prevMouseY = self.currentMouseY
                print('Mouse moved to {0}'.format((x, y)))

    def on_click(self, x, y, button, pressed):
        if self.running:
            if pressed:
                # Get mouse position
                self.currentMouseX, self.currentMouseY = pyautogui.position()
                if button == mouseButton.left:
                    # Send to the server
                    self.absoluteMousePosX = round(self.currentMouseX / self.screen_width, 6)
                    self.absoluteMousePosY = round(self.currentMouseY / self.screen_height, 6)
                    message = str(self.absoluteMousePosX) + " " + str(self.absoluteMousePosY) + " left"
                    # print(message)
                    pickled_message = pickle.dumps(message)
                    network_packet = struct.pack("Q", len(pickled_message)) + pickled_message
                    # Prints optimal packet recv size for max fps
                    print(len(network_packet))
                    self.client_socket.sendall(network_packet)
                if button == mouseButton.right:
                    # Send to the server
                    self.absoluteMousePosX = round(self.currentMouseX / self.screen_width, 6)
                    self.absoluteMousePosY = round(self.currentMouseY / self.screen_height, 6)
                    message = str(self.absoluteMousePosX) + " " + str(self.absoluteMousePosY) + " right"
                    # print(message)
                    pickled_message = pickle.dumps(message)
                    network_packet = struct.pack("Q", len(pickled_message)) + pickled_message
                    # Prints optimal packet recv size for max fps
                    print(len(network_packet))
                    self.client_socket.sendall(network_packet)
            print('Mouse '+str(button)+' {0} at {1}'.format('pressed' if pressed else 'released', (x, y)))
            if not pressed:
                # Stop listener
                return False

    def on_scroll(self, x, y, dx, dy):
        if self.running:
            # Send to the server
            print('Mouse scrolled {0} at {1}'.format(
                'down' if dy < 0 else 'up',
                (x, y)))

    def on_press(self, key):
        if self.running:
            try:
                message = 'Letter key {0} pressed'.format(key)
                pickled_message = pickle.dumps(message)
                network_packet = struct.pack("Q", len(pickled_message)) + pickled_message
                # Prints optimal packet recv size for max fps
                print(len(network_packet))
                self.client_socket.sendall(network_packet)
            except AttributeError:
                message = 'Unique key {0} pressed'.format(key)
                pickled_message = pickle.dumps(message)
                network_packet = struct.pack("Q", len(pickled_message)) + pickled_message
                # Prints optimal packet recv size for max fps
                print(len(network_packet))
                self.client_socket.sendall(network_packet)

    def on_release(self, key):
        if self.running:
            try:
                message = 'Letter key {0} released'.format(key)
                pickled_message = pickle.dumps(message)
                network_packet = struct.pack("Q", len(pickled_message)) + pickled_message
                # Prints optimal packet recv size for max fps
                print(len(network_packet))
                self.client_socket.sendall(network_packet)
            except AttributeError:
                message = 'Unique key {0} released'.format(key)
                pickled_message = pickle.dumps(message)
                network_packet = struct.pack("Q", len(pickled_message)) + pickled_message
                # Prints optimal packet recv size for max fps
                print(len(network_packet))
                self.client_socket.sendall(network_packet)
        if key == keyboard.Key.esc:
            self.running = False
            # Stop listener
            # return False


myClient = Client()
myClient.client_logic()
