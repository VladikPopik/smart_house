# import asyncio


# if __name__=="__main__":
#     loop = asyncio.new_event_loop()
#     loop.run_forever()

from concurrent.futures import ProcessPoolExecutor

from monitoring import DhtSensor

from motion import Capture
import math

PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

if __name__ == "__main__":
    # dht = DhtSensor[float](4)

    for i in range(5):
        with ProcessPoolExecutor(2) as executor:
            camera = Capture()

            # executor.submit(dht.read())
            future_camera = executor.submit(camera.capture_camera())