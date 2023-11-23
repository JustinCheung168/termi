#!/usr/bin/env python3
import pyautogui
# import mouse
import pynput
import queue
from dataclasses import dataclass

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
    button: pynput.mouse.Button
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
            on_scroll=self.on_scroll
        )

        self.queue: queue.Queue = input_queue

        self.start()

    def on_move(self, x, y):
        # message = f'Pointer moved to ({x}, {y})'
        self.queue.put(MouseMoveEvent(x, y))

    def on_click(self, x, y, button, pressed):
        # pressed_str = 'Pressed' if pressed else 'Released'
        # message = f'{pressed_str} {button} at ({x}, {y})'
        self.queue.put(MouseClickEvent(x, y, button, pressed))

    def on_scroll(self, x, y, dx, dy):
        # direction_str = 'down' if dy < 0 else 'up'
        # message = f'Scrolled {direction_str} at ({x}, {y})'
        self.queue.put(MouseScrollEvent(x, y, dx, dy))

