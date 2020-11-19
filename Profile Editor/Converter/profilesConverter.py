
import struct
import sys


filename = sys.argv[1]


print ("filename is: " + filename)
   

def convertProfiles():
   
   
   

   f = open(filename,'r+b')
   
   f.seek(0, 2)
   bytecount = f.tell()
   
   convertedData=b''
   
   print ("Size of file: " + str(bytecount))
   profilecount = bytecount/62
   
   i=0;
   i2=0;
   position=0;
   
   profilesList=[]
   f.seek(0)
   while (i<profilecount):
       #print (f.read(62))
       #currentProfile=f.read(62)
       profilesList.append(f.read(62))
       i+=1
   #print (profilesList)
   
   print ("Profile count: " + str(profilecount))
   #f.seek(0*80+0x00)
   #comboP1B2.set(digitalinputlist[int.from_bytes(f.read(1),"big")])
   
   f.close()
   
   f = open(filename,'r+b')
   for prof in profilesList:
       f.write(prof)
       f.write(b'\x1C\x1D') #coins
       f.write(b'\x00\x00\x00\x00\x00\x00\x00\x00') #outputs2
       f.write(b'\x00\x00\x00\x00\x00\x00\x00\x00') #outputs3
   
   f.close()
   
   print ("Conversion completed!")

convertProfiles()