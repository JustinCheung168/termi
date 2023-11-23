#!/usr/bin/env python3
import socket
import time
import os

if 'DISPLAY' not in os.environ:
    os.environ['DISPLAY'] = ':0'
import pyautogui

import inputs

def run():
    # Server socket details
    host = '192.168.1.191'
    port = 12345

    x_dim, y_dim = pyautogui.size()

    with socket.socket() as client_socket:
        try:
            # Connect to server
            client_socket.connect((host, port))
        except ConnectionRefusedError:
            print("Server refused connection; is it running?")
            return

        client_input = inputs.ClientInput(client_socket, x_dim, y_dim)

        client_input.send_introduction()

        print("Now accepting input. Press Ctrl+C to quit.")

        try:
            while True:
                time.sleep(1/10000)
                client_input.send()
        except KeyboardInterrupt:
            print("\nQuitting...")
        except BrokenPipeError:
            print("Lost connection to server; quitting...")


if __name__ == '__main__':
    run()