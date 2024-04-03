import time 
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

OSC_IP = "127.0.0.1"

BCI_TIME_PORT = 12345
BCI_BAND_PORT = 12346

PURE_DATA_PORT = 5000

BLINK_TIMEOUT_MS = 500
BLINK_RMS_THRESHOLD = 40

time_of_last_blink = 0


'''
OSC Implementation
'''

OSC_CLIENT = SimpleUDPClient (OSC_IP, PURE_DATA_PORT)

# if the user presses space, send a blink signal
while True:
    if input() == ' ':
        OSC_CLIENT.send_message ("/blink", 1)
        print ('blink detected')
    else:
        OSC_CLIENT.send_message ("/blink", 0)
        print ('no blink detected')