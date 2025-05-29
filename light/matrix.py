import time
from logging import getLogger
from singletonmeta import Singleton
from multiprocessing import Process
import adafruit_max7219.matrices
import board
import busio
import digitalio
import adafruit_max7219
import time
import skfuzzy as fuzz
import numpy as np
from skfuzzy import control as ctrl

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
        self.lux = 0
        self.coef = 15
        self.brightness_res = 0

        self.process: Process = Process(
                    target=self.adjust,
        )
        self.process.start()

        # Инициализация драйвера MAX7219
        self.spi = busio.SPI(clock=board.SCLK, MISO=None, MOSI=board.MOSI)
        self.cs_pin = digitalio.DigitalInOut(board.CE0)
        self.matrix = adafruit_max7219.matrices.Matrix8x8(spi=self.spi, cs=self.cs_pin)

        # Входящая переменная: уровень освещенности
        self.illuminance = ctrl.Antecedent(np.arange(0, 80000, 1), 'illuminance')

        # Исходящая переменная: яркость матрицы
        self.brightness = ctrl.Consequent(np.arange(0, 100, 1), 'brightness')

    def adjust(self) -> None:
        #Включение
        try:
            low = fuzz.trimf(self.illuminance.universe, [0, 0, 150])
            medium = fuzz.trimf(self.illuminance.universe, [0, 150, 300])
            high = fuzz.trimf(self.illuminance.universe, [150, 300, 800000])

            dim = fuzz.trimf(self.brightness.universe, [0, 0, 50])
            normal = fuzz.trimf(self.brightness.universe, [0, 50, 100])
            bright = fuzz.trimf(self.brightness.universe, [50, 100, 100])
            # Функции принадлежности для освещенности (низкая, средняя, высокая)
            self.illuminance['low'] = low
            self.illuminance['medium'] = medium
            self.illuminance['high'] = high

            # Функции принадлежности для яркости (низкая, средняя, высокая)
            self.brightness['dim'] = dim
            self.brightness['normal'] = normal
            self.brightness['bright'] = bright

            # Правила нечёткого вывода
            rules = [
                ctrl.Rule(self.illuminance['low'], self.brightness['bright']),       # Если темно, делаем ярко
                ctrl.Rule(self.illuminance['medium'], self.brightness['normal']),   # Средняя освещенность, нормальный режим
                ctrl.Rule(self.illuminance['high'], self.brightness['dim']),         # Высокая освещенность, приглушённый режим
            ]

            # Система контроля
            self.control_system = ctrl.ControlSystem(rules)
            self.simulator = ctrl.ControlSystemSimulation(self.control_system)
            try:
                self.matrix.fill(True)
                while True:
                    logger.info(f"Освещенность: {self.lux:.2f} lux")
                    
                    # Передача входящего значения освещенности в нечёткий регулятор
                    self.simulator.input['illuminance'] = self.lux
                    self.simulator.compute()
                    # Получаем выходное значение яркости
                    output_brightness = self.simulator.output['brightness']
                    self.brightness_res = round(output_brightness / 100 * self.coef)
                    logger.info(f"Яркость матрицы: {output_brightness:.2f}")
                    logger.info(self.brightness_res)
                    # Устанавливаем яркость матрицы
                    self.matrix.brightness(self.brightness_res)  # Масштабируем яркость в диапазон от 0 до 15
                    self.matrix.show()
                    time.sleep(0.5)

            except Exception as e:
                logger.info(e)
            finally:
                self.matrix.brightness(self.brightness_res)  # Выключаем матрицу перед выходом’’’
                self.matrix.fill(False)
                self.matrix.show()
        
        except Exception as e:
            logger.exception(f"{e}")

    def perform(self, lux) -> None:
        try:
            self.lux = lux
            if self.process.is_alive():
                self.process.kill()
            logger.info(f"ON PROCESS {self.process}")
            self.process = Process(
                target=self.adjust,
            )
            self.process.start()
            logger.info(f"Пришло: {lux}, люкс")
        except Exception as e:
            logger.exception(f"{e}")