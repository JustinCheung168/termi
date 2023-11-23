import queue
from dataclasses import dataclass

import pynput.mouse

@dataclass
class MouseEvent:
    """Common struct format for mouse input events like 
    mouse moves/clicks/scrolls"""
    x: float
    y: float

@dataclass
class MouseMoveEvent(MouseEvent):
    """Mouse move"""

@dataclass
class MouseClickEvent(MouseEvent):
    button: str
    pressed: bool

@dataclass
class MouseScrollEvent(MouseEvent):
    dx: float
    dy: float

class ClientMouse(pynput.mouse.Listener):
    def __init__(self, input_queue):
        super().__init__(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll, 
            suppress=True
        )

        self.queue: queue.Queue = input_queue

        self.start()
        self.wait()

    def on_move(self, x, y):
        # message = f'Pointer moved to ({x}, {y})'
        self.queue.put(MouseMoveEvent(x, y))

    def on_click(self, x, y, button: pynput.mouse.Button, pressed):
        # pressed_str = 'Pressed' if pressed else 'Released'
        # message = f'{pressed_str} {button} at ({x}, {y})'
        self.queue.put(MouseClickEvent(x, y, button.name, pressed))

    def on_scroll(self, x, y, dx, dy):
        # direction_str = 'down' if dy < 0 else 'up'
        # message = f'Scrolled {direction_str} at ({x}, {y})'
        # print(dy)
        self.queue.put(MouseScrollEvent(x, y, dx, dy))


class ServerMouse(pynput.mouse.Controller):
    def __init__(self):
        """"""
        super().__init__()

    def actuate(self, event: MouseEvent, x_scale: float, y_scale: float):
        if isinstance(event, MouseMoveEvent):
            self.move(event.x * x_scale, event.y * y_scale)
        elif isinstance(event, MouseClickEvent):
            if event.pressed:
                self.press(event.button)
            else:
                self.release(event.button)
        elif isinstance(event, MouseScrollEvent):
            print('scroll')
            self.scroll(int(event.dy * y_scale)+1)
        else:
            pass
            # print(f'Unknown mouse event {type(event)}, {event}')

    def move(self, x: float, y: float):
        self.position = (x, y)
    
    def press(self, button: str):
        if button == "left":
            super().press(pynput.mouse.Button.left)
        elif button == "right":
            super().press(pynput.mouse.Button.right)
        elif button == "middle":
            super().press(pynput.mouse.Button.middle)
        else:
            pass
            # print(f'Unknown mouse button pressed {button}')

    def release(self, button: str):
        if button == "left":
            super().release(pynput.mouse.Button.left)
        elif button == "right":
            super().release(pynput.mouse.Button.right)
        elif button == "middle":
            super().release(pynput.mouse.Button.middle)
        else:
            pass
            # print(f'Unknown mouse button released {button}')

    def scroll(self, dy: float):
        # TODO fix scrolling, it's broken rn
        print(dy)
        super().scroll(0, 100)
