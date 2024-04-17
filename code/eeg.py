import time 
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
from pythonosc.udp_client import SimpleUDPClient

OSC_IP = "127.0.0.1"

BCI_BAND_PORT = 12345

PURE_DATA_PORT = 5000

BLINK_TIMEOUT_MS = 500
BLINK_RMS_THRESHOLD = 25

time_of_last_blink = 0


'''
OSC Implementation
'''

OSC_CLIENT = SimpleUDPClient (OSC_IP, PURE_DATA_PORT)


def openbci_band_handler (address, *args):
    global time_of_last_blink
    current_time = round (time.time() * 1000)

    if ("0" in address):
        rms = (sum (map (lambda x: x ** 2, args)) / len (args)) ** 0.5

        if (rms > BLINK_RMS_THRESHOLD and current_time - time_of_last_blink > BLINK_TIMEOUT_MS):
            time_of_last_blink = current_time
            OSC_CLIENT.send_message ("/blink", 1)
            print ('blink detected')
            return

        OSC_CLIENT.send_message ("/blink", 0)


OSC_DISPATCHER = Dispatcher()
OSC_DISPATCHER.map ("/openbci/*", openbci_band_handler)


OSC_SERVER = BlockingOSCUDPServer ((OSC_IP, BCI_BAND_PORT), OSC_DISPATCHER)
OSC_SERVER.serve_forever()

