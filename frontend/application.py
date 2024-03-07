import tkinter as tk
from camera_frame import MainFrame
from settings1 import SettingsFrame1
from settings2 import SettingsFrame2


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SearchLightScanner")

        self.configure(bg='#7C889C')

        self.maximize_window()

        self.frames = {}
        for F in (MainFrame, SettingsFrame1, SettingsFrame2):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.switch_frame(MainFrame)

    def switch_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

    def switch_settings1(self):
        self.switch_frame(SettingsFrame1)

    def switch_settings2(self):
        self.switch_frame(SettingsFrame2)

    def switch_main_frame(self):
        self.switch_frame(MainFrame)


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
