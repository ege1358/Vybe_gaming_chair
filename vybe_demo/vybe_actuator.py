import math
import json
import serial 
import serial.tools.list_ports
from vybe_helper import *

class actuator(object):

	def __init__(self, index, vybe_desc):
		self.vybe_index = index
		if self.vybe_index <= 6:
			self.hardware = "VC"
			self.index = 7-index
			
		else:
			self.hardware = "M"
			self.index = 13-index
	 	
		self.desc = vybe_desc["actuators"][self.hardware + str(self.index)]
		pos_x = self.desc["x"]-23
		pos_sx = linear_map(pos_x,-9,10,-3,3)
		if self.vybe_index > 8:
			pos_y = self.desc["y"]-53
			pos_sy = linear_map(pos_y,0,28,-4,4)
			pos_sz = pos_z = 0
		else:
			pos_sy = pos_y = 0
			pos_z = 53-self.desc["y"]
			pos_sz = linear_map(pos_z,0,32,-5,5)
		self.pos = [pos_x,pos_y,pos_z]
		self.spos = [pos_sx,pos_sy,pos_sz]

 	
	def get_type(self):
		return self.desc["actuatortype"]

	def get_pos(self):
		return self.pos

	def get_spos(self):
		return self.spos

	def set(self, value,serial):
		value = int(min(max(0, value), 255))
		
		if self.hardware == "VC":
			# format: "VCL <number as character> <buzz value 0-255 as character\n"
			msg = 	"VCL %s %s\n"%(str(self.index), chr(value))
		else:
			# format: "MTR <number as character> <buzz value 0-255 as character\n"			
			msg = 	"MTR %s %s\n"%(str(self.index), chr(value))
		serial.write(msg)
		serial.flush()

	def play(self, source_pos,serial):
		self.set(linear_map(distance(self.spos,source_pos),15,0,0,255),serial)

	def play_exp(self, source_pos,serial):
		self.set(exp_map(-1 * distance(self.spos,source_pos),255,1.35,0),serial)
		print str(exp_map(-1 * distance(self.spos,source_pos),255,1.35,0))
	def stop(self,serial):
		self.set(0,serial)

		
		
			
