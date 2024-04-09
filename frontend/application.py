from camera_frame import MainFrame
from settings1 import SettingsFrame1
from settings2 import SettingsFrame2
import tkinter as tk
import cv2
import os
import sys
import platform

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

from backend.gps_manager import GPSManager 

class CameraFeed:
    def __init__(self, video_source=0):
        # Initialize the video capture with the default source
        self.set_video_source(video_source)

    def set_video_source(self, video_source):
        # Release the current capture if it's open
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()

        # Update the video source and create a new capture object
        self.video_source = video_source
        self.cap = cv2.VideoCapture(video_source)

        # These are the resolutions that should be used on the scanner
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) 

        # Resolutions used for testing on laptop webcam
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

        if not self.cap.isOpened():
            raise ValueError("Unable to open video source", video_source)

    def get_frame(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                # Convert the color space from BGR to RGB
                return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return None

    def release(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SearchLightScanner")
        self.configure(bg='#7C889C')
        self.bind("<Escape>", self.minimize_window)
        self.maximize_window()

        # self.camera_feed = CameraFeed()  # Initialize CameraFeed
        # Set default camera to /dev/video0
        self.camera_feed = CameraFeed(video_source=0)

        self.gps_manager = GPSManager() # Initialize GPS device

        self.frames = {}
        for F in (MainFrame, SettingsFrame1, SettingsFrame2):
            if F == MainFrame:
                frame = F(self, self.gps_manager, self.camera_feed)
            elif F == SettingsFrame1:
                frame = F(self, self.camera_feed)  # Assuming SettingsFrame1 also modified to accept camera_feed
            else:
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
        # self.frames[SettingsFrame1] = SettingsFrame1(self, self.camera_feed)
        self.switch_frame(SettingsFrame1)

    def switch_settings2(self):
        self.switch_frame(SettingsFrame2)

    def switch_main_frame(self):
        self.switch_frame(MainFrame)

    def maximize_window(self):
        if platform.system() == "Linux":
            self.attributes('-fullscreen', True)
        elif platform.system() == "Windows":
            self.state('zoomed')
        else:
            self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))

    def minimize_window(self, event=None):
        self.iconify()

    def on_close(self):
        if hasattr(self, 'gps_manager'):
            self.gps_manager.stop()  # Stop the GPS manager
        self.frames[MainFrame].stop_camera_feed()
        self.camera_feed.release()  # Release the camera resource
        self.destroy()

if __name__ == "__main__":
    app = Application()
    app.protocol("WM_DELETE_WINDOW", app.on_close)  # Ensure clean exit
    app.mainloop()
