# BioData

A multi-media project inspired by Erin Gee et al. It uses an Arduino library for interpreting biological signals such as photoplethysmograph (heart sensor), galvanic skin response (GSR), respiration, and brain waves (OpenBCI EEG).

## Arduino Installation

Copy the BioData folder to your Arduino or Wiring libraries folder or download it with the Arduino library manager.

Code verified on [Arduino 2.0.3](https://www.arduino.cc/) on a [ESP32](https://www.espressif.com/en/products/socs/esp32) microcontroller.

## OpenBCI Installation and Operation

- Set all dipswitches to the down (negative) position
- Plug one ear clip into D_G, the other into REF
- Plug the frontal lobe electrodes into +1 and +2, back lobe electrodes into +3 and +4
- Plug in USB dongle, turn on Ganglion board
- Start OpenBCI_GUI
  - select Ganglion as the DATA SOURCE
  - select BLED112 Dongle as the transfer protocol
  - select the Ganglion-e16e from the list and START SESSION.
- There should be four panels present - on one of the panels, select "Networking" from the drop-down panel.
  - On top right of this panel, select OSC as the Protocol.
  - Under Stream 1, select BANDPOWER as the DataType, IP should be 127.0.0.1, PORT should be 12345
- Finally, under the NETWORKING window, click "Start OSC Stream"
- In the code folder, open up a terminal and run "eeg.py"
  - You will need to install `pip install python-osc`

## Sensors Operation

- Upload BioData.ino to your ESP32
- In the code folder, open up a terminal and launch "sensors.py"
  - You will need python-osc, PySerialTransfer, and PySerial to run it 
    - Install using `pip install pySerialTransfer`, `pip install pyserial`, and `pip install python-osc`

## PureData Operation

- You need a minimum of PureData 0.54-1
- To run our patches you will need the external "Gem" and "else" libraries.
  - To install them, in PureData go to the "Help" menu, and then "Find externals" 
  - Search and install "Gem" and "else".
- In the "pd" folder you will find "biofbk-2.pd", open it up.
- You should now be seeing a weird sphere with a brain on it undulated with your biology!


# Circuit Design

Refer to the [schematic](schematics/JJM_BioSynth_3-1_schem.pdf) and [bill of materials](schematics/JJM_BioSynth_3-1_bom.html)



# Credits

* Original Developer: [Erin Gee](http://www.eringee.net)
* Subsequent Developer: [Amanda Dawn Christie](http://amandadawnchristie.ca)
* Electronics & software nerd: [John Janigan-Mills](http://johnjaniganmills.ca)

Contributors:
* [Martin Peach](https://puredata.info/Members/martinrp/OSCobjects)
* [Thomas Ouellet Fredericks](https://github.com/thomasfredericks)
* [Sofian Audry](https://github.com/sofian)

# Copyright

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

Released under GNU GPL 3.0 License.  Copyright Erin Gee 2018.
