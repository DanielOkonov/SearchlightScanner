import tkinter as tk
from camera_frame import MainFrame
from settings2 import SettingsFrame

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SearchLightScanner")
        self.configure(bg='#7C889C')

        # self.state('zoomed')
        self.maximize_window()

        self.frames = {}
        self.create_frames()
        self.switch_frame(MainFrame)

    def switch_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

    def create_frames(self):
        main_frame = MainFrame(self, self.show_settings_frame)
        self.frames[MainFrame] = main_frame

        settings_frame = SettingsFrame(self, self.show_main_frame)
        self.frames[SettingsFrame] = settings_frame

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def show_main_frame(self):
        self.switch_frame(MainFrame)

    def show_settings_frame(self):
        self.switch_frame(SettingsFrame)

    def maximize_window(self):
        try:
            # For Linux, use the '-zoomed' attribute
            self.attributes('-zoomed', True)
        except Exception:
            # For Windows, set the window state to 'normal' and then maximize
            self.state('normal')
            self.wm_state('zoomed')

if __name__ == "__main__":
    app = Application()
    app.mainloop()
