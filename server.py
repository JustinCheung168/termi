#!/usr/bin/env python3
import socket
import os

if 'DISPLAY' not in os.environ:
    os.environ['DISPLAY'] = ':0'
import pyautogui
import yaml

import termi.inputs

def run():
    # Read server socket details
    with open("config.yaml", "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    host = data['host']
    port = data['port']

    x_dim, y_dim = pyautogui.size()

    # Bind the socket host and port
    server_socket = socket.socket()
    server_socket.bind((host, port))

    # Server can wait indefinitely
    server_socket.settimeout(None) 
    # Server can accept this many clients
    server_socket.listen(1)

    connection: socket.socket = None
    try: 
        print(f'Server launched.')
        while True:
            print(f'Awaiting client connection...')
            # Wait for client to connect
            connection, address = server_socket.accept()  # accept new connection
            print(f'Connected to {address}.')

            server_input = termi.inputs.ServerInput(connection, x_dim, y_dim)

            # Get introductory data packet from client
            intro_data = connection.recv(1024).decode()

            server_input.interpret_introduction(intro_data)

            try:
                connected: bool = True
                while connected:
                    # Wait for data from the client
                    data = connection.recv(1024).decode()

                    if data:
                        server_input.actuate(data)
                    else:
                        print(f'Lost contact with {address}; closing connection...')
                        connection.close()
                        connected = False
            except KeyboardInterrupt:
                print(f'Closing connection to {address}...')
                connection.close()
            
    except KeyboardInterrupt:
        print("\nQuitting...")

    finally:
        if connection is not None:
            connection.close()
        return


if __name__ == '__main__':
    run()