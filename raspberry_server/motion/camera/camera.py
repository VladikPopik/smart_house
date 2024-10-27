from cv2 import VideoCapture, imwrite, destroyAllWindows
from uuid import uuid4, UUID


class Capture:
    def __init__(self, camport: int = 0) -> None:
        self.camport = camport
        self.uuids: list[UUID] = []
        self.cam = VideoCapture(self.camport)

    def capture_camera(self) -> None:
        """Function to capture camera with opencv."""
        result, img = self.cam.read()

        if result:
            uuid = uuid4()
            imwrite(f"data/test{uuid}.png", img)
            self.uuids.append(uuid)
            destroyAllWindows()
            self.cam.release()
            print("SUCCESS")
        else:
            print("Error")
