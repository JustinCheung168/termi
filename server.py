#!/usr/bin/env python3
import socket

def run():
    # Server socket details
    host = '192.168.1.191'
    port = 12345

    # Bind the socket host and port
    server_socket = socket.socket()
    server_socket.bind((host, port))

    # Server can wait indefinitely
    server_socket.settimeout(None) 
    # Server can accept this many clients
    server_socket.listen(1)

    connection: socket.socket = None
    try: 
        while True:
            # Wait for client to connect
            connection, address = server_socket.accept()  # accept new connection
            print(f'Connected to {address}')

            connected: bool = True
            while connected:
                # Wait for data from the client
                data = connection.recv(1024).decode()
                if data:
                    print(f'Received: {data}')
                else:
                    print(f'Lost connection to {address}')
                    connection.close()
                    connected = False
            
    except KeyboardInterrupt:
        print("\nQuitting...")
        if connection is not None:
            connection.close()
        return


if __name__ == '__main__':
    run()