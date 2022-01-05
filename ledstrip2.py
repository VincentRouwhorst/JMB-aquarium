import RPi.GPIO as GPIO
import time

# Setup Raspberry Pi PWM pins
GPIO.setmode(GPIO.BOARD)

# Setup GPIO Pins
GPIO.setup(12, GPIO.OUT)
#GPIO.setup(32, GPIO.OUT)
#GPIO.setup(33, GPIO.OUT)
#GPIO.setup(35, GPIO.OUT)

# Set PWM instance and their frequency
pwm12 = GPIO.PWM(12, 400)
#pwm32 = GPIO.PWM(32, 400)
#pwm33 = GPIO.PWM(33, 400)
#pwm35 = GPIO.PWM(35, 400)

# Start PWM with 0% Duty Cycle, OFF state
pwm12.start(0)
#pwm32.start(0)
#pwm33.start(0)
#pwm35.start(0)

try:
  while True:
    for dutyCycle in range (0, 100, 1):
      pwm12.ChangeDutyCycle(dutyCycle)
      #pwm32.ChangeDutyCycle(100-dutyCycle)
      #pwm33.ChangeDutyCycle(dutyCycle)
      #pwm35.ChangeDutyCycle(100-dutyCycle)
      time.sleep(0.5)
      print(dutyCycle)
      if dutyCycle == 0:
         time.sleep(10)
         print("sleep A 10 seconds")

    for dutyCycle in range (100, 0, -1):
      pwm12.ChangeDutyCycle(dutyCycle)
      #pwm32.ChangeDutyCycle(100-dutyCycle)
      #pwm33.ChangeDutyCycle(dutyCycle)
      #pwm35.ChangeDutyCycle(100-dutyCycle)
      time.sleep(0.5)
      print(dutyCycle)
      if dutyCycle == 100:
         time.sleep(10)
         print("sleep B 10 seconds")

except KeyboardInterrupt:
  pwm12.stop()
  #pwm32.stop()
  #pwm33.stop()
  #pwm35.stop()

# Cleans the GPIO
GPIO.cleanup()
