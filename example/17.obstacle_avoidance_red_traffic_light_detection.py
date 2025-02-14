# Part of the code is from https://github.com/Murasamy/vilib/blob/picamera2/examples/traffic_sign_detect.py

from picarx import Picarx
import time
from vilib import Vilib
from time import sleep

POWER = 200
SafeDistance = 40   # > 40 safe
DangerDistance = 25 # > 20 && < 40 turn around, 
                    # < 20 backward

'''
Vilib.traffic_detect_switch(flag=True)     # True / False

Vilib.traffic_sign_obj_parameter['x']       # the largest traffic sign block center x-axis coordinate
Vilib.traffic_sign_obj_parameter['y']       # the largest traffic sign block center y-axis coordinate
Vilib.traffic_sign_obj_parameter['w']       # the largest traffic sign block pixel width
Vilib.traffic_sign_obj_parameter['h']       # the largest traffic sign block pixel height
Vilib.traffic_sign_obj_parameter['t']       # traffic sign text, could be: 'none', 'stop','right','left','forward'
Vilib.traffic_sign_obj_parameter['acc']     # accuracy
  
'''



def main():
    try:
        px = Picarx()
        # px = Picarx(ultrasonic_pins=['D2','D3']) # tring, echo
        Vilib.camera_start(vflip=False, hflip=False) # size=(640,, 480)
        Vilib.show_fps()
        Vilib.display(local=True, web=True)
        Vilib.color_detect(color="red")  # red, green, blue, yellow , orange, purple
        sleep(1)

        last_camera_detection_time = time.time()
        camera_detection_interval = 1  # seconds

       
        while True:
            distance = round(px.ultrasonic.read(), 2)
            print("distance: ", distance)
            
            current_time = time.time()
            if current_time - last_camera_detection_time >= camera_detection_interval:
                last_camera_detection_time = current_time
                n = Vilib.color_obj_parameter['n']
                color = Vilib.color_obj_parameter['color']
                
                if n != 0: # traffic sign detected
                    x = Vilib.color_obj_parameter['x']
                    y = Vilib.color_obj_parameter['y']
                    w = Vilib.color_obj_parameter['w']
                    h = Vilib.color_obj_parameter['h']
                    print(f"stop traffic sign detected, x: {x}, y: {y}, w: {w}, h: {h}")
                    px.stop()

            if distance >= SafeDistance:
                px.set_dir_servo_angle(0)
                px.forward(POWER)
            elif distance >= DangerDistance:
                px.set_dir_servo_angle(30)
                px.forward(POWER)
                time.sleep(0.1)
            else:
                px.set_dir_servo_angle(-30)
                px.backward(POWER)
                time.sleep(0.8)
    finally:
        px.forward(0)


if __name__ == "__main__":
    main()
