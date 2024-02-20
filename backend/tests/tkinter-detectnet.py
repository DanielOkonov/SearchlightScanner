import tkinter as tk
from PIL import Image, ImageTk
from jetson_inference import detectNet
from jetson_utils import videoSource
import time

root = tk.Tk()
root.title("Object Detection")
canvas = tk.Canvas(root, width=1920, height=1080)
canvas.pack()
net = detectNet("ssd-mobilenet-v2", threshold=0.5)
input = videoSource("/dev/video0", argv=["--input-width=1920", "--input-height=1080"])


def update():
    start_time = time.time()
    img = input.Capture()
    detections = net.Detect(img, overlay="box,labels,conf")
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
        print(detection)
        left = detection.Left
        top = detection.Top
        right = detection.Right
        bottom = detection.Bottom
        label = detection.ClassID
        confidence = detection.Confidence
        canvas.create_rectangle(left, top, right, bottom, outline="red")


update()

root.mainloop()
