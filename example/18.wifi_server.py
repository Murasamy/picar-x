import socket
from picarx import Picarx
from time import sleep
import readchar
import sys
import subprocess
import os
import json

HOST = "192.168.119.171" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)
px = Picarx()

def cpu_temperature():
    raw_cpu_temperature = subprocess.getoutput("cat /sys/class/thermal/thermal_zone0/temp")
    cpu_temperature = round(float(raw_cpu_temperature)/1000,2)               # convert unit
    print("cpu_temperature:", cpu_temperature)
    return cpu_temperature

def gpu_temperature():
    raw_gpu_temperature = subprocess.getoutput( 'vcgencmd measure_temp' )
    gpu_temperature = round(float(raw_gpu_temperature.replace( 'temp=', '' ).replace( '\'C', '' )), 2)
    print("gpu_temperature:", gpu_temperature)
    return gpu_temperature

# def cpu_usage():
#     result = os.popen("mpstat").read().strip()
#     result = result.split('\n')[-1].split(' ')[-1]
#     result = round(100 - float(result), 2)
#     result = str(result)
#     return result

def disk_space():               # disk_space
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()         
        if i==2:
            return line.split()[1:5]    

def ram_info():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return list(map(lambda x:round(int(x) / 1000,1), line.split()[1:4]))   

def pi_read():
    result = {
        "cpu_temperature": cpu_temperature(), 
        "gpu_temperature": gpu_temperature(),
        # "cpu_usage": cpu_usage(), 
        "disk": disk_space(), 
        "ram": ram_info(), 
    }
    result = json.dumps(result)
    return result 

def Keyborad_control(key):
    global power_val
    global pan_angle
    global tilt_angle
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
            # print("server recv from: ", clientInfo)
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                # print(data)     
                Keyborad_control(data)
                # client.sendall(data) # Echo back to client
                print("pi_read:", pi_read())
                client.sendall(pi_read().encode())
                client.close()
    except:

        print("Closing socket")
        # print error message
        print("Unexpected error:", sys.exc_info())
        client.close()
        s.close()  
    finally:
        px.set_cam_tilt_angle(0)
        px.set_cam_pan_angle(0)  
        px.set_dir_servo_angle(0)  
        px.stop()
        sleep(.2)
