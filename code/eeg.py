# import time 
# from pythonosc.dispatcher import Dispatcher
# from pythonosc.osc_server import BlockingOSCUDPServer
# from pythonosc.udp_client import SimpleUDPClient

# OSC_IP = "127.0.0.1"

# BCI_BAND_PORT = 12345

# PURE_DATA_PORT = 5000

# BLINK_TIMEOUT_MS = 500
# BLINK_RMS_THRESHOLD = 25

# time_of_last_blink = 0


# '''
# OSC Implementation
# '''

# OSC_CLIENT = SimpleUDPClient (OSC_IP, PURE_DATA_PORT)


# def openbci_band_handler (address, *args):
#     global time_of_last_blink
#     current_time = round (time.time() * 1000)

#     if ("0" in address):
#         rms = (sum (map (lambda x: x ** 2, args)) / len (args)) ** 0.5

#         if (rms > BLINK_RMS_THRESHOLD and current_time - time_of_last_blink > BLINK_TIMEOUT_MS):
#             time_of_last_blink = current_time
#             OSC_CLIENT.send_message ("/blink", 1)
#             print ('blink detected')
#             return

#         OSC_CLIENT.send_message ("/blink", 0)


# OSC_DISPATCHER = Dispatcher()
# OSC_DISPATCHER.map ("/openbci/*", openbci_band_handler)


# OSC_SERVER = BlockingOSCUDPServer ((OSC_IP, BCI_BAND_PORT), OSC_DISPATCHER)
# OSC_SERVER.serve_forever()



from math import sqrt
import numpy as np
from pythonosc.udp_client import SimpleUDPClient

OSC_IP = "127.0.0.1"
PURE_DATA_PORT = 5000
OSC_CLIENT = SimpleUDPClient (OSC_IP, PURE_DATA_PORT)


class OSCMessageHandler:
    def __init__(self):
        self.band_power = {}  
        self.accelerometer = {}  
        self.accelerometer_buffer = {'x': [], 'y': [], 'z': []}
        self.buffer_size = 256

    def handle_osc_message(self, address, *args):
        address_parts = address.split('/')    
        if address_parts[2] == "band-power":
            band_index = int(address_parts[3])           
            data_array = list(map(float, args))
            
            # Calculate the Root Mean Square (RMS) value
            rms_value = sqrt(sum(value**2 for value in data_array))/len(data_array)
  
            # Subtract RMS of accelerometer axes from bandpower
            # rms_accelerometer = self.get_accelerometer_rms()            
            # if rms_accelerometer:
            #     self.band_power[band_index] = rms_value - rms_accelerometer
            
            self.band_power[band_index] = rms_value 

            OSC_CLIENT.send_message (f'/band{band_index}', self.band_power[band_index])   
                    
        elif address_parts[2] == "accelerometer":  
            axis = address_parts[3]        
            value = float(args[0])        
            self.accelerometer[axis] = value
            # Update accelerometer buffer for each axis
            self.accelerometer_buffer[axis].append(value)
            if len(self.accelerometer_buffer[axis]) > self.buffer_size:
                self.accelerometer_buffer[axis].pop(0)

        print(f"Updated Values: BandPower: {self.band_power}, Accelerometer: {self.accelerometer}")      
    
    def get_accelerometer_rms(self):
        """Calculate the RMS of each accelerometer axis"""
        accelerometer_data = {axis: np.array(self.accelerometer_buffer[axis]) for axis in self.accelerometer_buffer.keys()}
        rms_values = []
        for axis, data in accelerometer_data.items():
            if len(data) == self.buffer_size: 
                rms_values.append(sqrt(np.mean(data**2)))
            else:
                return None  # Not enough data for rolling average
        return sum(rms_values) / len(rms_values) 
 
    def get_band_power(self, band_index):  
        return self.band_power.get(band_index, None)  
 
from pythonosc.osc_server import BlockingOSCUDPServer  
from pythonosc.dispatcher import Dispatcher  

IP = '127.0.0.1'        
PORT = 12345          

def main():    
    handler = OSCMessageHandler()   
    dispatcher = Dispatcher()        
    dispatcher.map("/openbci/*", handler.handle_osc_message)      
    server = BlockingOSCUDPServer((IP, PORT), dispatcher)      
    print(f"Listening for OSC messages on IP: {IP}, Port: {PORT}...")     
    server.serve_forever()  
    
if __name__ == "__main__":          
    main()  

