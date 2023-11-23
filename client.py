#!/usr/bin/env python3
import socket
import time
import os
import sys

if 'DISPLAY' not in os.environ:
    os.environ['DISPLAY'] = ':0'
import pyautogui
import yaml

import inputs

def run():
    # Read server socket details
    with open("config.yaml", "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    host = data['host']
    port = data['port']

    x_dim, y_dim = pyautogui.size()

    with socket.socket() as client_socket:

        print(sys.argv)
        if len(sys.argv) > 1 and sys.argv[1] == "--no-server":
            client_input = inputs.ClientInput(x_dim, y_dim, None)
        else:
            try:
                # Connect to server
                client_socket.connect((host, port))
            except ConnectionRefusedError:
                print("Server refused connection; is it running?")
                return

            client_input = inputs.ClientInput(x_dim, y_dim, client_socket)

            client_input.send_introduction()

        print("Now accepting input. Press Ctrl+C to quit.")

        try:
            while True:
                time.sleep(1/10000)
                client_input.send()
        except inputs.ExitException:
            print("\nQuitting...")
        except BrokenPipeError:
            print("Lost connection to server; quitting...")


if __name__ == '__main__':
    run()