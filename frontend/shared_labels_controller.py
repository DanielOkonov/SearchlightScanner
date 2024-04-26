class SharedLabels:

    labels = {
        'TRUCK': (0, 0, 0),
        'BUS': (0, 0, 0),
        'BOAT': (0, 0, 0),
        'AIRPLANE': (0, 0, 0),
        'BICYCLE': (0, 0, 0),
        'CAR': (0, 0, 0)
    }

    def __init__(self):
        self.selected_labels = {}

    def get_selected_labels(self):
        return self.selected_labels
    
    def set_selected_labels(self, new_labels):
        self.labels = new_labels

    def get_all_labels(self):
        return SharedLabels.labels
    
    def get_init_labels(self):
        return [(l, c) for l, c in SharedLabels.labels.items()]

    def get_label_color(self):
        # this function should return the selected labels, along with the colors
        return [(l, c) for l, c in SharedLabels.labels.items() if l in self.selected_labels]

shared_labels = SharedLabels()