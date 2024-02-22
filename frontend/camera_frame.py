import tkinter as tk
from tkinter import font as tkFont
from settings2 import SettingsFrame

class MainFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg='#7C889C')  # Set a background color for the frame

        # Ensure the main frame expands to fill the root window
        self.grid_rowconfigure(0, weight=1)  # Make all other rows expandable except the last one
        self.grid_columnconfigure(0, weight=1)  # Make the column expandable

        # Create a custom font for the button
        custom_font = tkFont.Font(family="Helvetica", size=12, weight="bold")

        # Create a frame for the settings button with specified dimensions
        self.settings_button_frame = tk.Frame(self, bg='#7C889C', width=275, height=80)
        # Place it at the bottom left using 'sw', ensure it doesn't shrink or expand
        self.settings_button_frame.grid(row=1, column=0, sticky='sw', pady=3, padx=3)
        self.settings_button_frame.grid_propagate(False)  # Prevent frame from resizing to content

        # Create the settings button
        self.settings_button = tk.Button(self.settings_button_frame, bg='green', text="SETTINGS",
                                         font=custom_font,
                                         width=25,
                                         height=3,
                                         command=self.on_settings_click)
        # Position the button within the frame
        self.settings_button.grid(pady=5, padx=5)

    def on_settings_click(self):
        self.master.switch_frame(SettingsFrame)
