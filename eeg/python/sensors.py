import serial
import serial.tools
import serial.tools.list_ports

from pySerialTransfer import pySerialTransfer as txfer

import time 
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

OSC_IP = "127.0.0.1"

BCI_BAND_PORT = 12345

PURE_DATA_PORT = 5000

BLINK_TIMEOUT_MS = 500
BLINK_RMS_THRESHOLD = 30

time_of_last_blink = 0


'''
OSC Implementation
'''

OSC_CLIENT = SimpleUDPClient (OSC_IP, PURE_DATA_PORT)
skin_address = "/skin"
time_of_last_check = time.time()
check_interval_ms = 50.0
serial_port = '/dev/tty.usbserial-0001'
buad_rate = 19200



''' Detect serial values from Arduino '''
print ('hi')
# list all serial ports
print (serial.tools.list_ports.comports())
ser = serial.Serial (serial_port, buad_rate)

while True:

    try:

        if ser.in_waiting <= 0:
            continue

        time_of_last_check = time.time()
        
        line = ser.readline().decode('utf-8').strip(" ")
        print (line)

        try: 
            value = float (line)
            print (value)
            OSC_CLIENT.send_message (skin_address, line)
        
        except ValueError:
            print ("Invalid value")

    except serial.SerialException:
        print ("Serial Exception")

    except KeyboardInterrupt:
        break

ser.close()