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
        
        found = False
        for h in range(24):
            for w in range(32):
                t = frame[h*32 + w]
                if t >= 30:
                    text = ""
                    if w >= 0 and h <= 9:
                        text = "right 3"
                    elif w >= 10 and h <= 21:
                        text = "center 3"
                    else:
                        text = "left 3"
                    s.send(bytes(text, 'UTF-8'))
                    found = True
                    time.sleep(2)
                    break

            if found:
                break

except KeyboardInterrupt:
    print("Ctrl-C Pressed: Exiting Program")

s.close()