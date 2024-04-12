import tkinter as tk
from tkinter import font as tkFont
from tkinter import ttk
from .shared_confidence_controller import shared_confidence

# Custom slider class
class CustomSlider(tk.Canvas):
    def __init__(self, parent, id, length=610, width=120, handle_size=60, bar_thickness=60, min_val=0, max_val=100, bg='black', callback=None, bar_fill="#697283", bar_outline="black", handle_fill="#24D215", **kwargs):
        kwargs.pop('command', None)
        super().__init__(parent, height=width, width=length, bg=bg, highlightthickness=0, **kwargs)
        self.callback = callback
        self.length = length
        self.width = width
        self.handle_size = handle_size
        self.bar_thickness = bar_thickness
        self.min_val = min_val
        self.max_val = max_val
        self.id = id
        self.value = min_val
        self.bg = bg
        self.bar_fill = bar_fill
        self.bar_outline = bar_outline
        self.handle_fill = handle_fill
        self.bind('<ButtonPress-1>', self.on_click)
        self.bind('<B1-Motion>', self.on_drag)
        self.draw_slider()

    def draw_slider(self):
        self.delete("all")
        padding = self.handle_size // 34

        # Draw the slider bar with custom fill and outline colors
        self.create_rectangle(padding, self.width/2 - self.bar_thickness/2, 
                              self.length - padding, self.width/2 + self.bar_thickness/2, 
                              fill=self.bar_fill, outline=self.bar_outline, width=4)
        
        # Calculate the handle position based on the current value
        handle_position = self.value_to_position(self.value)

        # Draw the handle with a custom fill color
        self.create_oval(handle_position - self.handle_size/2, 
                         self.width/2 - self.handle_size/2,
                         handle_position + self.handle_size/2, 
                         self.width/2 + self.handle_size/2,
                         fill=self.handle_fill, outline="white")
    def value_to_position(self, value):
        # Adjust position calculation to account for padding
        padding = self.handle_size // 2
        return padding + (value - self.min_val) / (self.max_val - self.min_val) * (self.length - padding * 2)

    def position_to_value(self, position):
        # Adjust value calculation to account for padding
        padding = self.handle_size // 2
        return (position - padding) / (self.length - padding * 2) * (self.max_val - self.min_val) + self.min_val

    def set_value(self, value, update=True):
        self.value = max(self.min_val, min(self.max_val, value))
        self.draw_slider()
        # Only call the callback if update is True, which should be the case
        # only when the slider is moved by the user, not when synchronizing sliders.
        if update and self.callback:
            self.callback(self.value)

    def on_click(self, event):
        self.set_value(self.position_to_value(event.x))

    def on_drag(self, event):
        self.set_value(self.position_to_value(event.x))

        # Method to set bar fill color
    def set_bar_fill(self, color):
        self.bar_fill = color
        self.draw_slider()

    # Method to set bar outline color
    def set_bar_outline(self, color):
        self.bar_outline = color
        self.draw_slider()

    # Method to set handle fill color
    def set_handle_fill(self, color):
        self.handle_fill = color
        self.draw_slider()

    def set_background_fill(self, color):
        self.configure(bg=color)  # Update the canvas background color
        self.draw_slider()  # Redraw the slider to refresh the look

# Settings frame with custom sliders
class SettingsFrame1(tk.Frame):
    def __init__(self, parent, camera_feed, application, color_scheme, **kwargs):
        super().__init__(parent, **kwargs)
        self.application = application
        self.color_scheme = color_scheme
        self.focus_mode = tk.StringVar(value="Automatic")
        shared_confidence.register_observer(self.update_confidence)
        self.camera_feed = camera_feed  # Reference to the CameraFeed object
        self.current_cam = tk.IntVar(value=0)  # 0 for cam1, 1 for cam2
        self.style = ttk.Style()
        self.create_widgets()
        self.update_colors()

    def update_colors(self):
        mode = "dark" if self.color_scheme["dark_mode"] else "light"
        color_scheme = self.color_scheme["colors"][mode]

        self.configure(bg=color_scheme["application/window_and_frame_color"])
        self.sliders_frame.configure(bg=color_scheme["application/window_and_frame_color"],
                                     highlightbackground=color_scheme["frame_outline_color"],
                                     highlightcolor=color_scheme["frame_outline_color"])
        
        self.confidence_frame.configure(bg=color_scheme["application/window_and_frame_color"],
                                        highlightbackground=color_scheme["frame_outline_color"],
                                        highlightcolor=color_scheme["frame_outline_color"])
        
        self.confidence_label.configure(bg=color_scheme["application/window_and_frame_color"],
                                        fg=color_scheme["label_font_color/fg"])
        
        self.confidence_slider.set_background_fill(color_scheme["slider_background_color"])
        self.confidence_slider.set_bar_fill(color_scheme["slider_bar_fill"])
        self.confidence_slider.set_handle_fill(color_scheme["slider_knob_color"])
        self.confidence_slider.set_bar_outline(color_scheme["frame_outline_color"])

        self.cam_select_buttons_frame.configure(bg=color_scheme["application/window_and_frame_color"])
        self.cam_select_label.configure(bg=color_scheme["application/window_and_frame_color"],
                                        fg=color_scheme["label_font_color/fg"])

        if self.current_cam.get() == 0:
            self.camera_one_button.configure(bg=color_scheme["focus_button_bg_dark_active"] if mode == "dark" else color_scheme["focus_button_bg_light_active"])
            self.camera_two_button.configure(bg=color_scheme["focus_button_bg_dark_inactive"] if mode == "dark" else color_scheme["focus_button_bg_light_inactive"]) 
        else:
            self.camera_one_button.configure(bg=color_scheme["focus_button_bg_dark_inactive"] if mode == "dark" else color_scheme["focus_button_bg_light_inactive"])
            self.camera_two_button.configure(bg=color_scheme["focus_button_bg_dark_active"] if mode == "dark" else color_scheme["focus_button_bg_light_active"]) 

        self.darkmode_toggle_frame.configure(bg=color_scheme["application/window_and_frame_color"],
                                        highlightbackground=color_scheme["frame_outline_color"],
                                        highlightcolor=color_scheme["frame_outline_color"])
        
        self.darkmode_toggle_label.configure(bg=color_scheme["application/window_and_frame_color"],
                                        fg=color_scheme["label_font_color/fg"])
        
        self.darkmode_toggle_canvas.configure(bg=color_scheme["application/window_and_frame_color"],
                                              highlightbackground=color_scheme["frame_outline_color"],
                                              highlightcolor=color_scheme["frame_outline_color"])

        self.settings1_button.configure(bg=color_scheme["selected_color"])
        self.settings2_button.configure(bg=color_scheme["unselected_settings_button"])

        self.apply_button_frame.configure(bg=color_scheme["apply_changes_background"])
        self.apply_changes_button.configure(bg=color_scheme["selected_color"])

        self.resolution_frame_and_label.configure(bg=color_scheme["application/window_and_frame_color"],
                                              highlightbackground=color_scheme["frame_outline_color"],
                                              highlightcolor=color_scheme["frame_outline_color"])
        
        self.resolution_label.configure(bg=color_scheme["application/window_and_frame_color"],
                                        fg=color_scheme["label_font_color/fg"])

        self.resolutions_frame.configure(bg=color_scheme["button_bg"],
                                         highlightbackground=color_scheme["frame_outline_color"],
                                         highlightcolor=color_scheme["frame_outline_color"])

        # Update the styles for TMenubutton and TMenu
        self.style.map('TMenubutton', background=[('active', color_scheme["selected_color"]), ('!active', color_scheme["button_bg"])],
                       foreground=[('active', color_scheme["button_font_color/fg"]), ('!active', color_scheme["button_font_color/fg"])])
        self.style.configure('TMenubutton', background=color_scheme["button_bg"], foreground=color_scheme["button_font_color/fg"])
        self.style.configure('TMenu', background=color_scheme["button_bg"], foreground=color_scheme["button_font_color/fg"], borderwidth=0)
        self.style.map('TMenu', background=[('active', color_scheme["selected_color"])])

    def update_confidence(self, value):
        # This method updates the slider's position and the label's text
        self.confidence_slider.set_value(value, update=False)  # Update the slider
        self.confidence_label.config(text=f"CONFIDENCE: {int(round(value))}%")  # Update the label

    def toggle_darkmode_switch(
        self, switch_canvas, switch_background, switch_indicator, switch_state
    ):
        switch_state["is_on"] = not switch_state["is_on"]

        if switch_state["is_on"]:
            switch_canvas.itemconfig(switch_background, fill="#006400")
            switch_canvas.coords(switch_indicator, 60, 10, 90, 40)
            self.update_colors()
        else:
            switch_canvas.itemconfig(switch_background, fill="#697283")
            switch_canvas.coords(switch_indicator, 10, 10, 40, 40)

        # Call the method on the Application class to update all frames
        self.application.toggle_dark_mode()

    def select_camera(self, cam_index):
        # Update camera source in CameraFeed
        self.camera_feed.set_video_source(cam_index)
        self.current_cam.set(cam_index)
        self.update_camera_selection()

    def update_camera_selection(self):
        self.update_colors()

    def on_slider_change(self, value):
        from .shared_confidence_controller import shared_confidence
        shared_confidence.set_value(value)

    def selection_changed(self, value):
        print("Selected:", value)

    def create_widgets(self):
        font_used = tkFont.Font(family="Helvetica", size=12, weight="bold")

        # Create a parent frame for sliders
        self.sliders_frame = tk.Frame(self, width=1190, height=520, bg="#7C889C", highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.sliders_frame.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')
        self.sliders_frame.grid_propagate(False)

        # Create frames for each slider within the parent sliders_frame
        self.confidence_frame = tk.Frame(self.sliders_frame, width=615, height=180, bg="#7C889C", highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.confidence_frame.grid(row=0, column=0, padx=10, pady=22)
        self.confidence_frame.grid_propagate(False)


        # Confidence slider and label
        self.confidence_label = tk.Label(self.confidence_frame, text="CONFIDENCE: 0%", bg="#7C889C", fg="black", font=font_used)
        self.confidence_label.grid(row=0, column=0, sticky='nsew')

        self.confidence_slider = CustomSlider(self.confidence_frame, id='confidence_slider', length=605, width=120, handle_size=60, bar_fill="blue", bar_outline="yellow", handle_fill="green", bg="#7C889C", min_val=0, max_val=100, callback=self.on_slider_change)
        self.confidence_slider.grid(row=1, column=0, padx=2)

        # Create a frame to hold the OptionMenu
        self.resolution_frame_and_label = tk.Frame(self.sliders_frame, bg="#7C889C", highlightbackground="black", highlightcolor="black", highlightthickness=2, width=10, height=180)
        self.resolution_frame_and_label.grid(row=2, column=0, padx=(10, 0), pady=(17,0), sticky="ew")
        self.resolution_frame_and_label.grid_propagate(False)

        self.resolution_label = tk.Label(self.resolution_frame_and_label, text="SELECT RESOLUTION", bg="#7C889C", fg="black", font=font_used)
        self.resolution_label.grid(row=0, column=0, sticky="ew")

        self.resolutions_frame = tk.Frame(self.resolution_frame_and_label, bg="#7C889C", highlightbackground="black", highlightcolor="black", highlightthickness=2, width=10, height=108)
        self.resolutions_frame.grid(row=1, column=0, sticky="ew")

        # Create a frame to hold the OptionMenu
        menu_font = tkFont.Font(family="Helvetica", size=14, weight="bold")
        frame = tk.Frame(self.resolutions_frame, bg='darkgrey')
        frame.pack(padx=10, pady=10)

        # Create a Tkinter variable
        selected_option = tk.StringVar(value="280x720 pixels")

        # Set the list of choices
        options = [
            "280x720 pixels",
            "1920x1080 pixels",
            "2560x1440 pixels",
            "3840x2160 pixels"
        ]

        # Create the dropdown menu and add it to the frame
        self.option_menu = ttk.OptionMenu(frame, selected_option, selected_option.get(), *options, command=self.selection_changed)
        self.option_menu.pack(expand=True, fill='both')

        # Apply custom styles
        self.style.configure('TMenubutton', font=menu_font, width=50, height=30)

        menu = self.option_menu['menu']
        menu.config(font=menu_font)  # Set the font for menu items

        # Camera selection frame and buttons
        self.cam_select_buttons_frame = tk.Frame(self.sliders_frame, bg="#7C889C", width=70, height=108)
        self.cam_select_buttons_frame.place(x=750, y=176)

        self.cam_select_label = tk.Label(self.cam_select_buttons_frame, text="SELECT CAMERA INPUT", bg="#7C889C", fg="black", font=font_used)
        self.cam_select_label.grid(row=0, column=0, columnspan=2, pady=(0, 22))

        self.camera_one_button = tk.Button(self.cam_select_buttons_frame, text="CAMERA 1", bg="#24D215", fg="white", font=font_used, width=20, height=3, command=lambda: self.select_camera(0))
        self.camera_one_button.grid(row=1, column=0)

        self.camera_two_button = tk.Button(self.cam_select_buttons_frame, text="CAMERA 2", bg="grey", fg="white", font=font_used, width=20, height=3, command=lambda: self.select_camera(1))
        self.camera_two_button.grid(row=1, column=1)

        # Toggle dark mode button and label
        self.darkmode_toggle_frame = tk.Frame(
            self.sliders_frame,
            bg="#7C889C",
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=2,
            # width=225,
            width=420,
            height=149,
        )  # Adjusted height for layout
        self.darkmode_toggle_frame.place(
            x=750, y=346
        )  # Placed in row=1, added more pady for spacing


        self.darkmode_toggle_label = tk.Label(
            self.darkmode_toggle_frame,
            text="DARK MODE",
            bg="#7C889C",
            fg="black",
            font=font_used,
        )  # Corrected to add to operator_alerts_toggle_frame
        self.darkmode_toggle_label.place(x=30, y=57)

        darkmode_switch_state = {"is_on": False}

        self.darkmode_toggle_canvas = tk.Canvas(
            self.darkmode_toggle_frame,
            width=100,
            height=50,
            bg="#7C889C",
            highlightthickness=0,
            highlightbackground="black",
            highlightcolor="black",
        )
        self.darkmode_toggle_canvas.place(x=260, y=45)

        self.darkmode_switch_background = self.darkmode_toggle_canvas.create_rectangle(
            5, 10, 95, 40, fill="#697283"
        )
        darkmode_switch = self.darkmode_toggle_canvas.create_oval(
            10, 10, 40, 40, outline="black", fill="white"
        )
        self.darkmode_toggle_canvas.tag_bind(
            darkmode_switch,
            "<Button-1>",
            lambda event: self.toggle_darkmode_switch(
                self.darkmode_toggle_canvas,
                self.darkmode_switch_background,
                darkmode_switch,
                darkmode_switch_state,
            ),
        )

        # Settings frame and toggle
        self.settings_toggle_frame = tk.Frame(self, width=100, height=108)
        self.settings_toggle_frame.grid(row=1, column=0, padx=10, pady=15, sticky="w")

        self.settings1_button = tk.Button(
            self.settings_toggle_frame,
            command=self.master.switch_settings1,
            text="SETTINGS 1",
            bg="#24D215",
            fg="white",
            font=font_used,
            width=25,
            height=5,
        )
        self.settings1_button.grid(row=0, column=0, sticky="ew")

        self.settings2_button = tk.Button(
            self.settings_toggle_frame,
            command=self.master.switch_settings2,
            text="SETTINGS 2",
            bg='#555',
            fg="white",
            font=font_used,
            width=25,
            height=5,
        )
        self.settings2_button.grid(row=0, column=1, sticky="ew")

        # Apply changes button
        self.apply_button_frame = tk.Frame(self, bg="red", width=565, height=108)
        self.apply_button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.apply_button_frame.grid_propagate(False)

        self.apply_changes_button = tk.Button(
            self.apply_button_frame,
            text="APPLY CHANGES",
            bg="#24D215",
            fg="white",
            font=font_used,
            width=53,
            height=4,
        )
        self.apply_changes_button.grid(row=0, column=0, padx=11, pady=9)

        # Close frame and button
        self.close_menu_button_frame = tk.Frame(
            self,
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=2,
            width=51,
            height=51,
        )
        self.close_menu_button_frame.grid(row=0, column=1, padx=(5,10), pady=5, sticky="nw")
        self.close_menu_button_frame.grid_propagate(False)

        x_button_font = tkFont.Font(family="Helvetica", size=20, weight="bold")
        close_menu_button = tk.Button(
            self.close_menu_button_frame,
            text="X",
            bg="red",
            fg="white",
            font=x_button_font,
            command=self.master.switch_main_frame,
        )
        close_menu_button.pack(ipadx=5, ipady=5, expand=True)