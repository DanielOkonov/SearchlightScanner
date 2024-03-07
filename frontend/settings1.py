import tkinter as tk
from tkinter import font as tkFont

# Define constant variables for colors
BG_COLOR = "#7C889C"
BORDER_COLOR = "black"
FOCUS_BG_COLOR = "#24D215"
FOCUS_OUT_BG_COLOR = "#697283"


class SettingsFrame1(tk.Frame):

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg="#7C889C")
        self.create_widgets()

    def create_widgets(self):
        font_used = tkFont.Font(family="Helvetica", size=12, weight="bold")
        self.settings_frame = tk.Frame(
            self,
            bg="#7C889C",
            highlightbackground="black",
            highlightthickness=2,
            width=605,
            height=405,
        )
        self.settings_frame.grid(row=0, column=0, padx=10, pady=5)
        self.settings_frame.grid_propagate(False)

        def update_confidence(value):
            confidence_label.config(text=f"Confidence: {value}%")

        def update_distance(value):
            distance_label.config(text=f"Distance: {value} units")

        confidence_label = tk.Label(
            self.settings_frame,
            text="CONFIDENCE: 0%",
            bg="#7C889C",
            fg="black",
            font=font_used,
        )
        confidence_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        confidence_slider = tk.Scale(
            master=self.settings_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=200,
            command=update_confidence,
            bg="#7C889C",
            sliderrelief="raised",
            troughcolor="#24D215",
            highlightthickness=0,
        )
        confidence_slider.grid(row=1, column=0, rowspan=2)

        distance_label = tk.Label(
            self.settings_frame,
            text="DISTANCE: 0%",
            bg="#7C889C",
            fg="black",
            font=font_used,
        )
        distance_label.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

        confidence_slider = tk.Scale(
            master=self.settings_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=200,
            command=update_distance,
            bg="#7C889C",
            sliderrelief="raised",
            troughcolor="#24D215",
            highlightthickness=0,
        )
        confidence_slider.grid(row=4, column=0, rowspan=2)

        self.settings_toggle_frame = tk.Frame(self, bg="#7C889C", width=200, height=108)
        self.settings_toggle_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.settings_toggle_frame.grid_propagate(False)

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


# def switch_focus():
#     print("switch")
#     if automatic_focus_var.get():
#         focus_label_auto.config(bg=FOCUS_BG_COLOR)
#         focus_label_manual.config(bg=FOCUS_OUT_BG_COLOR)
#     else:
#         focus_label_manual.config(bg=FOCUS_BG_COLOR)
#         focus_label_auto.config(bg=FOCUS_OUT_BG_COLOR)


# window = tk.Tk()
# window.configure(bg=BG_COLOR)

# # Create a main frame to hold all elements except the "Apply Changes" button
# main_frame = tk.Frame(window, bg=BG_COLOR)
# main_frame.pack(expand=True, fill=tk.BOTH)

# confidenceFrame = tk.Frame(
#     master=main_frame, height=100, bg=BG_COLOR, bd=2, relief="solid"
# )
# confidenceFrame.pack(fill=tk.X, pady=(20, 10))

# confidence_label = tk.Label(master=confidenceFrame, text="Confidence: 0%", bg=BG_COLOR)
# confidence_label.pack(side=tk.LEFT, padx=10)

# confidence_slider = tk.Scale(
#     master=confidenceFrame,
#     from_=0,
#     to=100,
#     orient=tk.HORIZONTAL,
#     length=200,
#     command=update_confidence,
#     bg=BG_COLOR,
#     sliderrelief="raised",
#     troughcolor=FOCUS_BG_COLOR,
#     highlightthickness=0,
# )
# confidence_slider.pack(side=tk.LEFT)

# focusFrame = tk.Frame(master=main_frame, height=100, bg=BG_COLOR)
# focusFrame.pack(fill=tk.X)

# focus_label_auto = tk.Button(
#     master=focusFrame,
#     text="Automatic Focus",
#     bg=FOCUS_BG_COLOR,
#     command=lambda: switch_focus(),
# )
# focus_label_auto.pack(side=tk.LEFT, padx=10)

# focus_label_manual = tk.Button(
#     master=focusFrame,
#     text="Manual Focus",
#     bg=FOCUS_OUT_BG_COLOR,
#     command=lambda: switch_focus(),
# )
# focus_label_manual.pack(side=tk.LEFT, padx=10)

# automatic_focus_var = tk.BooleanVar()
# automatic_focus_var.set(True)

# distanceFrame = tk.Frame(
#     master=main_frame, height=100, bg=BG_COLOR, bd=2, relief="solid"
# )
# distanceFrame.pack(fill=tk.X, pady=(10, 20))

# distance_label = tk.Label(master=distanceFrame, text="Distance: 0 units", bg=BG_COLOR)
# distance_label.pack(side=tk.LEFT, padx=10)

# distance_slider = tk.Scale(
#     master=distanceFrame,
#     from_=0,
#     to=100,
#     orient=tk.HORIZONTAL,
#     length=200,
#     command=update_distance,
#     bg=BG_COLOR,
#     sliderrelief="raised",
#     troughcolor=FOCUS_BG_COLOR,
#     highlightthickness=0,
# )
# distance_slider.pack(side=tk.LEFT)

# # Create a frame to hold the "Apply Changes" button
# apply_frame = tk.Frame(window, bg=BG_COLOR)
# apply_frame.pack(fill=tk.X)

# apply_button = tk.Button(master=apply_frame, text="Apply Changes", bg=FOCUS_BG_COLOR)
# apply_button.pack(side=tk.RIGHT, padx=10, pady=10)

# window.mainloop()
