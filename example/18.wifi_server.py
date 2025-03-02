import socket
from picarx import Picarx
from time import sleep
import readchar

HOST = "192.168.119.171" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)
px = Picarx()

def Keyborad_control(key):
    global power_val
    print("key[0],key[1],key",key[0],key[1],key)

    if key == b'87':
        px.set_dir_servo_angle(0)
        px.forward(80)
        sleep(0.1)
    elif key == b'65':
        px.set_dir_servo_angle(0)
        px.backward(80)      
    elif key == b'83':
        px.set_dir_servo_angle(-30)
        px.forward(80)
    elif key == b'68':
        px.set_dir_servo_angle(30)
        px.forward(80)
    else:
        px.stop()
        
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                print(data)     
                client.sendall(data) # Echo back to client
    except: 
        print("Closing socket")
        client.close()
        s.close()    