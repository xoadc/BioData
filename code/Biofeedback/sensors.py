# pip install -r requirements.txt

import serial
import serial.tools
import serial.tools.list_ports
import re
import time 
from pythonosc.udp_client import SimpleUDPClient

# Get a list of available serial ports
ports = serial.tools.list_ports.comports()

# Print available ports
print("Available serial ports:")
for i, port in enumerate(ports, start=1):
    print(f"{i}. {port.device}")

# Let the user select a port
selected_port_index = int(input("Enter the number of the port you want to use: ")) - 1

# Get the name of the selected port
selected_port_name = list(ports)[selected_port_index].device

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
buad_rate = 19200


''' Detect serial values from Arduino '''
ser = serial.Serial (selected_port_name, buad_rate)

while True:

    try:

        current_time_ms = time.monotonic() * 1000.0

        #print (current_time_ms)

        if current_time_ms - time_of_last_check > check_interval_ms:

            time_of_last_check = current_time_ms

            line = ser.readline().decode('utf-8').strip().split(" ")
            heart           = cleanString (line[0])
            respiration     = cleanString (line[1])
            skinConductance = cleanString (line[2])

            print (heart, respiration, skinConductance)

            try: 
                OSC_CLIENT.send_message (heart_address, heart)
                OSC_CLIENT.send_message (skin_address, skinConductance)
                OSC_CLIENT.send_message (respiration_address, respiration)
            
            except ValueError:
                continue

            except KeyboardInterrupt:
                break

    except UnicodeDecodeError:
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