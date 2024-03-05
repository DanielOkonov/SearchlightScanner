import tkinter as tk
from tkinter import font as tkFont


class SettingsFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg="#7C889C")
        self.segments_frame = None
        self.segment_buttons = {}
        self.segmentation_switch_state = {"is_on": False}
        self.create_widgets()
        self.toggle_segment_visibility(self.segmentation_switch_state["is_on"])

    def targets_button_color(self, button):
        current_color = button.cget("bg")
        if current_color == "#697283":
            button.config(bg="#24D215")
        else:
            button.config(bg="#697283")

    def toggle_operator_switch(
        self, switch_canvas, switch_background, switch_indicator, switch_state
    ):
        switch_state["is_on"] = not switch_state["is_on"]

        if switch_state["is_on"]:
            switch_canvas.itemconfig(switch_background, fill="#24D215")
            switch_canvas.coords(switch_indicator, 60, 10, 90, 40)  # Move to the right
        else:
            switch_canvas.itemconfig(switch_background, fill="#697283")
            switch_canvas.coords(switch_indicator, 10, 10, 40, 40)  # Move to the left

    def toggle_segmentation_switch(
        self, switch_canvas, switch_background, switch_indicator, switch_state
    ):
        switch_state["is_on"] = not switch_state["is_on"]

        if switch_state["is_on"]:
            switch_canvas.itemconfig(switch_background, fill="#24D215")
            switch_canvas.coords(switch_indicator, 60, 10, 90, 40)
            self.toggle_segment_visibility(True)
        else:
            switch_canvas.itemconfig(switch_background, fill="#697283")
            switch_canvas.coords(switch_indicator, 10, 10, 40, 40)
            self.toggle_segment_visibility(False)

    def set_button_active(self, selected_button):
        # Reset all buttons to grey
        for button in self.segment_buttons.values():
            button.config(bg="#697283")
        # Set the clicked button to green
        selected_button.config(bg="#24D215")

    def toggle_segment_visibility(self, show):
        #############################################################################################################
        # SEGMENTATION FRAME

        if show:
            self.segments_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nes")

        else:
            self.segments_frame.grid_remove()

    def create_widgets(self):
        font_used = tkFont.Font(family="Helvetica", size=12, weight="bold")
        self.targets_frame = tk.Frame(
            self,
            bg="#7C889C",
            highlightbackground="black",
            highlightthickness=2,
            width=605,
            height=405,
        )
        self.targets_frame.grid(row=0, column=0, padx=10, pady=5)
        self.targets_frame.grid_propagate(False)

        targets_label = tk.Label(
            self.targets_frame,
            text="SELECT TARGETS TO DETECT",
            bg="#7C889C",
            fg="black",
            font=font_used,
        )
        targets_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        targets = [
            "PEOPLE",
            "CAR",
            "BICYCLE",
            "MOTORCYCLE",
            "TRUCK",
            "BUS",
            "TRAIN",
            "AIRPLANE",
            "BOAT",
        ]
        target_buttons = {}
        for i, target in enumerate(targets):
            button = tk.Button(
                self.targets_frame,
                bg="#697283",
                fg="white",
                text=target,
                font=font_used,
                width=18,
                height=5,
            )
            button.grid(row=(i // 3) + 1, column=i % 3, padx=5, pady=5)
            button.config(command=lambda b=button: self.targets_button_color(b))
            target_buttons[target] = button

        #############################################################################################################
        # BUTTON FOR TOGGLING OPERATOR ALERTS ON OR OFF

        self.operator_alerts_toggle_frame = tk.Frame(
            self,
            bg="#7C889C",
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=2,
            width=200,
            height=100,
        )
        self.operator_alerts_toggle_frame.grid(
            row=1, column=0, padx=10, pady=10, sticky="ew"
        )

        self.operator_alerts_toggle_frame.grid_propagate(False)

        operator_toggle_label = tk.Label(
            self.operator_alerts_toggle_frame,
            text="OPERATOR ALERTS",
            bg="#7C889C",
            fg="black",
            font=font_used,
        )
        operator_toggle_label.place(x=20, y=30)

        operator_alerts_switch_state = {"is_on": False}

        operator_toggle_canvas = tk.Canvas(
            self.operator_alerts_toggle_frame,
            width=100,
            height=50,
            bg="#7C889C",
            highlightthickness=0,
        )
        operator_toggle_canvas.place(x=485, y=17)

        operator_switch_background = operator_toggle_canvas.create_rectangle(
            5, 10, 95, 40, outline="black", fill="#697283"
        )
        operator_switch = operator_toggle_canvas.create_oval(
            10, 10, 40, 40, outline="black", fill="white"
        )
        operator_toggle_canvas.tag_bind(
            operator_switch,
            "<Button-1>",
            lambda event: self.toggle_operator_switch(
                operator_toggle_canvas,
                operator_switch_background,
                operator_switch,
                operator_alerts_switch_state,
            ),
        )

        #############################################################################################################
        # BUTTONS FOR SELECTING WHICH SETTINGS MENU TO GO TO

        self.settings_toggle_frame = tk.Frame(self, bg="#7C889C", width=200, height=108)
        self.settings_toggle_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.settings_toggle_frame.grid_propagate(False)

        settings1_button = tk.Button(
            self.settings_toggle_frame,
            text="SETTINGS 1",
            font=font_used,
            width=25,
            height=5,
        )
        settings1_button.grid(row=0, column=0)

        settings2_button = tk.Button(
            self.settings_toggle_frame,
            text="SETTINGS 2",
            font=font_used,
            width=25,
            height=5,
        )
        settings2_button.grid(row=0, column=1)

        #############################################################################################################
        # SEGMENTATION FRAME

        self.segments_frame = tk.Frame(
            self,
            bg="#7C889C",
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=2,
            width=565,
            height=300,
        )
        self.segments_frame.grid(row=0, column=1, padx=10, pady=5)

        self.segments_frame.grid_propagate(False)

        segments_label = tk.Label(
            self.segments_frame,
            text="CHOOSE AN AMOUNT OF SEGMENTS",
            bg="#7C889C",
            fg="black",
            font=font_used,
        )
        segments_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        segments = [1, 25, 4, 40, 9, 60, 16, 84]

        for i, segment in enumerate(segments):
            button = tk.Button(
                self.segments_frame,
                bg="#697283",
                fg="white",
                text=str(segment),
                font=font_used,
                width=26,
                height=3,
            )
            button.grid(row=(i // 2) + 1, column=i % 2, sticky="ew", padx=5, pady=5)
            button.config(command=lambda b=button: self.set_button_active(b))
            self.segment_buttons[segment] = button

        #############################################################################################################
        # BUTTON FOR TOGGLING SEGMENTATION ON OR OFF

        self.segmentation_toggle_frame = tk.Frame(
            self,
            bg="#7C889C",
            highlightbackground="black",
            highlightcolor="black",
            highlightthickness=2,
            width=565,
            height=100,
        )  # Adjusted height for layout
        self.segmentation_toggle_frame.grid(
            row=1, column=1, padx=10, pady=10
        )  # Placed in row=1, added more pady for spacing

        self.segmentation_toggle_frame.grid_propagate(False)

        segmentation_toggle_label = tk.Label(
            self.segmentation_toggle_frame,
            text="SEGMENTATION",
            bg="#7C889C",
            fg="black",
            font=font_used,
        )  # Corrected to add to operator_alerts_toggle_frame
        segmentation_toggle_label.place(x=20, y=30)

        segmentation_toggle_canvas = tk.Canvas(
            self.segmentation_toggle_frame,
            width=100,
            height=50,
            bg="#7C889C",
            highlightthickness=0,
        )
        segmentation_toggle_canvas.place(x=440, y=17)

        segmentation_switch_background = segmentation_toggle_canvas.create_rectangle(
            5, 10, 95, 40, outline="black", fill="#697283"
        )
        segmentation_switch = segmentation_toggle_canvas.create_oval(
            10, 10, 40, 40, outline="black", fill="white"
        )
        segmentation_toggle_canvas.tag_bind(
            segmentation_switch,
            "<Button-1>",
            lambda event: self.toggle_segmentation_switch(
                segmentation_toggle_canvas,
                segmentation_switch_background,
                segmentation_switch,
                self.segmentation_switch_state,
            ),
        )

        #############################################################################################################
        # APPLY CHANGES BUTTON

        self.apply_button_frame = tk.Frame(self, bg="red", width=200, height=100)
        self.apply_button_frame.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")
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

        #############################################################################################################
        # CLOSE SETTINGS MENU BUTTON

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
            command=self.on_close_menu_click,
        )
        close_menu_button.pack(ipadx=5, ipady=5, expand=True)

    def on_close_menu_click(self):
        from camera_frame import MainFrame

        self.master.switch_frame(MainFrame)
