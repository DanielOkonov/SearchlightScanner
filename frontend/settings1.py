import tkinter as tk
from tkinter import font as tkFont

# Custom slider class
class CustomSlider(tk.Canvas):
    def __init__(self, parent, id, length=500, width=120, handle_size=60, min_val=0, max_val=100, bg='black', callback=None, **kwargs):
        kwargs.pop('command', None)
        super().__init__(parent, height=width, width=length, bg=bg, highlightthickness=0, **kwargs)
        self.callback = callback
        # self.length = 300
        self.length=length
        self.width = width
        self.handle_size = handle_size
        self.min_val = min_val
        self.max_val = max_val
        self.id = id
        self.value = min_val
        self.bind('<ButtonPress-1>', self.on_click)
        self.bind('<B1-Motion>', self.on_drag)
        self.draw_slider()

    def draw_slider(self):
        self.delete("all")
        bar_thickness = 60  # Adjust the bar thickness here if needed
        # Ensure that the bar is drawn within the Canvas size
        self.create_rectangle(10, self.width/2 - bar_thickness/2, self.length - 10, self.width/2 + bar_thickness/2, fill="#555", outline="#ccc", width=2)
        handle_position = self.value_to_position(self.value)
        self.create_oval(handle_position - self.handle_size/2, self.width/2 - self.handle_size/2,
                         handle_position + self.handle_size/2, self.width/2 + self.handle_size/2,
                         fill="#24D215", outline="#eee")

    def value_to_position(self, value):
        return 10 + (value - self.min_val) / (self.max_val - self.min_val) * (self.length - 20)

    def position_to_value(self, position):
        return (position - 10) / (self.length - 20) * (self.max_val - self.min_val) + self.min_val

    def set_value(self, value):
        self.value = max(self.min_val, min(self.max_val, value))
        self.draw_slider()
        if self.callback:
            self.callback(self.value)

    def on_click(self, event):
        self.set_value(self.position_to_value(event.x))

    def on_drag(self, event):
        self.set_value(self.position_to_value(event.x))

# Settings frame with custom sliders
class SettingsFrame1(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg="#7C889C")
        self.focus_mode = tk.StringVar(value="Automatic")
        self.create_widgets()
        self.set_focus_mode_auto()

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
        value = int(round(value))
        self.confidence_label.config(text=f"CONFIDENCE: {value}%")

    def update_distance(self, value):
        value = int(round(value))
        self.distance_label.config(text=f"DISTANCE: {value} units")


    def create_widgets(self):
        font_used = tkFont.Font(family="Helvetica", size=12, weight="bold")

        # Create a parent frame for sliders
        self.sliders_frame = tk.Frame(self, width=1190, height=520, bg="#7C889C", highlightbackground="black", highlightcolor="black", highlightthickness=2)
        self.sliders_frame.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')
        self.sliders_frame.grid_propagate(False)

        # Create frames for each slider within the parent sliders_frame
        self.confidence_frame = tk.Frame(self.sliders_frame, width=300, bg="#7C889C", highlightthickness=0)
        self.confidence_frame.grid(row=0, column=0, sticky='nsew')

        self.distance_frame = tk.Frame(self.sliders_frame, bg="#7C889C", highlightthickness=0)
        self.distance_frame.grid(row=3, column=0, sticky='nsew')
        self.distance_frame.grid_remove()

        # Confidence slider and label
        self.confidence_label = tk.Label(self.confidence_frame, text="CONFIDENCE: 0%", bg="#7C889C", fg="black", font=font_used)
        self.confidence_label.grid(row=0, column=0, sticky='nsew')

        self.confidence_slider = CustomSlider(self.confidence_frame, id='confidence_slider', length=500, width=120, handle_size=60, bg="#7C889C", min_val=0, max_val=100, callback=self.update_confidence)
        self.confidence_slider.grid(row=1, column=0, padx=300)

        # Focus mode buttons
        self.automatic_focus_button = tk.Button(self.sliders_frame, text="AUTOMATIC FOCUS", bg="grey", fg="white", font=font_used, command=self.set_focus_mode_auto)
        self.automatic_focus_button.grid(row=2, column=0, sticky="ew")

        self.manual_focus_button = tk.Button(self.sliders_frame, text="MANUAL FOCUS", bg="grey", fg="white", font=font_used, command=self.set_focus_mode_manual)
        self.manual_focus_button.grid(row=2, column=1, sticky="ew")

        # Distance slider and label
        self.distance_label = tk.Label(self.distance_frame, text="DISTANCE: 0 units", bg="#7C889C", fg="black", font=font_used)
        self.distance_label.grid(row=0, column=0, sticky='nsew')

        self.distance_slider = CustomSlider(self.distance_frame, id='distance_slider', length=200, width=30, handle_size=30, bg="#7C889C", min_val=0, max_val=100, callback=self.update_distance)
        self.distance_slider.grid(row=1, column=0, sticky='nsew')

        # Settings frame and toggle
        self.settings_toggle_frame = tk.Frame(self, bg="#7C889C", width=200, height=108)
        self.settings_toggle_frame.grid(row=2, column=0, padx=10, pady=15, sticky="ew")

        settings1_button = tk.Button(
            self.settings_toggle_frame,
            command=self.master.switch_settings1,
            text="SETTINGS 1",
            font=font_used,
            width=25,
            height=5,
        )
        settings1_button.grid(row=0, column=0)

        settings2_button = tk.Button(
            self.settings_toggle_frame,
            command=self.master.switch_settings2,
            text="SETTINGS 2",
            font=font_used,
            width=25,
            height=5,
        )
        settings2_button.grid(row=0, column=1)

        # Close frame and button
        self.close_menu_button_frame = tk.Frame(
            self,
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=2,
            width=51,
            height=51,
        )
        self.close_menu_button_frame.grid(row=0, column=3, padx=5, pady=5, sticky="ne")
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