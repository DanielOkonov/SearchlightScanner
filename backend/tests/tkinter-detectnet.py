import sys

sys.path.append("/jetson-inference/data/SearchlightScanner/backend")
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from jetson_inference import detectNet
from jetson_utils import videoSource
import time
from ai_processor import AIProcessor


# Set up the AI model and camera
ai_processor = AIProcessor()
ai_processor.load_model("ssd-mobilenet-v2", 0.5)
input = videoSource("/dev/video0", argv=["--input-width=1920", "--input-height=1080"])

# Set up the root window
root = tk.Tk()
root.title("Object Detection")
canvas = tk.Canvas(root, width=1280, height=720)
canvas.pack()

# Slider for confidence level
conf_level = tk.IntVar()
slider_frame = ttk.Frame(root)
slider_frame.pack(pady=10)
ttk.Label(slider_frame, text="Detection Threshold:").pack(side=tk.LEFT, padx=10)
slider = ttk.Scale(slider_frame, from_=0, to=10, orient=tk.HORIZONTAL, variable=conf_level, length=300, 
                    command=lambda value: (threshold_label.config(text="{:.1f}".format(float(value)/10)), 
                    ai_processor.set_confidence(float(value)/10)))
slider.set(5)  # Initial value
slider.pack(side=tk.LEFT)
threshold_label = ttk.Label(slider_frame, text="0.5")
threshold_label.pack(side=tk.LEFT)


def update():
    start_time = time.time()
    img = input.Capture()
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
        if confidence > conf_level.get()/10:
            canvas.create_rectangle(left, top, right, bottom, outline="red")

update()

root.mainloop()
