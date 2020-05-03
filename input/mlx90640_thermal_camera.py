import time
import board
import busio
import adafruit_mlx90640

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
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ

frame = [0] * 768
try:
    while True:
        try:
            mlx.getFrame(frame)
        except ValueError:
            # these happen, no biggie - retry
            continue

        for h in range(24):
            for w in range(32):
                t = frame[h*32 + w]
                #print("%0.1f, " % t, end="")
                if t > 33:
                    print("human detected!")
            print()
        print()

except KeyboardInterrupt:
    print("Ctrl-C Pressed: Exiting Program")