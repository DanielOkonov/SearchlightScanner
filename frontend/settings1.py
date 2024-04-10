import tkinter as tk
from tkinter import font as tkFont
from shared_confidence_controller import shared_confidence

# Custom slider class
class CustomSlider(tk.Canvas):
    def __init__(self, parent, id, length=610, width=120, handle_size=60, bar_thickness=60, min_val=0, max_val=100, bg='black', callback=None, **kwargs):
        kwargs.pop('command', None)
        super().__init__(parent, height=width, width=length, bg=bg, highlightthickness=0, **kwargs)
        self.callback = callback
        self.length=length
        self.width = width
        self.handle_size = handle_size
        self.bar_thickness = bar_thickness
        self.min_val = min_val
        self.max_val = max_val
        self.id = id
        self.value = min_val
        self.bind('<ButtonPress-1>', self.on_click)
        self.bind('<B1-Motion>', self.on_drag)
        self.draw_slider()

    def draw_slider(self):
        self.delete("all")
        # bar_thickness = 60  # The thickness of the slider bar
        padding = self.handle_size // 34

        self.create_rectangle(padding, self.width/2 - self.bar_thickness/2, 
                            self.length - padding, self.width/2 + self.bar_thickness/2, 
                            fill="#697283", outline="black", width=4)
        
        handle_position = self.value_to_position(self.value)

        self.create_oval(handle_position - self.handle_size/2, 
                        self.width/2 - self.handle_size/2,
                        handle_position + self.handle_size/2, 
                        self.width/2 + self.handle_size/2,
                        fill="#24D215", outline="white")

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

# Settings frame with custom sliders
class SettingsFrame1(tk.Frame):
    def __init__(self, parent, camera_feed, application, color_scheme, **kwargs):
        super().__init__(parent, **kwargs)
        self.application = application
        self.color_scheme = color_scheme
        # self.configure(bg="#7C889C")
        self.update_colors()
        self.focus_mode = tk.StringVar(value="Automatic")
        shared_confidence.register_observer(self.update_confidence)
        self.camera_feed = camera_feed  # Reference to the CameraFeed object
        self.current_cam = tk.IntVar(value=0)  # 0 for cam1, 1 for cam2
        self.create_widgets()
        self.set_focus_mode_auto()

    def update_colors(self):
        mode = "dark" if self.color_scheme["dark_mode"] else "light"
        color_scheme = self.color_scheme["colors"][mode]
        self.configure(bg=color_scheme["application/window_and_frame_color"])


    def set_focus_mode_auto(self):
        self.focus_mode.set("Automatic")
        self.automatic_focus_button.configure(bg="#24D215")
        self.manual_focus_button.configure(bg="grey")
        self.update_focus_mode_display()

    def set_focus_mode_manual(self):
        self.focus_mode.set("Manual")
        self.manual_focus_button.configure(bg="#24D215")
        self.automatic_focus_button.configure(bg="grey")
        self.update_focus_mode_display()

    def update_focus_mode_display(self):
        if self.focus_mode.get() == "Automatic":
            self.distance_frame.grid_remove()
        else:
            self.distance_frame.grid()

    def update_confidence(self, value):
        # This method updates the slider's position and the label's text
        self.confidence_slider.set_value(value, update=False)  # Update the slider
        self.confidence_label.config(text=f"CONFIDENCE: {int(round(value))}%")  # Update the label

    def update_distance(self, value):
        value = int(round(value))
        self.distance_label.config(text=f"DISTANCE: {value} units")

    def toggle_darkmode_switch(
        self, switch_canvas, switch_background, switch_indicator, switch_state
    ):
        switch_state["is_on"] = not switch_state["is_on"]

        if switch_state["is_on"]:
            switch_canvas.itemconfig(switch_background, fill="#24D215")
            switch_canvas.coords(switch_indicator, 60, 10, 90, 40)
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
        # Update button colors based on the selected camera
        if self.current_cam.get() == 0:
            self.camera_one_button.configure(bg="#24D215")  # Green for selected
            self.camera_two_button.configure(bg="grey")      # Grey for not selected
        else:
            self.camera_one_button.configure(bg="grey")      # Grey for not selected
            self.camera_two_button.configure(bg="#24D215")  # Green for selected

    def on_slider_change(self, value):
        from shared_confidence_controller import shared_confidence
        shared_confidence.set_value(value)


    def create_widgets(self):
        font_used = tkFont.Font(family="Helvetica", size=12, weight="bold")

        # Create a parent frame for sliders
        self.sliders_frame = tk.Frame(self, width=1190, height=520, bg="#7C889C", highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.sliders_frame.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')
        self.sliders_frame.grid_propagate(False)

        # Create frames for each slider within the parent sliders_frame
        self.confidence_frame = tk.Frame(self.sliders_frame, width=615, height=180, bg="#7C889C", highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.confidence_frame.grid(row=0, column=0, padx=20, pady=22)
        # self.confidence_frame.grid_propagate(False)

        self.distance_frame = tk.Frame(self.sliders_frame, width=615, height=200, bg="#7C889C", highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.distance_frame.grid(row=3, column=0, padx=20, pady=22)
        # self.distance_frame.grid_propagate(False)
        self.distance_frame.grid_remove()

        # Confidence slider and label
        self.confidence_label = tk.Label(self.confidence_frame, text="CONFIDENCE: 0%", bg="#7C889C", fg="black", font=font_used)
        self.confidence_label.grid(row=0, column=0, sticky='nsew')

        self.confidence_slider = CustomSlider(self.confidence_frame, id='confidence_slider', length=605, width=120, handle_size=60, bg="#7C889C", min_val=0, max_val=100, callback=self.on_slider_change)
        self.confidence_slider.grid(row=1, column=0, padx=2)

        # Focus mode label and buttons
        self.focus_buttons_frame = tk.Frame(self.sliders_frame, bg="#7C889C", width=100, height=108)
        # self.focus_buttons_frame.grid(row=2, column=0, padx=100, pady=2, sticky="ew")
        self.focus_buttons_frame.grid(row=2, column=0, padx=20, pady=30, sticky="ew")

        self.automatic_focus_button = tk.Button(self.focus_buttons_frame, text="AUTOMATIC FOCUS", bg="grey", fg="white", font=font_used, width=30, height= 3, command=self.set_focus_mode_auto)
        self.automatic_focus_button.grid(row=1, column=0)

        self.manual_focus_button = tk.Button(self.focus_buttons_frame, text="MANUAL FOCUS", bg="grey", fg="white", font=font_used, width=30, height= 3, command=self.set_focus_mode_manual)
        self.manual_focus_button.grid(row=1, column=1)

        # Distance slider and label
        self.distance_label = tk.Label(self.distance_frame, text="DISTANCE: 0 units", bg="#7C889C", fg="black", font=font_used)
        self.distance_label.grid(row=0, column=0, sticky='nsew')

        self.distance_slider = CustomSlider(self.distance_frame, id='distance_slider', length=605, width=120, handle_size=60, bg="#7C889C", min_val=0, max_val=100, callback=self.update_distance)
        self.distance_slider.grid(row=1, column=0, padx=2)

        # Camera selection frame and buttons
        self.cam_select_buttons_frame = tk.Frame(self.sliders_frame, bg="#7C889C", width=70, height=108)
        # self.cam_select_buttons_frame.grid(row=0, column=1, padx=50, pady=(150, 0), sticky="ew")
        self.cam_select_buttons_frame.place(x=750, y=176)
        # self.cam_select_buttons_frame.grid_propagate(False)

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


        darkmode_toggle_label = tk.Label(
            self.darkmode_toggle_frame,
            text="DARK MODE",
            bg="#7C889C",
            fg="black",
            font=font_used,
        )  # Corrected to add to operator_alerts_toggle_frame
        darkmode_toggle_label.place(x=30, y=57)
        # darkmode_toggle_label.grid(row=0, column=0)

        darkmode_switch_state = {"is_on": False}

        darkmode_toggle_canvas = tk.Canvas(
            self.darkmode_toggle_frame,
            width=100,
            height=50,
            bg="#7C889C",
            highlightthickness=0,
        )
        # darkmode_toggle_canvas.grid(row=1, column=0)
        darkmode_toggle_canvas.place(x=260, y=45)

        darkmode_switch_background = darkmode_toggle_canvas.create_rectangle(
            5, 10, 95, 40, outline="black", fill="#697283"
        )
        darkmode_switch = darkmode_toggle_canvas.create_oval(
            10, 10, 40, 40, outline="black", fill="white"
        )
        darkmode_toggle_canvas.tag_bind(
            darkmode_switch,
            "<Button-1>",
            lambda event: self.toggle_darkmode_switch(
                darkmode_toggle_canvas,
                darkmode_switch_background,
                darkmode_switch,
                darkmode_switch_state,
            ),
        )

        # Settings frame and toggle
        self.settings_toggle_frame = tk.Frame(self, width=100, height=108)
        self.settings_toggle_frame.grid(row=1, column=0, padx=10, pady=15, sticky="w")

        settings1_button = tk.Button(
            self.settings_toggle_frame,
            command=self.master.switch_settings1,
            text="SETTINGS 1",
            bg="#24D215",
            fg="white",
            font=font_used,
            width=25,
            height=5,
        )
        settings1_button.grid(row=0, column=0, sticky="ew")

        settings2_button = tk.Button(
            self.settings_toggle_frame,
            command=self.master.switch_settings2,
            text="SETTINGS 2",
            bg='#555',
            fg="white",
            font=font_used,
            width=25,
            height=5,
        )
        settings2_button.grid(row=0, column=1, sticky="ew")

        # Apply changes button
        self.apply_button_frame = tk.Frame(self, bg="red", width=565, height=108)
        self.apply_button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.apply_button_frame.grid_propagate(False)

        apply_changes_button = tk.Button(
            self.apply_button_frame,
            text="APPLY CHANGES",
            bg="#24D215",
            fg="white",
            font=font_used,
            width=53,
            height=4,
        )
        apply_changes_button.grid(row=0, column=0, padx=11, pady=9)

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
        # self.close_menu_button_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
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