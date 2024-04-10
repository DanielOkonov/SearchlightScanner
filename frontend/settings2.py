import tkinter as tk
from tkinter import font as tkFont
from reorderable_listbox import ReorderableListbox


class SettingsFrame2(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg="#7C889C")
        self.segments_frame = None
        self.segment_buttons = {}
        self.targets_selected_count = 0
        self.segmentation_switch_state = {"is_on": False}
        self.selected_targets_dict = {}
        self.create_widgets()
        self.toggle_segment_visibility(self.segmentation_switch_state["is_on"])

    def targets_button_color(self, button):
        current_color = button.cget("bg")
        if current_color == "#697283" and self.targets_selected_count < 6:
            button.config(bg="#24D215")
            self.targets_selected_count += 1
        elif current_color == "#24D215":
            button.config(bg="#697283")
            self.targets_selected_count -= 1

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

        # self.targets_listbox = ReorderableListbox(self, font=font_used)
        # self.targets_listbox = ReorderableListbox(self, font=font_used, application_callback=self.update_order_from_listbox)
        self.targets_listbox = ReorderableListbox(
            self,
            font=font_used,
            update_order_callback=self.update_order_from_listbox,
            update_display_callback=self.update_listbox_display
        )
        # self.targets_listbox.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        self.targets_listbox.place_forget()  # Initially hidden

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
                # command=lambda t=target: self.toggle_target_selection(t)
            )
            button.grid(row=(i // 3) + 1, column=i % 3, padx=5, pady=5)
            button.config(command=lambda b=button, t=target: (self.targets_button_color(b), self.toggle_target_selection(t)))
            target_buttons[target] = button

        # Initially, the Listbox is hidden as no target is selected
        self.targets_listbox.place_forget()

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
            command=self.master.switch_settings1,
            text="SETTINGS 1",
            bg='#555',
            fg="white",
            font=font_used,
            width=25,
            height=5,
        )
        settings1_button.grid(row=0, column=0)

        settings2_button = tk.Button(
            self.settings_toggle_frame,
            command=self.master.switch_settings2,
            text="SETTINGS 2",
            bg="#24D215",
            fg="white",
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
            command=self.master.switch_main_frame,
        )
        close_menu_button.pack(ipadx=5, ipady=5, expand=True)


    def toggle_target_selection(self, target):
        if target in self.selected_targets_dict:
            # Target is being deselected
            del self.selected_targets_dict[target]
            items = list(self.targets_listbox.get(0, "end"))
            # Find and delete the target with its number from the listbox
            for i, listbox_entry in enumerate(items):
                if target == listbox_entry.split('. ')[-1]:
                    self.targets_listbox.delete(i)
                    break
            # Adjust the numbers after removal
            self.update_order_from_listbox()  # This function should update self.selected_targets_dict
        else:
            # Target is being selected
            if len(self.selected_targets_dict) < 6:
                self.selected_targets_dict[target] = len(self.selected_targets_dict) + 1
                self.targets_listbox.insert("end", f"{self.selected_targets_dict[target]}. {target}")
        
        # Print the current state of selected_targets_dict to the console
        print("Selected Targets Dict:", self.selected_targets_dict)
        
        # Update visibility of the Listbox based on selected targets count
        if self.selected_targets_dict:
            self.targets_listbox.place(x=5, y=300, width=580, height=100)
        else:
            self.targets_listbox.place_forget()


    def populate_listbox_with_targets(self):
        # Clear the Listbox
        self.targets_listbox.delete(0, 'end')
        # Insert items with their order numbers
        for index, target in enumerate(sorted(self.selected_targets_dict, key=self.selected_targets_dict.get), start=1):
            self.targets_listbox.insert('end', f"{index}. {target}")


    def update_order_from_listbox(self):
        # Get the current list of items from the Listbox
        items = list(self.targets_listbox.get(0, tk.END))
        
        # Clear the existing dictionary
        self.selected_targets_dict.clear()

        # Clear the Listbox before inserting updated items
        self.targets_listbox.delete(0, tk.END)

        # Assign new order numbers based on current Listbox order
        for order, item in enumerate(items, start=1):
            target = item.split('. ')[-1]  # Split and get the last part, the target name
            self.selected_targets_dict[target] = order
            # Insert updated items back into the Listbox
            self.targets_listbox.insert(tk.END, f"{order}. {target}")
        
        # Log to console for debugging
        print("Updated Selected Targets Dict:", self.selected_targets_dict)


    def update_listbox_display(self):
        # Clear the Listbox
        self.targets_listbox.delete(0, tk.END)

        # Get items sorted by their order value from the dictionary
        sorted_items = sorted(self.selected_targets_dict.items(), key=lambda x: x[1])

        # Insert items back into the Listbox with updated numbers
        for order, (target, _) in enumerate(sorted_items, start=1):
            formatted_item = f"{order}. {target}"
            self.targets_listbox.insert(tk.END, formatted_item)
