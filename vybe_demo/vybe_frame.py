import math
import json
import serial 
import serial.tools.list_ports
from operator import sub,add
import time

from vybe_actuator import * 
from vybe_helper import *

class frame(object):
	
	def __init__(self,dim,vybe_desc):
		self.actuators = []
		self.dim = dim
		if dim == "xy":
			for index in range(9,13):
				self.actuators.append(actuator(index, vybe_desc))
			self.mesh = ((0,3,2),(0,1,3))
		elif dim == "xz":
			for index in range(1,9):
				self.actuators.append(actuator(index, vybe_desc))
			self.mesh = (
				(
					((0,4,6),(0,1,4)), ((0,2,4),(2,5,4)),((2,3,5),(3,7,5))),
				(
					((0,4,6),(4,5,6)),
					((4,5,6),(5,7,6)),
					((5,7,6),(3,7,5)))
				)
			

	def createPoint(self,source_pos):
		if self.dim == "xy":
			point = [min(max(-9.7, source_pos[0]), 8.3),min(max(15.8, source_pos[1]), 28.3),0]
		elif self.dim == "xz":
			point =[min(max(-10.0, source_pos[0]), 8.6), 0, min(max(15.2, source_pos[2]), 32.0)]
		return point
	def findRec(self,point):
			if point[2] > 24.2:
				rec_y = 0
			else:
				rec_y = 1

			if point[0] > 2.4:
				rec_x = 0
			elif point[0] > -3.8:
				rec_x = 1
			else:
				rec_x = 2
			return (rec_x,rec_y)
	def calcTri(self,x,y,x1,y1,x2,y2,x3,y3):
		d = (y2 - y3)*(x1 - x3) - (x2 - x3)*(y1 - y3)
		a = round(((y2 - y3)*(x - x3) + (x3 - x2)*(y - y3)) / d,1)
		b = round(((y3 - y1)*(x - x3) + (x1 - x3)*(y - y3)) / d,1)
		c = round(1 - a - b,1)
		return (a,b,c)
	def findTri(self,point,rec):
		x,y,z = point
		print x,y,z
		if self.dim == "xy":
			for i in range(2):
				x1 = self.actuators[self.mesh[i][0]].get_pos()[0]
				print x1
				y1 = self.actuators[self.mesh[i][0]].get_pos()[1]
				print y1
				x2 = self.actuators[self.mesh[i][1]].get_pos()[0]
				print x2
				y2 = self.actuators[self.mesh[i][1]].get_pos()[1]
				print y2
				x3 = self.actuators[self.mesh[i][2]].get_pos()[0]
				print x3
				y3 = self.actuators[self.mesh[i][2]].get_pos()[1]
				print y3
				a,b,c = self.calcTri(x,y,x1,y1,x2,y2,x3,y3)
				if 0 <= a and a <= 1 and 0 <= b and b <= 1 and 0 <= c and c <= 1:
					return (self.mesh[i][0],self.mesh[i][1],self.mesh[i][2],a,b,c)
			y1 = y2 = 15.8
			y3 = 28.3
			if point[0] > 5.3:
				x1 = x3 = 8.3
				x2 = 5.3
				a,b,c = self.calcTri(x,y,x1,y1,x2,y2,x3,y3)
				return (-1,0,2,a,b,c)
			elif point[0] < -6.7:
				x1 = -6.7
				x2 = x3 = -9.7
				a,b,c = self.calcTri(x,y,x1,y1,x2,y2,y3,y3)
				return (1,-1,3,a,b,c)
		if self.dim == "xz":
			tri = self.mesh[rec[1]][rec[0]]
			for i in range(2):
				x1 = self.actuators[tri[i][0]].get_pos()[0]
				z1 = self.actuators[tri[i][0]].get_pos()[2]
				x2 = self.actuators[tri[i][1]].get_pos()[0]
				z2 = self.actuators[tri[i][1]].get_pos()[2]
				x3 = self.actuators[tri[i][2]].get_pos()[0]
				z3 = self.actuators[tri[i][2]].get_pos()[2]
				a,b,c = self.calcTri(x,z,x1,z1,x2,z2,x3,z3)
				if (0 <= a and a <= 1 and 0 <= b and b <= 1 and 0 <= c and c <= 1) or i == 1:
					return (tri[i][0],tri[i][1],tri[i][2],a,b,c)
			"""z1 = 32
			z2 = z3 = 15.2
			if rec[0] < 1:
				x1 = x3 = 8.6
				x2 = 7.9
				a,b,c = self.calcTri(x,z,x1,z1,x2,z2,x3,z3)
				return (0,6,-1,a,b,c)
			elif rec[0] > 1:
				x1 = x2 = -10
				x3 = -9.3
				a,b,c = self.calcTri(x,z,x1,z1,x2,z2,x3,z3)
				return (3,-1,7,a,b,c)"""
	def play(self,source_pos,serial):
		point = self.createPoint(source_pos)
		if self.dim == "xz":
			rec = self.findRec(point)
		else:
			rec = (0,0)
		p1, p2, p3, a, b, c = self.findTri(point,rec)
		amp = linear_map(distance(point,source_pos),20,0,0,255)
		for i in range(len(self.actuators)):
			if i == p1:
				self.actuators[p1].set(math.sqrt(max(0,a))*amp,serial)
			elif i == p2:
				self.actuators[p2].set(math.sqrt(max(0,b))*amp,serial)
			elif i == p3:
				self.actuators[p3].set(math.sqrt(max(0,c))*amp,serial)
			else:
				self.actuators[i].stop(serial)

	def play_exp(self,source_pos,serial):
		point = self.createPoint(source_pos)
		rec = self.findRec(point)
		p1, p2, p3, a, b, c = self.findTri(point,rec)
		amp = exp_map(-1 * distance(point,source_pos),255,1.35,0)
		print  amp
		for i in range(len(self.actuators)):
			if i == p1:
				self.actuators[p1].set(math.sqrt(a)*amp,serial)
			elif i == p2:
				self.actuators[p2].set(math.sqrt(b)*amp,serial)
			elif i == p3:
				self.actuators[p3].set(math.sqrt(c)*amp,serial)
			else:
				self.actuators[i].stop(serial)
