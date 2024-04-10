import serial
import serial.tools
import serial.tools.list_ports
import re

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

NUMBER_PATTERN = r'-?\d+[\.,]?\d*'

def cleanString (str):
    matches = re.findall (NUMBER_PATTERN, str)

    if matches:
        num_str = matches[0].replace (',', '.')
        return float (num_str) if '.' in num_str else int (num_str)
    
    return None


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return min (rightMax, max (rightMin, rightMin + (valueScaled * rightSpan)))

'''
OSC Implementation
'''

OSC_CLIENT = SimpleUDPClient (OSC_IP, PURE_DATA_PORT)
heart_address = "/heart"
skin_address = "/skin"
respiration_address = "/respiration"
time_of_last_check = time.monotonic() * 1000.0
check_interval_ms = 5.0
serial_port = '/dev/tty.usbserial-0001'
buad_rate = 9600



''' Detect serial values from Arduino '''
print ('hi')
# list all serial ports
print (serial.tools.list_ports.comports())
ser = serial.Serial (serial_port, buad_rate)

while True:

    try:

        if ser.in_waiting <= 0:
            continue

        current_time_ms = time.monotonic() * 1000.0

        #print (current_time_ms)

        if current_time_ms - time_of_last_check > check_interval_ms:

            time_of_last_check = current_time_ms

            line = ser.readline().decode('utf-8').split(" ")

            heartBpm = translate (cleanString (line[0]), 40.0, 150.0, 0.5, 4.0)
            respiration = translate (cleanString (line[1]), 300.0, 700.0, 0.0, 1.0)
            skinConductance = translate (cleanString (line[2]), 0.0, 3000.0, 0.0, 1.0)

            
            print (heartBpm, respiration, skinConductance)

            try: 
                OSC_CLIENT.send_message (heart_address, heartBpm)
                OSC_CLIENT.send_message (skin_address, skinConductance)
                OSC_CLIENT.send_message (respiration_address, respiration)
            
            except ValueError:
                continue

    except serial.SerialException:
        continue

    except KeyboardInterrupt:
        break

    except IndexError:
        continue

    except TypeError:
        continue

ser.close()