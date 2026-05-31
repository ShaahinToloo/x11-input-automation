import threading
import json
import time
from pynput import keyboard, mouse
import os


keyboard_events = []
mouse_events = []

pressed_keys_rn = []
pressed_mouses_rn = []

kb_listener = None
ms_listener = None

stop_event = threading.Event()
start_time = time.perf_counter()

time.sleep(float(input("Start After (seconds, float): ")))
print("\nStarted!\n")

# ---------- KEYBOARD ----------
def on_press(key):
    if key == keyboard.Key.esc:
        stop_all()
        return False

    t = time.perf_counter() - start_time
    if key not in pressed_keys_rn:
        keyboard_events.append({
            "type": "key_press",
            "key": str(key),
            "at": t
        })
        pressed_keys_rn.append(key)


def on_release(key):
    if key in pressed_keys_rn:
        pressed_keys_rn.remove(key)
    t = time.perf_counter() - start_time
    keyboard_events.append({
        "type": "key_release",
        "key": str(key),
        "at": t
    })


# ---------- MOUSE ----------
def on_click(x, y, button, pressed):
    t = time.perf_counter() - start_time
    if pressed:
        pressed_mouses_rn.append(button)
        mouse_events.append({
            "type": "mouse_click",
            "key": str(button),
            "at": t
        })
    else:
        if button in pressed_mouses_rn:
            pressed_mouses_rn.remove(button)
        mouse_events.append({
            "type": "mouse_release",
            "key": str(button),
            "at": t
        })


def on_move(x, y):
    t = time.perf_counter() - start_time
    mouse_events.append({
        "type": "mouse_move",
        "x": x,
        "y": y,
        "at": t
    })


def on_scroll(x, y, dx, dy):
    t = time.perf_counter() - start_time
    mouse_events.append({
        "type": "mouse_scroll",
        "dx": dx,
        "dy": dy,
        "at": t
    })


# ---------- STOP CLEANLY ----------
def stop_all():
    print("\nStopping...")
    
    stop_event.set()

    os.makedirs("macros", exist_ok=True)
    with open("macros/k_macro.json", "w") as f:
        json.dump(keyboard_events, f, indent=2)

    with open("macros/m_macro.json", "w") as f:
        json.dump(mouse_events, f, indent=2)

    print("Saved files")

    os._exit(0)


# ---------- START LISTENERS ----------
kb_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
ms_listener = mouse.Listener(on_click=on_click, on_move=on_move, on_scroll=on_scroll)

kb_listener.start()
ms_listener.start()

kb_listener.join()
ms_listener.join()

stop_event.wait()
