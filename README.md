# MEGA-JVS
Jamma Video Standard (JVS) IO board implemented using a MEGA 2560

Based on TeensyJVS by charcole: https://github.com/charcole/TeensyJVS

The included Arduino code is intended to be used with a MEGA 2560 and a MEGA JVS V2, V3, and V3.1 boards (created by winteriscoming), and the MultiJVS board by Darksoft which contains all components in a single board (i.e. this version has all Arduino components built in, so no extra components are needed): https://www.arcade-projects.com/forums/index.php?thread/13532-multi-jvs-v1-0/

The MEGA JVS V2, V3, and V3.1, and MultiJVS boards have a micro SD slot.  Profiles are stored on the card.  The directory called SD Card Contents needs to go in the root of the Micro SD card.  This includes PROFILES.HEX, LASTPROF.HEX, ID.HEX and DISPLAY.HEX.  If DISPLAY.HEX is present and contains a value of 0x01, then screen will be rotated 180 degrees.

In order to create more mapping profiles and edit existing ones, use profiles.py and open PROFILES.HEX (and optionally IDS.HEX) from the micro SD card.

The use of profiles.py is not well documented yet.  It requires python3 and pyserial.

You can install pyserial after installing python3 by using this command:
python -m pip install pyserial


The board uses a profile button to switch profiles on-the-fly.  It also uses a small OLED display like the one found <a href="https://www.amazon.com/Display-Serial-Arduino-Raspberry-DIYmall/dp/B073VD6W1H/ref=sr_1_1?ie=UTF8&qid=1533843988&sr=8-1&keywords=oled+diymall">here</a>. 

The creation of the MEGA JVS board is documented here: <a href="https://www.arcade-projects.com/forums/index.php?thread/944-custom-jvs-i-o-mega-jvs/&postID=10213#post10213">Custom JVS I/O - MEGA JVS</a>

There is a compiled binary included in this repository.  This is the firmware that can be uploaded to the board.  You can use a standalone program such as Xloader, which has a GUI, but may not work on newer Windows versions, or the command line tool Arduino Sketch Uploader: https://github.com/twinearthsoftware/ArduinoSketchUploader
Otherwise, the source code can be compiled and uploaded directly within the Arduino IDE.