import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Constants")
        self.configure(bg="#7C889C")
        self.geometry("400x300")

        # Instance variables to store values
        self.default_confidence_level = tk.StringVar(value="90")
        self.default_distance = tk.StringVar(value="1")
        self.default_targets = []
        self.default_segmentation = tk.StringVar(value="Segmentation 1")
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

    def update_confidence_level(self, event):
        self.default_confidence_level.set(self.confidence_level_entry.get())

    def update_distance(self, event):
        self.default_distance.set(self.distance_entry.get())

    def toggle_target(self, target):
        if target in self.default_targets:
            self.default_targets.remove(target)
        else:
            self.default_targets.append(target)
        self.update_selected_targets_display()

    def update_selected_targets_display(self):
        self.selected_targets_display.config(text=", ".join(self.default_targets))

    def update_segmentation(self, event):
        self.default_segmentation.set(self.segmentation_entry.get())

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

        # Default Distance
        distance_label = tk.Label(
            form_frame, text="Default Distance:", bg="#7C889C", fg="white"
        )
        distance_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.distance_entry = tk.Entry(form_frame, textvariable=self.default_distance)
        self.distance_entry.grid(row=1, column=1, padx=10, pady=5)
        self.distance_entry.bind("<KeyRelease>", self.update_distance)

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
            values=["Segmentation 1", "Segmentation 2", "Segmentation 3"],
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


if __name__ == "__main__":
    app = Application()
    app.protocol("WM_DELETE_WINDOW", app.on_close)  # Ensure clean exit
    app.mainloop()
