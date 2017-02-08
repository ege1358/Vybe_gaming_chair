import math

def distance(pos1,pos2):
	dis_x = pos1[0]-pos2[0]
	dis_y = pos1[1]-pos2[1]
	dis_z = pos1[2]-pos2[2]
	return math.sqrt((dis_x**2)+(dis_y**2)+(dis_z**2))

def linear_map(x, in_min, in_max, out_min, out_max):
    	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
def exp_map(x,a,b,c):
	return a * (b**x) + c
