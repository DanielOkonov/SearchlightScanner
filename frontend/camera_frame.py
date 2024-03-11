import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font as tkFont

class MainFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg="#7C889C")
        self.parent = parent

        # Camera feed label
        self.camera_label = tk.Label(self, bg='black')
        self.camera_label.grid(row=0, column=0, sticky='nsew')

        # Flag to control camera updates
        self.update_camera = False

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        custom_font = tkFont.Font(family="Helvetica", size=12, weight="bold")

        self.settings_button_frame = tk.Frame(self, bg='#7C889C', width=275, height=80)
        self.settings_button_frame.grid(row=1, column=0, sticky='sw', pady=3, padx=3)
        self.settings_button_frame.grid_propagate(False)

        self.settings_button = tk.Button(
            self.settings_button_frame,
            bg="green",
            text="SETTINGS",
            font=custom_font,
            width=25,
            height=3,
            command=self.on_settings_click
        )
        self.settings_button.grid(pady=5, padx=5)

    def start_camera_feed(self):
        self.update_camera = True
        self.update_frame()

    def stop_camera_feed(self):
        self.update_camera = False

    def update_frame(self):
        if self.update_camera:
            frame = self.parent.camera_feed.get_frame()
            if frame is not None:
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.camera_label.config(image=self.photo)
                self.camera_label.image = self.photo  # Keep a reference to the image
            self.after(10, self.update_frame)

    def on_settings_click(self):
        self.parent.switch_settings1()
