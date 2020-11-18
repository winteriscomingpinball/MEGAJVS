char versionNum[9]="v1.1.9";

//NEED TO REWORK MEGA 2560 HID inputs for debounce

//Confirmed working on Arduino IDE version 1.6.12

//MEGA JVS - Code V1.1.9 - For MEGA JVS V2, MEGA JVS V3, MEGA JVS V3.1 and Darksoft's MultiJVS: https://www.arcade-projects.com/forums/index.php?thread/13532-multi-jvs-v1-0/

//Built on top of TeensyJVS code by charcole.
//TeensyJVS can be found here: https://github.com/charcole/TeensyJVS
//TeensyJVS code was used with permission by the author.
//MEGA JVS code by winteriscoming.
//Special thanks to Darksoft and rtw.

//Not to be used for commmercial purposes.  Only private use is permitted.
//No warranty is given.  Use at your own risk.

//Much of the TeensyJVS methodology for handling JVS communication
//is in-tact, verbatim.  Additons were made to accomodate additional digital
//inptus, analog inputs, and outputs.  Other changes were made to adapt to
//the Arduino MEGA 2560 and overall to utilize MEGA JVS V2 pcb.

//HID functionality is not well tested and requires a firmware change on the MEGA 2560.
//Compatability with DUE has not been verified with this release.

//Code compiles on Arduino IDE 1.6.12 for the Arduino MEGA 2560

//Profiles are saved on the MicroSD card and can be edited/created with the supplied Python Script.

//Settings to make reading analog faster
#define FASTADC 1
// defines for setting and clearing register bits
#ifndef cbi
#define cbi(sfr, bit) (_SFR_BYTE(sfr) &= ~_BV(bit))
#endif
#ifndef sbi
#define sbi(sfr, bit) (_SFR_BYTE(sfr) |= _BV(bit))
#endif


#include <SPI.h>
#include <SD.h>

//Variable for Profiles file found on SD card.  File must be named PROFILES.HEX
File myFile;

//Debounce Time in MS
#define DEBOUNCE_TIME 25

#include <Bounce2.h>

Bounce * debouncerarray = new Bounce[34];

//Enter your steering min and max according to the values you see in the JVS input tests.
//Make sure to keep 0x in front of the number to define it as a HEX value.
#define STEERING_MIN 0x1F
#define STEERING_MAX 0xDF


#if defined (_VARIANT_ARDUINO_DUE_X_)
      // Arduino DUE - specific code
//#include <Joystick.h>
#endif

//#include <U8g2lib.h>
#include "U8glib.h"

//u8g2_t *lrc_u8g;

//U8G2_SSD1306_128X64_NONAME_1_SW_I2C u8g2(U8G2_R0, /* clock=*/ SCL, /* data=*/ SDA, /* reset=*/ U8X8_PIN_NONE);   // All Boards without Reset of the Display
//U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, /* clock=*/ SCL, /* data=*/ SDA, /* reset=*/ U8X8_PIN_NONE);   // All Boards without Reset of the Display

//U8G2_SSD1306_128X64_NONAME_1_HW_I2C u8g2(U8G2_R0,U8X8_PIN_NONE);

U8GLIB_SSD1306_128X64 u8g(U8G_I2C_OPT_NO_ACK);


//MEGA JVS Bitmap
uint8_t pic_Logo_bmp[] = {
0x00, 0x1F, 0x01, 0xF0, 0x00, 0x0F, 0xFF, 0xC0, 0x3F, 0xFF, 0xC0, 0x03, 0xC0, 0x00, 0x00,0x00,
0x00, 0x3F, 0x83, 0xF8, 0x00, 0x3F, 0xFF, 0xC0, 0xFF, 0xFF, 0xC0, 0x0F, 0xF0, 0x00, 0x00,0x00,
0x00, 0x7F, 0xC7, 0xFC, 0x00, 0x7F, 0xFF, 0xC1, 0xFF, 0xFF, 0xC0, 0x1F, 0xF0, 0x00, 0x00,0x00,
0x00, 0x7F, 0xEF, 0xFC, 0x00, 0xFF, 0xFF, 0xC3, 0xFF, 0xFF, 0xC0, 0x1F, 0xF8, 0x00, 0x00,0x00,
0x00, 0xF1, 0xEF, 0x1E, 0x01, 0xF8, 0x00, 0x07, 0xE0, 0x00, 0x00, 0x1E, 0x78, 0x00, 0x00,0x00,
0x00, 0xF7, 0xFF, 0x5E, 0x01, 0xE7, 0xFF, 0xC7, 0x9F, 0xFF, 0xC0, 0x3D, 0xBC, 0x00, 0x00,0x00,
0x00, 0xF6, 0xFE, 0xFE, 0x03, 0xEF, 0xFF, 0xCF, 0xBF, 0xFF, 0xC0, 0x3D, 0xBC, 0x00, 0x00,0x00,
0x01, 0xEE, 0xFE, 0xEF, 0x03, 0xDF, 0xFF, 0xCF, 0x7F, 0xFF, 0xC0, 0x3F, 0xFC, 0x00, 0x00,0x00,
0x01, 0xEF, 0x7E, 0xEF, 0x03, 0xDF, 0xFF, 0xCF, 0x7F, 0xFF, 0xC0, 0x7B, 0xDE, 0x00, 0x00,0x00,
0x01, 0xFF, 0x7D, 0xF7, 0x83, 0xDE, 0x00, 0x0F, 0x78, 0x00, 0x00, 0x7B, 0xDE, 0x00, 0x00,0x00,
0x03, 0xDF, 0x7D, 0xF7, 0x83, 0xDF, 0xFF, 0x0F, 0x7B, 0xFF, 0xC0, 0xFF, 0xEE, 0x00, 0x00,0x00,
0x03, 0xDF, 0xBF, 0xF7, 0x83, 0xDF, 0xFF, 0x0F, 0x7B, 0xFF, 0xC0, 0xF7, 0xEF, 0x00, 0x00,0x00,
0x07, 0xFF, 0xBB, 0xFB, 0xC3, 0xDF, 0xFF, 0x0F, 0x7B, 0xFF, 0xC0, 0xF7, 0xEF, 0x00, 0x00,0x00,
0x07, 0xBF, 0xBB, 0xFB, 0xC3, 0xDF, 0xFF, 0x0F, 0x7B, 0xFF, 0xC1, 0xEF, 0xF7, 0x80, 0x00,0x00,
0x07, 0xBF, 0xD7, 0xFB, 0xC3, 0xC0, 0x00, 0x0F, 0x78, 0x01, 0xC1, 0xEF, 0xF7, 0x80, 0x00,0x00,
0x0F, 0x7B, 0xD7, 0xBD, 0xE3, 0xDF, 0xFF, 0x0F, 0x7B, 0xFD, 0xC1, 0xEE, 0x77, 0x80, 0x00,0x00,
0x0F, 0x79, 0xF7, 0xBD, 0xE3, 0xDF, 0xFF, 0x0F, 0x7B, 0xFD, 0xC3, 0xDE, 0x7B, 0xC0, 0x00,0x00,
0x0F, 0x79, 0xEF, 0x3D, 0xE3, 0xDF, 0xFF, 0x0F, 0x7B, 0xFD, 0xC3, 0xDE, 0x7B, 0xC0, 0x00,0x00,
0x1E, 0xF1, 0xEF, 0x1E, 0xF3, 0xDF, 0xFF, 0x0F, 0x7B, 0xFD, 0xC3, 0xDC, 0x39, 0xC0, 0x00,0x00,
0x1E, 0xF0, 0xFF, 0x1E, 0xF3, 0xDE, 0x00, 0x0F, 0x78, 0x7D, 0xC7, 0xBC, 0x3D, 0xE0, 0x00,0x00,
0x1E, 0xF0, 0xFE, 0x0E, 0xFB, 0xDE, 0x00, 0x0F, 0x78, 0x7D, 0xC7, 0xBC, 0x3D, 0xE0, 0x00,0x00,
0x3D, 0xE0, 0xFE, 0x0F, 0x7B, 0xDF, 0xFF, 0xCF, 0x7F, 0xFD, 0xC7, 0xBF, 0xFE, 0xE0, 0x00,0x00,
0x3D, 0xE0, 0x7C, 0x0F, 0x7B, 0xCF, 0xFF, 0xCF, 0x3F, 0xFD, 0xCF, 0x7F, 0xFE, 0xF0, 0x00,0x00,
0x3D, 0xE0, 0x7C, 0x07, 0x3F, 0xEF, 0xFF, 0xCF, 0xBF, 0xFD, 0xCF, 0x7F, 0xFE, 0xF0, 0x00,0x00,
0x7B, 0xC0, 0x3C, 0x07, 0xBD, 0xE7, 0xFF, 0xC7, 0x9F, 0xFD, 0xDF, 0x7F, 0xFF, 0x70, 0x00,0x00,
0x7B, 0xC0, 0x38, 0x07, 0xBD, 0xF8, 0x00, 0x07, 0xE0, 0x01, 0xDE, 0xF0, 0x00, 0x78, 0x00,0x00,
0xFB, 0xC0, 0x38, 0x03, 0xDE, 0xFF, 0xFF, 0xC3, 0xFF, 0xFF, 0xDE, 0xFF, 0xFF, 0xF8, 0x00,0x00,
0xF7, 0x80, 0x18, 0x03, 0xDE, 0x7F, 0xFF, 0xC1, 0xFF, 0xFF, 0xFC, 0xEF, 0xFF, 0xFC, 0x00,0x00,
0xF7, 0x80, 0x10, 0x03, 0xDE, 0x3F, 0xFF, 0xC0, 0xFF, 0xFF, 0xFD, 0xEF, 0xFF, 0xFC, 0x00,0x00,
0xFF, 0x80, 0x10, 0x01, 0xEF, 0x0F, 0xFF, 0xC0, 0x3F, 0xFF, 0xFD, 0xEF, 0xFF, 0xFC, 0x00,0x00,
0x00, 0x00, 0x00, 0x00, 0x7B, 0xFE, 0xF0, 0x03, 0xDE, 0x07, 0xFF, 0xC0, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x00, 0x00, 0x7B, 0xDE, 0xF0, 0x03, 0xDE, 0x1F, 0xFF, 0xC0, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x00, 0x00, 0x7B, 0xDE, 0x70, 0x07, 0xBE, 0x7F, 0xFF, 0xC0, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x00, 0x00, 0x7B, 0xCF, 0x78, 0x07, 0xBC, 0xFF, 0xFF, 0xC0, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x00, 0x00, 0x7B, 0xCF, 0x78, 0x07, 0xBC, 0xF8, 0x00, 0x00, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x00, 0x00, 0x7B, 0xCF, 0xB8, 0x0F, 0x79, 0xF3, 0xFF, 0xC0, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x00, 0x00, 0x7B, 0xC7, 0xBC, 0x0F, 0x79, 0xEF, 0xFF, 0xC0, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x00, 0x00, 0x7B, 0xC7, 0xBC, 0x0F, 0x7B, 0xCF, 0xFF, 0xC0, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x00, 0x00, 0x7B, 0xC3, 0xDC, 0x1E, 0xF3, 0xDF, 0xFF, 0xC0, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x00, 0x00, 0x7B, 0xC3, 0xDE, 0x1E, 0xF3, 0xDF, 0x00, 0x00, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x07, 0xFF, 0x7B, 0xC3, 0xDE, 0x1E, 0xF3, 0xDF, 0xC0, 0x00, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x07, 0xFF, 0x7B, 0xC1, 0xEE, 0x3D, 0xE3, 0xCF, 0xF8, 0x00, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x07, 0xFF, 0x7B, 0xC1, 0xEF, 0x3D, 0xE3, 0xEF, 0xFE, 0x00, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x07, 0xFF, 0x7B, 0xC1, 0xEF, 0x3D, 0xE1, 0xE7, 0xFF, 0x00, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x07, 0x80, 0x7B, 0xC0, 0xF7, 0x7B, 0xC1, 0xF0, 0xFF, 0x00, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x07, 0xBF, 0x7B, 0xC0, 0xF7, 0xFB, 0xC1, 0xFE, 0x1F, 0x80, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x07, 0xBF, 0x7B, 0xC0, 0xF7, 0xFF, 0xC0, 0xFF, 0xC7, 0x80, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x07, 0xBF, 0x7B, 0xC0, 0x7B, 0xF7, 0x80, 0x7F, 0xF7, 0xC0, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x07, 0xBF, 0x7B, 0xC0, 0x7B, 0xF7, 0x80, 0x1F, 0xF3, 0xC0, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x07, 0xBC, 0x7B, 0xC0, 0x7B, 0xFF, 0x00, 0x03, 0xFB, 0xC0, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x07, 0xBC, 0x7B, 0xC0, 0x3D, 0xEF, 0x00, 0x00, 0xFB, 0xC0, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x07, 0xBF, 0xFB, 0xC0, 0x3D, 0xEF, 0x03, 0xFF, 0xFB, 0xC0, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x07, 0xBF, 0xFB, 0xC0, 0x1F, 0xDE, 0x03, 0xFF, 0xF3, 0xC0, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x07, 0xBF, 0xFB, 0xC0, 0x1E, 0xDE, 0x03, 0xFF, 0xF7, 0x80, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x07, 0xDF, 0xF7, 0xC0, 0x1E, 0xDE, 0x03, 0xFF, 0xCF, 0x80, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x03, 0xE0, 0x0F, 0x80, 0x0F, 0x3C, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x03, 0xFF, 0xFF, 0x80, 0x0F, 0xFC, 0x03, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x01, 0xFF, 0xFF, 0x00, 0x0F, 0xF8, 0x03, 0xFF, 0xFE, 0x00, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x00, 0xFF, 0xFE, 0x00, 0x07, 0xF8, 0x03, 0xFF, 0xF8, 0x00, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x00, 0x3F, 0xF8, 0x00, 0x01, 0xE0, 0x03, 0xFF, 0xE0, 0x00, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,0x00
};


//MEGA JVS Specific Pins
#define PIN_TXENABLE  2
#define PIN_SENSE 3
#define PIN_LED   13
#define PROFILE_PIN_NUM 4

//General JVS Type 1 I/O Pins - MEGA 2560 Pin Numbers
#define P1_START_NUM 12
#define P1_RIGHT_NUM 10
#define P1_LEFT_NUM 8
#define P1_UP_NUM 6
#define P1_DOWN_NUM 14
#define P1_SW1_NUM 48
#define P1_SW2_NUM 44
#define P1_SW3_NUM 40
#define P1_SW4_NUM 36
#define P1_SW5_NUM 32
#define P1_SW6_NUM 28
#define P1_SW7_NUM 24
#define P1_SERVICE_NUM 23
#define P2_START_NUM 11
#define P2_RIGHT_NUM 9
#define P2_LEFT_NUM 7
#define P2_UP_NUM 5
#define P2_DOWN_NUM 15
#define P2_SW1_NUM 46
#define P2_SW2_NUM 42
#define P2_SW3_NUM 38
#define P2_SW4_NUM 34
#define P2_SW5_NUM 30
#define P2_SW6_NUM 26
#define P2_SW7_NUM 22
#define P2_SERVICE_NUM 25
#define TEST_NUM 27
#define COIN1_NUM 29
#define COIN2_NUM 31

//OR2 Specific Names
#define VIEW_SW_PIN_NUM 14
#define SHIFT_UP_PIN_NUM 5
#define SHIFT_DOWN_PIN_NUM 15

//Optional Inputs
#define OPT_PIN1_NUM A11
#define OPT_PIN2_NUM A10
#define OPT_PIN3_NUM A9
#define OPT_PIN4_NUM A8

//Generic outputs per Type 1 I/O
//Note that MEGA JVS has an optional 5V and 12V output header. 
//These outputs are tied to output 1_3 and 2_3 repectively.
#define OUT1_1 33
#define OUT1_2 37
#define OUT1_3 41
#define OUT2_1 35
#define OUT2_2 39
#define OUT2_3 43

//OR2 specific output names
#define START_LAMP 33
#define VIEW_LAMP 39

#define DEBOUNCE_DELAY 0x0380

enum
{
  CMD_RESET = 0xF0,      // Always followed by 0xD9
  CMD_SETADDRESS = 0xF1,
  CMD_SETMETHOD = 0xF2,

  CMD_READID = 0x10,
  CMD_FORMATVERSION = 0x11,
  CMD_JVSVERSION = 0x12,
  CMD_COMMSVERSION = 0x13,
  CMD_GETFEATURES = 0x14,
  CMD_SETMAINBOARDID = 0x15,

  CMD_READSWITCHES = 0x20,
  CMD_READCOIN = 0x21,
  CMD_READANALOG = 0x22,
  CMD_READROTARY = 0x23,
  CMD_READKEYCODE = 0x24,
  CMD_READSCREENPOS = 0x25,
  CMD_READGPIO = 0x26,

  CMD_WRITEPAYOUTREMAINING = 0x2E,
  CMD_RESEND = 0x2F,
  CMD_WRITECOINSUBTRACT = 0x30,
  CMD_WRITEPAYOUT = 0x31,
  CMD_WRITEGPIO1 = 0x32,
  CMD_WRITEANALOG = 0x33,
  CMD_WRITECHAR = 0x34,
  CMD_WRITECOINADDED = 0x35,
  CMD_WRITEPAYOUTSUBTRACT = 0x36,
  CMD_WRITEGPIOBYTE = 0x37,
  CMD_WRITEGPIOBIT = 0x38
};

long logo_timer = 0;
bool logoOn = true;

bool waitForComms = true;
struct Packet
{
  int address;
  int length;
  //byte message[255];
  byte message[500];
};

struct Reply
{
  int length;
  byte message[255];
};

byte profileID[100];
bool profileIDSet = false;
byte IDLength = 0;

byte all_inputs[34] = 
{
  PROFILE_PIN_NUM,
  P1_START_NUM,
  P1_RIGHT_NUM,
  P1_LEFT_NUM,
  P1_UP_NUM,
  P1_DOWN_NUM,
  P1_SW1_NUM,
  P1_SW2_NUM,
  P1_SW3_NUM,
  P1_SW4_NUM,
  P1_SW5_NUM,
  P1_SW6_NUM,
  P1_SW7_NUM,
  P1_SERVICE_NUM,
  P2_START_NUM,
  P2_RIGHT_NUM,
  P2_LEFT_NUM,
  P2_UP_NUM,
  P2_DOWN_NUM,
  P2_SW1_NUM,
  P2_SW2_NUM,
  P2_SW3_NUM,
  P2_SW4_NUM,
  P2_SW5_NUM,
  P2_SW6_NUM,
  P2_SW7_NUM,
  P2_SERVICE_NUM,
  TEST_NUM,
  COIN1_NUM,
  COIN2_NUM,
  OPT_PIN1_NUM,
  OPT_PIN2_NUM,
  OPT_PIN3_NUM,
  OPT_PIN4_NUM
};


//Pins defined as position in array above
#define  PROFILE_PIN 0
#define  P1_START  1
#define  P1_RIGHT  2
#define  P1_LEFT  3
#define  P1_UP  4
#define  P1_DOWN 5
#define  P1_SW1 6
#define  P1_SW2 7
#define  P1_SW3 8
#define  P1_SW4 9
#define  P1_SW5 10
#define  P1_SW6 11
#define  P1_SW7 12
#define  P1_SERVICE 13
#define  P2_START 14
#define  P2_RIGHT 15
#define  P2_LEFT 16
#define  P2_UP 17
#define  P2_DOWN 18
#define  P2_SW1 19
#define  P2_SW2 20
#define  P2_SW3 21
#define  P2_SW4 22
#define  P2_SW5 23
#define  P2_SW6 24
#define  P2_SW7 25
#define  P2_SERVICE 26
#define  TEST 27
#define  COIN1 28
#define  COIN2 29
#define  OPT_PIN1 30
#define  OPT_PIN2 31
#define  OPT_PIN3 32
#define  OPT_PIN4 33

//OR2 Specific names as position in all_inputs array above
#define VIEW_SW_PIN P1_DOWN
#define SHIFT_UP_PIN P2_UP
#define SHIFT_DOWN_PIN P2_DOWN

//Byte to store last profile num as read in from the LASTPROF.HEX file on SD card.
//Used for assigning last read profile.
byte lastprofilenum = 0;

//Byte to store count of profiles as read from SD card.
byte profilecount =0;


struct Mapping_Profile
{
  byte player1_pins[16];
  byte player2_pins[16];
  byte analog_channels[8];
  byte outputs[8];
  char title[5];
  byte output_count;
  uint16_t steering_options[3];
  byte special_case;
  byte smoothing_count;
};

//A default profile struct in case SD card is not present
Mapping_Profile default_profile=
  {
 {
   P1_SW2,P1_SW1,P1_RIGHT,P1_LEFT,P1_DOWN,P1_UP,P1_SERVICE,P1_START,
   0,0,0,P1_SW7,P1_SW6,P1_SW5,P1_SW4,P1_SW3
 },
 {
   P2_SW2,P2_SW1,P2_RIGHT,P2_LEFT,P2_DOWN,P2_UP,P2_SERVICE,P2_START,
   0,0,0,P2_SW7,P2_SW6,P2_SW5,P2_SW4,P2_SW3
 },
 {A0,A1,A2,A3,A4,A5,0,0}
 ,
 {
 0,0,OUT2_3,OUT2_2,OUT2_1,OUT1_3,OUT1_2,OUT1_1
 },
 "DFLT",
 22,//changed from 6 to 22
 {1,0,0},
 0,
 0
};


Mapping_Profile current_profile=
  {
 {
   P1_SW2,P1_SW1,P1_RIGHT,P1_LEFT,P1_DOWN,P1_UP,P1_SERVICE,P1_START,
   0,0,0,P1_SW7,P1_SW6,P1_SW5,P1_SW4,P1_SW3
 },
 {
   P2_SW2,P2_SW1,P2_RIGHT,P2_LEFT,P2_DOWN,P2_UP,P2_SERVICE,P2_START,
   0,0,0,P2_SW7,P2_SW6,P2_SW5,P2_SW4,P2_SW3
 },
 {A0,A1,A2,A3,0,0,0,0}
 ,
 {
 0,0,OUT2_3,OUT2_2,OUT2_1,OUT1_3,OUT1_2,OUT1_1
 },
 "DFLT",
 6,
 {1,0,0},
 0,
 0
};

//Pointer to current profile so that it can be accessed as bytes.
byte *profbuff = (byte *) &current_profile;

//variable to store current special case - used for steering smoothing, gear management, etc.
byte special_case = 0;

//variable to store steering options
int steering_options[3]={0,0,0};


int current_profile_num = 0;
char current_profile_name[5] = "ABCD";

Packet packet;
Reply reply[2];
int curReply = 0;
int deviceId = -1;


//Coin variables
int coin1_val = 0;
int coin2_val = 0;
boolean coin1_state = false;
boolean coin2_state = false;


boolean profile_state = false;
boolean test_state = false;



int analog_smoothing[5] = {1};

byte center_steering = 0x83;
float steering_modifier = 1.5;

byte features[] =
{
  1, 2, 13, 0,    // Players=2 Switches=13
  2, 2, 0, 0,   // 2 coin slot
  3, 8, 0, 0,   // 8 analog channels - 0(unknown) bits
  18, 6, 0, 0,  // 6 GPIO outputs
  0       // End of features
};

byte analog_channel_data[16] =
{
  1,0,0,0,0,0,0,0,
  0,0,0,0,0,0,0,0
};

//Array to store analog pins from profile.
byte cur_analog_channel_pins[8] =
{
  //A0,A1,A2,A3,A4,A5,A6,A7
  A0,A1,A2,A3,0,0,0,0
};


byte P1_pins[16] =
{
0,VIEW_SW_PIN,0,0,SHIFT_DOWN_PIN,SHIFT_UP_PIN,P1_SERVICE,P1_START,
0,0,0,0,0,0,0,0
};

/*P2 Pin Order
 * P2 Button2, P2 Button1, P2 Right, P2 Left, P2 Down, P2 Up, P2 Service, P2 Start
 * P2 Button7, P2 Button6, P2 Button5, P2 Button4, P2 Button3,
*/
byte P2_pins[16] =
{
0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0
};

// Output pins in order (8,7,6,5,4,3,2,1)
byte Output_Pins[8]=
{
 0,0,OUT2_3,OUT2_2,OUT2_1,OUT1_3,OUT1_2,OUT1_1
};



boolean initialized = false;

byte zeros[64] = {
  0
};
byte errorbytes[1] = {
  3
};
byte tmp[4] = {
  0
};

void showlogo(){

  u8g.firstPage();
  do {
    u8g.drawBitmap(0,0,16,64,pic_Logo_bmp);
    //u8g.drawBitmapP(0,0,16,64,pic_Logo_bmp);

    //u8g.setFont(u8g_font_u8glib_4);
    //u8g.setFont(u8g_font_5x8);
    u8g.setFont(u8g_font_helvR08);
    u8g.drawStr(96,56,current_profile_name);
  } while ( u8g.nextPage() );

}

//Function to read last profile used from SD card.
void SDReadLastProfile(){
  if (SD.exists("LASTPROF.HEX")) {
      myFile = SD.open("LASTPROF.HEX", FILE_READ);
    
      lastprofilenum = myFile.read();
      myFile.close();
    
      Serial.print("Read LASTPROF.HEX: ");
      Serial.println(lastprofilenum);
    
      myFile = SD.open("PROFILES.HEX", FILE_READ);
      myFile.seek(lastprofilenum*62);
      myFile.read(profbuff, 62);
    
      profilecount = myFile.size()/62;
    
      Serial.print("Profile Count from SD Card: ");
      Serial.println(profilecount);
      
      myFile.close();
    
      current_profile_num = lastprofilenum;
  }
  else{
    Serial.println("Can't find LASTPROF.HEX on SD card.");
  }
}

//Function to lookup ID String from SD card.
void SDLookupIDString(){
  Serial.println("Looking up ID...");
  profileIDSet = false;
  IDLength=0;

  if (SD.exists("IDS.HEX")) {
      myFile = SD.open("IDS.HEX", FILE_READ);
      
      myFile.seek(0);
    
      Serial.println("Looking for this profile name:");
      Serial.println(current_profile_name);
      bool FoundID=myFile.find(current_profile_name);
      
      if (FoundID){
        IDLength=myFile.read();
        Serial.print("ID Length is: ");
        Serial.println(IDLength);
        memset(profileID, 0, 100);
        myFile.read(profileID, IDLength);
        profileIDSet = true;
        Serial.println("ID found!");
        Serial.print("#####");
        for (byte i = 0; i < IDLength; i = i + 1) {
          
          Serial.write(profileID[i]);
          
        }
        Serial.print("#####");
      }
      else{
        Serial.println("ID not found.");
      }
      
      myFile.close();
  }
  else{
    Serial.println("Can't find IDS.HEX on SD card.");
  }
}


//Function to read display option from SD card
void SDReadDisplayOptions(){

  if (SD.exists("DISPLAY.HEX")) {
      myFile = SD.open("DISPLAY.HEX", FILE_READ);
      byte displaydata=0;
    
      displaydata = myFile.read();
      myFile.close();
      
      displaydata = displaydata&0x0F;
    
      Serial.println("Checking display rotation value in DISPLAY.HEX:");
      Serial.println(displaydata);
    
      if (displaydata == 0x01){
        //rotate display
        Serial.println("Rotating display");
        u8g.setRot180();
      }
  }
  else{
    Serial.println("Can't find DISPLAY.HEX on SD card.");
  }
}


//Variable to store current special case - used for WMMT gear management.
//Available for furture potential expansion
byte cur_special_case = 0;

//variable to store steering options
uint16_t cur_steering_options[3]={0,0,0};

//variable for special USB switch testing mode
bool USBswitchmode = false;

//Variables used for sending digital switch states over JVS.
 byte result_p1_1 = 0;
 byte result_p1_2 = 0;

 byte result_p2_1 = 0;
 byte result_p2_2 = 0;

 byte testbuttonstatus = 0;
 

//Function to read a specific profile from SD card.
void SDReadProfileX(byte profilex){
  if (SD.exists("PROFILES.HEX")) {
      myFile = SD.open("PROFILES.HEX", FILE_READ);
      myFile.seek(profilex*62);
      myFile.read(profbuff, 62);
      myFile.close();
  }
  else{
    Serial.println("Can't find PROFILES.HEX on SD card.");
  }
}

//Function to write last profile used to SD card.
void SDWriteLastProfile(byte profilex){
  if (SD.exists("LASTPROF.HEX")) {
    myFile = SD.open("LASTPROF.HEX", FILE_WRITE);
    
    myFile.seek(0);
    myFile.write(profilex);
    myFile.close();
  
    Serial.print("Wrote profile num to SD card: ");
    Serial.println(profilex);
  }
  else{
    Serial.println("Can't find LASTPROF.HEX on SD card.");
  }
}


//Function to apply profiles.
void ApplyProfile(struct Mapping_Profile profile)
{
    Array_Copy( P1_pins, profile.player1_pins, 16 );
    Array_Copy( P2_pins, profile.player2_pins, 16 );
    Array_Copy( cur_analog_channel_pins, profile.analog_channels, 8);
    Array_Copy( Output_Pins, profile.outputs, 8 );
    memcpy( current_profile_name, profile.title, 5 );
    features[13]=profile.output_count;
    cur_special_case = profile.special_case;
    cur_steering_options[0]=profile.steering_options[0];
    cur_steering_options[1]=profile.steering_options[1];
    cur_steering_options[2]=profile.steering_options[2];

    Serial.print("Special Case from loaded profile: ");
    Serial.println(cur_special_case);

    SDLookupIDString();
}

//Function to change profile.
void ChangeProfile()
{
  USBswitchmode = false;
    if (current_profile_num < profilecount-1)
  {
    current_profile_num++;
  }
  else
  {
    current_profile_num = 0;
  }

  //read profile from SD card
  SDReadProfileX(current_profile_num);
  
  ApplyProfile(current_profile);

  //Write profile num to LASTPROF.HEX on SD Card
  SDWriteLastProfile(current_profile_num);

  #if PROFILE_SERIAL == 1
  Serial.print("Profile change to: ");
  Serial.println(current_profile_name);
  Serial.print("Profile num: ");
  Serial.println(current_profile_num);
  //Serial.print("Special case: ");
  //Serial.println(cur_special_case);
  #endif


    char  prof_num[16];
    sprintf(prof_num,"Profile #: %d",current_profile_num);   
      //u8g.clear();

      u8g.firstPage();
      do {
        u8g.setFont(u8g_font_timB10);
        u8g.drawStr(0,10,"Current profile:");
        u8g.setFont(u8g_font_ncenB24);
        u8g.drawStr(0,45,current_profile_name);
        u8g.setFont(u8g_font_timB10);
        u8g.drawStr(0,64,prof_num);
      } while ( u8g.nextPage() );

      logo_timer = millis();
      logoOn = false;
  
}

void setWaitForCommsDisplay()
{
  u8g.firstPage();
      do {
        u8g.setFont(u8g_font_timB10);
        u8g.drawStr(50,10,versionNum);
        u8g.drawStr(1,30,"Wait for JVS Comm");
        u8g.drawStr(25,50,"Profile: ");
        u8g.drawStr(75,50, current_profile_name);
      } while ( u8g.nextPage() );
      logo_timer = millis();
      logoOn = false;
}

void Array_Copy(byte array1[],byte array2[], int byte_count)
{
  for (int i=0; i<byte_count; i++){
  array1[i]=array2[i];
  }
}

void setup()
{
  #if FASTADC
 // set prescale to 16
 sbi(ADCSRA,ADPS2) ;
 cbi(ADCSRA,ADPS1) ;
 cbi(ADCSRA,ADPS0) ;
  #endif

  SD.begin(53);


  Serial.begin(115200);
  Serial1.begin(115200, SERIAL_8N1);

  SDReadDisplayOptions();
  
  
  u8g.begin();
  showlogo();
  
  //Serial.println(sizeof(mapping_profile_test));
  
  //u8g2.drawBitmap(0,0,16,54,pic_Logo_bmp);
  //u8g2.drawBitmap(0,0,16,64,pic_Logo_bmp);
  
//  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  // initialize with the I2C addr 0x3D (for the 128x64)
//  display.clearDisplay();
//  display.setTextSize(2);
//  display.setTextColor(WHITE);
//  display.setCursor(0,0);
//  display.println("MEGA JVS");
//  display.setTextSize(1);
//  display.display();
  
  int i =0;
  
  
  //Serial1.transmitterEnable(PIN_TXENABLE);
  pinMode(PIN_TXENABLE, OUTPUT);
  digitalWrite(PIN_TXENABLE, LOW);
  
  //Serial.println("Pin Sense set to OUTPUT and LOW");
  
  pinMode(PIN_LED, OUTPUT);

  pinMode(PIN_SENSE, OUTPUT);
  digitalWrite(PIN_SENSE, LOW);

  pinMode(PIN_SENSE, OUTPUT);
  digitalWrite(PIN_SENSE, LOW);
 
  for (i=0; i<8; i++)
  {
      if (Output_Pins[i]>0){
        pinMode(Output_Pins[i],OUTPUT);
        digitalWrite(Output_Pins[i],LOW);
      }
  }

  bool due_version=false;
  
  #if defined (_VARIANT_ARDUINO_DUE_X_)
  due_version = true;
  #endif
  
  digitalWrite(PIN_LED, HIGH);

  
  if (due_version==true){
  Serial.println("MEGA JVS - DUE Version");
  }
  else{
    Serial.println("MEGA JVS - MEGA 2560 Version");
  }
  

//  Serial.print("Number of profiles: ");
//  Serial.println(sizeof(mapping_profiles)/93);
  
//  if (steering_center_smoothing==true){
//    Serial.println("Steering smoothing: ON");
//  }
//  else{
//    Serial.println("Steering smoothing: OFF");
//  }
  

  //Initialize all main input pins as inputs                                         
  for (i = 0; i < sizeof(all_inputs); i++)
  {
      pinMode(all_inputs[i], INPUT_PULLUP);
      debouncerarray[i].attach(all_inputs[i]);
      debouncerarray[i].interval(DEBOUNCE_TIME);

      #if defined (_VARIANT_ARDUINO_DUE_X_)
      // Arduino DUE - specific code

      //Apply Debouncing and Glitch Filtering to DUE inputs
      g_APinDescription[all_inputs[i]].pPort -> PIO_IFER |= g_APinDescription[all_inputs[i]].ulPin;
      g_APinDescription[all_inputs[i]].pPort -> PIO_DIFSR |= g_APinDescription[all_inputs[i]].ulPin; // Debouncing Input Filter Select Register
      g_APinDescription[all_inputs[i]].pPort -> PIO_SCDR |= DEBOUNCE_DELAY; // Slow Clock Divider Register

      #endif
  }

  pinMode(A0,INPUT);
  pinMode(A1,INPUT);
  pinMode(A2,INPUT);
  pinMode(A3,INPUT);
  pinMode(A4,INPUT);
  pinMode(A5,INPUT);
  pinMode(A6,INPUT);
  pinMode(A7,INPUT);

  //Read in last used profile from SD card and apply it.
  SDReadLastProfile();
  ApplyProfile(current_profile);

  char  prof_num[16];
  sprintf(prof_num,"Profile #: %d",current_profile_num);
  
  //Draw information in display.
  u8g.firstPage();
  do {
    u8g.setFont(u8g_font_timB10);
    u8g.drawStr(0,10,"Current profile:");
    u8g.setFont(u8g_font_ncenB24);
    u8g.drawStr(0,45,current_profile_name);
    u8g.setFont(u8g_font_timB10);
    u8g.drawStr(0,64,prof_num);
  } while ( u8g.nextPage() );

  logo_timer = millis();
  logoOn = false;

  setWaitForCommsDisplay();

}

void ReplyBytes(const byte *bytes, int numBytes)
{
  Reply *r = &reply[curReply];
  r->message[r->length++] = 0x01;
  for (int i = 0; i < numBytes; i++)
  {
    r->message[r->length++] = bytes[i];
  }
}


boolean WMMT_shift_down_state = false;
int WMMT_shift_down_timer = 0;

boolean WMMT_shift_up_state = false;
int WMMT_shift_up_timer = 0;

int WMMT_Gear_Num = 1;

void WMMT_Gear_Change()
{

   //Serial.println("got here");
   WMMT_shift_up_timer++;
   WMMT_shift_down_timer++;
   int shift_direction = 0;
   
         //shift down
            if (!digitalRead(all_inputs[SHIFT_DOWN_PIN]) && WMMT_shift_down_state == false){
              //coin++;
              WMMT_shift_down_state = true;
              WMMT_shift_down_timer = 0;
              //digitalWrite(START_LAMP,HIGH);
            }
            
            if (WMMT_shift_down_timer > 5000){
              if ( WMMT_shift_down_state == true && digitalRead(all_inputs[SHIFT_DOWN_PIN]) ){
                //profile code
                
                WMMT_shift_down_state = false;
                shift_direction = -1;
                //digitalWrite(START_LAMP,LOW);
                //Serial.println("Profile button pressed!");
                WMMT_shift_down_timer=0;
              }
            }

         //shift up
            if (!digitalRead(all_inputs[SHIFT_UP_PIN]) && WMMT_shift_up_state == false){
              //coin++;
              WMMT_shift_up_state = true;
              WMMT_shift_up_timer = 0;
              //digitalWrite(START_LAMP,HIGH);
            }
            
            if (WMMT_shift_up_timer > 5000){
              if ( WMMT_shift_up_state == true && digitalRead(all_inputs[SHIFT_UP_PIN]) ){
                //profile code
                
                WMMT_shift_up_state = false;
                shift_direction = 1;
                //digitalWrite(START_LAMP,LOW);
                //Serial.println("Profile button pressed!");
                WMMT_shift_up_timer=0;
              }
            }


          //change gear
          if (shift_direction == -1 && WMMT_Gear_Num>1 && cur_special_case==3){
            //shift geear down
            WMMT_Gear_Num--;
            
          }
          if (shift_direction == -1 && WMMT_Gear_Num>0 && cur_special_case==2){
            //shift geear down
            WMMT_Gear_Num--;
            
          }
           if (shift_direction == 1 && WMMT_Gear_Num<6){
            //shift geear down
            WMMT_Gear_Num++;
          }

  if (shift_direction != 0){
  Serial.print("Current Gear: ");
  Serial.println(WMMT_Gear_Num);
  }
}


bool USB_Mode = false;

void toggleUSB()
{
  #if defined (_VARIANT_ARDUINO_DUE_X_)
      // Arduino DUE - specific code
    Serial.println("Toggling USB now...");
    if (USB_Mode == false){
      USB_Mode = true;

      
      
    }
    else{
      USB_Mode = false;
      //Joystick.end();
      Serial.println("USB Mode = FALSE");
    }
    #endif
}

void writeEscaped(byte b)
{
  //digitalWrite(PIN_TXENABLE, HIGH);
  if (b == 0xE0 || b == 0xD0)
  {
    Serial1.write(0xD0);
    //Serial.println("writing 0xD0");
    b--;
  }
  Serial1.write(b);
}

void FlushReply()
{
  digitalWrite(PIN_TXENABLE, HIGH);
  Reply *r = &reply[curReply];
  if (r->length > 0)
  {
    int sum = 3 + r->length;
    
    Serial1.write(0xE0);
    //Serial.println("Flushing: Writing SYNC - 0xE0");
    
    writeEscaped(0x00);
    writeEscaped(r->length + 2);
    writeEscaped(0x01);
    for (int i = 0; i < r->length; i++)
    {
      sum += r->message[i];
      writeEscaped(r->message[i]);
    }
    writeEscaped(sum & 0xFF);
    curReply = 1 - curReply;
    reply[curReply].length = 0;
  }
  //delay(5);
  Serial1.flush();
  //delay(5);
  digitalWrite(PIN_TXENABLE, LOW);
}

void Resend()
{
  Reply *r = &reply[curReply];
  Reply *old = &reply[1 - curReply];
  int length = old->length;
  for (int i = 0; i < length; i++)
  {
    r->message[r->length++] = old->message[i];
  }
}

#define Reply()      ReplyBytes(NULL,0)
#define ReplyError()       ReplyBytes(NULL,0)
#define ReplyString(str) ReplyBytes((const byte*)str,sizeof(str))
#define ReplyByte(b)   do { tmp[0]=b; ReplyBytes(tmp, 1); } while(0)



uint16_t coinModifier = 0;
byte slotNum =0;
byte IDSent=0;
byte featuresSent=0;


void ProcessPacket(struct Packet *p)
{
  if (p->address == 0xFF || p->address == deviceId) // Yay, it's for me
  {
    int length = p->length;
    byte *message = p->message;
    while (length > 0)
    {
      int sz = 1;
      switch (message[0])
      {
        case CMD_RESET:
          Serial.println("CMD_RESET");
       
          digitalWrite(START_LAMP,LOW);
          digitalWrite(VIEW_LAMP,LOW);
          coin1_val=0;
          coin2_val=0;
          waitForComms=true;
      
          
          sz = 2;
          deviceId = -1;
          digitalWrite(PIN_SENSE, LOW);    
          break;
          
        case CMD_SETADDRESS:
          sz = 2;
          
          deviceId = message[1];
          
          Serial.println("CMD_SETADDRESS");
          Serial.print("Address is: ");
          Serial.println(deviceId);
          digitalWrite(PIN_SENSE, HIGH); 
          Reply();
          
          
          break;
    
        case CMD_SETMETHOD:
          break;

        case CMD_READID:
        {
          Serial.println("CMD_READID");
          char outBuf[102] = { 0 };
          int id_size=0;
          
          if (profileIDSet){
              
              //Serial.print("ID Length is: ");
              //Serial.println(IDLength);

              //pProfileId = profileID;

              strcpy(outBuf, profileID); 
              id_size=IDLength+1;
          }
          else{
              #if defined(__AVR_ATmega2560__)
              char full_id[]="MEGA JVS;I/O BD JVS;MEGA 2560 Version";
              //char full_id[]="SEGA ENTERPRISES,LTD.;I/O BD JVS;837-13551 ;Ver1.00;98/10";
              //char full_id[]=  "SEGA CORPORATION;I/O BD JVS;837-14572;Ver1.00;2005/10";
              
              #endif
              #if defined (_VARIANT_ARDUINO_DUE_X_)
              char full_id[]="MEGA JVS;I/O BD JVS;DUE Version";
              #endif
              //int i2=0;
              id_size = sizeof(full_id);
              
              //for (int i = id_size-1; i<id_size+8; i++){
              // full_id[i]=current_profile_name[i2];
              // i2++;
              //}
              //id_size+=i2;
              id_size++;
              //pProfileId=full_id;
              
              strcpy(outBuf, full_id); 

              
              
          }
          //id_size = strlen(outBuf) + 1;
          ReplyBytes(outBuf, id_size);
          
          //IDSent=1;
          //if (IDSent==1 && featuresSent==1){
          //  waitForComms=false;
          //}
          //Serial.println(outBuf);
          
          
          
          
          
          break;
        }
        
        case CMD_FORMATVERSION:
          Serial.println("CMD_FORMATVERSION");
          ReplyByte(0x13);
          //ReplyByte(0x11);
          break;
        case CMD_JVSVERSION:
          Serial.println("CMD_JVSVERSION");
          ReplyByte(0x30);
          //ReplyByte(0x20);
          break;
        case CMD_COMMSVERSION:
          Serial.println("CMD_COMMSVERSION");
          ReplyByte(0x10);
          break;
        case CMD_GETFEATURES:
          {
          Serial.println("CMD_GETFEATURES");
          ReplyBytes(features, 17);
          //featuresSent=1;
          //if (IDSent==1 && featuresSent==1){
          //  waitForComms=false;
          //}
          break;
          }
        case CMD_SETMAINBOARDID:
          {
          Serial.println("CMD_SETMAINBOARDID");
          sz = strlen((char*)&message[1]) + 1;
          Reply();
          //ReplyString("test;test;1;1");
          break;
          }

        case CMD_READSWITCHES:
          {
            sz = 3;
            waitForComms=false;
            
            byte results[5];
            
            results[0] = testbuttonstatus;
            results[1] = result_p1_1 & 0xFF;
            results[2] = result_p1_2 & 0xFF;
            results[3] = result_p2_1 & 0xFF;
            results[4] = result_p2_2 & 0xFF;
            
            ReplyBytes(results, message[1]*message[2] + 1);
            break;
          }
        case CMD_READCOIN:
          {
            
            
            
         
            byte coins[4] = {(byte)(coin1_val >> 8), (byte)coin1_val, (byte)(coin2_val >> 8), (byte)coin2_val};
            //byte coins[2] = {(byte)(coin >> 8), (byte)coin};
            //Serial.println("CMD_READCOIN");
            sz = 2;
            ReplyBytes(coins, message[1] * 2);
            break;
          }
//        case CMD_READANALOG:
//        {
//          #if DEBUG == 1
//          Serial.println("CMD_READANALOG");
//          #endif
//          sz = 2;
//
//          for (int i = 0; i < 8; i++)
//            { 
//              int analogVal = 0;
//              byte analogByte1 = 0;
//              byte analogByte2 = 0;
//              if (cur_analog_channel_pins[i] != 0){
//                analogVal = analogRead(cur_analog_channel_pins[i]);
//
//               //Check if steering channel and apply special cases if needed.
//               switch (i)
//               {
//                case 0:
//                {
//                //apply scaling to steering if steering option is set to 2 or 3
//               
//                if (cur_steering_options[0]==2 || cur_steering_options[0]==3){
//                  analogByte1 = analogVal>>2;
//                  analogByte1 = map(analogByte1,STEERING_MIN,STEERING_MAX,cur_steering_options[1],cur_steering_options[2]);
//                  analogByte2 = 0;
//                }
//                else{
//                  analogByte1 = analogVal>>2;
//                  analogByte2 = analogVal<<6;
//                }
//                
//               }
//
//               
//               break;
//
//               case 1:
//               {
//                //Do Nothing
//               }
//
//               analogByte1 = analogVal>>2;
//               analogByte2 = analogVal<<6;
//                
//               break;
//
//               case 2:
//               {
//                //Do Nothing
//               }
//               analogByte1 = analogVal>>2;
//               analogByte2 = analogVal<<6;
//               break;
//               
//               default:
//               analogByte1 = analogVal>>2;
//               analogByte2 = analogVal<<6;
//               break;
//               }
//                
//                
//                
//              
//              }
//              else{
//                analogByte1 =0;
//                analogByte2 =0;
//              }
//
//              
//              //suppress 2nd byte of analog data if steering options are set to 1 or 3
//              if (cur_steering_options[0]==1 || cur_steering_options[0]==3){
//                 analogByte2 = 0x00;
//              }
//
//              
//              analog_channel_data[i*2] = analogByte1;
//              analog_channel_data[i*2 + 1] = analogByte2;
//            }
//          
//          ReplyBytes(analog_channel_data, message[1] * 2);
//          break;
//        }
        case CMD_READANALOG:
        {
          #if DEBUG == 1
          Serial.println("CMD_READANALOG");
          #endif
          sz = 2;
          
          ReplyBytes(analog_channel_data, message[1] * 2);
          break;
        }
        case CMD_READROTARY:
          Serial.println("CMD_READROTARY");
          sz = 2;
          ReplyBytes(zeros, message[1] * 2);
          break;
        case CMD_READKEYCODE:
          Serial.println("CMD_READKEYCODE");
          Reply();
          break;
        case CMD_READSCREENPOS:
          Serial.println("CMD_READSCREENPOS");
          sz = 2;
          ReplyBytes(zeros, 4);
          break;
        case CMD_READGPIO:
          Serial.println("CMD_READGPIO");
          sz = 2;
          ReplyBytes(zeros, message[1]);
          break;

        case CMD_WRITEPAYOUTREMAINING:
          Serial.println("CMD_WRITEPAYOUTREMAINING");
          sz = 2;
          ReplyBytes(zeros, 4);
          break;
        case CMD_RESEND:
          Serial.println("CMD_RESEND");
          Resend();
          break;
        case CMD_WRITECOINSUBTRACT:
          {
          
          slotNum= message[1];
          coinModifier = (message[2] << 8) | message[3];
          
          Serial.println("CMD_WRITECOINSUBTRACT");
          
              sz = 4;
            
            
            
                  if (slotNum == 1)
                  {
                      if ((coin1_val - coinModifier) >= 0)
                      {
                          coin1_val -= coinModifier;
                      }
                      else
                      {
                          coin1_val = 0;
                      }
                  } else if (slotNum == 2)
                  {
                      if ((coin2_val - coinModifier) >= 0)
                      {
                          coin2_val -= coinModifier;
                      }
                      else
                      {
                          coin2_val = 0;
                      }
                  }
            //Serial.println("Start: ");
            //for (int i=0; i<50; i++){
            //  Serial.print(": 0x");
            //  Serial.print(packet.message[i],HEX);
            //}
            //Serial.println(": End");
            
            
            Reply();
            break;
          }
        case CMD_WRITEPAYOUT:
          Serial.println("CMD_WRITEPAYOUT");
          sz = 4;
          Reply();
          break;
        case CMD_WRITEGPIO1:
        {
          //Serial.println("CMD_WRITEGPIO1");
          byte OutputCommand = message[2];
          for (int i=0;i<8;i++)
          {
//            if (bitRead(OutputCommand,i)==1){
//              Serial.print("Output bit # is ON: ");
//              Serial.println(i);
//            }
            if (Output_Pins[i]>0){
              if (bitRead(OutputCommand,i)==1){
                digitalWrite(Output_Pins[i],HIGH);
              }
              else{
                digitalWrite(Output_Pins[i],LOW);
              }
            }
          }
        }
          sz = 2 + message[1];
          Reply();
          break;
        case CMD_WRITEANALOG:
          Serial.println("CMD_WRITEANALOG");
          sz = 2 + 2 * message[1];
          Reply();
          break;
        case CMD_WRITECHAR:
          Serial.println("CMD_WRITECHAR");
          sz = 2 + message[1];
          Reply();
          break;
        case CMD_WRITECOINADDED:
          {
            Serial.println("CMD_WRITECOINADDED");
          
          sz = 4;

                    coinModifier = (message[2] << 8) | message[3];
                    slotNum= message[1];
          
                if (slotNum == 1)
                {
                    
                        coin1_val += coinModifier;
                    
                } else if (slotNum == 2)
                {
                   
                        coin2_val += coinModifier;
                  

                }

                
          Reply();
          break;
          }
        case CMD_WRITEPAYOUTSUBTRACT:
          Serial.println("CMD_WRITEPAYOUTSUBTRACT");
          sz = 4;
          Reply();
          break;
        case CMD_WRITEGPIOBYTE:
          Serial.println("CMD_WRITEGPIOBYTE");
          sz = 3;
          Reply();
          break;
        case CMD_WRITEGPIOBIT:
          Serial.println("CMD_WRITEGPIOBIT");
          sz = 3;
          Reply();
          break;
        default:
          Serial.println("Got unknown");
          Reply();
          break;
      }
      message += sz;
      length -= sz;
    }
    
    if (length < 0)
    {
      Serial.println("Underflowed!");
      Reply();
      //FlushErrorReply();
    }
    FlushReply();
  }
  else
  {
    //Serial.println("Not for me");
  }
}

// Recieving
bool bRecieving = false;
bool bEscape = false;
int phase = 0;
int checksum = 0;
int cur = 0;
bool bAddCoin = false;

int current_time = 0;
int timer = 0;
int USB_mode_timer = 0;
bool profile_USB_state=false;
// Last state of the button

int lastButtonState[12] = {0};
void USB_loop() {
  #if defined (_VARIANT_ARDUINO_DUE_X_)
      // Arduino DUE - specific code
  // Read digital pins values
  for (int index = 0; index < 11; index++)
  {
    int currentButtonState = !digitalRead(all_inputs[index]);
    if (currentButtonState != lastButtonState[index])
    {
      //Joystick.setButton(index, currentButtonState);
      lastButtonState[index] = currentButtonState;
    }
  }

  //Read Analog
  int analogVal = 0;
  int convertedVal = 0;
  float part1 = 0.00001f;
  //Read X axis
  analogVal = analogRead(A0);
  
  convertedVal = analogVal/8;
  
//  if (analogVal>511){
//    convertedVal = 1*(1-((analogVal-512)/(1023-512)))+127*((analogVal-512)/(1023-512));
//    //part1 = 1-(analogVal-512)/(1023-512);
//    //Serial.println(part1);
//    //Serial.println(1023-512);
//    //Serial.println(1*(1-((analogVal-512)/(1023-512))));
//  }
//  else{
//    if (analogVal<511){
//      convertedVal= -127*(1-((analogVal-0)/(510-0)))+(-1)*((analogVal-0)/(510-0));
//    }
//    else{
//      convertedVal=0;
//      }
//  }


  //Joystick.setXAxis(convertedVal);
  
SerialUSB.print("Actual Value: ");
SerialUSB.print(analogVal);
  SerialUSB.print("     - Converted Val: ");
  SerialUSB.println(convertedVal);

  analogVal=analogRead(A1);
  //Joystick.setXAxisRotation(analogVal/3);

  analogVal=analogRead(A2);
  //Joystick.setYAxisRotation(analogVal/3);
  
  delay(50);
  #endif
}

int profile_i = 4;
byte serialbuffer[4]={0,0,0,0};


void loop()
{

  if (logoOn==false && millis()-logo_timer >5000 && waitForComms==false && USBswitchmode==false){
    //u8g2.clearDisplay();
    Serial.print("millis():");
    Serial.println(millis());
    Serial.print("Logo Timer:");
    Serial.println(logo_timer);
    
    logoOn=true;
    showlogo();
  }
          timer++;
      #if defined (_VARIANT_ARDUINO_DUE_X_)
      // Arduino DUE - specific code
          if (!digitalRead(PROFILE_PIN_NUM) && profile_USB_state == false){
              //coin++;
              profile_USB_state = true;
              USB_mode_timer=millis();
              digitalWrite(START_LAMP,HIGH);
           }

          if (!digitalRead(PROFILE_PIN_NUM) && profile_USB_state == true && (millis()-USB_mode_timer)>5000){
            Serial.println("USB Mode Toggled!");
            digitalWrite(START_LAMP,LOW);
            delay(500);
            digitalWrite(START_LAMP,HIGH);
            delay(500);
            digitalWrite(START_LAMP,LOW);
            delay(500);
            digitalWrite(START_LAMP,HIGH);
            delay(500);
            digitalWrite(START_LAMP,LOW);
            delay(500);
            digitalWrite(START_LAMP,HIGH);
            delay(500);
            digitalWrite(START_LAMP,LOW);
            delay(500);
            profile_USB_state = false;
            profile_state = false;
            toggleUSB();
          }
        #endif
  
            if (!digitalRead(PROFILE_PIN_NUM) && profile_state == false){
              //coin++;
              profile_state = true;
              timer = 0;
              USB_mode_timer=millis();
              digitalWrite(START_LAMP,HIGH);
            }

        #if defined (_VARIANT_ARDUINO_DUE_X_)
        // Arduino DUE - specific code
            if (digitalRead(PROFILE_PIN_NUM) && profile_USB_state == true && (millis()-USB_mode_timer)<5000){
              //coin++;
              profile_USB_state = false;
              USB_mode_timer=millis();
            }
        #endif
            
            if (timer > 10000){
              if ( profile_state == true && digitalRead(PROFILE_PIN_NUM) ){
                //profile code
                ChangeProfile();
                profile_state = false;
                profile_USB_state = false;
                digitalWrite(START_LAMP,LOW);
                //Serial.println("Profile button pressed!");
                timer=0;
              }
            }

if (USB_Mode==false){


            //Check USB serial port for incoming profile change command
  byte serialbyte = 0;
  
  
  if (Serial.available()>0){
    serialbyte=Serial.read();

    if (serialbyte == 0x70 && serialbuffer[0] != 0x70 && serialbuffer[0] != 0x53){
      profile_i=0;
      serialbuffer[0]=serialbyte;
    }else if (serialbyte == 0x53 && serialbuffer[0] != 0x70 && serialbuffer[0] != 0x53){
      profile_i=0;
      serialbuffer[0]=serialbyte;
    }
    else{
      serialbuffer[profile_i]=serialbyte;
    }
    
    if (profile_i<4){
      profile_i++;   
    }
      
  }

  if(serialbuffer[0]==0x70 && serialbuffer[1]==0x72 && serialbuffer[2]==0x6F && profile_i==4){
    current_profile_num = serialbuffer[3];
    current_profile_num--;
    ChangeProfile();
    serialbuffer[0]= 0;
    serialbuffer[1]= 0;
    serialbuffer[2]= 0;
    serialbuffer[3]= 0;
    profile_i=0;
  }

  if(serialbuffer[0]==0x53 && serialbuffer[1]==0x50 && serialbuffer[2]<=0x05 && profile_i==4){
    //Code to activate USB switch test mode
    if (USBswitchmode == false){
      u8g.firstPage();
      do {
        u8g.setFont(u8g_font_timB10);
        u8g.drawStr(0,10,"USB Switch");
        u8g.setFont(u8g_font_timB10);
        u8g.drawStr(0,30,"Test Mode");
      } while ( u8g.nextPage() );
      current_profile_num--;
      USBswitchmode = true;
    }
     
    switch(serialbuffer[2]){
      case 0x00:
        result_p1_1 = 0;
        result_p1_2 = 0;
        result_p2_1 = 0;
        result_p2_2 = 0;
        testbuttonstatus= 0;
        break;
      case 0x01:
        result_p1_1 ^= serialbuffer[3];
        break;
      case 0x02:
        result_p1_2 ^= serialbuffer[3];
        break;
      case 0x03:
        result_p2_1 ^= serialbuffer[3];
        break;
      case 0x04:
        result_p2_2 ^= serialbuffer[3];
        break;
      case 0x05:
        testbuttonstatus ^= serialbuffer[3];
        break;
        
    }
      
    serialbuffer[0]= 0;
    serialbuffer[1]= 0;
    serialbuffer[2]= 0;
    serialbuffer[3]= 0;
    profile_i=0;
  }

  
            if (cur_special_case==3 || cur_special_case==2){
              WMMT_Gear_Change();
            }



//            if (current_profile_num == 4){
//              if (!digitalRead(P1_START_PIN) && test_state == false){
//              //coin++;
//              test_state = true;
//              timer = 0;
//              digitalWrite(START_LAMP,HIGH);
//            }
//            
//            if (timer > 10000){
//              if ( test_state == true && digitalRead(P1_START_PIN) ){
//                //profile code
//                //ChangeProfile();
//                test_state = false;
//                digitalWrite(START_LAMP,LOW);
//                test_i++;
//                if (test_i>28) {
//                  test_i=0;
//                }
//                Serial.print("Test i: ");
//                Serial.println(test_i);
//                
//                //Serial.println("Profile button pressed!");
//                timer=0;
//              }
//            }
//           
//            }



            
//  if (!digitalRead(22))
//  {
//    if (bAddCoin)
//    {
//      coin++;
//      bAddCoin = false;
//    }
//  }
//  else
//  {
//    bAddCoin = true;
//  }
  if (Serial1.available() > 0)
  {
    digitalWrite(PIN_LED, LOW);
    byte incomingByte = Serial1.read();
    //Serial.println("read something");
    switch (incomingByte)
    {
      case 0xE0: // sync
        bRecieving = true;
        bEscape = false;
        phase = 0;
        cur = 0;
        checksum = 0;
        break;
      case 0xD0: // Escape
        bEscape = true;
        break;
      default:
        if (bEscape)
        {
          incomingByte++;
          bEscape = false;
        }
        switch (phase)
        {
          case 0:
            packet.address = incomingByte;
            checksum += incomingByte;
            phase++;
            break;
          case 1:
            packet.length = incomingByte - 1;
            checksum += incomingByte;
            phase++;
            break;
          case 2:
            if (cur >= packet.length)
            {
              checksum &= 0xFF;
              if (checksum == incomingByte)
              {
                ProcessPacket(&packet);
              }
              else
              {
                Serial.println("Dropping packet");
              }
              bRecieving = false;
            }
            else
            {
              checksum += incomingByte;
              packet.message[cur++] = incomingByte;
            }
            break;
        }
        break;
    }
    digitalWrite(PIN_LED, HIGH);
  }else{

    //read digital inputs
    byte mask = 1;
            
            
            if(!USBswitchmode){
          testbuttonstatus = 0;
          result_p1_1 = 0;
          result_p1_2 = 0;

          result_p2_1 = 0;
          result_p2_2 = 0;
              
                  //P1 switches
                  for (int i = 0; i < 8; i++)
                      {
                        if(P1_pins[i]>0){
                          debouncerarray[P1_pins[i]].update();
                          if (!debouncerarray[P1_pins[i]].read())
                            result_p1_1 |= mask;
                        }
                        mask <<= 1;
                      }
                      mask = 1;
                      for (int i = 8; i < 16; i++)
                      {
                        if(P1_pins[i]>0){
                          debouncerarray[P1_pins[i]].update();
                          if (!debouncerarray[P1_pins[i]].read())
                            result_p1_2 |= mask;
                        }
                        mask <<= 1;
                      }
                      mask = 1;
      
                      
                  
                  //P2 switches
                      for (int i = 0; i < 8; i++)
                      {
                        if(P2_pins[i]>0){
                          debouncerarray[P2_pins[i]].update();
                          if (!debouncerarray[P2_pins[i]].read())
                            result_p2_1 |= mask;
                        }
                        mask <<= 1;
                      }
                      mask = 1;
                      for (int i = 8; i < 16; i++)
                      {
                        if(P2_pins[i]>0){
                          debouncerarray[P2_pins[i]].update();
                          if (!debouncerarray[P2_pins[i]].read())
                            result_p2_2 |= mask;
                        }
                        mask <<= 1;
                        
                      }
                      
      
                  //Test pin
                  debouncerarray[TEST].update();
                  if (!debouncerarray[TEST].read()){
                    testbuttonstatus= 0x80;
                  }
      
                  
      
                  //If special case is 3 or 2, then apply current gear bits for WMMT
                      if (cur_special_case==3 || cur_special_case==2){
                        switch(WMMT_Gear_Num){
                          case 1:
                               result_p1_2 |= B10100000;
                          break;
                          case 2:
                               result_p1_2 |= B01100000;
                          break;
                          case 3:
                               result_p1_2 |= B10000000;
                          break;
                          case 4:
                               result_p1_2 |= B01000000;
                          break;
                          case 5:
                               result_p1_2 |= B10010000;
                          break;
                          case 6:
                               result_p1_2 |= B01010000;
                          break;
                        }
                        
                      }
            }

            //read analog inputs

            for (int i = 0; i < 8; i++)
            { 
              int analogVal = 0;
              byte analogByte1 = 0;
              byte analogByte2 = 0;
              if (cur_analog_channel_pins[i] != 0){
                analogVal = analogRead(cur_analog_channel_pins[i]);

               //Check if steering channel and apply special cases if needed.
               switch (i)
               {
                case 0:
                {
                //apply scaling to steering if steering option is set to 2 or 3
               
                if (cur_steering_options[0]==2 || cur_steering_options[0]==3){
                  analogByte1 = analogVal>>2;
                  analogByte1 = map(analogByte1,STEERING_MIN,STEERING_MAX,cur_steering_options[1],cur_steering_options[2]);
                  analogByte2 = 0;
                }
                else{
                  analogByte1 = analogVal>>2;
                  analogByte2 = analogVal<<6;
                }
                
               }

               
               break;

               case 1:
               {
                //Do Nothing
               }

               analogByte1 = analogVal>>2;
               analogByte2 = analogVal<<6;
                
               break;

               case 2:
               {
                //Do Nothing
               }
               analogByte1 = analogVal>>2;
               analogByte2 = analogVal<<6;
               break;
               
               default:
               analogByte1 = analogVal>>2;
               analogByte2 = analogVal<<6;
               break;
               }
                
                
                
              
              }
              else{
                analogByte1 =0;
                analogByte2 =0;
              }

              
              //suppress 2nd byte of analog data if steering options are set to 1 or 3
              if (cur_steering_options[0]==1 || cur_steering_options[0]==3){
                 analogByte2 = 0x00;
              }

              
              analog_channel_data[i*2] = analogByte1;
              analog_channel_data[i*2 + 1] = analogByte2;
            }

            

            //read coins
            debouncerarray[COIN1].update();
            if (!debouncerarray[COIN1].read()){
              //coin++;
              coin1_state = true;
            }

            debouncerarray[COIN2].update();
            if (!debouncerarray[COIN2].read()){
              //coin2++;
              coin2_state = true;
            }

            if (coin1_state == true && debouncerarray[COIN1].read() ){
              coin1_val++;
              coin1_state = false;
            }

            if (coin2_state == true && debouncerarray[COIN2].read() ){
              coin2_val++;
              coin2_state = false;
            }



            
  }

}
else{
  USB_loop();
}
  
}
