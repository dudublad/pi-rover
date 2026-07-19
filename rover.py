from gpiozero import motor
from gpio_pins import GPIO_Pins

class Rover:

    def __init__(self, in1R, in2R, in1L, in2L, enableR=None, enableL=None):
        self._motorR = Motor(forward=in1R, backward=in2R, enable=enableR, pwm=True)
        self._motorL = Motor(forward=in1L, backward=in2L, enable=enableL, pwm=True)

    def forward(speed):
        self._motorR.forward(speed)
        self._motorL.forward(speed)

    def backward(speed):
        self._motorR.backward(speed)
        self._motorL.backward(speed)

    def stop():
        self._motorR.stop()
        self._motorL.stop()


if __name__ == "__main__":
    from time import sleep
 
    # For hardware-timed PWM on a Pi 4 or older, uncomment these two lines:
    # from gpiozero import Device
    # from gpiozero.pins.pigpio import PiGPIOFactory
    # Device.pin_factory = PiGPIOFactory()

    Rover rover(GPIO_Pins.R_MOTOR_IN1, GPIO_Pins.R_MOTOR_IN2, GPIO_Pins.L_MOTOR_IN1, GPIO_Pins.L_MOTOR_IN2)
    rover.forward(1)
    sleep(2)
    rover.backward(1)
    sleep(2)
    motor.stop()