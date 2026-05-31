import json
from os import system
import time
import subprocess
from pynput import keyboard


with open("macros/k_macro.json") as f:
    keyboard_events = json.load(f)

with open("macros/m_macro.json") as f:
    mouse_events = json.load(f)

events = keyboard_events + mouse_events
events.sort(key=lambda e: e["at"])


def parse_key(key):
    if key.startswith("Key."):
        return key.split(".", 1)[1]

    if key.startswith("'") and key.endswith("'"):
        return key[1:-1]

    return key


def parse_mouse_button(btn):
    if "left" in btn:
        return "1"
    if "middle" in btn:
        return "2"
    if "right" in btn:
        return "3"
    return None


stop_flag = False

def check_cancelling(key):
    global stop_flag
    if key == keyboard.Key.esc:
        print("ESC pressed, stopping playback...")
        stop_flag = True
        return False  # stops listener


listener = keyboard.Listener(on_press=check_cancelling)
listener.start()

# ---------- Start ----------
time.sleep(3)
start = time.perf_counter()

for event in events:
    if stop_flag:
        break

    target = event["at"]

    while (time.perf_counter() - start) < target:
        time.sleep(0.001) # If we use pass, thread will be busy at 100%, then no scheduling works on the current thread -> slowing system down

    etype = event["type"]

    # ---------- Keyboard ----------
    if etype == "key_press":
        key = parse_key(event["key"])
        subprocess.run(["xdotool", "keydown", key])

    elif etype == "key_release":
        key = parse_key(event["key"])
        subprocess.run(["xdotool", "keyup", key])

    # ---------- Mouse buttons ----------
    elif etype == "mouse_click":
        btn = parse_mouse_button(event["key"])
        if btn:
            subprocess.run(["xdotool", "mousedown", btn])

    elif etype == "mouse_release":
        btn = parse_mouse_button(event["key"])
        if btn:
            subprocess.run(["xdotool", "mouseup", btn])

    # ---------- Mouse movement ----------
    elif etype == "mouse_move":
        subprocess.run([
            "xdotool",
            "mousemove_relative",
            "--",
            str(event["dx"]),
            str(event["dy"])
        ])

    # ---------- Scroll ----------
    elif etype == "mouse_scroll":
        dy = event["y"]

        if dy > 0:
            for _ in range(abs(int(dy))):
                subprocess.run(["xdotool", "click", "4"])

        elif dy < 0:
            for _ in range(abs(int(dy))):
                subprocess.run(["xdotool", "click", "5"])
