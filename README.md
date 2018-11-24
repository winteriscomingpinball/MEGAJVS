# MEGA-JVS
Jamma Video Standard (JVS) IO board implemented using a MEGA 2560

Based on TeensyJVS by charcole: https://github.com/charcole/TeensyJVS

The included Arduino code is intended to be used with a MEGA 2560 and a MEGA JVS V2 board (created by winteriscoming).  The boards are currently not available for sale.

The MEGA JVS V2 and V3 boards have a micro SD slot.  Profiles are stored on the card.  The directory called SD Card Contents needs to go in the root of the Micro SD card.  This includes PROFILES.HEX, LASTPROF.HEX, and DISPLAY.HEX.  If DISPLAY.HEX is present and contains a value of 0x01, then screen will be rotated 180 degrees.

In order to create more mapping profiles and edit existing ones, use profiles.py and open PROFILES.HEX from the micro SD card.

The use of profiles.py is not well documented yet.

The MEGA JVS V2 board uses a profile button to switch profiles on-the-fly.  It also uses a small OLED display like the one found <a href="https://www.amazon.com/Display-Serial-Arduino-Raspberry-DIYmall/dp/B073VD6W1H/ref=sr_1_1?ie=UTF8&qid=1533843988&sr=8-1&keywords=oled+diymall">here</a>. 

The creation of this board is documented here: <a href="https://www.arcade-projects.com/forums/index.php?thread/944-custom-jvs-i-o-mega-jvs/&postID=10213#post10213">Custom JVS I/O - MEGA JVS</a>
