import tkinter as tk
from camera_frame import MainFrame
from settings2 import SettingsFrame

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SearchLightScanner")
        self.configure(bg='#7C889C')
        self.state('zoomed')

        self.frames = {}
        for F in (MainFrame, SettingsFrame):
            frame = F(self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.switch_frame(MainFrame)

    def switch_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
