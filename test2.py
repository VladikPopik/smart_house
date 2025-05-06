import re
import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT


serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial)

for i in range(5):
    show_message(device, "KHARITONOV MONSTR", fill="white", font=proportional(CP437_FONT), scroll_delay=0.15)
    time.sleep(1)

# time.sleep(1)
# for x in range(255):
#     with canvas(device) as draw:
#         text(draw, (0, 0), chr(x), fill="white")
#         time.sleep(0.1)

# time.sleep(1)
# with canvas(device) as draw:
#     text(draw, (0, 0), "@", fill="white")

# time.sleep(1)
# while True:
#     for intensity in range(16):
#         device.contrast(intensity * 16)
#         time.sleep(0.1)