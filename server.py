#!/usr/bin/env python3
import socket

def server_program():
    # get the hostname
    host = '192.168.1.191'
    port = 12345  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    server_socket.bind((host, port))  # bind host address and port together
    server_socket.settimeout(None) # socket can wait indefinitely

    # configure how many client the server can listen simultaneously
    server_socket.listen(1)

    # Wait for client to connect
    try:
        conn, address = server_socket.accept()  # accept new connection
        print("Connection from: " + str(address))
    except KeyboardInterrupt:
        print("Didn't receive a connection")
        return

    try:
        while True:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            data = conn.recv(1024).decode()
            if not data:
                # if data is not received break
                break
            print("from connected user: " + str(data))
        print("Lost connection")
        conn.close()  # close the connection
        return
    except KeyboardInterrupt:
        print("Quitting")
        conn.close()  # close the connection
        return


if __name__ == '__main__':
    server_program()