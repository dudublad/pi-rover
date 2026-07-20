import os
import select
import sys
import termios
import time
import tty

from rover import Rover
from gpio_pins import R_MOTOR_IN1, R_MOTOR_IN2, L_MOTOR_IN1, L_MOTOR_IN2

# For hardware-timed PWM on a Pi 4 or older, uncomment these two lines:
# from gpiozero import Device
# from gpiozero.pins.pigpio import PiGPIOFactory
# Device.pin_factory = PiGPIOFactory()

SPEED = 0.5

# A plain SSH terminal never sends a key-release event, only repeated
# keystrokes while a key is held (via the OS's own key-repeat). If we don't
# see a repeat of the active key within this window, treat it as released.
# Must be longer than your terminal's initial repeat delay (often ~250-500ms)
# or a held key will look like rapid press/release/press. Increase this if
# the rover stutters while a key is held; decrease it for a snappier stop.
RELEASE_TIMEOUT = 0.5

ARROW_CODES = {
    "A": "up",
    "B": "down",
    "C": "right",
    "D": "left",
}

ACTIONS = {
    "up": lambda: rover.forward(SPEED),
    "down": lambda: rover.backward(SPEED),
    "left": lambda: rover.left(SPEED),
    "right": lambda: rover.right(SPEED),
}


def read_key(fd, timeout):
    """Return 'up'/'down'/'left'/'right'/'quit', or None if nothing usable arrived."""
    ready, _, _ = select.select([fd], [], [], timeout)
    if not ready:
        return None

    # Read raw bytes via the fd directly (not sys.stdin.read), since a
    # buffered read can silently pull the rest of an escape sequence out of
    # the kernel before the next select() gets a chance to see it.
    ch = os.read(fd, 1)

    if ch == b"\x03":  # Ctrl+C
        return "quit"

    if ch != b"\x1b":
        return None

    # Arrow keys arrive as a burst: ESC, '[', <letter>. Give it a brief
    # moment to arrive; if nothing follows, it was a lone Escape press.
    ready, _, _ = select.select([fd], [], [], 0.05)
    if not ready:
        return "quit"

    ch2 = os.read(fd, 1)
    if ch2 != b"[":
        return None

    ch3 = os.read(fd, 1)
    return ARROW_CODES.get(ch3.decode(errors="ignore"))


if __name__ == "__main__":
    rover = Rover(R_MOTOR_IN1, R_MOTOR_IN2, L_MOTOR_IN1, L_MOTOR_IN2)

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    active_key = None
    last_seen = 0.0

    print("Use the arrow keys to drive the rover. Esc or Ctrl+C to quit.")

    try:
        tty.setraw(fd)
        while True:
            key = read_key(fd, 0.05)
            now = time.monotonic()

            if key == "quit":
                break

            if key in ACTIONS:
                if key != active_key:
                    active_key = key
                    ACTIONS[key]()
                last_seen = now

            if active_key is not None and now - last_seen > RELEASE_TIMEOUT:
                active_key = None
                rover.stop()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        rover.stop()
        print("\r\nStopped.")
