import socket
import queue

import mice

class ClientInput():
    def __init__(self, client_socket):
        self.queue = queue.Queue()

        self.mouse = mice.ClientMouse(self.queue)

        self.socket: socket.socket = client_socket

    def send(self):
        if not self.queue.empty():
            packet = repr(self.queue.get()).encode() + ";"
            self.socket.send(packet)
            # thing = eval(packet)
            # print(type(thing))


class ServerInput():
    def __init__(self, connection):
        self.mouse = ServerMouse()

        self.connection = connection

    def actuate(self, data: str):

        event_reprs = data.split(";")[:-1]

        for event_repr in event_reprs:
            event = eval(event_repr)

            print(event)

            # print(f'Received: {data}')

            # packet = repr(self.queue.get()).encode()
            # self.socket.send(packet)

class ServerMouse():
    def __init__(self):
        """"""
        # super().__init__
