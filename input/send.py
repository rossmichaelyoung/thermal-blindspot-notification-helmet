import socket
import time
import board
import busio
import adafruit_mlx90640

serverMACAddress = 'B8:27:EB:FE:88:6E' # sending data to the pi zero
port = 1
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,port))

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)

mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C", [hex(i) for i in mlx.serial_number])

'''
Refresh Rates
REFRESH_0_5_HZ
REFRESH_1_HZ
REFRESH_2_HZ
REFRESH_4_HZ
REFRESH_8_HZ
REFRESH_16_HZ
REFRESH_32_HZ
REFRESH_64_HZ
'''
# could not go higher than 2_HZ without errors
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
frame = [0] * 768
try:
    while True:
        try:
            mlx.getFrame(frame)
        except ValueError:
            # these happen, no biggie - retry
            continue
        
        num_cycles = "4"
        found_right = False
        found_left = False
        can_break = False
        for h in range(24):
            for w in range(32):
                t = frame[h*32 + w]
                if t >= 30:
                    # using height instead of width because camera is fitted sideways on helmet
                    if h >= 0 and h <= 11:
                        found_right = True
                        h = 11
                        break
                    else:
                        found_left = True
                        can_break = True
                        break

            if can_break:
                break
        
        if found_right or found_left:
            text = ""
            if found_right and found_left:
                text = "center " + num_cycles
            elif found_right:
                text = "right " + num_cycles
            else:
                text = "left " + num_cycles
            s.send(bytes(text, 'UTF-8'))
            cycle_length = 0.5
            sleep_time = int(num_cycles) * cycle_length
            time.sleep(sleep_time)


except KeyboardInterrupt:
    print("Ctrl-C Pressed: Exiting Program")

s.close()