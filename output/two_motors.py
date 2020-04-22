import RPi.GPIO as GPIO
import time
import threading

left_motor = 23
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

# print_cycle prints out which motor would be actived but does not activate it      
def print_cycle(motor, num_cycles):
    for i in range(0, num_cycles):
        print(motor)
        
def alert(direction, num_cycles):
    if direction == "left":
        #cycle(left_motor, num_cycles)
        print_cycle(left_motor, num_cycles)
    elif direction == "right":
        #cycle(right_motor, num_cycles)
        print_cycle(right_motor, num_cycles)
    elif direction == "center":
        #t1 = threading.Thread(target=cycle, args=(left_motor, num_cycles,))
        #t2 = threading.Thread(target=cycle, args=(right_motor, num_cycles,))
        t1 = threading.Thread(target=print_cycle, args=(left_motor, num_cycles,))
        t2 = threading.Thread(target=print_cycle, args=(right_motor, num_cycles,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    else:
        print("Direction not valid")
   
try:
    while True:
        direction = input("Enter direction of input: ")
        num_cycles = int(input("Enter number of cycles: "))
        alert(direction, num_cycles)
        
except KeyboardInterrupt:
    print("Ctrl-C Pressed: Exiting Program")

GPIO.cleanup()