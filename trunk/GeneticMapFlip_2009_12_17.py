#!/usr/bin/python

####################################################
#                                                  #
#      FLIP GENETIC MAP IN REVERSE ORDER           #
#                                                  #
#       COPYRIGHT, ALEXANDER KOZIK, 2009           #
#                                                  #
####################################################

def Genetic_Map_Flip(in_name, out_name, order_by):

	print "====================================="
	print "INPUT FILE  (MAP)    :   " + in_name
	print "OUTPUT FILE          :   " + out_name
	print "ORDER BY             :   " + order_by
	print "====================================="

	time.sleep(2)

	in_file  = open(in_name, "rb")
	out_map  = open(out_name + ".rev.map", "wb")

	map_array = {}
	lgr_array = {}
	map_list  = []

	#################################
	max_pos = 0
	max_crd = 0
	while 1:
		t = in_file.readline()
		if t == '':
			break
		if '\n' in t:
			t = t[:-1]
		if '\r' in t:
			t = t[:-1]
		t = t.split('\t')

		lg = t[0]
		id = t[1]
		ps = t[2]
		ps = float(ps)
		map_array[id] = ps
		lgr_array[id] = lg
		map_list.append(id)

		print id + "    " + `ps`

		max_pos = max_pos + 1
		max_crd = ps

	#################################

	### REVERSE LIST ###
	map_list_rev = map_list[:]	# will be reverse string
	map_list_rev.reverse()

	p = 0
	for item in map_list_rev:

		if order_by == "ORDER":
			coordinates = str(p)

		if order_by == "POSITION":
			coordinates = max_crd - map_array[item]
			coordinates = str(round(coordinates,2))

		out_map.write(lgr_array[item] + '\t' + item + '\t' + coordinates + '\n')

		print item + "    " + coordinates

		p = p + 1

	in_file.close()
	out_map.close()

##################
#                #
#   MAIN BODY    #
#                #
##################

import math
import re
import sys
import string
import time
import os

if __name__ == "__main__":
	if len(sys.argv) <= 3 or len(sys.argv) > 4:
		print "Program usage: "
		print "input_file(MAP) output_file ORDER/POSITION"
		sys.exit()
	if len(sys.argv) == 4:
		in_name   = sys.argv[1]
		out_name  = sys.argv[2]
		order_by  = sys.argv[3]
		Genetic_Map_Flip(in_name, out_name, order_by)
### THE END ###

