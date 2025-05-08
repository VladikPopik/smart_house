import time
from logging import getLogger
from singletonmeta import Singleton
from multiprocessing import Process, Queue

import spidev

logger = getLogger()

class Matrix(metaclass=Singleton):
    def __init__(
        self, pin: int, device_name: str, *,
        on: bool = False,
        device_type: str="matrix",
    ) -> None:
        self.device_name = device_name
        self.device_type = device_type
        self.pin = pin
        self.on = on
        #Храним процесс отвечающий за переключение 
        self.process: Process | None = None

        self.process: Process = Process(
                    target=self.adjust
                )
        self.process.start()

        self.queue = Queue()
        self.cols = 8
        self.intensity = 1

        # Настройка SPI интерфейса
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0) # bus=0, device=0
        self.spi.max_speed_hz = 1000000
        self.NO_OP = 0x00
        self.DIGIT_0 = 0x01
        self.SHUTDOWN_REGISTER = 0x0C
        self.DISPLAY_TEST_REGISTER = 0x0F
        self.DECODE_MODE_REGISTER = 0x09
        self.INTENSITY_REGISTER = 0x0A
        self.SCAN_LIMIT_REGISTER = 0x0B

    def write_register(self, register, value):
        self.spi.xfer([register, value])

    def adjust(self) -> None:
        intensity = self.queue.get()
        logger.info(f"INTENSITY: {intensity}")
        try:
            self.write_register(self.SHUTDOWN_REGISTER, 0x01)     # Включаем дисплей
            self.write_register(self.DISPLAY_TEST_REGISTER, 0x00)  # Выключаем тестовый режим
            self.write_register(self.DECODE_MODE_REGISTER, 0x00)   # Устанавливаем прямой доступ к регистраторам
            self.write_register(self.INTENSITY_REGISTER, intensity)     # Увеличиваем яркость до среднего уровня
            self.write_register(self.SCAN_LIMIT_REGISTER, 0x07)    # Максимальное количество строк сканирования (всего 8 строк)
            def set_leds(column_data):
                for i in range(8):
                    self.write_register(i + self.DIGIT_0, column_data[i])
            for col_value in range(1 << self.cols):  # 0..255
                data = [(col_value >> x & 1) * 0xff for x in range(8)]
            set_leds(data)
            time.sleep(0.1)
        except Exception as e:
            logger.exception(f"{e}")

    def perform(self, lux) -> None:
        #Циклично вызывает процессы 
        try:
            logger.info(f"Пришло: {lux}, люкс")
            #Если значение меньше 50 и не включен диод то включаем 
            if lux < 140:
                if self.intensity < 255:
                    self.intensity += 1
                else:
                    self.intensity = 255
            elif lux > 160:
                if self.intensity > 2:
                    self.intensity -= 1
                else:
                    self.intensity = 1

            self.queue.put(self.intensity)
        except Exception as e:
            logger.exception(f"{e}")