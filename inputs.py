import socket
import queue

from mice import *
from keyboards import *

class ClientInput():
    def __init__(self, client_socket, x_dim, y_dim):
        self.queue = queue.Queue()

        self.mouse = ClientMouse(self.queue)
        self.keyboard = ClientKeyboard(self.queue)

        self.socket: socket.socket = client_socket

        self.x_dim = x_dim
        self.y_dim = y_dim

    def send_introduction(self):
        intro_data = {"x_dim": self.x_dim, "y_dim": self.y_dim}
        self.socket.send(repr(intro_data).encode())

    def send(self):
        if not self.queue.empty():
            packet = repr(self.queue.get()).encode() + b';'
            self.socket.send(packet)


class ServerInput():
    def __init__(self, connection, x_dim: int, y_dim: int):
        self.mouse = ServerMouse()
        self.keyboard = ServerKeyboard()

        self.connection = connection

        self.x_dim = x_dim
        self.y_dim = y_dim

    def interpret_introduction(self, data: str):
        """"""
        intro_data: dict = eval(data)
        self.set_client_scaling(intro_data["x_dim"], intro_data["y_dim"])

    def set_client_scaling(self, x_dim: int, y_dim: int):
        self.x_scale = self.x_dim / float(x_dim)
        self.y_scale = self.y_dim / float(y_dim)

    def actuate(self, data: str):

        event_reprs = data.split(";")[:-1]

        for event_repr in event_reprs:
            try:
                event = eval(event_repr)

                if isinstance(event, MouseEvent):
                    self.mouse.actuate(event, self.x_scale, self.y_scale)
                elif isinstance(event, KeyboardEvent):
                    self.keyboard.actuate(event)
                else:
                    print(f"Unknown event type {type(event)}")

            except NameError:
                print(f"Could not evaluate instruction: {event_repr}")
            except Exception:
                print(f"Unknown error encountered while evaluating instruction: {event_repr}")

