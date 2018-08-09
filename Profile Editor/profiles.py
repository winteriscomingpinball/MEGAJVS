from tkinter import *
from tkinter import filedialog, ttk
import serial

import struct

profilearray = bytearray(62)
profilelist=[]
profilecount=0

savedindex=0

profilemanageropen = False
switchtestopen=False
serialopen=False

wheelmin=0
wheelmax=255

ser = serial.Serial

digitalinputlist = [
"NOT ASSIGNED",
"P1_START",
"P1_RIGHT",
"P1_LEFT",
"P1_UP",
"P1_DOWN",
"P1_SW1",
"P1_SW2",
"P1_SW3",
"P1_SW4",
"P1_SW5",
"P1_SW6",
"P1_SW7",
"P1_SERVICE",
"P2_START",
"P2_RIGHT",
"P2_LEFT",
"P2_UP",
"P2_DOWN",
"P2_SW1",
"P2_SW2",
"P2_SW3",
"P2_SW4",
"P2_SW5",
"P2_SW6",
"P2_SW7",
"P2_SERVICE",
"TEST",
"COIN1",
"COIN2",
"OPT_PIN1",
"OPT_PIN2",
"OPT_PIN3",
"OPT_PIN4",
]

digitalinputdict = {
   "NOT ASSIGNED" : 0,
   "P1_START" : 1,
   "P1_RIGHT" : 2,
   "P1_LEFT": 3,
   "P1_UP": 4,
   "P1_DOWN": 5,
   "P1_SW1": 6,
   "P1_SW2": 7,
   "P1_SW3": 8,
   "P1_SW4": 9,
   "P1_SW5": 10,
   "P1_SW6": 11,
   "P1_SW7": 12,
   "P1_SERVICE": 13,
   "P2_START": 14,
   "P2_RIGHT": 15,
   "P2_LEFT": 16,
   "P2_UP": 17,
   "P2_DOWN": 18,
   "P2_SW1": 19,
   "P2_SW2": 20,
   "P2_SW3": 21,
   "P2_SW4": 22,
   "P2_SW5": 23,
   "P2_SW6": 24,
   "P2_SW7": 25,
   "P2_SERVICE": 26,
   "TEST": 27,
   "COIN1": 28,
   "COIN2": 29,
   "OPT_PIN1": 30,
   "OPT_PIN2": 31,
   "OPT_PIN3": 32,
   "OPT_PIN4": 33
   }

analogdict = {
   0  : "NOT ASSIGNED",
   54 : "A0",
   55 : "A1",
   56 : "A2",
   57 : "A3",
   58 : "A4",
   59 : "A5",
   60 : "A6",
   61 : "A7"
   }

analogreversedict = {
   "NOT ASSIGNED" :0,
   "A0" : 54,
   "A1" : 55,
   "A2" : 56,
   "A3" : 57,
   "A4" : 58,
   "A5" : 59,
   "A6" : 60,
   "A7" : 61
   }

analoglist = [
   "NOT ASSIGNED",
   "A0",
   "A1",
   "A2",
   "A3",
   "A4",
   "A5",
   "A6",
   "A7"
   ]

outputlist = [
   "NOT ASSIGNED",
   "Out1_1",
   "Out1_2",
   "Out1_3",
   "Out2_1",
   "Out2_2",
   "Out2_3"
   ]

outputdict = {
   0  : "NOT ASSIGNED",
   33 : "Out1_1",
   37 : "Out1_2",
   41 : "Out1_3",
   35 : "Out2_1",
   39 : "Out2_2",
   43 : "Out2_3"
   }

outputreversedict = {
   "NOT ASSIGNED" : 0,
   "Out1_1" : 33,
   "Out1_2" : 37,
   "Out1_3" : 41,
   "Out2_1" : 35,
   "Out2_2" : 39,
   "Out2_3" : 43
   }

analogoptionslist= ["0 - NONE","1 - SUPPRESS 2ND BYTE","2 - SCALE STEERING" ,"3 - SCALE & SUPPRESS"]

analogoptreversedict={
   "0 - NONE" : 0,
   "1 - SUPPRESS 2ND BYTE" : 1,
   "2 - SCALE STEERING" : 2,
   "3 - SCALE & SUPPRESS" : 3
   }

specialcaselist= ["0 - NONE","1 - RESERVED","2 - RESERVED" ,"3 - 2 POS SHIFTER"]

specialcasereversedict={
   "0 - NONE" : 0,
   "1 - RESERVED" : 1,
   "2 - RESERVED" : 2,
   "3 - 2 POS SHIFTER" : 3
   }


filename =""
outfilename ="testsave.hex"

def openprofiles():
   labelStatus.configure(fg="black",text="")
   global profilelist
   profilelist[:]=[]
   global filename

   filename = filedialog.askopenfilename(filetypes=[("HEX files","*.hex")],title="Open Profiles file.")                               
   f = open(filename,'rb')
   bytecount=1
   f.seek(0, 2)
   bytecount = f.tell()
   global profilecount
   profilecount = bytecount/62
   i=0
   if profilecount > 0:
      while i<profilecount:
         f.seek(i*62+0x30)
         profilelist.append(f.read(4))
         i+=1;
         
   f.close()
   
   print("byte count")
   print(bytecount)
   print("profile count:")
   profilecount = int(bytecount/62)
   print(int(profilecount))
   print("List of profiles:")
   print(profilelist)
   comboProfiles['values']=profilelist
   comboProfiles.current(newindex=0)
   selectedprofile(0)

def reopenprofiles():
   labelStatus.configure(fg="black",text="")
   global profilelist
   profilelist[:]=[]
   global filename
   global savedindex
   
   f = open(filename,'rb')
   bytecount=1
   f.seek(0, 2)
   bytecount = f.tell()
   global profilecount
   profilecount = bytecount/62
   i=0
   if profilecount > 0:
      while i<profilecount:
         f.seek(i*62+0x30)
         profilelist.append(f.read(4))
         i+=1;
         
   f.close()
   print("profile count:")
   profilecount = int(bytecount/62)
   
   comboProfiles['values']=profilelist
   comboProfiles.current(newindex=savedindex)
   selectedprofile(0)

def setupserial():
   global ser
   global serialopen
   #setup serial connection for USB Switch Test Mode
   print("Setting up serial")
   portname = txtserialportname.get()
   print("Attempting to open port: " + portname)

   try:
      ser = serial.Serial(port=portname,bytesize=serial.EIGHTBITS,baudrate=115200,
                          parity=serial.PARITY_EVEN,stopbits=serial.STOPBITS_ONE,
                          dsrdtr=True)
      labelswitchteststatus.configure(text="Serial port opened.",fg="green")
      serialopen=True
      resetswitches()
   except:
      labelswitchteststatus.configure(text="Error opening port.",fg="red")
      ser.close()
      serialopen=False

def closeserial():
   global ser
   global serialopen
   serialopen=False
   ser.close()
   labelswitchteststatus.configure(text="Serial port closed.",fg="black")
   
   
def importprofile():
   print("import profile")
   labelStatus.configure(fg="black",text="")
   global filename
   global savedindex
   if filename:
      importfilename = filedialog.askopenfilename(filetypes=[("HEX files","*.hex")],title="Open Profile export.")
      if importfilename:
         f = open(filename,'a+b')
         f2= open(importfilename,'rb')
         bytecount=1
         i=0
         #write import file to end of profiles file
         while i<62:
            f.write(f2.read(1))
            i +=1
               
         f.close()
         f2.close()
         
         indexval= profilecount
         savedindex=indexval

         reopenprofiles()
         labelStatus.configure(fg="green",text="Profile imported.")
      
   else:
      print("no file opened")
      labelStatus.configure(fg="red",text="No file selected!")
      
def resetswitches():
   global ser
   global serialopen
   if serialopen:
      packet = bytes([0x53,0x50,0x00,0x00])
      ser.write(packet)
      
      lblP1_START.configure(text='OFF',fg='black')
      lblP1_SERVICE.configure(text='OFF',fg='black')
      lblP1_UP.configure(text='OFF',fg='black')
      lblP1_DOWN.configure(text='OFF',fg='black')
      lblP1_LEFT.configure(text='OFF',fg='black')
      lblP1_RIGHT.configure(text='OFF',fg='black')
      lblP1_B1.configure(text='OFF',fg='black')
      lblP1_B2.configure(text='OFF',fg='black')
      lblP1_B3.configure(text='OFF',fg='black')
      lblP1_B4.configure(text='OFF',fg='black')
      lblP1_B5.configure(text='OFF',fg='black')
      lblP1_B6.configure(text='OFF',fg='black')
      lblP1_B7.configure(text='OFF',fg='black')
      lblP1_B8.configure(text='OFF',fg='black')
      lblP1_B9.configure(text='OFF',fg='black')
      lblP1_B10.configure(text='OFF',fg='black')
      lblP2_START.configure(text='OFF',fg='black')
      lblP2_SERVICE.configure(text='OFF',fg='black')
      lblP2_UP.configure(text='OFF',fg='black')
      lblP2_DOWN.configure(text='OFF',fg='black')
      lblP2_LEFT.configure(text='OFF',fg='black')
      lblP2_RIGHT.configure(text='OFF',fg='black')
      lblP2_B1.configure(text='OFF',fg='black')
      lblP2_B2.configure(text='OFF',fg='black')
      lblP2_B3.configure(text='OFF',fg='black')
      lblP2_B4.configure(text='OFF',fg='black')
      lblP2_B5.configure(text='OFF',fg='black')
      lblP2_B6.configure(text='OFF',fg='black')
      lblP2_B7.configure(text='OFF',fg='black')
      lblP2_B8.configure(text='OFF',fg='black')
      lblP2_B9.configure(text='OFF',fg='black')
      lblP2_B10.configure(text='OFF',fg='black')

      
      
   
def sendswitchserial(section,switchByte,lbl):
   
   global ser
   global serialopen
   packet = bytes([0x53,0x50,section,switchByte])

   if serialopen:
      ser.write(packet)
      swstate=lbl.cget("text")
      if swstate=="ON":
         lbl.configure(text='OFF',fg="black")
      else:
         lbl.configure(text='ON',fg="green")
   else:
      labelswitchteststatus.configure(text="Port not open!",fg="red")

def exportprofile():
   global filename
   if filename:
      print("export profile")
      expfilename = filedialog.asksaveasfilename(filetypes=[("HEX files","*.hex")],title="Open Profiles file.")
      f = open(expfilename,'w+b')

      #write digital inputs
      f.write(digitalinputdict[comboP1B2.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B1.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1RIGHT.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1LEFT.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1DOWN.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1UP.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1Service.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1Start.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B10.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B9.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B8.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B7.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B6.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B5.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B4.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B3.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B2.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B1.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2RIGHT.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2LEFT.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2DOWN.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2UP.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2Service.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2Start.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B10.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B9.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B8.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B7.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B6.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B5.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B4.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B3.get()].to_bytes(1,byteorder='little'))

      #write analog channels
      f.write(analogreversedict[comboA0.get()].to_bytes(1,byteorder='little'))
      f.write(analogreversedict[comboA1.get()].to_bytes(1,byteorder='little'))
      f.write(analogreversedict[comboA2.get()].to_bytes(1,byteorder='little'))
      f.write(analogreversedict[comboA3.get()].to_bytes(1,byteorder='little'))
      f.write(analogreversedict[comboA4.get()].to_bytes(1,byteorder='little'))
      f.write(analogreversedict[comboA5.get()].to_bytes(1,byteorder='little'))
      f.write(analogreversedict[comboA6.get()].to_bytes(1,byteorder='little'))
      f.write(analogreversedict[comboA7.get()].to_bytes(1,byteorder='little'))

      #write outputs
      byteval=0
      f.write(byteval.to_bytes(1,byteorder='little'))
      f.write(byteval.to_bytes(1,byteorder='little'))
      f.write(outputreversedict[comboOut2_3.get()].to_bytes(1,byteorder='little'))
      f.write(outputreversedict[comboOut2_2.get()].to_bytes(1,byteorder='little'))
      f.write(outputreversedict[comboOut2_1.get()].to_bytes(1,byteorder='little'))
      f.write(outputreversedict[comboOut1_3.get()].to_bytes(1,byteorder='little'))
      f.write(outputreversedict[comboOut1_2.get()].to_bytes(1,byteorder='little'))
      f.write(outputreversedict[comboOut1_1.get()].to_bytes(1,byteorder='little'))

      
      #write out name - up to 4 characters
      nameval = "1234"
      nameval = txtName.get()

      if (len(nameval)>0):
         f.write(ord(nameval[0]).to_bytes(1,byteorder='little'))
      else:
         f.write(byteval.to_bytes(1,byteorder='little'))
      if (len(nameval)>1):
         f.write(ord(nameval[1]).to_bytes(1,byteorder='little'))
      else:
         f.write(byteval.to_bytes(1,byteorder='little'))
      if (len(nameval)>2):
         f.write(ord(nameval[2]).to_bytes(1,byteorder='little'))
      else:
         f.write(byteval.to_bytes(1,byteorder='little'))
      if (len(nameval)>3):
         f.write(ord(nameval[3]).to_bytes(1,byteorder='little'))
      else:
         f.write(byteval.to_bytes(1,byteorder='little'))

      f.write(byteval.to_bytes(1,byteorder='little'))

      #write output count
      f.write(int(txtOutputCount.get(),base=10).to_bytes(1,byteorder='little'))

      #write analog options
      f.write(analogoptreversedict[comboAnalogOpts.get()].to_bytes(2,byteorder='little'))
      f.write(int(txtAnalogMin.get(),base=10).to_bytes(2,byteorder='little'))
      f.write(int(txtAnalogMax.get(),base=10).to_bytes(2,byteorder='little'))

      #write special case
      specialcasereversedict
      f.write(specialcasereversedict[comboSpecialCase.get()].to_bytes(1,byteorder='little'))

      f.write(byteval.to_bytes(1,byteorder='little'))
      f.close()
      
      labelStatus.configure(fg="green",text="Profile exported.")
   else:
      print("no file open")
      labelStatus.configure(fg="red",text="No file selected!")
   
def saveprofile():
   global filename
   global savedindex
   if filename:
      print("Saving profile")
      labelStatus.configure(fg="green",text="Profile saved.")
      f = open(filename,'r+b')
      indexval= comboProfiles.current()
      savedindex=indexval
      
      f.seek(indexval*62+0x00)

      #write digital inputs
      f.write(digitalinputdict[comboP1B2.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B1.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1RIGHT.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1LEFT.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1DOWN.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1UP.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1Service.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1Start.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B10.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B9.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B8.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B7.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B6.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B5.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B4.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B3.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B2.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B1.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2RIGHT.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2LEFT.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2DOWN.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2UP.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2Service.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2Start.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B10.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B9.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B8.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B7.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B6.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B5.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B4.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B3.get()].to_bytes(1,byteorder='little'))

      #write analog channels
      f.write(analogreversedict[comboA0.get()].to_bytes(1,byteorder='little'))
      f.write(analogreversedict[comboA1.get()].to_bytes(1,byteorder='little'))
      f.write(analogreversedict[comboA2.get()].to_bytes(1,byteorder='little'))
      f.write(analogreversedict[comboA3.get()].to_bytes(1,byteorder='little'))
      f.write(analogreversedict[comboA4.get()].to_bytes(1,byteorder='little'))
      f.write(analogreversedict[comboA5.get()].to_bytes(1,byteorder='little'))
      f.write(analogreversedict[comboA6.get()].to_bytes(1,byteorder='little'))
      f.write(analogreversedict[comboA7.get()].to_bytes(1,byteorder='little'))

      #write outputs
      byteval=0
      f.write(byteval.to_bytes(1,byteorder='little'))
      f.write(byteval.to_bytes(1,byteorder='little'))
      f.write(outputreversedict[comboOut2_3.get()].to_bytes(1,byteorder='little'))
      f.write(outputreversedict[comboOut2_2.get()].to_bytes(1,byteorder='little'))
      f.write(outputreversedict[comboOut2_1.get()].to_bytes(1,byteorder='little'))
      f.write(outputreversedict[comboOut1_3.get()].to_bytes(1,byteorder='little'))
      f.write(outputreversedict[comboOut1_2.get()].to_bytes(1,byteorder='little'))
      f.write(outputreversedict[comboOut1_1.get()].to_bytes(1,byteorder='little'))

      
      #write out name - up to 4 characters
      nameval = "1234"
      nameval = txtName.get()

      if (len(nameval)>0):
         f.write(ord(nameval[0]).to_bytes(1,byteorder='little'))
      else:
         f.write(byteval.to_bytes(1,byteorder='little'))
      if (len(nameval)>1):
         f.write(ord(nameval[1]).to_bytes(1,byteorder='little'))
      else:
         f.write(byteval.to_bytes(1,byteorder='little'))
      if (len(nameval)>2):
         f.write(ord(nameval[2]).to_bytes(1,byteorder='little'))
      else:
         f.write(byteval.to_bytes(1,byteorder='little'))
      if (len(nameval)>3):
         f.write(ord(nameval[3]).to_bytes(1,byteorder='little'))
      else:
         f.write(byteval.to_bytes(1,byteorder='little'))

      f.write(byteval.to_bytes(1,byteorder='little'))

      #write output count
      f.write(int(txtOutputCount.get(),base=10).to_bytes(1,byteorder='little'))

      #write analog options
      f.write(analogoptreversedict[comboAnalogOpts.get()].to_bytes(2,byteorder='little'))
      f.write(int(txtAnalogMin.get(),base=10).to_bytes(2,byteorder='little'))
      f.write(int(txtAnalogMax.get(),base=10).to_bytes(2,byteorder='little'))

      #write special case
      specialcasereversedict
      f.write(specialcasereversedict[comboSpecialCase.get()].to_bytes(1,byteorder='little'))

      f.write(byteval.to_bytes(1,byteorder='little'))

      f.close()
      
      reopenprofiles()

      
   else:
      print("No file has been selected")
      labelStatus.configure(fg="red",text="No file selected!")
         

def selectedanalogopt(val):
   print ("selected analog option")
   entry=comboAnalogOpts.get()
   print ("value is" + entry)
   txtAnalogMin.config(state='disabled')
   txtAnalogMax.config(state='disabled')
   if entry == "2 - SCALE STEERING" or entry == "3 - SCALE & SUPPRESS":
      txtAnalogMin.config(state='normal')
      txtAnalogMax.config(state='normal')

def addprofile():
   global filename
   global profilecount
   global savedindex
   if filename:
      print("adding profile")
      labelStatus.configure(fg="green",text="New profile added.")

      f = open(filename,'r+b')
      indexval= profilecount
      savedindex=indexval
      

      f.seek(indexval*62+0x00)

      #write digital inputs
      f.write(digitalinputdict[comboP1B2.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B1.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1RIGHT.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1LEFT.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1DOWN.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1UP.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1Service.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1Start.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B10.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B9.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B8.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B7.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B6.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B5.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B4.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP1B3.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B2.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B1.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2RIGHT.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2LEFT.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2DOWN.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2UP.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2Service.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2Start.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B10.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B9.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B8.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B7.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B6.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B5.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B4.get()].to_bytes(1,byteorder='little'))
      f.write(digitalinputdict[comboP2B3.get()].to_bytes(1,byteorder='little'))

      #write analog channels
      f.write(analogreversedict[comboA0.get()].to_bytes(1,byteorder='little'))
      f.write(analogreversedict[comboA1.get()].to_bytes(1,byteorder='little'))
      f.write(analogreversedict[comboA2.get()].to_bytes(1,byteorder='little'))
      f.write(analogreversedict[comboA3.get()].to_bytes(1,byteorder='little'))
      f.write(analogreversedict[comboA4.get()].to_bytes(1,byteorder='little'))
      f.write(analogreversedict[comboA5.get()].to_bytes(1,byteorder='little'))
      f.write(analogreversedict[comboA6.get()].to_bytes(1,byteorder='little'))
      f.write(analogreversedict[comboA7.get()].to_bytes(1,byteorder='little'))

      #write outputs
      byteval=0
      f.write(byteval.to_bytes(1,byteorder='little'))
      f.write(byteval.to_bytes(1,byteorder='little'))
      f.write(outputreversedict[comboOut2_3.get()].to_bytes(1,byteorder='little'))
      f.write(outputreversedict[comboOut2_2.get()].to_bytes(1,byteorder='little'))
      f.write(outputreversedict[comboOut2_1.get()].to_bytes(1,byteorder='little'))
      f.write(outputreversedict[comboOut1_3.get()].to_bytes(1,byteorder='little'))
      f.write(outputreversedict[comboOut1_2.get()].to_bytes(1,byteorder='little'))
      f.write(outputreversedict[comboOut1_1.get()].to_bytes(1,byteorder='little'))

      
      #write out name - up to 4 characters
      nameval = "1234"
      nameval = txtName.get()

      if (len(nameval)>0):
         f.write(ord(nameval[0]).to_bytes(1,byteorder='little'))
      else:
         f.write(byteval.to_bytes(1,byteorder='little'))
      if (len(nameval)>1):
         f.write(ord(nameval[1]).to_bytes(1,byteorder='little'))
      else:
         f.write(byteval.to_bytes(1,byteorder='little'))
      if (len(nameval)>2):
         f.write(ord(nameval[2]).to_bytes(1,byteorder='little'))
      else:
         f.write(byteval.to_bytes(1,byteorder='little'))
      if (len(nameval)>3):
         f.write(ord(nameval[3]).to_bytes(1,byteorder='little'))
      else:
         f.write(byteval.to_bytes(1,byteorder='little'))

      f.write(byteval.to_bytes(1,byteorder='little'))

      #write output count
      f.write(int(txtOutputCount.get(),base=10).to_bytes(1,byteorder='little'))

      #write analog options
      f.write(analogoptreversedict[comboAnalogOpts.get()].to_bytes(2,byteorder='little'))
      f.write(int(txtAnalogMin.get(),base=10).to_bytes(2,byteorder='little'))
      f.write(int(txtAnalogMax.get(),base=10).to_bytes(2,byteorder='little'))

      #write special case
      specialcasereversedict
      f.write(specialcasereversedict[comboSpecialCase.get()].to_bytes(1,byteorder='little'))

      f.write(byteval.to_bytes(1,byteorder='little'))

      f.close()
      reopenprofiles()
      
   else:
      print("No file has been selected")
      labelStatus.configure(fg="red",text="No file selected!")

def setupswitchtest():
   global switchtestopen
   
   if switchtestopen == False:
      w = root.winfo_width()
      h = root.winfo_height()
      x = root.winfo_x()
      y = root.winfo_y()
      switchtestwindow.geometry("%dx%d+%d+%d" % (w, h, x, y))
      switchtestwindow.deiconify()
      
      root.withdraw()
      switchtestwindow.protocol("WM_DELETE_WINDOW", switchtestclosing)
      switchtestopen = True
      
def profilemanager():
   global profilemanageropen
   global filename
   labelStatus.configure(fg="black",text="")

   if filename:
      if profilemanageropen == False:
         listboxprofiles.delete(0, END)
         for item in profilelist:
             listboxprofiles.insert(END, item)
         w = root.winfo_width()
         h = root.winfo_height()
         x = root.winfo_x()
         y = root.winfo_y()
         profilemanagerwindow.geometry("%dx%d+%d+%d" % (w, h, x, y))
         profilemanagerwindow.deiconify()
         
         root.withdraw()
         profilemanagerwindow.protocol("WM_DELETE_WINDOW", profmanclosing)
         profilemanageropen = True
   else:
      labelStatus.configure(fg="red",text="No file selected!")
      
   

def profmanclosing():
   global profilemanageropen
   global savedindex
   profilemanageropen = False
   print("closed profile manager")
   
   w = profilemanagerwindow.winfo_width()
   h = profilemanagerwindow.winfo_height()
   x = profilemanagerwindow.winfo_x()
   y = profilemanagerwindow.winfo_y()
   root.geometry("%dx%d+%d+%d" % (w, h, x, y))
   root.deiconify()
   profilemanagerwindow.withdraw()

   savedindex=0
   reopenprofiles()

def switchtestclosing():
   global filename
   global switchtestopen
   global savedindex
   switchtestopen = False
   #print("closed USB Switch Test")
   
   w = switchtestwindow.winfo_width()
   h = switchtestwindow.winfo_height()
   x = switchtestwindow.winfo_x()
   y = switchtestwindow.winfo_y()
   root.geometry("%dx%d+%d+%d" % (w, h, x, y))
   root.deiconify()
   switchtestwindow.withdraw()

   savedindex=0
   if filename:
      reopenprofiles()

def deleteprofileatindex(index,size):
   global filename
   f = open(filename,'r+b')
   f.seek((index+1)*62)
   #profiledata = f.read((size-1)*62)
   profiledata = f.read()
   f.seek(index*62)
   f.write(profiledata)
   #f.seek((size-1)*62)
   f.truncate()
   f.close()

def deleteprofile():
   global filename
   #print("delete profile")
   #print(listboxprofiles.curselection())
   if str(listboxprofiles.curselection()) != "()":
      index = int(listboxprofiles.curselection()[0])
   else:
      index = -1
      
   size = listboxprofiles.size()
   if size>1 and index>=0:
      listboxprofiles.delete(index, last=None )
      #add code to delete profile at given index
      deleteprofileatindex(index,size)
      

def moveprofileup():
   #print("move profile up")
   global filename
   if str(listboxprofiles.curselection()) != "()":
      index = int(listboxprofiles.curselection()[0])
   else:
      index = -1
      
   size = listboxprofiles.size()
   if size>1 and index>0:
      listboxprofiles.insert(index-1, listboxprofiles.get(index))
      listboxprofiles.delete(index+1, last=None)
      listboxprofiles.activate(index-1)
      listboxprofiles.selection_set(index-1)
      listboxprofiles.see(index-1)
      #add code to manage profile movement up
      f = open(filename,'r+b')
      f.seek((index)*62)
      shiftedprofile = f.read(62)
      f.seek((index-1)*62)
      profiledata = f.read()
      f.seek(index*62)
      f.write(profiledata)
      f.seek((index-1)*62)
      f.write(shiftedprofile)
      f.close()
      deleteprofileatindex(index+1,size+1)

def readconfigfile():
   configfile="config.ini"
   f=open(configfile, "r")
   global wheelmax
   global wheelmin
   #f.seek(1)
   f.readline()
   minval = int(f.readline().rstrip(),base=10)
   #print(hex(minval))
   #f.seek(3)
   f.readline()
   maxval = int(f.readline().rstrip(),base=10)
   #print(hex(maxval))
   f.close()
   wheelmax=maxval
   wheelmin=minval
   labelActualMin.configure(text="Actual Min: " + str(wheelmin))
   labelActualMax.configure(text="Actual Max: " + str(wheelmax))
   #ScaleAnalogMin.set(wheelmin)
   #ScaleAnalogMax.set(wheelmax)

def moveprofiledown():
   #print("move profile down")
   global filename
   if str(listboxprofiles.curselection()) != "()":
      index = int(listboxprofiles.curselection()[0])
   else:
      index = -1
      
   size = listboxprofiles.size()
   if size>1 and index>=0 and index+1 !=size:
      listboxprofiles.insert(index+2, listboxprofiles.get(index))
      listboxprofiles.delete(index, last=None)
      listboxprofiles.activate(index+1)
      listboxprofiles.selection_set(index+1)
      listboxprofiles.see(index+1)
      
      #add code to manage profile movement down
      f = open(filename,'r+b')
      f.seek((index)*62)
      shiftedprofile = f.read(62)
      f.seek((index+1)*62)
      #profiledata = f.read((size-1)*62)
      profiledata = f.read()
      f.seek((index+2)*62)
      f.write(profiledata)
      f.seek((index+2)*62)
      f.write(shiftedprofile)
      f.close()
      deleteprofileatindex(index,size+1)

def selectedprofile(val):
   labelStatus.configure(fg="black",text="")
   indexval= comboProfiles.current()
   print("selected a profile")
   print("index: ")
   print(indexval)
   print("value: ")
   print(comboProfiles.get())
   txtName.delete(0,END)
   txtName.insert(0,comboProfiles.get())
   
   labelCurrentProfNum['text'] = "Profile " + str(indexval+1) + " of " + str(profilecount)
   f = open(filename,'rb')
   
   f.seek(indexval*62+0x00)
   comboP1B2.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP1B1.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP1RIGHT.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP1LEFT.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP1DOWN.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP1UP.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP1Service.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP1Start.set(digitalinputlist[int.from_bytes(f.read(1),"big")])

   comboP1B10.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP1B9.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP1B8.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP1B7.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP1B6.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP1B5.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP1B4.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP1B3.set(digitalinputlist[int.from_bytes(f.read(1),"big")])

   comboP2B2.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP2B1.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP2RIGHT.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP2LEFT.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP2DOWN.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP2UP.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP2Service.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP2Start.set(digitalinputlist[int.from_bytes(f.read(1),"big")])

   comboP2B10.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP2B9.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP2B8.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP2B7.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP2B6.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP2B5.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP2B4.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   comboP2B3.set(digitalinputlist[int.from_bytes(f.read(1),"big")])

   comboA0.set(analogdict[int.from_bytes(f.read(1),"big")])
   comboA1.set(analogdict[int.from_bytes(f.read(1),"big")])
   comboA2.set(analogdict[int.from_bytes(f.read(1),"big")])
   comboA3.set(analogdict[int.from_bytes(f.read(1),"big")])
   comboA4.set(analogdict[int.from_bytes(f.read(1),"big")])
   comboA5.set(analogdict[int.from_bytes(f.read(1),"big")])
   comboA6.set(analogdict[int.from_bytes(f.read(1),"big")])
   comboA7.set(analogdict[int.from_bytes(f.read(1),"big")])

   f.seek(indexval*62+0x2A)
   comboOut2_3.set(outputdict[int.from_bytes(f.read(1),"big")])
   comboOut2_2.set(outputdict[int.from_bytes(f.read(1),"big")])
   comboOut2_1.set(outputdict[int.from_bytes(f.read(1),"big")])
   comboOut1_3.set(outputdict[int.from_bytes(f.read(1),"big")])
   comboOut1_2.set(outputdict[int.from_bytes(f.read(1),"big")])
   comboOut1_1.set(outputdict[int.from_bytes(f.read(1),"big")])

   f.seek(indexval*62+0x35)
   txtOutputCount.delete(0,END)
   txtOutputCount.insert(0,int.from_bytes(f.read(1),"big"))

   comboAnalogOpts.set(analogoptionslist[int.from_bytes(f.read(2),"little")])
   txtAnalogMin.config(state='normal')
   txtAnalogMax.config(state='normal')
      
   txtAnalogMin.delete(0,END)
   readval = int.from_bytes(f.read(2),"little")
   txtAnalogMin.insert(0,int(readval))
   txtAnalogMax.delete(0,END)
   readval = int.from_bytes(f.read(2),"little")
   txtAnalogMax.insert(0,int(readval))
   readval = int.from_bytes(f.read(1),"big")
   print (readval)
   comboSpecialCase.set(specialcaselist[readval])
   
   f.close()
   selectedanalogopt(0)

root = Tk()
menubar = Menu(root)
root.config(menu=menubar)
root.wm_title("MEGA JVS PROFILE EDITOR")
root.geometry('{}x{}'.format(940, 1000))

submenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label="File",menu=submenu);
menubar.add_command(label = "Profile Manager",command=profilemanager)
submenu.add_command(label = "Open Profiles",command=openprofiles)


menubar.add_command(label = "Re-Open Config",command=readconfigfile)
menubar.add_command(label = "USB Switch Test",command=setupswitchtest)

submenu.add_command(label = "Quit",command=root.quit)
#submenu.add_command(label = "Save Profiles",command=saveprofile)

buttonAddProfile = ttk.Button(root, text='Add As New Profile', command=addprofile, width = 20)
buttonSaveProfile = ttk.Button(root, text='Save Current Profile', command=saveprofile, width = 20)
buttonExportProfile = ttk.Button(root, text='Export Current Profile', command=exportprofile, width = 20)
buttonImportProfile = ttk.Button(root, text='Import Profile', command=importprofile, width = 20)


labelChooseProf = Label(text="Choose Profile", fg="black",justify=LEFT,anchor=W,width = 15)
labelDigitalInputs = Label(text="Digital Inputs:", fg="black",justify=LEFT,anchor=W,width = 15)
labelAnalogInputs = Label(text="Analog Inputs:", fg="black",justify=LEFT,anchor=W,width = 15)
labelOutputs = Label(text="Outputs:", fg="black",justify=LEFT,anchor=W,width = 15)
labelOutputReport = Label(text="Reported Ouputs:", fg="black",justify=LEFT,anchor=W,width = 17)
labelAnalogOptions = Label(text="Analog Options:", fg="black",justify=LEFT,anchor=W,width = 17)

labelSpecialCase = Label(text="Special Case:", fg="black",justify=LEFT,anchor=W,width = 17)
comboSpecialCase = ttk.Combobox(root)

labelStatus = Label(text="", fg="black",justify=LEFT,anchor=W,width = 17)

labelName = Label(text="Name (4 Chars MAX):", fg="black",justify=RIGHT,anchor=E,width = 18)
txtName = Entry(root)

labelCurrentProfNum = Label(text="", fg="black")

lst1 = ['Option1','Option2','Option3']
comboProfiles = ttk.Combobox(root)
#comboProfiles['values']=lst1
#comboProfiles.current(newindex=0)
comboProfiles.bind('<<ComboboxSelected>>', selectedprofile)
comboProfiles.state(['readonly'])

labelP1UP = Label(text="P1 - UP", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP1UP = ttk.Combobox(root)
labelP1DOWN = Label(text="P1 - DOWN", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP1DOWN = ttk.Combobox(root)
labelP1LEFT = Label(text="P1 - LEFT", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP1LEFT = ttk.Combobox(root)
labelP1RIGHT = Label(text="P1 - RIGHT", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP1RIGHT = ttk.Combobox(root)

labelP1B1 = Label(text="P1 - BUTTON 1", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP1B1 = ttk.Combobox(root)
labelP1B2 = Label(text="P1 - BUTTON 2", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP1B2 = ttk.Combobox(root)
labelP1B3 = Label(text="P1 - BUTTON 3", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP1B3 = ttk.Combobox(root)
labelP1B4 = Label(text="P1 - BUTTON 4", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP1B4 = ttk.Combobox(root)
labelP1B5 = Label(text="P1 - BUTTON 5", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP1B5 = ttk.Combobox(root)
labelP1B6 = Label(text="P1 - BUTTON 6", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP1B6 = ttk.Combobox(root)
labelP1B7 = Label(text="P1 - BUTTON 7", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP1B7 = ttk.Combobox(root)
labelP1B8 = Label(text="P1 - BUTTON 8", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP1B8 = ttk.Combobox(root)
labelP1B9 = Label(text="P1 - BUTTON 9", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP1B9 = ttk.Combobox(root)
labelP1B10 = Label(text="P1 - BUTTON 10", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP1B10 = ttk.Combobox(root)
labelP1Service = Label(text="P1 - Service", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP1Service = ttk.Combobox(root)
labelP1Start = Label(text="P1 - Start", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP1Start = ttk.Combobox(root)


labelP2UP = Label(text="P2 - UP", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP2UP = ttk.Combobox(root)
labelP2DOWN = Label(text="P2 - DOWN", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP2DOWN = ttk.Combobox(root)
labelP2LEFT = Label(text="P2 - LEFT", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP2LEFT = ttk.Combobox(root)
labelP2RIGHT = Label(text="P2 - RIGHT", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP2RIGHT = ttk.Combobox(root)

labelP2B1 = Label(text="P2 - BUTTON 1", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP2B1 = ttk.Combobox(root)
labelP2B2 = Label(text="P2 - BUTTON 2", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP2B2 = ttk.Combobox(root)
labelP2B3 = Label(text="P2 - BUTTON 3", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP2B3 = ttk.Combobox(root)
labelP2B4 = Label(text="P3 - BUTTON 4", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP2B4 = ttk.Combobox(root)
labelP2B5 = Label(text="P2 - BUTTON 5", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP2B5 = ttk.Combobox(root)
labelP2B6 = Label(text="P2 - BUTTON 6", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP2B6 = ttk.Combobox(root)
labelP2B7 = Label(text="P2 - BUTTON 7", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP2B7 = ttk.Combobox(root)
labelP2B8 = Label(text="P2 - BUTTON 8", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP2B8 = ttk.Combobox(root)
labelP2B9 = Label(text="P2 - BUTTON 9", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP2B9 = ttk.Combobox(root)
labelP2B10 = Label(text="P2 - BUTTON 10", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP2B10 = ttk.Combobox(root)
labelP2Service = Label(text="P2 - Service", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP2Service = ttk.Combobox(root)
labelP2Start = Label(text="P2 - Start", fg="black",justify=RIGHT,anchor=E,width = 15)
comboP2Start = ttk.Combobox(root)


labelA0=Label(text="A0", fg = "black",justify=RIGHT,anchor=E,width = 15)
comboA0=ttk.Combobox(root)
labelA1=Label(text="A1", fg = "black",justify=RIGHT,anchor=E,width = 15)
comboA1=ttk.Combobox(root)
labelA2=Label(text="A2", fg = "black",justify=RIGHT,anchor=E,width = 15)
comboA2=ttk.Combobox(root)
labelA3=Label(text="A3", fg = "black",justify=RIGHT,anchor=E,width = 15)
comboA3=ttk.Combobox(root)
labelA4=Label(text="A4", fg = "black",justify=RIGHT,anchor=E,width = 15)
comboA4=ttk.Combobox(root)
labelA5=Label(text="A5", fg = "black",justify=RIGHT,anchor=E,width = 15)
comboA5=ttk.Combobox(root)
labelA6=Label(text="A6", fg = "black",justify=RIGHT,anchor=E,width = 15)
comboA6=ttk.Combobox(root)
labelA7=Label(text="A7", fg = "black",justify=RIGHT,anchor=E,width = 15)
comboA7=ttk.Combobox(root)

labelOut1_1=Label(text="Out1_1", fg = "black",justify=RIGHT,anchor=E,width = 15)
labelOut1_2=Label(text="Out1_2", fg = "black",justify=RIGHT,anchor=E,width = 15)
labelOut1_3=Label(text="Out1_3", fg = "black",justify=RIGHT,anchor=E,width = 15)
labelOut2_1=Label(text="Out2_1", fg = "black",justify=RIGHT,anchor=E,width = 15)
labelOut2_2=Label(text="Out2_2", fg = "black",justify=RIGHT,anchor=E,width = 15)
labelOut2_3=Label(text="Out2_3", fg = "black",justify=RIGHT,anchor=E,width = 15)

comboOut1_1=ttk.Combobox(root)
comboOut1_2=ttk.Combobox(root)
comboOut1_3=ttk.Combobox(root)
comboOut2_1=ttk.Combobox(root)
comboOut2_2=ttk.Combobox(root)
comboOut2_3=ttk.Combobox(root)

txtOutputCount = Entry(root)

labelAnalogOpts = Label(text="Option:", fg="black",justify=RIGHT,anchor=E,width = 15)
comboAnalogOpts = ttk.Combobox(root)

comboAnalogOpts.bind('<<ComboboxSelected>>', selectedanalogopt)

labelAnalogMin = Label(text="Steering Min:", fg="black",justify=RIGHT,anchor=E,width = 15)
txtAnalogMin = Entry(root)
labelAnalogMax = Label(text="Steering Max:", fg="black",justify=RIGHT,anchor=E,width = 15)
txtAnalogMax = Entry(root)

labelActualMin = Label(text="Actual Min:" + str(wheelmin), fg="black",anchor=S,width = 15)
labelActualMax = Label(text="Actual Max:" + str(wheelmax), fg="black",anchor=S,width = 15)

#ScaleAnalogMin = Scale(root, from_=0, to=255, orient=HORIZONTAL)
#ScaleAnalogMax = Scale(root, from_=0, to=255, orient=HORIZONTAL)

labelChooseProf.grid(row=0,column=0)
comboProfiles.grid(row=0,column=1)
labelCurrentProfNum.grid(row=0,column=2)
buttonAddProfile.grid(row=0,column=4)
buttonSaveProfile.grid(row=0,column=3)
buttonImportProfile.grid(row=1,column=4)
buttonExportProfile.grid(row=1,column=3)

labelName.grid(row=1,column=0)
txtName.grid(row=1,column=1)

labelStatus.grid(row=0,column=5)

labelDigitalInputs.grid(row=3,column=0)

labelP1Start.grid(row=4, column=0)
comboP1Start.grid(row=4, column=1)
labelP1Service.grid(row=5, column=0)
comboP1Service.grid(row=5, column=1)
labelP1UP.grid(row=6, column=0)
comboP1UP.grid(row=6, column=1)
labelP1DOWN.grid(row=7, column=0)
comboP1DOWN.grid(row=7, column=1)
labelP1LEFT.grid(row=8, column=0)
comboP1LEFT.grid(row=8, column=1)
labelP1RIGHT.grid(row=9, column=0)
comboP1RIGHT.grid(row=9, column=1)
labelP1B1.grid(row=10, column=0)
comboP1B1.grid(row=10, column=1)
labelP1B2.grid(row=11, column=0)
comboP1B2.grid(row=11, column=1)
labelP1B3.grid(row=12, column=0)
comboP1B3.grid(row=12, column=1)
labelP1B4.grid(row=13, column=0)
comboP1B4.grid(row=13, column=1)
labelP1B5.grid(row=14, column=0)
comboP1B5.grid(row=14, column=1)
labelP1B6.grid(row=15, column=0)
comboP1B6.grid(row=15, column=1)
labelP1B7.grid(row=16, column=0)
comboP1B7.grid(row=16, column=1)
labelP1B8.grid(row=17, column=0)
comboP1B8.grid(row=17, column=1)
labelP1B9.grid(row=18, column=0)
comboP1B9.grid(row=18, column=1)
labelP1B10.grid(row=19, column=0)
comboP1B10.grid(row=19, column=1)



labelP2Start.grid(row=4, column=3)
comboP2Start.grid(row=4, column=4)
labelP2Service.grid(row=5, column=3)
comboP2Service.grid(row=5, column=4)
labelP2UP.grid(row=6, column=3)
comboP2UP.grid(row=6, column=4)
labelP2DOWN.grid(row=7, column=3)
comboP2DOWN.grid(row=7, column=4)
labelP2LEFT.grid(row=8, column=3)
comboP2LEFT.grid(row=8, column=4)
labelP2RIGHT.grid(row=9, column=3)
comboP2RIGHT.grid(row=9, column=4)
labelP2B1.grid(row=10, column=3)
comboP2B1.grid(row=10, column=4)
labelP2B2.grid(row=11, column=3)
comboP2B2.grid(row=11, column=4)
labelP2B3.grid(row=12, column=3)
comboP2B3.grid(row=12, column=4)
labelP2B4.grid(row=13, column=3)
comboP2B4.grid(row=13, column=4)
labelP2B5.grid(row=14, column=3)
comboP2B5.grid(row=14, column=4)
labelP2B6.grid(row=15, column=3)
comboP2B6.grid(row=15, column=4)
labelP2B7.grid(row=16, column=3)
comboP2B7.grid(row=16, column=4)
labelP2B8.grid(row=17, column=3)
comboP2B8.grid(row=17, column=4)
labelP2B9.grid(row=18, column=3)
comboP2B9.grid(row=18, column=4)
labelP2B10.grid(row=19, column=3)
comboP2B10.grid(row=19, column=4)


labelAnalogInputs.grid(row=22,column=0)
labelA0.grid(row=23, column=0)
comboA0.grid(row=23, column=1)
labelA1.grid(row=24, column=0)
comboA1.grid(row=24, column=1)
labelA2.grid(row=25, column=0)
comboA2.grid(row=25, column=1)
labelA3.grid(row=26, column=0)
comboA3.grid(row=26, column=1)
labelA4.grid(row=23, column=3)
comboA4.grid(row=23, column=4)
labelA5.grid(row=24, column=3)
comboA5.grid(row=24, column=4)
labelA6.grid(row=25, column=3)
comboA6.grid(row=25, column=4)
labelA7.grid(row=26, column=3)
comboA7.grid(row=26, column=4)



labelOutputs.grid(row=28, column=0)
labelOut1_1.grid(row=29, column=0)
labelOut1_2.grid(row=30, column=0)
labelOut1_3.grid(row=31, column=0)
labelOut2_1.grid(row=29, column=3)
labelOut2_2.grid(row=30, column=3)
labelOut2_3.grid(row=31, column=3)

comboOut1_1.grid(row=29, column=1)
comboOut1_2.grid(row=30, column=1)
comboOut1_3.grid(row=31, column=1)
comboOut2_1.grid(row=29, column=4)
comboOut2_2.grid(row=30, column=4)
comboOut2_3.grid(row=31, column=4)

labelOutputReport.grid(row=33, column=0)
txtOutputCount.grid(row=33, column=1)

labelAnalogOptions.grid(row=35,column=0)
labelAnalogOpts.grid(row=36,column=0)
comboAnalogOpts.grid(row=36,column=1)
comboAnalogOpts.state(['readonly'])

labelAnalogMin.grid(row=38,column=0)
txtAnalogMin.grid(row=38,column=1)
labelAnalogMax.grid(row=38,column=2)
txtAnalogMax.grid(row=38,column=3)

#ScaleAnalogMin.grid(row=38,column=2)
#ScaleAnalogMax.grid(row=38,column=5)

labelActualMin.grid(row=37,column=1)
labelActualMax.grid(row=37,column=3)


labelSpecialCase.grid(row=40,column=0)
comboSpecialCase.grid(row=40,column=1)
comboSpecialCase.state(['readonly'])
   
comboP1B1.state(['readonly'])
comboP1B10.state(['readonly'])
comboP1B2.state(['readonly'])
comboP1B3.state(['readonly'])
comboP1B4.state(['readonly'])
comboP1B5.state(['readonly'])
comboP1B6.state(['readonly'])
comboP1B7.state(['readonly'])
comboP1B8.state(['readonly'])
comboP1B9.state(['readonly'])
comboP1DOWN.state(['readonly'])
comboP1LEFT.state(['readonly'])
comboP1RIGHT.state(['readonly'])
comboP1Service.state(['readonly'])
comboP1Start.state(['readonly'])
comboP1UP.state(['readonly'])

comboP2B1.state(['readonly'])
comboP2B10.state(['readonly'])
comboP2B2.state(['readonly'])
comboP2B3.state(['readonly'])
comboP2B4.state(['readonly'])
comboP2B5.state(['readonly'])
comboP2B6.state(['readonly'])
comboP2B7.state(['readonly'])
comboP2B8.state(['readonly'])
comboP2B9.state(['readonly'])
comboP2DOWN.state(['readonly'])
comboP2LEFT.state(['readonly'])
comboP2RIGHT.state(['readonly'])
comboP2Service.state(['readonly'])
comboP2Start.state(['readonly'])
comboP2UP.state(['readonly'])

comboOut1_1.state(['readonly'])
comboOut1_2.state(['readonly'])
comboOut1_3.state(['readonly'])
comboOut2_1.state(['readonly'])
comboOut2_2.state(['readonly'])
comboOut2_3.state(['readonly'])

comboAnalogOpts.state(['readonly'])

comboP1B1['values']=digitalinputlist
comboP1B10['values']=digitalinputlist
comboP1B2['values']=digitalinputlist
comboP1B3['values']=digitalinputlist
comboP1B4['values']=digitalinputlist
comboP1B5['values']=digitalinputlist
comboP1B6['values']=digitalinputlist
comboP1B7['values']=digitalinputlist
comboP1B8['values']=digitalinputlist
comboP1B9['values']=digitalinputlist
comboP1DOWN['values']=digitalinputlist
comboP1LEFT['values']=digitalinputlist
comboP1RIGHT['values']=digitalinputlist
comboP1Service['values']=digitalinputlist
comboP1Start['values']=digitalinputlist
comboP1UP['values']=digitalinputlist

comboP2B1['values']=digitalinputlist
comboP2B10['values']=digitalinputlist
comboP2B2['values']=digitalinputlist
comboP2B3['values']=digitalinputlist
comboP2B4['values']=digitalinputlist
comboP2B5['values']=digitalinputlist
comboP2B6['values']=digitalinputlist
comboP2B7['values']=digitalinputlist
comboP2B8['values']=digitalinputlist
comboP2B9['values']=digitalinputlist
comboP2DOWN['values']=digitalinputlist
comboP2LEFT['values']=digitalinputlist
comboP2RIGHT['values']=digitalinputlist
comboP2Service['values']=digitalinputlist
comboP2Start['values']=digitalinputlist
comboP2UP['values']=digitalinputlist

comboA0.state(['readonly'])
comboA1.state(['readonly'])
comboA2.state(['readonly'])
comboA3.state(['readonly'])
comboA4.state(['readonly'])
comboA5.state(['readonly'])
comboA6.state(['readonly'])
comboA7.state(['readonly'])

comboA0['values']=analoglist
comboA1['values']=analoglist
comboA2['values']=analoglist
comboA3['values']=analoglist
comboA4['values']=analoglist
comboA5['values']=analoglist
comboA6['values']=analoglist
comboA7['values']=analoglist

comboOut1_1['values']=outputlist
comboOut1_2['values']=outputlist
comboOut1_3['values']=outputlist
comboOut2_1['values']=outputlist
comboOut2_2['values']=outputlist
comboOut2_3['values']=outputlist

comboAnalogOpts['values']=analogoptionslist

comboSpecialCase['values']=specialcaselist

profilemanagerwindow = Toplevel()
profilemanagerwindow.title("MEGA JVS PROFILE MANAGER")
labelprofmanmain = Label(profilemanagerwindow, text="Profile List")
#l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

switchtestwindow = Toplevel()
switchtestwindow.title("MEGA JVS USB SWITCH TEST")
switchtestmenubar = Menu(switchtestwindow)
switchtestmenubar.add_command(label = "Profile Editor",command=switchtestclosing)
switchtestwindow.config(menu=switchtestmenubar)

labelserialportname = Label(switchtestwindow, text="Enter Serial Port Name.")
labelserialportname.grid(row=0,column=0)
txtserialportname = Entry(switchtestwindow)
txtserialportname.grid(row=0,column=1)
buttonsetupserial = ttk.Button(switchtestwindow, text='Start Serial', command=setupserial, width = 20)
buttonsetupserial.grid(row=0,column=2)
labelswitchteststatus = Label(switchtestwindow, text="")
labelswitchteststatus.grid(row=0,column=3)
buttoncloseserial = ttk.Button(switchtestwindow, text='Close Serial', command=closeserial, width = 20)
buttoncloseserial.grid(row=2,column=2)
labeldirections = Label(switchtestwindow, text="Click to toggle input.")
labeldirections.grid(row=3,column=0)

buttonresetswitches = ttk.Button(switchtestwindow, text='Reset Switches', command=resetswitches, width = 20)
buttonresetswitches.grid(row=3,column=1)

buttonswtstP1_START = ttk.Button(switchtestwindow, text='P1_START', command= lambda: sendswitchserial(0x01,0x80,lblP1_START) , width = 20)
buttonswtstP1_SERVICE = ttk.Button(switchtestwindow, text='P1_SERVICE', command= lambda: sendswitchserial(0x01,0x40,lblP1_SERVICE) , width = 20)
buttonswtstP1_UP = ttk.Button(switchtestwindow, text='P1_UP', command= lambda: sendswitchserial(0x01,0x20,lblP1_UP) , width = 20)
buttonswtstP1_DOWN = ttk.Button(switchtestwindow, text='P1_DOWN', command= lambda: sendswitchserial(0x01,0x10,lblP1_DOWN) , width = 20)
buttonswtstP1_LEFT = ttk.Button(switchtestwindow, text='P1_LEFT', command= lambda: sendswitchserial(0x01,0x08,lblP1_LEFT) , width = 20)
buttonswtstP1_RIGHT = ttk.Button(switchtestwindow, text='P1_RIGHT', command= lambda: sendswitchserial(0x01,0x04,lblP1_RIGHT) , width = 20)
buttonswtstP1_B1 = ttk.Button(switchtestwindow, text='P1_B1', command= lambda: sendswitchserial(0x01,0x02,lblP1_B1) , width = 20)
buttonswtstP1_B2 = ttk.Button(switchtestwindow, text='P1_B2', command= lambda: sendswitchserial(0x01,0x01,lblP1_B2) , width = 20)
buttonswtstP1_B3 = ttk.Button(switchtestwindow, text='P1_B3', command= lambda: sendswitchserial(0x02,0x80,lblP1_B3) , width = 20)
buttonswtstP1_B4 = ttk.Button(switchtestwindow, text='P1_B4', command= lambda: sendswitchserial(0x02,0x40,lblP1_B4) , width = 20)
buttonswtstP1_B5 = ttk.Button(switchtestwindow, text='P1_B5', command= lambda: sendswitchserial(0x02,0x20,lblP1_B5) , width = 20)
buttonswtstP1_B6 = ttk.Button(switchtestwindow, text='P1_B6', command= lambda: sendswitchserial(0x02,0x10,lblP1_B6) , width = 20)
buttonswtstP1_B7 = ttk.Button(switchtestwindow, text='P1_B7', command= lambda: sendswitchserial(0x02,0x08,lblP1_B7) , width = 20)
buttonswtstP1_B8 = ttk.Button(switchtestwindow, text='P1_B8', command= lambda: sendswitchserial(0x02,0x04,lblP1_B8) , width = 20)
buttonswtstP1_B9 = ttk.Button(switchtestwindow, text='P1_B9', command= lambda: sendswitchserial(0x02,0x02,lblP1_B9) , width = 20)
buttonswtstP1_B10 = ttk.Button(switchtestwindow, text='P1_B10', command= lambda: sendswitchserial(0x02,0x01,lblP1_B10) , width = 20)
buttonswtstP2_START = ttk.Button(switchtestwindow, text='P2_START', command= lambda: sendswitchserial(0x03,0x80,lblP2_START) , width = 20)
buttonswtstP2_SERVICE = ttk.Button(switchtestwindow, text='P2_SERVICE', command= lambda: sendswitchserial(0x03,0x40,lblP2_SERVICE) , width = 20)
buttonswtstP2_UP = ttk.Button(switchtestwindow, text='P2_UP', command= lambda: sendswitchserial(0x03,0x20,lblP2_UP) , width = 20)
buttonswtstP2_DOWN = ttk.Button(switchtestwindow, text='P2_DOWN', command= lambda: sendswitchserial(0x03,0x10,lblP2_DOWN) , width = 20)
buttonswtstP2_LEFT = ttk.Button(switchtestwindow, text='P2_LEFT', command= lambda: sendswitchserial(0x03,0x08,lblP2_LEFT) , width = 20)
buttonswtstP2_RIGHT = ttk.Button(switchtestwindow, text='P2_RIGHT', command= lambda: sendswitchserial(0x03,0x04,lblP2_RIGHT) , width = 20)
buttonswtstP2_B1 = ttk.Button(switchtestwindow, text='P2_B1', command= lambda: sendswitchserial(0x03,0x02,lblP2_B1) , width = 20)
buttonswtstP2_B2 = ttk.Button(switchtestwindow, text='P2_B2', command= lambda: sendswitchserial(0x03,0x01,lblP2_B2) , width = 20)
buttonswtstP2_B3 = ttk.Button(switchtestwindow, text='P2_B3', command= lambda: sendswitchserial(0x04,0x80,lblP2_B3) , width = 20)
buttonswtstP2_B4 = ttk.Button(switchtestwindow, text='P2_B4', command= lambda: sendswitchserial(0x04,0x40,lblP2_B4) , width = 20)
buttonswtstP2_B5 = ttk.Button(switchtestwindow, text='P2_B5', command= lambda: sendswitchserial(0x04,0x20,lblP2_B5) , width = 20)
buttonswtstP2_B6 = ttk.Button(switchtestwindow, text='P2_B6', command= lambda: sendswitchserial(0x04,0x10,lblP2_B6) , width = 20)
buttonswtstP2_B7 = ttk.Button(switchtestwindow, text='P2_B7', command= lambda: sendswitchserial(0x04,0x08,lblP2_B7) , width = 20)
buttonswtstP2_B8 = ttk.Button(switchtestwindow, text='P2_B8', command= lambda: sendswitchserial(0x04,0x04,lblP2_B8) , width = 20)
buttonswtstP2_B9 = ttk.Button(switchtestwindow, text='P2_B9', command= lambda: sendswitchserial(0x04,0x02,lblP2_B9) , width = 20)
buttonswtstP2_B10 = ttk.Button(switchtestwindow, text='P2_B10', command= lambda: sendswitchserial(0x04,0x01,lblP2_B10) , width = 20)


buttonswtstP1_START.grid(row=4,column=0)
buttonswtstP1_SERVICE.grid(row=5,column=0)
buttonswtstP1_UP.grid(row=6,column=0)
buttonswtstP1_DOWN.grid(row=7,column=0)
buttonswtstP1_LEFT.grid(row=8,column=0)
buttonswtstP1_RIGHT.grid(row=9,column=0)
buttonswtstP1_B1.grid(row=10,column=0)
buttonswtstP1_B2.grid(row=11,column=0)
buttonswtstP1_B3.grid(row=12,column=0)
buttonswtstP1_B4.grid(row=13,column=0)
buttonswtstP1_B5.grid(row=14,column=0)
buttonswtstP1_B6.grid(row=15,column=0)
buttonswtstP1_B7.grid(row=16,column=0)
buttonswtstP1_B8.grid(row=17,column=0)
buttonswtstP1_B9.grid(row=18,column=0)
buttonswtstP1_B10.grid(row=19,column=0)
buttonswtstP2_START.grid(row=4,column=3)
buttonswtstP2_SERVICE.grid(row=5,column=3)
buttonswtstP2_UP.grid(row=6,column=3)
buttonswtstP2_DOWN.grid(row=7,column=3)
buttonswtstP2_LEFT.grid(row=8,column=3)
buttonswtstP2_RIGHT.grid(row=9,column=3)
buttonswtstP2_B1.grid(row=10,column=3)
buttonswtstP2_B2.grid(row=11,column=3)
buttonswtstP2_B3.grid(row=12,column=3)
buttonswtstP2_B4.grid(row=13,column=3)
buttonswtstP2_B5.grid(row=14,column=3)
buttonswtstP2_B6.grid(row=15,column=3)
buttonswtstP2_B7.grid(row=16,column=3)
buttonswtstP2_B8.grid(row=17,column=3)
buttonswtstP2_B9.grid(row=18,column=3)
buttonswtstP2_B10.grid(row=19,column=3)


lblP1_START=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP1_SERVICE=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP1_UP=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP1_DOWN=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP1_LEFT=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP1_RIGHT=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP1_B1=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP1_B2=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP1_B3=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP1_B4=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP1_B5=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP1_B6=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP1_B7=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP1_B8=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP1_B9=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP1_B10=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP2_START=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP2_SERVICE=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP2_UP=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP2_DOWN=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP2_LEFT=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP2_RIGHT=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP2_B1=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP2_B2=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP2_B3=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP2_B4=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP2_B5=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP2_B6=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP2_B7=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP2_B8=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP2_B9=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)
lblP2_B10=Label(switchtestwindow, text='OFF',fg='black',justify=LEFT,anchor=W,width=20)





lblP1_START.grid(row=4,column=1)
lblP1_SERVICE.grid(row=5,column=1)
lblP1_UP.grid(row=6,column=1)
lblP1_DOWN.grid(row=7,column=1)
lblP1_LEFT.grid(row=8,column=1)
lblP1_RIGHT.grid(row=9,column=1)
lblP1_B1.grid(row=10,column=1)
lblP1_B2.grid(row=11,column=1)
lblP1_B3.grid(row=12,column=1)
lblP1_B4.grid(row=13,column=1)
lblP1_B5.grid(row=14,column=1)
lblP1_B6.grid(row=15,column=1)
lblP1_B7.grid(row=16,column=1)
lblP1_B8.grid(row=17,column=1)
lblP1_B9.grid(row=18,column=1)
lblP1_B10.grid(row=19,column=1)
lblP2_START.grid(row=4,column=4)
lblP2_SERVICE.grid(row=5,column=4)
lblP2_UP.grid(row=6,column=4)
lblP2_DOWN.grid(row=7,column=4)
lblP2_LEFT.grid(row=8,column=4)
lblP2_RIGHT.grid(row=9,column=4)
lblP2_B1.grid(row=10,column=4)
lblP2_B2.grid(row=11,column=4)
lblP2_B3.grid(row=12,column=4)
lblP2_B4.grid(row=13,column=4)
lblP2_B5.grid(row=14,column=4)
lblP2_B6.grid(row=15,column=4)
lblP2_B7.grid(row=16,column=4)
lblP2_B8.grid(row=17,column=4)
lblP2_B9.grid(row=18,column=4)
lblP2_B10.grid(row=19,column=4)






profmanmenubar = Menu(profilemanagerwindow)
profmanmenubar.add_command(label = "Profile Editor",command=profmanclosing)
profilemanagerwindow.config(menu=profmanmenubar)
profilemanagerwindow.geometry('{}x{}'.format(940, 1000))
buttonDeleteProfile = ttk.Button(profilemanagerwindow, text='Delete Selected Profile', command=deleteprofile, width = 20)
buttonMoveProfileUp = ttk.Button(profilemanagerwindow, text='Move Up', command=moveprofileup, width = 20)
buttonMoveProfileDown = ttk.Button(profilemanagerwindow, text='Move Down', command=moveprofiledown, width = 20)





frame = Frame(profilemanagerwindow,width=32,height=31)
scrollbar = Scrollbar(frame, orient=VERTICAL)
listboxprofiles = Listbox(frame, yscrollcommand=scrollbar.set)
listboxprofiles.configure(height=30,width=20)
scrollbar.config(command=listboxprofiles.yview)
scrollbar.pack(side=RIGHT, fill=Y)
listboxprofiles.pack(side=LEFT, fill=BOTH, expand=1)

frame.grid(row=1,column=1)

#listboxprofiles = Listbox(frame)
labelprofmanmain.grid(row=0,column=1)
#listboxprofiles.configure(height=30)
#listboxprofiles.grid(row=1,column=1)
buttonDeleteProfile.grid(row=0,column=4)
buttonMoveProfileUp.grid(row=0,column=2)
buttonMoveProfileDown.grid(row=0,column=3)

profilemanagerwindow.withdraw()
switchtestwindow.withdraw()
#profilemanagerwindow.destroy()
readconfigfile()

root.config(menu=menubar)
root.mainloop()
