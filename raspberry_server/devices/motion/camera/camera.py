from uuid import UUID, uuid4
from cv2 import VideoCapture, destroyAllWindows, imwrite
from devices.utils import Singleton

class Capture(metaclass=Singleton):
    error: str = "Couldnt open camera port"

    def __init__(self, camport: int = 0, number_of_shots: int=5) -> None:
        self.uuid: UUID = uuid4()
        self.camport = camport
        self.uuids: list[UUID] = []
        self.cam = None
        self.number_of_shots = number_of_shots

    def capture_camera(self) -> bool:
        """Function to capture camera with opencv."""
        self.cam = VideoCapture(self.camport) if not self.cam else self.cam
        if not self.cam.isOpened():
            self.cam = VideoCapture(1)

        for _idx in range(self.number_of_shots):
            if self.cam.isOpened():
                result, img = self.cam.read()
            else:
                result = False
                t = False

            if result:
                uuid = uuid4()
                file_path = f"data/test{uuid}.png"
                t = imwrite(file_path, img)
                print(f"Is image saved? {t}, image uuid: {uuid}")  # noqa: T201
                self.uuids.append(uuid)
        destroyAllWindows()
        self.cam.release()

        return result or t
