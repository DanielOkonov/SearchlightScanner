from datetime import datetime
from PIL import ImageDraw, ImageFont


class ScannerImage:
    def __init__(self, image, detections, gps_coords):
        self.image = image
        self.detections = detections
        self.gps_coords = gps_coords
        self.date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._annotate()

    def _annotate(self):
        draw = ImageDraw.Draw(self.image)
        font = ImageFont.truetype("arial", 48)
        text = f"{self.date_time}   {self.gps_coords}"
        draw.text((0, 0), text, (0, 255, 0), font=font)
        # set the long and lat of the image
