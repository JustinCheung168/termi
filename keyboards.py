import queue
from dataclasses import dataclass
from typing import Union

import pynput.keyboard

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
        elif isinstance(key, pynput.keyboard.Key):
            self.queue.put(KeyPressSpecialEvent(pressed, key.name))


class ServerKeyboard(pynput.keyboard.Controller):

    def __init__(self):
        """"""
        super().__init__()
        self.pressed_keys = set()
        self.valid_special_keys: dict[str, pynput.keyboard.Key] = self.get_valid_special_keys()

    def get_valid_special_keys(self):
        valid_special_keys = {}
        for attribute in dir(pynput.keyboard.Key):
            if attribute[0] != '_':
                attr: pynput.keyboard.Key = getattr(pynput.keyboard.Key, attribute)
                valid_special_keys[attr.name] = attr

        # Manually swap cmd and ctrl
        swap = valid_special_keys['cmd']
        valid_special_keys['cmd'] = valid_special_keys['ctrl']
        valid_special_keys['ctrl'] = swap

        swap = valid_special_keys['cmd_r']
        valid_special_keys['cmd_r'] = valid_special_keys['ctrl_r']
        valid_special_keys['ctrl_r'] = swap

        # Ensure each key starts in released state
        for key in ['cmd', 'ctrl', 'cmd_r', 'ctrl_r']:
            super().release(valid_special_keys[key])
        # for key in valid_special_keys.keys():
        #     try:
        #         super().release(valid_special_keys[key])
        #     except Exception as e:
        #         print(f'Could not release {key} ({e}); skipping it')

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

        if 'ctrl' in self.pressed_keys and 'q' in self.pressed_keys:
            return "escape"

    def release(self, key: str):
        try:
            if key in self.valid_special_keys.keys():
                super().release(self.valid_special_keys[key])
            else:
                super().release(key)
        except Exception as e:
            print(f"Unknown released key: {key} with exception {e}")
        self.pressed_keys.discard(key)

