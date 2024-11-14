from uuid import UUID, uuid4

from cv2 import VideoCapture, destroyAllWindows, imwrite
from devices.utils import Singleton

from logging import getLogger

logger = getLogger()

class Capture(metaclass=Singleton):
    error: str = "Couldnt open camera port"

    def __init__(
        self,
        device_name: str,
        voltage: float,
        pin: int,
        *,
        on: bool = False,
        camport: int = 0,
        number_of_shots: int = 1,
    ) -> None:
        self.device_name = device_name
        self.uuid: UUID = uuid4()
        self.camport = camport
        self.pin = pin
        self.voltage = voltage
        self.on = on
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

            destroyAllWindows()
            self.cam.release()

            if result:
                uuid = uuid4()
                file_path = f"data/test{uuid}.png"
                t = imwrite(file_path, img)
                logger.info(f"Is image saved? {t}, image uuid: {uuid}")  # noqa: T201
                self.uuids.append(uuid)

        return result or t
