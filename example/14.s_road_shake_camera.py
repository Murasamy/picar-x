from picarx import Picarx
import time

POWER = 50
DangerDistance = 25 # > 20 && < 40 turn around, 
                    # < 20 backward

def main():
    try:
        px = Picarx()
        # px = Picarx(ultrasonic_pins=['D2','D3']) # tring, echo       
        while True:
            distance = round(px.ultrasonic.read(), 2)
            print("distance: ",distance)
            if distance <=  DangerDistance: 
                px.stop()
            # test motor
            px.forward(30)
            time.sleep(0.5)
            # test direction servo
            for angle in range(0, 35):
                px.set_dir_servo_angle(angle)
                time.sleep(0.01)
            for angle in range(35, -35, -1):
                px.set_dir_servo_angle(angle)
                time.sleep(0.01)
            for angle in range(-35, 0):
                px.set_dir_servo_angle(angle)
                time.sleep(0.01)
   

    finally:
        px.stop()
        time.sleep(0.2)
        


if __name__ == "__main__":
    main()