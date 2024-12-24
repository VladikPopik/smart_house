import RPi.GPIO as GPIO
import time
from logging import getLogger
from singletonmeta import Singleton
from multiprocessing import Process

logger = getLogger()

class Diod(metaclass=Singleton):
    def __init__(
        self, pin: int, device_name: str, *,
        on: bool = False,
        device_type: str="diod",
        is_on = False,
    ) -> None:
        self.device_name = device_name
        self.device_type = device_type
        self.pin = pin
        self.on = on
        #is_on нужен чтобы проверять был ли запущен процесс включения или выключения
        self.is_on = is_on
        #Храним процесс отвечающий за переключение 
        self.process = None

    def switch_on(self) -> None:
        #Включение
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(True)
            GPIO.setup(self.pin, GPIO.OUT)
            logger.info(f"{self.device_name}: led on")
            GPIO.output(self.pin, GPIO.HIGH)
        except Exception as e:
            logger.exception(f"{e}")
            GPIO.cleanup(self.pin)

        logger.info(f"ON PROCESS {self.process}")
        

    def switch_off(self) -> None:
        #Выключение
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(True)
            GPIO.setup(self.pin, GPIO.OUT)
            GPIO.output(self.pin, GPIO.LOW)
            logger.info(f"{self.device_name}: led off")
        except Exception as e:
            logger.exception(f"{e}")
        finally:
            GPIO.cleanup(self.pin)

        logger.info(f"OFF PROCESS {self.process}")

    def perform(self, percent) -> None:
        #Циклично вызывает процессы 
        try:
            logger.info(f"{self.is_on}, {percent}")
            #Если значение меньше 50 и не включен диод то включаем 
            if percent <= 50 and not self.is_on:
                if self.process:
                    #Если был процесс его нужно уничтожить и затереть ток на диоде 
                    self.process.kill()
                    GPIO.cleanup(self.pin)
                    logger.info(f"PROCESS TERMINATED {self.process}")
                #Создаем процесс который будет выполнять функцию switch_on то есть пускать ток
                p = Process(
                        target=self.switch_on
                    )
                p.start()
                logger.info(p)
                #Указываем что процесс запущен и что диод включен на железяке
                self.process = p
                logger.info(f"TO ON PROCESS {self.process}")
                self.is_on = True
            elif percent > 50 and self.is_on:
                #Аналогично для выключения разницы нет
                if self.process:
                    self.process.kill()
                    GPIO.cleanup(self.pin)
                    logger.info(f"PROCESS TERMINATED {self.process}")

                p = Process(
                        target=self.switch_off
                    )
                p.start()
                self.process = p
                logger.info(f"TO OFF PROCESS {self.process}")
                self.is_on = False
        except Exception as e:
            logger.exception(f"{e}")
            #Если всё упало с ошибкой тонужно указать что всё ок и всё затереть для нового цикла
            if self.process:
                self.process.kill()
                GPIO.cleanup(self.pin)
                self.is_on = False