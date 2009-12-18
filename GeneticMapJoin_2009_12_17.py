#!/usr/bin/python

####################################################
#                                                  #
#     JOIN TWO MAPS AND GENERATE DUMMY MATRIX      #
#            FOR GENOPIX 2 D-PLOTTER               #
#                                                  #
#       COPYRIGHT, ALEXANDER KOZIK, 2005           #
#                                                  #
####################################################

def Genetic_Map_Join(in_name1, in_name2, out_name, order_by, k1, k2):

	print "====================================="
	print "INPUT FILE 1 (MAP 1) :   " + in_name1
	print "INPUT FILE 2 (MAP 2) :   " + in_name2
	print "OUTPUT FILE          :   " + out_name
	print "ORDER BY             :   " + order_by
	print "K1 IS                :   " + `k1`
	print "K2 IS                :   " + `k2`
	print "====================================="

	time.sleep(2)

	in_file1  = open(in_name1, "rb")
	in_file2  = open(in_name2, "rb")
	out_map   = open(out_name + ".genopix.coords", "wb")
	out_mtx   = open(out_name + ".genopix.matrix", "wb")

	map1_array = {}
	map2_array = {}

	map1_list  = []
	map2_list  = []

	#################################
	while 1:
		t = in_file1.readline()
		if t == '':
			break
		if '\n' in t:
			t = t[:-1]
		if '\r' in t:
			t = t[:-1]
		t = t.split('\t')

		id = t[1]
		ps = t[2]
		ps = float(ps)*k1
		ps = str(round(ps,2))
		map1_array[id] = ps
		map1_list.append(id)

		print id + "    " + ps

	#################################
	while 1:
		t = in_file2.readline()
		if t == '':
			break
		if '\n' in t:
			t = t[:-1]
		if '\r' in t:
			t = t[:-1]
		t = t.split('\t')

		id = t[1]
		ps = t[2]
		ps = float(ps)*k2
		ps = str(round(ps,2))
		map2_array[id] = ps
		map2_list.append(id)

		print id

	#################################

	p = 0
	for item in map1_list:

		if order_by == "ORDER":
			coordinates = str(p)

		if order_by == "POSITION":
			coordinates = map1_array[item]

		out_map.write("1" + '\t' + item + "__1" + '\t' + coordinates + '\t' + "C" + '\t' + "yellow" + '\n')

		print item + "    " + coordinates

		p = p + 1

	p = 0
	for item in map2_list:

		if order_by == "ORDER":
			coordinates = str(p)

		if order_by == "POSITION":
			coordinates = map2_array[item]

		out_map.write("2" + '\t' + item + "__2" + '\t' + coordinates + '\t' + "W" + '\t' + "orange" + '\n')

		print item + "    " + coordinates

		p = p + 1

	for item1 in map1_list:
		if item1 in map2_list:
			out_mtx.write(item1 + "__1" + '\t' + item1 + "__2" + '\t' + "1.00" + '\n')
			print " + "
		if item1 not in map2_list:
			print " - "

	in_file1.close()
	in_file2.close()
	out_map.close()
	out_mtx.close()

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
	if len(sys.argv) <= 6 or len(sys.argv) > 7:
		print "Program usage: "
		print "input_file1(MAP1) input_file2(MAP2) output_file ORDER/POSITION K1 K2"
		sys.exit()
	if len(sys.argv) == 7:
		in_name1  = sys.argv[1]
		in_name2  = sys.argv[2]
		out_name  = sys.argv[3]
		order_by  = sys.argv[4]
		k1        = float(sys.argv[5])
		k2        = float(sys.argv[6])
		Genetic_Map_Join(in_name1, in_name2, out_name, order_by, k1, k2)
### THE END ###

