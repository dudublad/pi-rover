from gpiozero import Motor

class Rover:

    def __init__(self, in1R, in2R, in1L, in2L, enableR=None, enableL=None):
        self._motorR = Motor(forward=in1R, backward=in2R, enable=enableR, pwm=True)
        self._motorL = Motor(forward=in1L, backward=in2L, enable=enableL, pwm=True)

    def forward(self, speed):
        self._motorR.forward(speed)
        self._motorL.forward(speed)

    def backward(self, speed):
        self._motorR.backward(speed)
        self._motorL.backward(speed)

    def right(self, speed):
        self._motorR.backward(speed)
        self._motorL.forward(speed)

    def left(self, speed):
        self._motorR.forward(speed)
        self._motorL.backward(speed)

    def stop(self):
        self._motorR.stop()
        self._motorL.stop()


if __name__ == "__main__":
    from gpio_pins import R_MOTOR_IN1, R_MOTOR_IN2, L_MOTOR_IN1, L_MOTOR_IN2
    from time import sleep
 
    # For hardware-timed PWM on a Pi 4 or older, uncomment these two lines:
    # from gpiozero import Device
    # from gpiozero.pins.pigpio import PiGPIOFactory
    # Device.pin_factory = PiGPIOFactory()

    rover = Rover(R_MOTOR_IN1, R_MOTOR_IN2, L_MOTOR_IN1, L_MOTOR_IN2)

    rover.forward(1)
    sleep(2)

    rover.right(0.8)
    sleep(2)

    rover.left(0.8)
    sleep(2)

    rover.backward(1)
    sleep(2)

    rover.stop()