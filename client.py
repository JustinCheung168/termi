#!/usr/bin/env python3
import socket

def run():
    # Server socket details
    host = '192.168.1.191'
    port = 12345

    with socket.socket() as client_socket:
        try:
            # Connect to server
            client_socket.connect((host, port))
        except ConnectionRefusedError:
            print("Server refused connection; is it running?")
            return

        try:
            while True:
                message = input("Enter something: ")
                client_socket.send(message.encode())
        except KeyboardInterrupt:
            print("\nQuitting...")
        except BrokenPipeError:
            print("Lost connection to server; quitting...")


if __name__ == '__main__':
    run()