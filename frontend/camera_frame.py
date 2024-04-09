import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font as tkFont
from .settings1 import CustomSlider
from backend.image_processor import ImageProcessor


class MainFrame(tk.Frame):
    def __init__(self, parent, gps_manager, camera_feed, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg="#7C889C")
        self.parent = parent
        self.gps_manager = gps_manager
        self.camera_feed = camera_feed
        self.create_widgets()
        self.ai = ImageProcessor()

    def update_confidence(self, value):
        value = int(round(value))
        self.confidence_label.config(text=f"CONFIDENCE: {value}%")

    def create_widgets(self):
        # Camera feed label
        self.camera_label = tk.Label(self, bg="black")
        self.camera_label.grid(row=0, column=0, sticky="nws")
        self.camera_label.grid_propagate(False)

        # Flag to control camera updates
        self.update_camera = False

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        custom_font = tkFont.Font(family="Helvetica", size=12, weight="bold")

        # Menu options frame
        self.menu_options_frame = tk.Frame(self, bg="#7C889C", width=1000, height=180)
        self.menu_options_frame.grid(row=1, column=0, sticky="sw", padx=3)

        # Settings frame and button
        self.settings_button_frame = tk.Frame(
            self.menu_options_frame, bg="#7C889C", width=275, height=80
        )
        self.settings_button_frame.grid(row=0, column=0, sticky="sw", padx=3)
        self.settings_button_frame.grid_propagate(False)

        self.settings_button = tk.Button(
            self.settings_button_frame,
            bg="#24D215",
            fg="white",
            text="SETTINGS",
            font=custom_font,
            width=25,
            height=3,
            command=self.on_settings_click,
        )
        self.settings_button.grid(pady=5, padx=5)

        # Confidence frame and slider
        self.confidence_slider_frame = tk.Frame(
            self.menu_options_frame,
            bg="#7C889C",
            width=400,
            height=68,
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=2,
        )
        self.confidence_slider_frame.grid(
            row=0, column=1, sticky="nsew", padx=3, pady=4
        )
        self.confidence_slider_frame.grid_propagate(False)

        self.confidence_label = tk.Label(
            self.confidence_slider_frame,
            text="CONFIDENCE: 0%",
            bg="#7C889C",
            fg="black",
            font=custom_font,
        )
        self.confidence_label.grid(row=0, column=0, sticky="nsw", pady=10)

        self.confidence_slider = CustomSlider(
            self.confidence_slider_frame,
            id="confidence_slider",
            length=180,
            width=50,
            handle_size=30,
            bar_thickness=30,
            bg="#7C889C",
            min_val=0,
            max_val=100,
            callback=self.update_confidence,
        )
        self.confidence_slider.grid(row=0, column=0, padx=195, sticky="nse", pady=10)

        # GPS frame and output
        self.gps_frame = tk.Frame(
            self.menu_options_frame,
            bg="#7C889C",
            width=400,
            height=68,
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=2,
        )
        self.gps_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=4)
        self.gps_frame.grid_propagate(False)

        self.gps_lat_long = tk.Label(
            self.gps_frame,
            text="LAT/LONG: ",
            bg="#7C889C",
            fg="black",
            font=custom_font,
        )
        self.gps_lat_long.place(x=2, y=2)

        self.gps_bearing = tk.Label(
            self.gps_frame, text="BEARING: ", bg="#7C889C", fg="black", font=custom_font
        )
        self.gps_bearing.place(x=255, y=2)

        self.gps_speed = tk.Label(
            self.gps_frame, text="SPEED: ", bg="#7C889C", fg="black", font=custom_font
        )
        self.gps_speed.place(x=2, y=40)

        self.gps_altitude = tk.Label(
            self.gps_frame,
            text="ALTITUDE: ",
            bg="#7C889C",
            fg="black",
            font=custom_font,
        )
        self.gps_altitude.place(x=235, y=40)
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
                # convert the image to cuda

                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.camera_label.config(image=self.photo)
                self.camera_label.image = self.photo  # Keep a reference to the image
            self.after(10, self.update_frame)

    def start_gps_thread(self):
        self.gps_manager.start()
        self.update_gps_data()

    def update_gps_data(self):
        # Update GPS coordinates
        try:
            coords = self.gps_manager.get_coords()  # Get the latest valid coordinates
            self.gps_lat_long.config(text=f"LAT/LONG: {coords}")
        except ValueError:
            pass  # Handle if no valid coordinates yet

        # Update Altitude
        try:
            altitude = self.gps_manager.get_latest_altitude()
            self.gps_altitude.config(text=f"ALTITUDE: {altitude} FT")
        except ValueError:
            pass  # Handle if no valid altitude yet

        # Update Speed
        try:
            speed = self.gps_manager.get_latest_speed()
            self.gps_speed.config(text=f"SPEED: {speed} M/S")
        except ValueError:
            pass  # Handle if no valid speed yet

        # Update Bearing
        try:
            bearing = self.gps_manager.get_latest_bearing()
            self.gps_bearing.config(text=f"BEARING: {bearing}°")
        except ValueError:
            pass  # Handle if no valid bearing yet

        # Schedule the next update
        self.after(1000, self.update_gps_data)  # Update every second

    def on_settings_click(self):
        self.parent.switch_settings1()
