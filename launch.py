#!/usr/bin/env python3
import pyautogui
import pynput
# import mouse
import time

class Mouse():
    def __init__(self):
        """Create non-blocking mouse listener"""
        self.listener = pynput.mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll
        )

    def listen(self):
        self.listener.start()

    @staticmethod
    def on_move(x, y):
        print('Pointer moved to {0}'.format(
            (x, y)))

    @staticmethod
    def on_click(x, y, button, pressed):
        print('{0} at {1}'.format(
            f'Pressed {button}' if pressed else f'Released {button}',
            (x, y)))
        # if not pressed:
        #     # Stop listener
        #     return False

    @staticmethod
    def on_scroll(x, y, dx, dy):
        print('Scrolled {0} at {1}'.format(
            'down' if dy < 0 else 'up',
            (x, y)))

    # # Collect events until released
    # with pynput.mouse.Listener(
    #         on_move=on_move,
    #         on_click=on_click,
    #         on_scroll=on_scroll) as listener:
    #     listener.join()

def main():
    


    my_mouse = Mouse()
    my_mouse.listen()
    
    print("Now accepting input. Press Ctrl+C to quit.")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nExiting...")


if __name__ == "__main__":
    main()
    # pyautogui.moveTo(100, 100, duration = 1)