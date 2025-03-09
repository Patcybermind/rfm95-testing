import time
import busio # type: ignore
import digitalio # type: ignore
import board # type: ignore
import microcontroller # type: ignore
import adafruit_rfm9x # type: ignore

# Board LED
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Create library object using our bus SPI port for radio
spi = busio.SPI(board.GP18, MOSI=board.GP19, MISO=board.GP16)
# RFM9x Breakout Pinouts
cs = digitalio.DigitalInOut(board.GP8)
rst = digitalio.DigitalInOut(board.GP9)

cs.direction = digitalio.Direction.OUTPUT
rst.direction = digitalio.Direction.OUTPUT
buffer = bytearray(1)



spi.try_lock()
spi.configure(baudrate=10_000)  # Set frequency to 5 MHz
cs.value = False
time.sleep(0.01)
rst.value = False
time.sleep(0.01)
rst.value = True
time.sleep(0.01)
spi.write(b'\x42')
spi.readinto(buffer)
cs.value = True
spi.unlock()

print("Version = ",buffer[0])