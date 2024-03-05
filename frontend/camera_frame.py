import tkinter as tk
from tkinter import font as tkFont
from settings1 import SettingsFrame1


class MainFrame(tk.Frame):
    def __init__(self, parent, show_settings_callback, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg="#7C889C")

        # Ensure the main frame expands to fill the root window
        self.grid_rowconfigure(
            0, weight=1
        )  # Make all other rows expandable except the last one
        self.grid_columnconfigure(0, weight=1)  # Make the column expandable

        custom_font = tkFont.Font(family="Helvetica", size=12, weight="bold")

        self.settings_button_frame = tk.Frame(self, bg="#7C889C", width=275, height=80)
        self.settings_button_frame.grid(row=1, column=0, sticky="sw", pady=3, padx=3)
        self.settings_button_frame.grid_propagate(False)

        self.settings_button = tk.Button(
            self.settings_button_frame,
            bg="green",
            text="SETTINGS",
            font=custom_font,
            width=25,
            height=3,
            command=self.on_settings_click,
        )
        self.settings_button.grid(pady=5, padx=5)

    def on_settings_click(self):
        self.master.switch_frame(SettingsFrame1)
