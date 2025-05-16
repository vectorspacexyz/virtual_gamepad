from collections import defaultdict
import uinput
import time
import evdev
from evdev import InputDevice, categorize, ecodes
import os
import select

# Xbox 360 controller setup
events = (
    uinput.BTN_A,
    uinput.BTN_B,
    uinput.BTN_X,
    uinput.BTN_Y,
    uinput.BTN_TL,
    uinput.BTN_TR,
    uinput.BTN_THUMBL,
    uinput.BTN_THUMBR,
    uinput.ABS_X + (0, 255, 0, 0),
    uinput.ABS_Y + (0, 255, 0, 0),
)

device = uinput.Device(
    events,
    vendor=0x045e,
    product=0x028e,
    version=0x110,
    name="Microsoft X-Box 360 pad",
)

# Center joystick
device.emit(uinput.ABS_X, 128, syn=False)
device.emit(uinput.ABS_Y, 128)

keymap = {
    'right': 'l',
    'left': 'h',
    'up': 'k',
    'down': 'j',
    'kick': 'd',
    'fight': 'f',
    'shadow': 's',
    'range': 'a',
    'jumpleft': 'i',
    'jumpright': 'o',
    'rollleft': 'n',
    'rollleft2': 'b',
    'rollright': 'm',
    'confirm': '0',
    '?': '-',
    'requests/cancel': '9',
    'zoomout': '8',
    'back': 'p',
}

# Convert the keymap values to the evdev KEY codes
key_to_evcode = {
    'a': ecodes.KEY_A,
    'b': ecodes.KEY_B,
    'c': ecodes.KEY_C,
    'd': ecodes.KEY_D,
    'e': ecodes.KEY_E,
    'f': ecodes.KEY_F,
    'g': ecodes.KEY_G,
    'h': ecodes.KEY_H,
    'i': ecodes.KEY_I,
    'j': ecodes.KEY_J,
    'k': ecodes.KEY_K,
    'l': ecodes.KEY_L,
    'm': ecodes.KEY_M,
    'n': ecodes.KEY_N,
    'o': ecodes.KEY_O,
    'p': ecodes.KEY_P,
    'q': ecodes.KEY_Q,
    'r': ecodes.KEY_R,
    's': ecodes.KEY_S,
    't': ecodes.KEY_T,
    'u': ecodes.KEY_U,
    'v': ecodes.KEY_V,
    'w': ecodes.KEY_W,
    'x': ecodes.KEY_X,
    'y': ecodes.KEY_Y,
    'z': ecodes.KEY_Z,
    '0': ecodes.KEY_0,
    '1': ecodes.KEY_1,
    '2': ecodes.KEY_2,
    '3': ecodes.KEY_3,
    '4': ecodes.KEY_4,
    '5': ecodes.KEY_5,
    '6': ecodes.KEY_6,
    '7': ecodes.KEY_7,
    '8': ecodes.KEY_8,
    '9': ecodes.KEY_9,
    '-': ecodes.KEY_MINUS,
}

# Create a reverse mapping from ecodes to our keymap keys
evcode_to_key = {}
for action, key in keymap.items():
    if key in key_to_evcode:
        evcode_to_key[key_to_evcode[key]] = key

def find_keyboard_devices():
    """Find all keyboard devices."""
    keyboards = []
    for path in evdev.list_devices():
        try:
            device = evdev.InputDevice(path)
            # Check if this is a keyboard
            if evdev.ecodes.EV_KEY in device.capabilities():
                keyboards.append(device)
                print(f"Found keyboard: {device.name} at {device.path}")
        except (PermissionError, OSError):
            print(f"Permission error accessing {path}. Try running with sudo.")
    return keyboards

def process_key_event(key_code, key_state):
    """Process a key event, mapping it to the appropriate gamepad action."""
    # Convert evdev key code to our key representation
    if key_code not in evcode_to_key:
        return
    
    k = evcode_to_key[key_code]
    
    # Key pressed (value 1) or key released (value 0)
    if key_state == 1:  # Key pressed
        if k == keymap['kick']:
            device.emit(uinput.BTN_A, 1)
        elif k == keymap['fight']:
            device.emit(uinput.BTN_B, 1)
        elif k == keymap['shadow']:
            device.emit(uinput.BTN_X, 1)
        elif k == keymap['range']:
            device.emit(uinput.BTN_Y, 1)
        elif k == keymap['confirm']:
            device.emit(uinput.BTN_TL, 1)
        elif k == keymap['?']:
            device.emit(uinput.BTN_TR, 1)
        elif k == keymap['requests/cancel']:
            device.emit(uinput.BTN_THUMBL, 1)
        elif k == keymap['zoomout']:
            device.emit(uinput.BTN_THUMBR, 1)
        elif k == keymap['up']:
            device.emit(uinput.ABS_Y, 0)
        elif k == keymap['jumpleft']:
            device.emit(uinput.ABS_Y, 0)
            device.emit(uinput.ABS_X, 0)
        elif k == keymap['jumpright']:
            device.emit(uinput.ABS_Y, 0)
            device.emit(uinput.ABS_X, 255)
        elif k == keymap['down']:
            device.emit(uinput.ABS_Y, 255)
        elif k == keymap['rollleft']:
            device.emit(uinput.ABS_Y, 255)
            device.emit(uinput.ABS_X, 0)
        elif k == keymap['rollleft2']:
            device.emit(uinput.ABS_Y, 255)
            device.emit(uinput.ABS_X, 0)
        elif k == keymap['rollright']:
            device.emit(uinput.ABS_Y, 255)
            device.emit(uinput.ABS_X, 255)
        elif k == keymap['left']:
            device.emit(uinput.ABS_X, 0)
        elif k == keymap['right']:
            device.emit(uinput.ABS_X, 255)
    
    elif key_state == 0:  # Key released
        if k == keymap['kick']:
            device.emit(uinput.BTN_A, 0)
        elif k == keymap['fight']:
            device.emit(uinput.BTN_B, 0)
        elif k == keymap['shadow']:
            device.emit(uinput.BTN_X, 0)
        elif k == keymap['range']:
            device.emit(uinput.BTN_Y, 0)
        elif k == keymap['confirm']:
            device.emit(uinput.BTN_TL, 0)
        elif k == keymap['?']:
            device.emit(uinput.BTN_TR, 0)
        elif k == keymap['requests/cancel']:
            device.emit(uinput.BTN_THUMBL, 0)
        elif k == keymap['zoomout']:
            device.emit(uinput.BTN_THUMBR, 0)
        elif k == keymap['up']:
            device.emit(uinput.ABS_Y, 128)
        elif k == keymap['jumpleft']:
            device.emit(uinput.ABS_Y, 128)
            device.emit(uinput.ABS_X, 128)
        elif k == keymap['jumpright']:
            device.emit(uinput.ABS_Y, 128)
            device.emit(uinput.ABS_X, 128)
        elif k == keymap['rollright']:
            device.emit(uinput.ABS_Y, 128)
            device.emit(uinput.ABS_X, 128)
        elif k == keymap['rollleft']:
            device.emit(uinput.ABS_Y, 128)
            device.emit(uinput.ABS_X, 128)
        elif k == keymap['rollleft2']:
            device.emit(uinput.ABS_Y, 128)
            device.emit(uinput.ABS_X, 128)
        elif k == keymap['down']:
            device.emit(uinput.ABS_Y, 128)
        elif k == keymap['left']:
            device.emit(uinput.ABS_X, 128)
        elif k == keymap['right']:
            device.emit(uinput.ABS_X, 128)

def main():
    # Find keyboard devices
    keyboards = find_keyboard_devices()
    
    if not keyboards:
        print("No keyboard devices found. Make sure you have the correct permissions.")
        print("Try running with sudo or adding your user to the input group.")
        return
    
    print(f"Monitoring {len(keyboards)} keyboard devices. Press Ctrl+C to exit.")
    
    # Create a dictionary of file descriptors to devices
    devices = {dev.fd: dev for dev in keyboards}
    
    # Run the event loop
    try:
        while True:
            r, w, x = select.select(devices, [], [])
            for fd in r:
                for event in devices[fd].read():
                    # Only process key events (type 1)
                    if event.type == ecodes.EV_KEY:
                        key_event = categorize(event)
                        process_key_event(key_event.scancode, key_event.keystate)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        # Close all devices
        for keyboard in keyboards:
            keyboard.close()

if __name__ == "__main__":
    main()
