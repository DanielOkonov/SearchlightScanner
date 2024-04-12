import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from constantsmanager import ConstantsManager

segmentation_options = [
    {
        "text": "1x1",
        "value": 1,
    },
    {
        "text": "2x2",
        "value": 4,
    },
    {
        "text": "3x3",
        "value": 9,
    },
    {
        "text": "4x4",
        "value": 16,
    },
    {
        "text": "5x5",
        "value": 25,
    },
    {
        "text": "4x8",
        "value": 32,
    },
    {
        "text": "5x8",
        "value": 40,
    },
    {
        "text": "5x10",
        "value": 50,
    },
    {
        "text": "6x10",
        "value": 60,
    },
    {
        "text": "7x12",
        "value": 84,
    },
]


def get_segmentation_value(text):
    for option in segmentation_options:
        if option["text"] == text:
            return option["value"]
    return None  # Return None if text is not found


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Constants")
        self.configure(bg="#7C889C")
        self.geometry("600x400")

        # Instance variables to store values
        self.default_confidence_level = tk.IntVar(value=90)
        self.default_distance = tk.IntVar(value=1)
        self.default_targets = []
        self.default_segmentation = tk.StringVar(value="1x1")
        self.default_model_path = tk.StringVar(value="")
        self.default_labels_path = tk.StringVar(value="")

        self.create_form()

    def on_close(self):
        self.destroy()

    def browse_model(self):
        model_path = filedialog.askopenfilename(
            filetypes=[("ONYX files", "*.onyx"), ("All files", "*.*")]
        )
        if model_path:
            self.default_model_path.set(model_path)

    def browse_labels(self):
        labels_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if labels_path:
            self.default_labels_path.set(labels_path)

    def toggle_target(self, target):
        if target in self.default_targets:
            self.default_targets.remove(target)
        else:
            self.default_targets.append(target)
        self.update_selected_targets_display()

    def validate_numeric_input(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def update_confidence_level(self, event):
        value = self.confidence_level_entry.get()
        if self.validate_numeric_input(value):
            self.default_confidence_level.set(int(value))
        else:
            self.confidence_level_entry.delete(0, tk.END)

    def update_distance(self, event):
        value = self.distance_entry.get()
        if self.validate_numeric_input(value):
            self.default_distance.set(int(value))
        else:
            self.distance_entry.delete(0, tk.END)

    def update_segmentation(self, event):
        self.default_segmentation.set(self.segmentation_entry.get())

    def save_constants(self):
        constants_manager = ConstantsManager()
        constants_manager.set_constant(
            "default_confidence_level", self.default_confidence_level.get()
        )
        constants_manager.set_constant("default_distance", self.default_distance.get())
        constants_manager.set_constant(
            "default_segmemtation",
            get_segmentation_value(self.default_segmentation.get()),
        )
        constants_manager.set_constant("path_to_model", self.default_model_path.get())
        constants_manager.set_constant("path_to_labels", self.default_labels_path.get())
        print("Constants saved successfully!")

    def create_form(self):
        root_label = tk.Label(
            self,
            text="Constants:",
            font=("Arial", 14, "bold"),
            bg="#7C889C",
            fg="white",
        )
        root_label.pack(pady=(10, 5))

        form_frame = tk.Frame(self, bg="#7C889C")
        form_frame.pack(pady=(0, 10))

        # Default Confidence Level
        confidence_level_label = tk.Label(
            form_frame, text="Default Confidence Level:", bg="#7C889C", fg="white"
        )
        confidence_level_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.confidence_level_entry = tk.Entry(
            form_frame, textvariable=self.default_confidence_level
        )
        self.confidence_level_entry.grid(row=0, column=1, padx=10, pady=5)
        self.confidence_level_entry.bind("<KeyRelease>", self.update_confidence_level)
        self.confidence_level_entry.config(validate="key")
        self.confidence_level_entry["validatecommand"] = (
            self.confidence_level_entry.register(self.validate_numeric_input),
            "%P",
        )

        # Default Distance
        distance_label = tk.Label(
            form_frame, text="Default Distance:", bg="#7C889C", fg="white"
        )
        distance_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.distance_entry = tk.Entry(form_frame, textvariable=self.default_distance)
        self.distance_entry.grid(row=1, column=1, padx=10, pady=5)
        self.distance_entry.bind("<KeyRelease>", self.update_distance)
        self.distance_entry.config(validate="key")
        self.distance_entry["validatecommand"] = (
            self.distance_entry.register(self.validate_numeric_input),
            "%P",
        )

        # Default Targets (Multi-select)
        targets_label = tk.Label(
            form_frame, text="Default Targets:", bg="#7C889C", fg="white"
        )
        targets_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        targets = ["Target 1", "Target 2", "Target 3", "Target 4"]  # Example targets
        for idx, target in enumerate(targets):
            button = tk.Button(
                form_frame, text=target, command=lambda t=target: self.toggle_target(t)
            )
            button.grid(row=2, column=idx + 1, padx=(0, 5), pady=5, sticky="w")

        selected_targets_label = tk.Label(
            form_frame, text="Selected Targets:", bg="#7C889C", fg="white"
        )
        selected_targets_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.selected_targets_display = tk.Label(
            form_frame, text=", ".join(self.default_targets), bg="#FFFFFF", fg="#000000"
        )
        self.selected_targets_display.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Default Segmentation (Single-select)
        segmentation_label = tk.Label(
            form_frame, text="Default Segmentation:", bg="#7C889C", fg="white"
        )
        segmentation_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.segmentation_entry = ttk.Combobox(
            form_frame,
            values=[option["text"] for option in segmentation_options],
            textvariable=self.default_segmentation,
        )
        self.segmentation_entry.grid(row=4, column=1, padx=10, pady=5)
        self.segmentation_entry.bind("<<ComboboxSelected>>", self.update_segmentation)

        # Model Frame
        model_frame = tk.Frame(form_frame, bg="#7C889C")
        model_frame.grid(row=5, columnspan=2, pady=(10, 5))

        path_to_model_label = tk.Label(
            model_frame, text="Path to Model:", bg="#7C889C", fg="white"
        )
        path_to_model_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.model_entry = tk.Entry(
            model_frame, width=30, textvariable=self.default_model_path
        )
        self.model_entry.grid(row=0, column=1, padx=10, pady=5)
        browse_model_button = tk.Button(
            model_frame, text="Browse", command=self.browse_model
        )
        browse_model_button.grid(row=0, column=2, padx=5, pady=5)

        # Labels Frame
        labels_frame = tk.Frame(form_frame, bg="#7C889C")
        labels_frame.grid(row=6, columnspan=2, pady=(5, 10))

        path_to_label_file_label = tk.Label(
            labels_frame, text="Path to Labels File:", bg="#7C889C", fg="white"
        )
        path_to_label_file_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.labels_entry = tk.Entry(
            labels_frame, width=30, textvariable=self.default_labels_path
        )
        self.labels_entry.grid(row=0, column=1, padx=10, pady=5)
        browse_labels_button = tk.Button(
            labels_frame, text="Browse", command=self.browse_labels
        )
        browse_labels_button.grid(row=0, column=2, padx=5, pady=5)

        # Save Button
        save_button = tk.Button(
            self,
            text="Save",
            bg="#4CAF50",  # Green color for highlighting
            fg="white",
            font=("Arial", 12),
            command=self.save_constants,
            width=10,  # Adjust the width as needed
            height=2,  # Adjust the height as needed
            relief=tk.RAISED,  # Add a raised border
        )
        save_button.pack(pady=(10, 20))


if __name__ == "__main__":
    app = Application()
    app.protocol("WM_DELETE_WINDOW", app.on_close)  # Ensure clean exit
    app.mainloop()
