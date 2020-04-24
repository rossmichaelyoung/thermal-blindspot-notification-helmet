import socket
import vibration_motors

hostMACAddress = 'B8:27:EB:FE:88:6E' # The MAC address of a Bluetooth adapter on the server aka the pi zero.
port = 1
backlog = 1
size = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)
try:
    client, address = s.accept()
    while True:
        data = client.recv(size)
        if data:
            print(data)
            info = data.split()
            direction = chr(info[0])
            num_cycles = int(info[1])
            print(direction)
            print(num_cycles)
            #vibration_motors.alert(data)
except RuntimeError as e:
    print("Closing socket")
    vibration_motors.clean_up()
    client.close()
    s.close()
    print(e)