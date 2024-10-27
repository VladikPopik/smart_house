from concurrent.futures import ProcessPoolExecutor

from motion import Capture


if __name__ == "__main__":

    camera = Capture()
    for _i in range(5):
        with ProcessPoolExecutor(2) as executor:
            camera = Capture()
            future_camera = executor.submit(
                camera.capture_camera()
            )  # pyright: ignore[reportUnknownVariableType]
