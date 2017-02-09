import math
import json
import serial 
import serial.tools.list_ports
from operator import sub,add
import time
import openal 
from sys import argv
from vybe_actuator import *
from vybe_frame import *
from vybe_helper import *

test = argv[1]
movement = argv[2]
posx = 0
posy = 0
posz = 0
if len(argv) > 3:
    posx = float(argv[3])
    posy = float(argv[4])
    posz = float(argv[5])
#####################################
#
# Detect and Connect to Vybe Device
#
#####################################

#Load Vybe device details
vybe_desc = {}
with open('vybe.json', 'r') as f:
	vybe_desc = json.load(f)

vybe = None
ports = list(serial.tools.list_ports.comports())
'''if not "usb" in ports[0][0]:
raise IOError("%s not detected."%(vybe_desc["name"])) '''
for p in ports:
    if "usb" in p[0]:
        vybe= None
vybe = serial.Serial(p[0], 9600)
'''#Search for all connected Vybe devices
connectedDevices = []
for portcandidate in serial.tools.list_ports.comports():
	port_type = portcandidate[2] #each port description is a list of length 3; item 3 has vendor id and product id
	if port_type.find('USB VID:PID=%s:%d'%(str(vybe_desc["comm"]["usbserial"]["vid"]), vybe_desc["comm"]["usbserial"]["pid"])) >= 0:
		print "Found %s"%(portcandidate[0],)
		connectedDevices.append(portcandidate[0]) #name of this port

#Connect to first found Vybe device
vybe = None
if connectedDevices:
	portname = connectedDevices[0]
	vybe = serial.Serial(port=portname, baudrate=vybe_desc["comm"]["usbserial"]["baud"], writeTimeout = 0.05)
else:
	raise IOError("%s not detected."%(vybe_desc["name"]))
	
contextlistener = openal.Device().ContextListener()
contextlistener.position = [0, 0, 0]
contextlistener.velocity = [0, 0, 0]
contextlistener.orientation = [0, 1, 0, 0, 0, 1]

source1 = contextlistener.get_source()
source1.buffer = openal.Buffer("0.wav")
source1.looping = True
'''
source1_position = [posx,posy,posz]
'''
source1.play()
'''
ops = [sub, add]

actuators = []
for i in range(12):
    actuators.append(actuator((i+1),vybe_desc))
xy = frame("xy",vybe_desc)
xz = frame("xz",vybe_desc)
   

try:
	while True:
		source1_position = [ops[0](source1_position[0], 0.5 * int("x" in movement)), ops[0](source1_position[1], 0.5 * int("y" in movement)), ops[0](source1_position[2], 0.5 * int("z" in movement))]
		print("\t".join([str(round(p,4)) for p in source1_position]))

                if test == "0":
                    for i in range(12):
                        actuators[i].stop
                        
		elif test == "1" or test == "1.linear":
			for i in range(12):
				actuators[i].play(source1_position,vybe)
		elif test == "1.exp":
			for i in range(12):
				actuators[i].play_exp(source1_position,vybe)
		elif test == "2" or test == "2.linear":
			x,y,z = source1_position
			x0,y0,z0 = [-0.7,22.0,33.1]
			played = []
			if x >= x0:
				if y >= y0:
					played.append(11)
				elif y <= y0:
					played.append(9)
				if z >= z0:
					played.append(1)
					played.append(2)
				elif z <= z0:
					played.append(5)
					played.append(7)
			elif x <= x0:
				if y >= y0:
					played.append(12)
				elif y <= y0:
					played.append(10)
				elif z >= z0:
					played.append(3)
					played.append(4)
				elif z <= z0:
					played.append(6)
					played.append(8)
			for i in range(12):
				if (i+1) in played:
					actuators[i].play(source1_position,vybe)
				else:
					actuators[i].stop
                        del played[:]
                        
		elif test == "2.exp":
			x,y,z = source1_position
			x0,y0,z0 = [-0.7,22.0,33.1]
			played = []
			if x >= x0:
				print "right"
				if y >= y0:
					played.append(11)
				if y <= y0:
					played.append(9)
				if z >= z0:
					played.append(1)
					played.append(2)
				if z <= z0:
					played.append(5)
					played.append(7)
			if x <= x0:
				print "left"
				if y >= y0:
					played.append(12)
				if y <= y0:
					played.append(10)
				if z >= z0:
					played.append(3)
					played.append(4)
				if z <= z0:
					played.append(6)
					played.append(8)
			for i in range(12):
				if (i+1) in played:
					actuators[i].play_exp(source1_position,vybe)
					print i
				else:
					actuators[i].stop
			del played[:]
		elif test == "3" or test == "3.linear":
			xy.play(source1_position,vybe)
			xz.play(source1_position,vybe)
		elif test == "3.exp":
			xy.play_exp(source1_position,vybe)
			xz.play_exp(source1_position,vybe)
		elif test == "4" or test == "4.linear":
			if source1_position[1] > 0 and source1_position[2] > 0:
				continue
			elif distance(source1_position,xy.createPoint(source1_position)) < distance(source1_position,xz.createPoint(source1_position)) :
				xy.play(source1_position,vybe)
			else:
				xz.play(source1_position,vybe)
		elif test == "4.exp":
			if source1_position[1] > 0 and source1_position[2] > 0:
				continue
			elif distance(source1_position,xy.createPoint(source1_position)) < distance(source1_position,xz.createPoint(source1_position)) :
				xy.play_exp(source1_position,vybe)
			else:
				xz.play_exp(source1_position,vybe)

		time.sleep(0.2)
		if abs(source1_position[0]) > 20 or abs(source1_position[1]) > 20 or abs(source1_position[2]) > 20:
			ops = list(reversed(ops))

except (KeyboardInterrupt, SystemExit):
	for i in range(12):
			actuators[i].stop(vybe)
	raise
