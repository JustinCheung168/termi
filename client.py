#!/usr/bin/env python3
import socket

def client_program():
    # host = socket.gethostname()  # as both code is running on same pc
    host = '192.168.1.191'
    port = 12345  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    try:
        while True:
            message = input(" -> ")  # again take input
            client_socket.send(message.encode())  # send message
    except KeyboardInterrupt:
        print("Quitting")
        client_socket.close()  # close the connection


if __name__ == '__main__':
    client_program()