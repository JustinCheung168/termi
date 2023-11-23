import socket
import queue

from mice import *

class ClientInput():
    def __init__(self, client_socket):
        self.queue = queue.Queue()

        self.mouse = ClientMouse(self.queue)

        self.socket: socket.socket = client_socket

    def send(self):
        if not self.queue.empty():

            # thing = self.queue.get()
            # if type(thing) == MouseClickEvent:
            #     print(thing)
            #     print(thing.button)
            #     print(thing.button.name)
            #     print(thing.button.value)

            packet = repr(self.queue.get()).encode() + b';'
            self.socket.send(packet)




class ServerInput():
    def __init__(self, connection):
        self.mouse = ServerMouse()

        self.connection = connection

    def actuate(self, data: str):

        event_reprs = data.split(";")[:-1]

        for event_repr in event_reprs:
            try:
                event = eval(event_repr)

                event_type = type(event)
                print(event_type)
                if isinstance(event_type, MouseEvent):
                    print('mouse event')
                    self.mouse.actuate(event)
                # elif isinstance(event_type, KeyboardEvent):
                #     self.keyboard.actuate(event)

            except NameError:
                print(f"Could not evaluate instruction: {event_repr}")
            except Exception:
                print(f"Unknown error encountered while evaluating instruction: {event_repr}")

            

            # print(f'Received: {data}')

            # packet = repr(self.queue.get()).encode()
            # self.socket.send(packet)
