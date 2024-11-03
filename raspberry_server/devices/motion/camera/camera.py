from uuid import UUID, uuid4
from pathlib import Path
from cv2 import VideoCapture, destroyAllWindows, imwrite


class Capture:
    error: str = "Couldnt open camera port"

    def __init__(self, camport: int = 0) -> None:
        self.uuid: UUID = uuid4()
        self.camport = camport
        self.uuids: list[UUID] = []

    def capture_camera(self) -> bool:
        """Function to capture camera with opencv."""
        self.cam = VideoCapture(self.camport)
        if not self.cam.isOpened():
            self.cam = VideoCapture(1)

        result, img = self.cam.read()

        if result:
            uuid = uuid4()
            file_path = f"./raspberry_server/data/test{uuid}.png"
            t = imwrite(file_path, img)
            print(f"Is image saved? {t}, image uuid: {uuid}")
            self.uuids.append(uuid)
            destroyAllWindows()
            self.cam.release()
            return result and t

        raise ValueError(self.error)
