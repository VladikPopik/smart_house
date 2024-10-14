from cv2 import VideoCapture, imwrite, destroyAllWindows
from uuid import uuid4

class Capture:
    def __init__(self, camport: int=0) -> None:
        self.camport = camport

        self.cam = VideoCapture(self.camport)

    def capture_camera(self) -> None:
        """Function to capture camera with opencv."""
        result, img = self.cam.read()

        if result:
            imwrite(f"test{uuid4()}.png", img)
            destroyAllWindows()
            self.cam.release()
        else:
            print("Error")
