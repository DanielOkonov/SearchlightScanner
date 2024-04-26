import os

class SoundManager:
    def __init__(self):
        self.sounds = {
            "default": "../sounds/beep.mp3",
            "powerline": "../sounds/Alarm__Missile_Jettison.ogg.mp3"
        }

    async def play_sound(self, detections):
        if detections:
            sound = self.sounds["default"]
            for detection in detections:
                if detection.label == 5:
                    sound = self.sounds["powerline"]
                    break
            os.system(f"mpg123 {sound}")