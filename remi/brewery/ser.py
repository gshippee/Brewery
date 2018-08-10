import serial
import struct
#from visual import *
import numpy as np
from time import sleep

 
#Start the serial port to communicate with arduino
data = serial.Serial(port='/dev/cu.SLAB_USBtoUART', baudrate=115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)


print("connected to: " + data.portstr)
count=1
pos = 90
while (1==1):
	pos = pos+10
	if (pos<=180 and pos >= 0):
		data.write(struct.pack('>B',pos)) #code and send the angle to the Arduino through serial port
	else:
		print("Number must be between 0 and 180\n")
	line = data.readline()
	print(line)
	line = data.readline()
	print(line)
	sleep(.5)
	#count = count+1

ser.close()
