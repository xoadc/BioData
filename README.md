# BioData

An intermedia project using biological sensors to manipulate images in realtime. This project starts with the biosynth device developed by Erin Gee et al., and then expands upon it by adding EEG signals. It uses an Arduino library for interpreting biological signals such as photoplethysmograph (heart sensor), galvanic skin response (GSR), respiration, and brain waves (OpenBCI EEG).

# Initial Installation

Download and install the following programs and libraries.

## Arduino Installation

 - Copy the BioData folder to your Arduino or Wiring libraries folder or download it with the Arduino library manager.
 - Upload BioData.ino to your ESP32

Code verified on [Arduino 2.0.3](https://www.arduino.cc/) on a [ESP32](https://www.espressif.com/en/products/socs/esp32) microcontroller.

## PureData Installation and Libraries

- You need a minimum of PureData 0.54-1
- To run our patches you will need the external "Gem" and "else" libraries.
  - To install them, in PureData go to the "Help" menu, and then "Find externals" 
  - Search and install `Gem` and `ELSE`.

## OpenBCI Installation

- Download and install Open BCI GUI


# Operation Procedure

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

## Sensors Operation

- In the `code/Biofeedback` folder, open up a terminal and run `pip install -r requirements.txt` and then `sensors.py`
  - Make sure to open terminal from inside the folder (by default terminal opens in your root directory)
  - To open terminal inside the desired folder you can do one of the following:
  - Right-click inside a folder in finder and there should be an option "Open in Terminal"
  - Use the "cd" command in terminal, which stands for "change directory".  Type "cd" in terminal and drag the folder from finder into the terminal to automatically fill the location.



## PureData Operation

- In the `pd` folder you will find `biofbk-2.pd`, open it up.
- You should now be seeing a weird sphere with a brain on it undulated with your biology!


# Circuit Design

Refer to the [schematic](schematics/JJM_BioSynth_3-1_schem.pdf) and [bill of materials](schematics/JJM_BioSynth_3-1_bom.html)



# Credits

* Original Developer: [Erin Gee](http://www.eringee.net)
* Subsequent Developer: [Amanda Dawn Christie](http://amandadawnchristie.ca)
* Subsequent electronics & software developer: [John Janigan-Mills](http://johnjaniganmills.ca)

Contributors:
* [Theverant](https://github.com/theverant)
* [Martin Peach](https://puredata.info/Members/martinrp/OSCobjects)
* [Thomas Ouellet Fredericks](https://github.com/thomasfredericks)
* [Sofian Audry](https://github.com/sofian)

# Copyright

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

Released under GNU GPL 3.0 License.  Copyright Erin Gee 2018.
