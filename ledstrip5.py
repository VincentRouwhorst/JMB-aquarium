import pigpio
import time

LED=18
pi = pigpio.pi()
dc=1000000
pi.hardware_PWM(LED, 200, dc)
time.sleep(1)

print(">>Go<<")

#pi.hardware_PWM(18, 800, 250000) # 800Hz 25% dutycycle
#pi.hardware_PWM(18, 2000, 750000) # 2000Hz 75% dutycycle


while 1:
   pi.hardware_PWM(LED,200,dc)
   time.sleep(1)
