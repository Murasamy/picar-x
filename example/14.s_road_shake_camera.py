from picarx import Picarx
import time
from time import sleep
from robot_hat import Music,TTS
import readchar
from os import geteuid

POWER = 50
DangerDistance = 25 # > 20 && < 40 turn around, 
                    # < 20 backward

music = Music()
tts = TTS()
music.music_set_volume(20)
print("Press 'q' to exit")

def main():
    try:
        px = Picarx()
        # px = Picarx(ultrasonic_pins=['D2','D3']) # tring, echo
        # music.music_play('../musics/slow-trail-Ahjay_Stelino.mp3')
       
        while True:
            distance = round(px.ultrasonic.read(), 2)
            print("distance: ",distance)
            if distance <=  DangerDistance: 

                px.stop()
                music.music_stop()
                break
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
        music.music_stop()
        


if __name__ == "__main__":
    main()