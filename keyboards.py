import queue
from dataclasses import dataclass

import pynput

@dataclass
class KeyboardEvent:
    """Common struct format for keyboard input events"""
    key: str
    special: bool

@dataclass
class KeyPressEvent(KeyboardEvent):
    """"""
    pressed: bool


class ClientKeyboard(pynput.keyboard.Listener):
    def __init__(self, input_queue):
        super().__init__(
            on_press=self.on_press,
            on_release=self.on_release,
            suppress=True
        )

        self.queue: queue.Queue = input_queue

        self.start()

    def on_press(self, key: pynput.keyboard.Key):
        self.on_button_event(key, True)

    def on_release(self, key: pynput.keyboard.Key):
        self.on_button_event(key, False)

    def on_button_event(self, key: pynput.keyboard.KeyCode | pynput.keyboard.Key, pressed: bool):
        if isinstance(key, pynput.keyboard.KeyCode):
            self.queue.put(KeyPressEvent(key.char, False, pressed))
        elif isinstance(key, pynput.keyboard.Key):
            self.queue.put(KeyPressEvent(key.name, True, pressed))


class ServerKeyboard(pynput.keyboard.Controller):
    def __init__(self):
        """"""
        super().__init__()
        self.pressed_keys = set()

    def actuate(self, event: KeyboardEvent):
        if isinstance(event, KeyPressEvent):
            if event.pressed:
                self.press(event.key, event.special)
            else:
                self.release(event.key, event.special)
        else:
            print('Unknown keyboard event')
    
    def press(self, key: str, _):
        try:
            super().press(key)
        except:
            print(f"Unknown key: {key}")
        self.pressed_keys.add(key)

    def release(self, key: str, _):
        try:
            super().release(key)
        except:
            print(f"Unknown key: {key}")
        self.pressed_keys.discard(key)

