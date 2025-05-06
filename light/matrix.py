import time
from logging import getLogger
from singletonmeta import Singleton
from multiprocessing import Process

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
        self.process = None
        self.cols = 8
        self.intensity = 128

        # Настройка SPI интерфейса
        self.spi = spidev.SpiDev()

    def write_register(self, register, value):
        self.spi.xfer([register, value])

    def adjust(self, cols=0, intensity=0x0E) -> None:
        #Включение
        try:
            # Определяем константы регистров MAX7219
            self.spi.open(0, 0) # bus=0, device=0
            self.spi.max_speed_hz = 1000000
            NO_OP = 0x00
            DIGIT_0 = 0x01
            SHUTDOWN_REGISTER = 0x0C
            DISPLAY_TEST_REGISTER = 0x0F
            DECODE_MODE_REGISTER = 0x09
            INTENSITY_REGISTER = 0x0A
            SCAN_LIMIT_REGISTER = 0x0B
            # Инициализация дисплея
            self.write_register(SHUTDOWN_REGISTER, 0x01)     # Включаем дисплей
            self.write_register(DISPLAY_TEST_REGISTER, 0x00)  # Выключаем тестовый режим
            self.write_register(DECODE_MODE_REGISTER, 0x00)   # Устанавливаем прямой доступ к регистраторам
            self.write_register(INTENSITY_REGISTER, intensity)     # Увеличиваем яркость до среднего уровня
            self.write_register(SCAN_LIMIT_REGISTER, 0x07)    # Максимальное количество строк сканирования (всего 8 строк)
            def set_leds(column_data):
                for i in range(8):       # Цикл по столбцам (цифрам)
                    self.write_register(i + DIGIT_0, column_data[i])  

            for col_value in range(1 << cols):  # 0..255
                data = [(col_value >> x & 1) * 0xff for x in range(8)]
            set_leds(data)
            time.sleep(0.1)
        
        except Exception as e:
            logger.exception(f"{e}")
            self.write_register(SHUTDOWN_REGISTER, 0x00)  # Отключение дисплея
            self.spi.close()

        logger.info(f"ON PROCESS {self.process}")

    def kill(self):
        try:
            SHUTDOWN_REGISTER = 0x0C
            self.write_register(SHUTDOWN_REGISTER, 0x00)  # Отключение дисплея
            self.spi.close()
        except Exception as e:
            logger.info(e)
        try:
            if self.process:
                self.process.kill()
                logger.info(f"PROCESS TERMINATED {self.process}")
                self.process = None
        except Exception as e:
            logger.info(e)

    def perform(self, lux) -> None:
        #Циклично вызывает процессы 
        try:
            logger.info(f"Пришло: {lux}, люкс")
            #Если значение меньше 50 и не включен диод то включаем 
            if lux < 140:
                self.kill()
                #Создаем процесс который будет выполнять функцию switch_on то есть пускать ток

                if self.intensity < 255:
                    self.intensity += 1
                else:
                    self.intensity = 255

                p = Process(
                        target=self.adjust,
                        args=(self.cols, self.intensity)
                    )
                p.start()
                logger.info(p)
                #Указываем что процесс запущен и что диод включен на железяке
                self.process = p
                logger.info(f"TO ON PROCESS {self.process}")
            elif lux > 160:
                if self.intensity > 2:
                    self.intensity -= 1
                else:
                    self.intensity = 1

                self.kill()

                p = Process(
                        target=self.adjust,
                        args=(self.cols, self.intensity)
                    )
                p.start()
                self.process = p
                logger.info(f"TO OFF PROCESS {self.process}")
        except Exception as e:
            logger.exception(f"{e}")
            #Если всё упало с ошибкой тонужно указать что всё ок и всё затереть для нового цикла
            self.kill()