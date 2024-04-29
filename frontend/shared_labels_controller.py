from .application_current_settings_route import current_settings_route
from constants.constantsmanager import ConstantsManager


class SharedLabels:

    def __init__(self):
        self.constants_manager = ConstantsManager(filename=current_settings_route)
        self.labels = {}
        self.selected_labels = {}

        targets = self.constants_manager.get_constant("default_targets")
        for key, value in targets.items():
            self.labels[key] = eval(value)

    def get_selected_labels(self):
        return self.selected_labels

    def set_selected_labels(self, new_labels):
        self.selected_labels = new_labels

    def get_all_labels(self):
        return self.labels

    def get_init_labels(self):
        return [(l, c) for l, c in self.labels.items()]

    def get_label_color(self):
        label_colors = [("BACKGROUND", self.labels["BACKGROUND"])]
        for l, c in self.labels.items():
            if l != "BACKGROUND":
                if l in self.selected_labels:
                    label_colors.append((l, c))
                else:
                    label_colors.append(("void", (255, 255, 255)))
        return label_colors


shared_labels = SharedLabels()
