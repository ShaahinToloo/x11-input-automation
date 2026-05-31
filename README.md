# Linux-X11 Python mouse and keyboard automation
Written in python. Uses xdotool to generate inputs to system.

> [!WARNING]
> This works on Linux.
> To use it on windows you must use pydirectinput instead of xdotool.
> This DOES NOT work on wayland.
> Solution? Don't use Wayland!

## Requirements
Python requirements:
```bash
pip install pynput
```

System requirements:
```bash
sudo apt install xdotool
```

## Run

Record:
- Run recorder.py and do your route.
- Press `Esc` to stop the recording.
- Head back to terminal and press Ctrl-C to shutdown the threads

Playback:
- Run playback.py and after 3 seconds it starts the route.
- Press `Esc` to cancel the macro.
