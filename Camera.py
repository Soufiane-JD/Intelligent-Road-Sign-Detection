import cv2
import threading


# Camera handling
class Camera:
    def __init__(self):
        self.cap = None
        self.lock = threading.Lock()
        self.timer = None

    def initialize_camera(self):
        with self.lock:
            if self.cap is None:
                self.cap = cv2.VideoCapture(0)  # Initialize the camera
                if not self.cap.isOpened():
                    raise Exception("Could not open camera")
            if self.timer:
                self.timer.cancel()  # Cancel any existing timer
            self.timer = threading.Timer(5, self.release_camera)  # Set a 5-second timer
            self.timer.start()

    def release_camera(self):
        with self.lock:
            if self.cap:
                self.cap.release()
                self.cap = None
            self.timer = None

    def capture_frame(self):
        with self.lock:
            if self.cap is None:
                self.initialize_camera()
            ret, frame = self.cap.read()
            if not ret:
                raise Exception("Failed to grab frame")
            return frame
