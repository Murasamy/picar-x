import socket
from picarx import Picarx
from time import sleep
import readchar
import sys

HOST = "192.168.119.171" # IP address of your Raspberry PI
PORT = 65431          # Port to listen on (non-privileged ports are > 1023)
px = Picarx()

def Keyborad_control(key):
    global power_val
    print("key[0],key[1],key",key[0],key[1],key)

    if key == b'87': # w
        px.set_dir_servo_angle(0)
        px.forward(80)
        sleep(0.5)
        px.forward(0)
    elif key == b'65': # a
        px.set_dir_servo_angle(-30)
        px.forward(80)
        sleep(0.5)  
        px.forward(0)    
    elif key == b'83': # s
        px.set_dir_servo_angle(0)
        px.backward(80)
        sleep(0.5)
        px.forward(0)
    elif key == b'68': # d
        px.set_dir_servo_angle(30)
        px.forward(80)
        sleep(0.5)
        px.forward(0)
    elif key == b'73': # i
        tilt_angle+=5
        if tilt_angle>30:
            tilt_angle=30
        px.set_cam_tilt_angle(tilt_angle)
    elif key == b'75': # k
        tilt_angle-=5
        if tilt_angle<-30:
            tilt_angle=-30
        px.set_cam_tilt_angle(tilt_angle)
    elif key == b'76': # l
        pan_angle+=5
        if pan_angle>30:
            pan_angle=30
        px.set_cam_pan_angle(pan_angle) 
    elif key == b'74': # j
        pan_angle-=5
        if pan_angle<-30:
            pan_angle=-30  
        px.set_cam_pan_angle(pan_angle)     
    
        
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        pan_angle = 0
        tilt_angle = 0
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                print(data)     
                Keyborad_control(data)
                client.sendall(data) # Echo back to client
    except:

        print("Closing socket")
        # print error message
        print("Unexpected error:", sys.exc_info()[0])
        client.close()
        s.close()  
    finally:
        px.set_cam_tilt_angle(0)
        px.set_cam_pan_angle(0)  
        px.set_dir_servo_angle(0)  
        px.stop()
        sleep(.2)
