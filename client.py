#!/usr/bin/env python3
import socket

def client_program():
    # Server socket details
    host = '192.168.1.191'
    port = 12345


    client_socket = socket.socket()
    try:
        # Connect to server
        client_socket.connect((host, port))
    except ConnectionRefusedError:
        print("Server refused connection; is it running?")
        client_socket.close()
        return

    try:
        while True:
            message = input("Enter something: ")
            client_socket.send(message.encode())
    except KeyboardInterrupt:
        print("Quitting...")
    except BrokenPipeError:
        print("Lost connection to server; quitting...")
    
    # Cleanup
    client_socket.close()
    return


if __name__ == '__main__':
    client_program()