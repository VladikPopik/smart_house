import RPi.GPIO as GPIO
import time

pin = 32

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN)

def measure(time_to_cycle, start_time):
    cycle_time = time.time()
    while GPIO.input(pin) == 1:
        curr_time = time.time()
        if curr_time - cycle_time > time_to_cycle:
            break

    pulse_start = time.time()
    while GPIO.input(pin) == 0:
        curr_time = time.time()
        if curr_time - pulse_start > time_to_cycle:
            break
    
    pulse_end = time.time()
    
    pulse_duration = pulse_end - pulse_start
    total_duration = pulse_end - cycle_time
    
    duty_cycle = int(pulse_duration / total_duration * 100)
    
    return duty_cycle

try:
    time_to_cycle = 1
    start_time = time.time()
    while True:
        duty_cycle = measure(time_to_cycle, start_time)
        print(f"Освещенность: {duty_cycle}%")
        time.sleep(0.1)
finally:
    GPIO.cleanup()