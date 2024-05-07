import os

from PIL import Image
import time
import re
import datetime
import pytesseract
from virtmaker.utils.cli import ShellPrinter
from virtmaker import config


def vnc_screenshot(client):
    screenshot_dir = os.path.join(config.get_cache_dir(), "screenshots")
    if not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)
    with ShellPrinter(tag="vnc", verbosity=2, tag_color='white') as print:
        filename = f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
        filepath = os.path.join(screenshot_dir, filename)
        print(f"Saving screenshot to {filepath}")
        client.captureScreen(filepath)
        return filepath

def vnc_ocr_screenshot(client):
    filepath = vnc_screenshot(client)
    text = pytesseract.image_to_string(Image.open(filepath))
    os.remove(filepath)
    return text

def vncdotool_lex(keystrokes: str) -> list:
    to_send = []
    keystroke_groups = re.split(r'(<[^>]+>)', keystrokes)
    for group in keystroke_groups:
        if group.startswith('<') and group.endswith('>'):
            to_send.append(group.lstrip('<').rstrip('>'))
        else:
            for char in group:
                to_send.append(char)
    return to_send



class VNC:
    _client = None
    def __init__(self, client):
        self._client = client

    def wait_for_ocr_text(self, text: str, timeout: int = 60) -> bool:
        with ShellPrinter(tag="vncocr", verbosity=0, tag_color='white') as print:
            print(f"Waiting for text '{text}'")
            start = datetime.datetime.now()
            while True:
                if (datetime.datetime.now() - start).seconds > timeout:
                    return False
                ocr_text = vnc_ocr_screenshot(self._client)
                with ShellPrinter(tag="ocr", verbosity=4, tag_color='white') as ocr_debug_print:
                    ocr_debug_print(ocr_text)
                if text.lower() in ocr_text.lower():
                    ocr_debug_print(f"Found '{text}'")
                    return True
                time.sleep(1)

    def send_ocr_keystroke(self, text, keystrokes, key_delay_time: float = 0.1):
        self.wait_for_ocr_text(text)
        with ShellPrinter(tag="vnc", verbosity=1, tag_color='white') as print:
            if isinstance(keystrokes, list):
                keystrokes = '<delay 2>'.join(keystrokes)
            print(f"Sending keystrokes: '{''.join(keystrokes)}'")
            for keystroke in vncdotool_lex(keystrokes):
                if keystroke.startswith('delay'):
                    time.sleep(float(keystroke.split(' ')[1]))
                else:
                    self._client.keyPress(keystroke)
                time.sleep(float(key_delay_time))

    def send_ocr_keystrokes(self, expectations: list, key_delay_time: float = 0.1):
        for expectation in expectations:
            for text, keystrokes in expectation.items():
                self.send_ocr_keystroke(text=text, keystrokes=keystrokes, key_delay_time=key_delay_time)

    def send_blind_keystrokes(self, keystrokes: str, key_delay_time: float = 0.1):
        with ShellPrinter(tag="cmd", verbosity=1, tag_color='white') as print:
            print("Sending keystroke: ", end='', flush=True)
            if isinstance(keystrokes, list):
                keystrokes = '<delay 2>'.join(keystrokes)
            for keystroke in vncdotool_lex(keystrokes):
                if len(keystroke) > 1:
                    print(f"<{keystroke}>", end='', flush=True)
                else:
                    print(keystroke, end='', flush=True)
                if keystroke.startswith('delay'):
                    time.sleep(float(keystroke.split(' ')[1]))
                else:
                    self._client.keyPress(keystroke)
                time.sleep(float(key_delay_time))
            print()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._client.disconnect()
