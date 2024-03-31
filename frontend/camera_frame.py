import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font as tkFont
from settings1 import CustomSlider

class MainFrame(tk.Frame):
    def __init__(self, parent, gps_manager, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg="#7C889C")
        self.parent = parent
        self.gps_manager = gps_manager
        self.create_widgets()

    def update_confidence(self, value):
        value = int(round(value))
        self.confidence_label.config(text=f"CONFIDENCE: {value}%")

    def create_widgets(self):
        # Camera feed label
        self.camera_label = tk.Label(self, bg='black')
        self.camera_label.grid(row=0, column=0, sticky='nws')
        self.camera_label.grid_propagate(False)

        # Flag to control camera updates
        self.update_camera = False

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        custom_font = tkFont.Font(family="Helvetica", size=12, weight="bold")

        # Menu options frame
        self.menu_options_frame = tk.Frame(self, bg='#7C889C', width=1000, height=180)
        self.menu_options_frame.grid(row=1, column=0, sticky='sw', padx=3)

        # Settings frame and button
        self.settings_button_frame = tk.Frame(self.menu_options_frame, bg='#7C889C', width=275, height=80)
        self.settings_button_frame.grid(row=0, column=0, sticky='sw', padx=3)
        self.settings_button_frame.grid_propagate(False)

        self.settings_button = tk.Button(
            self.settings_button_frame,
            bg="#24D215",
            fg="white",
            text="SETTINGS",
            font=custom_font,
            width=25,
            height=3,
            command=self.on_settings_click
        )
        self.settings_button.grid(pady=5, padx=5)

        # Confidence frame and slider
        self.confidence_slider_frame = tk.Frame(self.menu_options_frame, bg='#7C889C', width= 400, height= 68, highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.confidence_slider_frame.grid(row=0, column=1, sticky= 'nsew', padx=3, pady=4)
        self.confidence_slider_frame.grid_propagate(False)

        self.confidence_label = tk.Label(self.confidence_slider_frame, text="CONFIDENCE: 0%", bg="#7C889C", fg="black", font=custom_font)
        self.confidence_label.grid(row=0, column=0, sticky='nsw', pady=10)

        self.confidence_slider = CustomSlider(self.confidence_slider_frame, id='confidence_slider', length=180, width=50, handle_size=30, bar_thickness=30, bg="#7C889C", min_val=0, max_val=100, callback=self.update_confidence)
        self.confidence_slider.grid(row=0, column=0, padx=195, sticky='nse', pady=10)

        # GPS frame and output
        self.gps_frame = tk.Frame(self.menu_options_frame, bg='#7C889C', width=400, height=68, highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.gps_frame.grid(row=0, column=2, sticky='nsew', padx=10, pady=4)
        self.gps_frame.grid_propagate(False)

        self.gps_coordinates = tk.Label(self.gps_frame, text="CURRENT COORDINATES: ", bg="#7C889C", fg="black", font=custom_font)
        self.gps_coordinates.grid(row=0, column=0, sticky='nsw', pady=10)
        self.start_gps_thread()

    # Camera methods
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

    def start_gps_thread(self):
        self.gps_manager.start()
        self.update_gps_coordinates()

    def update_gps_coordinates(self):
        # Check if GPS has valid coordinates and update label
        try:
            coords = self.gps_manager.get_coords()  # Attempt to get the latest valid coordinates
            if coords:
                self.gps_coordinates.config(text=f"CURRENT COORDINATES: \n {coords}")
        except ValueError:
            pass  # If no valid coordinates, do nothing
        
        # Schedule the next coordinates update
        self.after(1000, self.update_gps_coordinates)  # Update every second

    def on_settings_click(self):
        self.parent.switch_settings1()

