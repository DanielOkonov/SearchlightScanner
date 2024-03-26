class ScannerImage:
    def __init__(self, pil_image, detections, gps_coords, priority_levels):
        self.pil_image = pil_image
        self.detections = detections
        self.gps_coords = gps_coords
        self.priority_levels = priority_levels
