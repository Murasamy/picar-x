from picarx import Picarx
import time

from time import sleep
from robot_hat import Music,TTS
import readchar
from os import geteuid

if geteuid() != 0:
    print(f"\033[0;33m{'The program needs to be run using sudo, otherwise there may be no sound.'}\033[0m")

music = Music()
tts = TTS()

POWER = 50

DangerDistance = 25 # > 20 && < 40 turn around, 
                    # < 20 backward
counter = 0

def play_music():
    print("play music")
    flag_bgm = False
    music.music_set_volume(20)
    tts.lang("en-US")

    while True:
        key = readchar.readkey()
        key = key.lower()
        if key == "q":
            flag_bgm = not flag_bgm
            if flag_bgm is True:
                print('Play Music')
                music.music_play('../musics/Chopin-Nocturne.mp3')
            else:
                print('Stop Music')
                music.music_stop()

        elif key == readchar.key.SPACE:
            print('Beep beep beep !')
            music.sound_play('../sounds/car-double-horn.wav')
            sleep(0.05)

        elif key == "c":
            print('Beep beep beep !')
            music.sound_play_threading('../sounds/car-double-horn.wav')
            sleep(0.05)

        elif key == "t":
            words = "Hello"
            print(f'{words}')
            tts.say(words)


def main():
    global counter
    try:
        px = Picarx()
        # px = Picarx(ultrasonic_pins=['D2','D3']) # tring, echo       
        while True:
            distance = round(px.ultrasonic.read(), 2)
            print("distance: ",distance)
            if distance <=  DangerDistance: 
                counter += 1
            if counter >= 2:
                print('play_music')
                px.stop()
                play_music()
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
        


if __name__ == "__main__":
    main()