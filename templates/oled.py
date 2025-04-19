from machine import SPI, Pin
from utime import sleep

from presentation.oled.ssd1351 import SSD1351

# 色定義
COLORS = {
    "BLACK": 0,
    "WHITE": 0xFFFF,
    "RED": 0xF800,
    "GREEN": 0x07E0,
    "BLUE": 0x001F,
    "YELLOW": 0xFFE0,
    "CYAN": 0x07FF,
    "MAGENTA": 0xF81F,
}

# SPI 設定
spi = SPI(0, baudrate=10000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19))
dc = Pin(16, Pin.OUT)
cs = Pin(20, Pin.OUT)
rst = Pin(17, Pin.OUT)

# ディスプレイの初期化
display = SSD1351(128, 128, spi, dc, cs, rst)

# Main Loop
while True:
    try:
        display.fill(COLORS["BLACK"])
        display.hline(0, 10, 128, COLORS["WHITE"])
        display.text("Hello World!", 4, 60, COLORS["WHITE"], size=2)
        display.text("Pico W", 0, 90, COLORS["MAGENTA"])
        display.text("x", 35, 90, COLORS["WHITE"])
        display.text("MicroPython", 40, 100, COLORS["YELLOW"])
        display.show()
        sleep(1)
    except KeyboardInterrupt:
        break
