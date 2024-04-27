class SharedLabels:

    labels = {
        'BACKGROUND': (255, 255, 255),
        'vehicle': (34, 177, 76),
        'ocean debris': (255, 242, 0),
        'person': (163, 73, 164),
        'powerline': (255, 174, 201),
        'dog': (185, 122, 87),
        'ship wake': (136, 0, 21),
        'airplane': (237, 28, 36),
        'helicopter': (0, 162, 232),
        'Persons_Thermal': (63, 72, 204),
        'crashed aircraft': (255, 127, 39),
        'crashed helicopter': (255, 127, 39),
    }

    def __init__(self):
        self.selected_labels = {}

    def get_selected_labels(self):
        return self.selected_labels
    
    def set_selected_labels(self, new_labels):
        self.selected_labels = new_labels

    def get_all_labels(self):
        return SharedLabels.labels
    
    def get_init_labels(self):
        return [(l, c) for l, c in SharedLabels.labels.items()]

    def get_label_color(self):
        label_colors = [('BACKGROUND', SharedLabels.labels['BACKGROUND'])]
        for l, c in SharedLabels.labels.items():
            if l != 'BACKGROUND':
                if l in self.selected_labels:
                    label_colors.append((l, c))
                else:
                    label_colors.append(('void', (255, 255, 255)))
        return label_colors

shared_labels = SharedLabels()