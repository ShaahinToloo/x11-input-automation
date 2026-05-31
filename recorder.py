import threading
import json
import time
from pynput import keyboard, mouse


keyboard_events = []
mouse_events = []

kb_listener = None
ms_listener = None

pressed_keys_rn = []
pressed_mouses_rn = []

stop_event = threading.Event()
start_time = time.perf_counter()

# ---------- KEYBOARD ----------
def on_press(key):
    global pressed_keys_rn

    if key == keyboard.Key.esc:
        stop_all()
        return False

    #keyboard_events.append(("press", str(key)))
    t = time.perf_counter() - start_time

    if key not in pressed_keys_rn:
        keyboard_events.append({
            "type": "key_press", 
            "key": str(key),
            "at": t
        })
        pressed_keys_rn.append(key)


def on_release(key):
    global pressed_keys_rn
    pressed_keys_rn.remove(key)

    t = time.perf_counter() - start_time

    keyboard_events.append({
        "type": "key_release", 
        "key": str(key),
        "at": t
    })


def keyboard_worker():
    global kb_listener
    kb_listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release
    )
    kb_listener.join()


# ---------- MOUSE ----------
def on_click(x, y, button, pressed):
    global old_button, mouse_pressed

    t = time.perf_counter() - start_time

    if pressed:
        pressed_mouses_rn.append(button)
        mouse_events.append({
            "type": "mouse_click",
            "key": str(button),
            "at": t
        })

    else:
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
        "x": dx,
        "y": dy,
        "at": t
    })


def mouse_worker():
    global ms_listener
    ms_listener = mouse.Listener(
        on_click=on_click,
        on_move=on_move,
        on_scroll=on_scroll
    )
    ms_listener.join()


# ---------- STOP CLEANLY ----------
def stop_all():
    print("Stopping...")

    stop_event.set()

    if kb_listener:
        kb_listener.stop()

    if ms_listener:
        ms_listener.stop()

    with open("k_macro.json", "w") as f:
        json.dump(keyboard_events, f, indent=2)

    with open("m_macro.json", "w") as f:
        json.dump(mouse_events, f, indent=2)

    print("Saved files")


# ---------- THREADS ----------
kb_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
ms_listener = mouse.Listener(on_click=on_click,
                             on_move=on_move,
                             on_scroll=on_scroll)

kb_listener.start()
ms_listener.start()

stop_event.wait()
