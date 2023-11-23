#!/usr/bin/env python3
import socket

def client_program():
    # host = socket.gethostname()  # as both code is running on same pc
    host = '192.168.1.191'
    port = 12345  # socket server port number

    client_socket = socket.socket()  # instantiate

    try:
        client_socket.connect((host, port))  # connect to the server
    except ConnectionRefusedError:
        print("Server refused connection; is it running?")
        client_socket.close()
        return

    try:
        while True:
            message = input(" -> ")  # again take input
            client_socket.send(message.encode())  # send message
    except KeyboardInterrupt:
        print("Quitting")
        client_socket.close()  # close the connection
        return
    except BrokenPipeError:
        print("Lost connection to server")
        client_socket.close()
        return


if __name__ == '__main__':
    client_program()