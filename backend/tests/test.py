import sys

sys.path.append("/jetson-inference/data/SearchlightScanner/backend")
from aiprocessor import AIProcessor
from cameramanager import CameraManager
from jetson_utils import videoOutput

"""
Test class to ensure the ai processor and camera manager work
"""


def main():
    ai = AIProcessor()
    cam = CameraManager()
    ai.load_model("ssd-mobilenet-v2", 0.5)
    cam.open("/dev/video0")
    output = videoOutput()

    iterations = 0

    while True:
        iterations += 1
        frame = cam.fetch_frame()
        detections = ai.detect_objects(frame)
        output.Render(frame)
        if iterations == 100:
            cam.close()


if __name__ == "__main__":
    main()
