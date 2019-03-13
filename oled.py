#!/usr/bin/env python

import time
import socket
import fcntl
import struct
import commands
import os

from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1309, ssd1325, ssd1331, sh1106


# rev.1 users set port=0
# substitute spi(device=0, port=0) below if using that interface
#serial = i2c(port=1, address=0x3C)

# substitute ssd1331(...) or sh1106(...) below if using that device
#device = ssd1306(serial)

#with canvas(device) as draw:
#    draw.rectangle(device.bounding_box, outline="white", fill="black")
#    draw.text((30, 40), "Hello World", fill="white")

lock="/run/lock/oled"

def getIP(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(), 
        0x8915,  # SIOCGIFADDR 
        struct.pack('256s', ifname[:15]) 
    )[20:24])


def showStatus(oled):
    with canvas(oled) as draw:
        draw.rectangle(oled.bounding_box, outline="white", fill="black")
        draw.text((20, 16), "IP:" + getIP("wlan0"), fill="white")
    time.sleep(1)


def main():
    if os.path.isfile(lock):
        return
    os.mknod(lock)
    oled = ssd1306(port=1, address=0x3C)
    while True:
        if not(os.path.isfile(lock)):
            break
        showStatus(oled)

if __name__ == "__main__":
    main()
