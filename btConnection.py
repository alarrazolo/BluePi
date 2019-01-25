"""
A simple Python script to receive messages from a client over
Bluetooth using Python sockets (with Python 3.3 or above).
"""
import os
import socket

from Securitron import Securitron


class BtConnection:

    def __init__(self, timeout=0, victor=None):
        # self.client = ''
        # self.address = ''
        os.system('sudo sdptool add --channel=22 SP')
        # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
        self.hostMACAddress = 'B8:27:EB:B7:6D:62'
        self.port = 22  # 3 is an arbitrary choice. However, it must match the port used by the client.
        self.backlog = 1
        self.size = 1024
        self.timeout = timeout
        self.connection = None
        self.client = None
        self.address = None
        # self.connection_flag = False
        self.connection_flag = True
        if victor:
            self.robot_subject = victor
        else:
            self.robot_subject = Securitron()
        # self.start_connection()

    def start_connection(self):
        connection = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        if self.timeout is not 0:
            connection.settimeout(self.timeout)
        connection.bind((self.hostMACAddress, self.port))
        connection.listen(self.backlog)
        try:
            client, address = connection.accept()
            self.client = client
            self.address = address
            self.connection = connection
            # self.connection_flag = True
            print(self.client)
            print(self.address)

            print('Waiting for data')
        except socket.timeout:
            print("Closing socket Timed out!")
            connection.close()
        except socket.error:
            print("Closing socket Error")
            connection.close()

    def get_data(self):
        data = None
        if self.connection_flag:
            try:
                data = self.client.recv(self.size)
            except ConnectionResetError:
                self.connection.close()
                print("No connection")
                # self.connection_flag = False
                self.robot_subject.hit_breaks()
                self.start_connection()
            except BrokenPipeError:
                self.robot_subject.hit_breaks()
                self.start_connection()
            # self.client.send(bytes('this is a test', encoding='utf-8'))
            if data:
                message = data.decode('utf-8')
                print(message)
                if message == "Forward":
                    print("telling Victor to go straight")
                    self.send_data("telling Victor to go straight")
                    self.robot_subject.forward()
                if message == "ForwardRight":
                    print("telling Victor to go forward and slight right")
                    self.send_data("telling Victor to go forward and slight right")
                    self.robot_subject.forward_right()
                if message == "ForwardLeft":
                    print("telling Victor to go forward and slight left")
                    self.send_data("telling Victor to go forward and slight left")
                    self.robot_subject.forward_left()
                if message == "Back":
                    print("telling Victor to go back")
                    self.send_data("telling Victor to go back")
                    self.robot_subject.back()
                if message == "BackRight":
                    print("telling Victor to go back and slight right")
                    self.send_data("telling Victor to go back and slight right")
                    self.robot_subject.back_right()
                if message == "BackLeft":
                    print("telling Victor to go back and slight left")
                    self.send_data("telling Victor to go back and slight left")
                    self.robot_subject.back_left()
                # if message == "StrongLeft":
                #     print("telling Victor to go left")
                #     self.send_data("telling Victor to go left")
                #     self.robot_subject.strong_left()
                # if message == "StrongRight":
                #     print("telling Victor to go right")
                #     self.send_data("telling Victor to go right")
                #     self.robot_subject.strong_right()
                if message == "stop":
                    print("Woah there Victor")
                    self.send_data("Woah there Victor")
                    self.robot_subject.hit_breaks()
        else:
            print("No connection123")
            # self.connection_flag = False
            self.start_connection()

    def send_data(self, data):
        message = data
        encoded_data = message.encode('utf-8')
        self.client.send(encoded_data)

    # def is_connected(self):
        # return self.connection_flag

    def close_connection(self):
        if self.connection:
            self.connection.close()
