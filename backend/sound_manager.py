import os
import time

class SoundManager:
    def __init__(self):
        self.sounds = {
            "default": "/home/sar/SearchlightScanner-dev/sounds/beep.mp3",
            "powerline": "/home/sar/SearchlightScanner-dev/sounds/Alarm__Missile_Jettison.ogg.mp3"
        }
        self.last_play_time = 0
        self.cooldown = 0

    def play_sound(self, detections):
        # check if enough time has passed since last sound
        if time.time() - self.last_play_time < self.cooldown:
            return

        # play sound based on detections
        if detections:
            sound = self.sounds["default"]
            self.cooldown = 2
            for detection in detections:
                if detection.label == 5:
                    sound = self.sounds["powerline"]
                    self.cooldown = 9
                    break
            os.system(f"mpg123 {sound} > /dev/null 2>&1")
            self.last_play_time = time.time()