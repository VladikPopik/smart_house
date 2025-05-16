import spidev
import time


# Настройка SPI интерфейса
spi = spidev.SpiDev()
spi.open(0, 0) # bus=0, device=0
spi.max_speed_hz = 1000000

# Определяем константы регистров MAX7219
NO_OP = 0x00
DIGIT_0 = 0x01
SHUTDOWN_REGISTER = 0x0C
DISPLAY_TEST_REGISTER = 0x0F
DECODE_MODE_REGISTER = 0x09
INTENSITY_REGISTER = 0x0A
SCAN_LIMIT_REGISTER = 0x0B

def write_register(register, value):
    spi.xfer([register, value])

def set_leds(column_data):
    for i in range(8):       # Цикл по столбцам (цифрам)
        write_register(i + DIGIT_0, column_data[i])  


write_register(SHUTDOWN_REGISTER, 0x01)     # Включаем дисплей
write_register(DISPLAY_TEST_REGISTER, 0x00)  # Выключаем тестовый режим
write_register(DECODE_MODE_REGISTER, 0x00)   # Устанавливаем прямой доступ к регистраторам
write_register(INTENSITY_REGISTER, 0xFF)     # Увеличиваем яркость до среднего уровня
write_register(SCAN_LIMIT_REGISTER, 0x07)    # Максимальное количество строк сканирования (всего 8 строк)


try:
    # for i in range(255):
        # Инициализация дисплея
        while True:
        # Заполняем колонки постепенно (от одной точки до полной строки)
            for col_value in range(1 << 8):  # 0..255
                data = [(col_value >> x & 1) * 0xff for x in range(8)]
            set_leds(data)
            time.sleep(0.5)
        
except KeyboardInterrupt:
    pass
finally:
    write_register(SHUTDOWN_REGISTER, 0x00)  # Отключение дисплея
    spi.close()