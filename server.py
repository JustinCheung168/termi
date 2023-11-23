#!/usr/bin/env python3
import socket
import inputs

def run():
    # Server socket details
    host = '192.168.1.191'
    port = 12345
    
    x_dim = 1920
    y_dim = 1080

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

            server_input = inputs.ServerInput(connection, x_dim, y_dim)

            # Get introductory data packet from client
            intro_data = connection.recv(1024).decode()
            server_input.interpret_intro_data(intro_data)

            connected: bool = True
            while connected:
                # Wait for data from the client
                data = connection.recv(1024).decode()
                if data:
                    server_input.actuate(data)
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