import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

# Setup GPIO Pins
GPIO.setup(12, GPIO.OUT)

# Set PWM instance and their frequency
pwm8 = GPIO.PWM(12, 8000)

# Start PWM with 50% Duty Cycle
pwm8.start(100)

raw_input('Press return to stop:')	#Wait

# Stops the PWM
pwm8.stop()

# Cleans the GPIO
GPIO.cleanup()
