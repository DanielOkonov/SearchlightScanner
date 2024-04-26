from datetime import datetime
from PIL import ImageDraw, ImageFont
import piexif
import os


class ScannerImage:

    font_color = (0, 255, 0)
    custom_font_path = None
    font_size = 16
    potential_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    def __init__(self, image, detections, gps_coords):
        self.image = image
        self.detections = detections
        self.gps_coords = gps_coords
        self.date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        self.exif_bytes = None
        if ScannerImage.custom_font_path is None:
            if os.path.isfile(ScannerImage.potential_font_path):
                ScannerImage.custom_font_path = ScannerImage.potential_font_path

    def _annotate(self):
        draw = ImageDraw.Draw(self.image)
        text = f"{self.date_time}   {self.gps_coords if self.gps_coords else '-'}"
        if ScannerImage.custom_font_path:
            font = ImageFont.truetype(ScannerImage.custom_font_path, size=ScannerImage.font_size)
        else:
            font = ImageFont.load_default()
        draw.text((0, 0), text, self.font_color, font=font)

    def _set_gps_coords(self):
        if self.gps_coords is None:
            return
        lat, lon = self.gps_coords
        if "exif" in self.image.info:
            exif_dict = piexif.load(self.image.info["exif"])
        else:
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
        exif_dict["GPS"][piexif.GPSIFD.GPSLatitude] = self._convert_to_degrees(lat)
        exif_dict["GPS"][piexif.GPSIFD.GPSLatitudeRef] = "N" if lat >= 0 else "S"
        exif_dict["GPS"][piexif.GPSIFD.GPSLongitude] = self._convert_to_degrees(lon)
        exif_dict["GPS"][piexif.GPSIFD.GPSLongitudeRef] = "E" if lon >= 0 else "W"
        self.exif_bytes = piexif.dump(exif_dict)

    @staticmethod
    def _convert_to_degrees(value):
        """Convert a decimal degree value to a tuple of degrees, minutes, and seconds."""
        d = int(value)
        md = abs(value - d) * 60
        m = int(md)
        sd = (md - m) * 60
        return ((d, 1), (m, 1), (int(sd), 1))

    def save(self, filename):
        self._annotate()
        self._set_gps_coords()

        if self.exif_bytes:
            self.image.save(filename, exif=self.exif_bytes)
        else:
            self.image.save(filename)