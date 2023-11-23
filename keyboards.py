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
            # suppress=True
        )

        self.queue: queue.Queue = input_queue

        self.start()

    def on_press(self, key: pynput.keyboard.Key):
        self.on_button_event(key, True)

    def on_release(self, key: pynput.keyboard.Key):
        self.on_button_event(key, False)

    def on_button_event(self, key: Union[pynput.keyboard.KeyCode, pynput.keyboard.Key], pressed: bool):
        if isinstance(key, pynput.keyboard.KeyCode):
            self.queue.put(KeyPressAlphanumericEvent(pressed, key.char))
        elif isinstance(key, pynput.keyboard.Key):
            self.queue.put(KeyPressSpecialEvent(pressed, key.value))


class ServerKeyboard(pynput.keyboard.Controller):

    # KEYS = {
    #     58: pynput.keyboard.Key.alt,
    #     61: pynput.keyboard.Key.alt_r,
    #     51: pynput.keyboard.Key.backspace,
    #     57: pynput.keyboard.Key.caps_lock,
    #     55: pynput.keyboard.Key.cmd,
    #     54: pynput.keyboard.Key.cmd_r,
    #     59: pynput.keyboard.Key.ctrl,
    #     62: pynput.keyboard.Key.ctrl_r,
    #     117: pynput.keyboard.Key.delete,
    #     125: pynput.keyboard.Key.down,
    #     119: pynput.keyboard.Key.end,
    #     36: pynput.keyboard.Key.enter,
    #     53: pynput.keyboard.Key.esc,
    #     122: pynput.keyboard.Key.f1,
    #     120: pynput.keyboard.Key.f2,

    # }

    def __init__(self):
        """"""
        super().__init__()
        self.pressed_keys = set()
        self.valid_special_keys: dict[int, pynput.keyboard.Key] = self.get_valid_special_keys()

    def get_valid_special_keys(self):
        valid_special_keys = {}
        for attribute in dir(pynput.keyboard.Key):
            if attribute[0] != '_':
                attr: pynput.keyboard.Key = getattr(pynput.keyboard.Key, attribute)
                valid_special_keys[attr.value] = attr
        return valid_special_keys

    def actuate(self, event: KeyboardEvent):
        if isinstance(event, KeyPressAlphanumericEvent):
            if event.pressed:
                self.press(event.key)
            else:
                self.release(event.key)
        elif isinstance(event, KeyPressSpecialEvent):
            if event.pressed:
                self.press(event.key)
            else:
                self.release(event.key)
        else:
            print('Unknown keyboard event')
    
    def press(self, key: Union[str, int]):
        try:
            if key in self.valid_special_keys.keys():
                super().press(self.valid_special_keys[key])
            else:
                super().press(key)
        except Exception as e:
            print(f"Unknown key: {key} with exception {e}")
        self.pressed_keys.add(key)

    def release(self, key: Union[str, int]):
        try:
            super().release(key)
        except Exception as e:
            print(f"Unknown key: {key} with exception {e}")
        self.pressed_keys.discard(key)

