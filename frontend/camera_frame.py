import tkinter as tk
from PIL import Image, ImageTk
from tkinter import font as tkFont

from .shared_confidence_controller import shared_confidence
from .settings1 import CustomSlider
from backend.image_processor import ImageProcessor


class MainFrame(tk.Frame):
    def __init__(self, parent, gps_manager, camera_feed, color_scheme, **kwargs):
        super().__init__(parent, **kwargs)
        self.color_scheme = color_scheme
        self.configure(bg="blue")
        self.parent = parent
        self.gps_manager = gps_manager
        self.camera_feed = camera_feed
        shared_confidence.register_observer(self.update_confidence)
        self.create_widgets()
        self.ai = ImageProcessor()

        self.update_colors()

    def update_colors(self):
        mode = "dark" if self.color_scheme["dark_mode"] else "light"
        color_scheme = self.color_scheme["colors"][mode]

        self.configure(bg=color_scheme["application/window_and_frame_color"])
        self.menu_options_frame.configure(bg=color_scheme["application/window_and_frame_color"])
        self.settings_button_frame.configure(bg=color_scheme["application/window_and_frame_color"])
        self.settings_button.configure(bg=color_scheme["selected_color"])
        self.confidence_slider_frame.configure(bg=color_scheme["application/window_and_frame_color"],
                                               highlightbackground=color_scheme["frame_outline_color"],
                                               highlightcolor=color_scheme["frame_outline_color"])

        self.confidence_label.configure(bg=color_scheme["application/window_and_frame_color"],
                                        fg=color_scheme["label_font_color/fg"])
        self.confidence_slider.set_background_fill(color_scheme["slider_background_color"])
        self.confidence_slider.set_bar_fill(color_scheme["slider_bar_fill"])
        self.confidence_slider.set_handle_fill(color_scheme["slider_knob_color"])
        self.confidence_slider.set_bar_outline(color_scheme["frame_outline_color"])

        self.gps_frame.configure(bg=color_scheme["application/window_and_frame_color"],
                                 highlightbackground=color_scheme["frame_outline_color"],
                                 highlightcolor=color_scheme["frame_outline_color"])
        self.gps_lat_long.configure(bg=color_scheme["application/window_and_frame_color"],
                                    fg=color_scheme["label_font_color/fg"])
        self.gps_bearing.configure(bg=color_scheme["application/window_and_frame_color"],
                                    fg=color_scheme["label_font_color/fg"])
        self.gps_speed.configure(bg=color_scheme["application/window_and_frame_color"],
                                    fg=color_scheme["label_font_color/fg"])
        self.gps_altitude.configure(bg=color_scheme["application/window_and_frame_color"],
                                    fg=color_scheme["label_font_color/fg"])


    def update_confidence(self, value):
        # This method updates the slider's position and the label's text
        self.confidence_slider.set_value(value, update=False)  # Update the slider
        self.confidence_label.config(text=f"CONFIDENCE: {int(round(value))}%")  # Update the label

    def on_slider_change(self, value):
        from shared_confidence_controller import shared_confidence
        shared_confidence.set_value(value)

    def create_widgets(self):
        mode = "dark" if self.color_scheme["dark_mode"] else "light"
        color_scheme = self.color_scheme["colors"][mode]
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
        self.settings_button_frame = tk.Frame(self.menu_options_frame, bg='#7C889C', width=275, height=60)
        self.settings_button_frame.grid(row=0, column=0, sticky='nw', padx=3)
        self.settings_button_frame.grid_propagate(False)

        self.settings_button = tk.Button(
            self.settings_button_frame,
            bg="#24D215",
            fg="white",
            text="SETTINGS",
            font=custom_font,
            width=25,
            height=2,
            command=self.on_settings_click,
        )
        self.settings_button.grid(pady=3, padx=5)

        # Confidence frame and slider
        self.confidence_slider_frame = tk.Frame(self.menu_options_frame, width= 400, height= 30, highlightbackground="black", highlightcolor="black", highlightthickness=2)

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
        self.confidence_label.grid(row=0, column=0, sticky='nsw', pady=0)


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
        self.confidence_slider.grid(row=0, column=0, padx=195, sticky='nse', pady=0)

        # GPS frame and output
        self.gps_frame = tk.Frame(self.menu_options_frame, bg='#7C889C', width=400, height=53, highlightbackground="black", highlightcolor="black", highlightthickness=2)

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
        self.gps_speed.place(x=2, y=20)

        self.gps_altitude = tk.Label(
            self.gps_frame,
            text="ALTITUDE: ",
            bg="#7C889C",
            fg="black",
            font=custom_font,
        )
        self.gps_altitude.place(x=235, y=20)
        self.start_gps_thread()

    # Camera methods
    def start_camera_feed(self):
        self.update_camera = True
        self.update_frame()

    def stop_camera_feed(self):
        self.update_camera = False

    def update_frame(self):
        if self.update_camera:
            frame = self.parent.camera_feed.capture()
            if frame is not None:
                detections = self.ai.detect(frame)
                img_rgb = Image.frombytes("RGB", (frame.width, frame.height), frame)
                self.photo = ImageTk.PhotoImage(image=img_rgb)
                self.camera_label.config(image=self.photo)
                self.camera_label.image = self.photo  # Keep a reference to the image
            self.after(1, self.update_frame)

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
