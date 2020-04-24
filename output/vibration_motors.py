import RPi.GPIO as GPIO
import time
import threading

left_motor = 14
right_motor = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(left_motor, GPIO.OUT)
GPIO.setup(right_motor, GPIO.OUT)

def on(motor):
    GPIO.output(motor, GPIO.HIGH)
    
def off(motor):
    GPIO.output(motor, GPIO.LOW)
    
def cycle(motor, num_cycles):
    for i in range(0, num_cycles):
        on(motor)
        time.sleep(0.5)
        off(motor)
        time.sleep(0.25)
        
def alert(packet):
    info = packet[2:len(packet)-1].split()
    direction = info[0]
    num_cycles = info[1]
    if direction == "left":
        cycle(left_motor, num_cycles)
    elif direction == "right":
        cycle(right_motor, num_cycles)
    elif direction == "center":
        t1 = threading.Thread(target=cycle, args=(left_motor, num_cycles,))
        t2 = threading.Thread(target=cycle, args=(right_motor, num_cycles,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    else:
        print("Direction not valid")


def clean_up():
    GPIO.cleanup()