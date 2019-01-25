import os
import socket

os.system('sudo sdptool add --channel=22 SP')
hostMACAddress = 'B8:27:EB:B7:6D:62'  # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 22  # 3 is an arbitrary choice. However, it must match the port used by the client.
backlog = 1
size = 1024

connection = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
connection.bind((hostMACAddress, port))
connection.listen(backlog)
print("got to this point")

try:
    client, address = connection.accept()
    print(client)
    print(address)
    print('Waiting for data')
    while 1:
        data = client.recv(size)
        client.send(bytes('this is a test', encoding='utf-8'))
        if data:
            message = data.decode('utf-8')
            print(message)
except socket.timeout:
    print("Closing socket Timed out!")
    if client:
        client.close()
    connection.close()
except socket.error:
    print("Closing socket")
    if client:
        client.close()
    connection.close()
except KeyboardInterrupt:
    print("Closing socket KeyboardInterrupt")
    if client:
        client.close()
    connection.close()
