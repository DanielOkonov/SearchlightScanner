import tkinter as tk
from tkinter import font as tkFont

class MainFrame(tk.Frame):
    def __init__(self, parent, show_settings_callback, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg='#7C889C')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        custom_font = tkFont.Font(family="Helvetica", size=12, weight="bold")

        #############################################################################################################
        #SETTINGS BUTTON FRAME

        self.settings_button_frame = tk.Frame(self, bg='#7C889C', width=275, height=80)
        self.settings_button_frame.grid(row=1, column=0, sticky='sw', pady=3, padx=3)
        self.settings_button_frame.grid_propagate(False)

        self.settings_button = tk.Button(self.settings_button_frame, bg='green', text="SETTINGS",
                                         font=custom_font,
                                         width=25,
                                         height=3,
                                         command=show_settings_callback)
        self.settings_button.grid(pady=5, padx=5)

