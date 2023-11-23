import queue
from dataclasses import dataclass
from typing import Union
from string import ascii_lowercase

import pynput.keyboard

class ExitException(Exception):
    """Raise when user inputs exit sequence"""

@dataclass
class KeyboardEvent:
    """Common struct format for keyboard input events"""

@dataclass
class KeyPressEvent(KeyboardEvent):
    """"""
    pressed: bool

@dataclass
class KeyPressAlphanumericEvent(KeyPressEvent):
    """"""
    key: str
    

@dataclass
class KeyPressSpecialEvent(KeyPressEvent):
    """"""
    key: int


class ClientKeyboard(pynput.keyboard.Listener):
    def __init__(self, input_queue):
        super().__init__(
            on_press=self.on_press,
            on_release=self.on_release,
            suppress=True
        )
        self.pressed_keys = set()

        self.queue: queue.Queue = input_queue

        self.start()
        self.wait()

    def on_press(self, key: pynput.keyboard.Key):
        self.on_button_event(key, True)

    def on_release(self, key: pynput.keyboard.Key):
        self.on_button_event(key, False)

    def on_button_event(self, key: Union[pynput.keyboard.KeyCode, pynput.keyboard.Key], pressed: bool):
        if isinstance(key, pynput.keyboard.KeyCode):
            self.queue.put(KeyPressAlphanumericEvent(pressed, key.char))
            if pressed:
                self.pressed_keys.add(key.char)
            else:
                self.pressed_keys.discard(key.char)
        elif isinstance(key, pynput.keyboard.Key):
            self.queue.put(KeyPressSpecialEvent(pressed, key.name))
            if pressed:
                self.pressed_keys.add(key.name)
            else:
                self.pressed_keys.discard(key.name)


class ServerKeyboard(pynput.keyboard.Controller):

    def __init__(self):
        """"""
        super().__init__()
        self.pressed_keys = set()
        self.valid_special_keys: dict[str, pynput.keyboard.Key] = self.get_valid_special_keys()

        # Ensure these keys start in released state if they were used to exit
        for key in ['cmd', 'ctrl', 'cmd_r', 'ctrl_r']:
            try:
                super().release(self.valid_special_keys[key])
            except:
                print(f'Skipping {key} release')
        for keychar in ascii_lowercase:
            super().release(keychar)

    def get_valid_special_keys(self):
        valid_special_keys = {}
        for attribute in dir(pynput.keyboard.Key):
            if attribute[0] != '_':
                attr: pynput.keyboard.Key = getattr(pynput.keyboard.Key, attribute)
                valid_special_keys[attr.name] = attr

        # Manually swap cmd and ctrl
        # swap = valid_special_keys['cmd']
        # valid_special_keys['cmd'] = valid_special_keys['ctrl']
        # valid_special_keys['ctrl'] = swap

        # swap = valid_special_keys['cmd_r']
        # valid_special_keys['cmd_r'] = valid_special_keys['ctrl_r']
        # valid_special_keys['ctrl_r'] = swap

        return valid_special_keys

    def actuate(self, event: KeyboardEvent):
        if isinstance(event, KeyPressAlphanumericEvent):
            if event.pressed:
                return self.press(event.key)
            else:
                self.release(event.key)
        elif isinstance(event, KeyPressSpecialEvent):
            if event.pressed:
                return self.press(event.key)
            else:
                self.release(event.key)
        else:
            print(f'Unknown keyboard event {type(event)}, {event}')
    
    def press(self, key: str):
        try:
            if key in self.valid_special_keys.keys():
                super().press(self.valid_special_keys[key])
            else:
                super().press(key)
        except Exception as e:
            print(f"Unknown pressed key: {key} with exception {e}")
        self.pressed_keys.add(key)

    def release(self, key: str):
        try:
            if key in self.valid_special_keys.keys():
                super().release(self.valid_special_keys[key])
            else:
                super().release(key)
        except Exception as e:
            print(f"Unknown released key: {key} with exception {e}")
        self.pressed_keys.discard(key)

