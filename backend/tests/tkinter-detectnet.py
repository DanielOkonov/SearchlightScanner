import sys

sys.path.append("/jetson-inference/data/SearchlightScanner/backend")
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from jetson_inference import detectNet
from jetson_utils import videoSource
import time
from ai_processor import AIProcessor
from camera_manager import CameraManager


# Set up the AI model
ai_processor = AIProcessor()
ai_processor.load_model("ssd-mobilenet-v2", 0.5)

# Set up the camera
camera_manager = CameraManager()
camera_manager.open("/dev/video0", argv=["--input-width=1920", "--input-height=1080"])

# Set up the root window
root = tk.Tk()
root.title("Object Detection")
canvas = tk.Canvas(root, width=1280, height=720)
canvas.pack()

# Slider for confidence threshold
conf_thresh = tk.IntVar()
slider_frame = ttk.Frame(root)
slider_frame.pack(pady=10)
confidence_label = ttk.Label(slider_frame, text="0.5")
confidence_label.pack(side=tk.LEFT)
ttk.Label(slider_frame, text="Confidence threshold:").pack(side=tk.LEFT, padx=10)
slider = ttk.Scale(slider_frame, from_=0, to=10, orient=tk.HORIZONTAL, variable=conf_thresh, length=300, 
                    command=lambda value: (confidence_label.config(text="{:.1f}".format(float(value)/10)), 
                    ai_processor.set_confidence(float(value)/10)))
slider.set(5)  # Initial value
slider.pack(side=tk.LEFT)


def update():
    start_time = time.time()
    img = camera_manager.fetch_frame()
    detections = ai_processor.detect_objects(img)
    render_image(img, detections)
    fps = 1.0 / (time.time() - start_time)
    print("FPS: {:.2f}".format(fps))
    root.after(1, update)

def render_image(img, detections):
    img_rgb = Image.frombytes("RGB", (img.width, img.height), img)
    img_tk = ImageTk.PhotoImage(image=img_rgb)
    canvas.img_tk = img_tk
    canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
    for detection in detections:
        left = detection.Left
        top = detection.Top
        right = detection.Right
        bottom = detection.Bottom
        label = detection.ClassID
        confidence = detection.Confidence
        if confidence >= conf_thresh.get()/10:
            canvas.create_rectangle(left, top, right, bottom, outline="red")

update()

root.mainloop()

camera_manager.close()
