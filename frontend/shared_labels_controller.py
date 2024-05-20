from .application_current_settings_route import current_settings_route
from constants.constantsmanager import ConstantsManager


def json_to_dict(json):
    labels = {}
    for key, value in json.items():
        labels[key] = eval(value)
    return labels


def dict_to_json(dict):
    json = {}
    for key, value in dict.items():
        json[key] = str(value)
    return json


class SharedLabels:

    def __init__(self):
        self.constants_manager = ConstantsManager(filename=current_settings_route)

        targets = self.constants_manager.get_constant("default_targets")
        self.labels = json_to_dict(targets)

        selected_targets = self.constants_manager.get_constant("selected_targets")
        self.selected_labels = json_to_dict(selected_targets)

    def get_selected_labels(self):
        return self.selected_labels

    def set_selected_labels(self, new_labels):
        self.selected_labels = new_labels
        self.constants_manager.set_constant(
            "selected_targets", dict_to_json(new_labels)
        )

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
