# import tkinter as tk
from camera_frame import MainFrame
from settings1 import SettingsFrame1
from settings2 import SettingsFrame2


# class Application(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.title("SearchLightScanner")

#         self.configure(bg='#7C889C')

#         self.maximize_window()

#         self.frames = {}
#         for F in (MainFrame, SettingsFrame1, SettingsFrame2):
#             frame = F(self)
#             self.frames[F] = frame
#             frame.grid(row=0, column=0, sticky="nsew")

#         self.switch_frame(MainFrame)

#     def switch_frame(self, frame_class):
#         frame = self.frames[frame_class]
#         frame.tkraise()

#     def switch_settings1(self):
#         self.switch_frame(SettingsFrame1)

#     def switch_settings2(self):
#         self.switch_frame(SettingsFrame2)

#     def switch_main_frame(self):
#         self.switch_frame(MainFrame)


#     def maximize_window(self):
#         try:
#             # For Linux, use the '-zoomed' attribute
#             self.attributes('-zoomed', True)
#         except Exception:
#             # For Windows, set the window state to 'normal' and then maximize
#             self.state('normal')
#             self.wm_state('zoomed')

# if __name__ == "__main__":
#     app = Application()
#     app.mainloop()


import tkinter as tk
# from tkinter import font as tkFont
# from PIL import Image, ImageTk
import cv2

# Assuming camera_frame.py, settings1.py, and settings2.py exist and contain the appropriate classes
from camera_frame import MainFrame
from settings1 import SettingsFrame1
from settings2 import SettingsFrame2

class CameraFeed:
    def __init__(self, video_source=0):
        self.video_source = video_source
        self.cap = cv2.VideoCapture(video_source)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        if not self.cap.isOpened():
            raise ValueError("Unable to open video source", video_source)

    def get_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return None

    def release(self):
        if self.cap.isOpened():
            self.cap.release()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SearchLightScanner")
        self.configure(bg='#7C889C')
        self.maximize_window()

        self.camera_feed = CameraFeed()  # Initialize CameraFeed

        self.frames = {}
        for F in (MainFrame, SettingsFrame1, SettingsFrame2):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.switch_frame(MainFrame)

    def switch_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

        # Start updating camera feed only when MainFrame is raised
        if frame_class == MainFrame:
            frame.start_camera_feed()
        else:
            self.frames[MainFrame].stop_camera_feed()

    def switch_settings1(self):
        self.switch_frame(SettingsFrame1)

    def switch_settings2(self):
        self.switch_frame(SettingsFrame2)

    def switch_main_frame(self):
        self.switch_frame(MainFrame)

    def maximize_window(self):
        try:
            self.attributes('-zoomed', True)
        except Exception:
            self.state('normal')
            self.wm_state('zoomed')

    def on_close(self):
        self.frames[MainFrame].stop_camera_feed()
        self.camera_feed.release()  # Release the camera resource
        self.destroy()

if __name__ == "__main__":
    app = Application()
    app.protocol("WM_DELETE_WINDOW", app.on_close)  # Ensure clean exit
    app.mainloop()
