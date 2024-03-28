import threading
import queue
import time
import os
from datetime import datetime
from scanner_image import ScannerImage


class ImageSaver:
    def __init__(self, save_rate, save_dir, images_per_rate):
        self.save_rate = save_rate
        self.save_dir = save_dir
        self.images_per_rate = images_per_rate
        self.queue = queue.Queue()
        self.priority_mapping = {
            "Highest": 1.00,
            "Very High": 0.95,
            "High": 0.90,
            "Fairly High": 0.80,
            "Moderate": 0.70,
            "Fairly Low": 0.60,
            "Low": 0.50,
        }
        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.running = False

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def add_image(self, image, detections, gps_coords):
        scanner_image = ScannerImage(image, detections, gps_coords)
        self.queue.put(scanner_image)

    def run(self):
        while self.running:
            try:
                self.process_queue()
                time.sleep(self.save_rate)
            except queue.Empty:
                continue

    def process_queue(self):
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        save_path = os.path.join(self.save_dir, current_time)
        os.makedirs(save_path, exist_ok=True)

        images_to_save = self.collect_and_sort_images()

        for i, scanner_image in enumerate(
            images_to_save[: self.images_per_rate], start=1
        ):
            image_path = os.path.join(save_path, f"{i}.png")
            scanner_image.pil_image.save(image_path)

    def collect_and_sort_images(self):
        images_to_process = []
        while not self.queue.empty():
            scanner_image = self.queue.get()
            self.assign_priority_scores(scanner_image)
            images_to_process.append(scanner_image)

        images_to_process.sort(
            key=lambda img: max(d["priority_score"] for d in img.detections),
            reverse=True,
        )
        return images_to_process

    def assign_priority_scores(self, scanner_image):
        for detection in scanner_image.detections:
            label, classID, priority_label = detection
            priority_score = (
                self.priority_mapping.get(priority_label, 1.00)
                * detection["confidence"]
            )
            detection["priority_score"] = priority_score
