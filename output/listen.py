import socket
import vibration_motors

hostMACAddress = 'DC:A6:32:6D:8B:D4' # The MAC address of a Bluetooth adapter on the server.
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
            #vibration_motors.alert(data)
            #client.send(data)
except:	
    print("Closing socket")
    vibration_motors.clean_up()
    client.close()
    s.close()