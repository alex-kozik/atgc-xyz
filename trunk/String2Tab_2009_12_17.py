#!/usr/bin/python

####################################################
#                                                  #
#                 DUMMY TABULATOR                  #
#                                                  #
#       COPYRIGHT, ALEXANDER KOZIK, 2005           #
#                                                  #
####################################################

def Seqs_Extractor(in_name1, out_name, tab_sep):

	print "====================================="
	print "INPUT FILE (TEXT_STR) :   " + in_name1
	print "OUTPUT FILE (TAB)     :   " + out_name
	print "====================================="

	time.sleep(2)

	in_file1  = open(in_name1, "rb")
	out_file  = open(out_name, "wb")

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

		id = t[0]
		seq = t[1]

		tab_seq = list(seq)

		tab_seq = "\t".join(tab_seq)

		print id

		out_file.write(id + '\t' + tab_seq + '\n')

	in_file1.close()
	out_file.close()

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
		print "input_file1(TEXT_STR) input_file2(TEXT_TAB) TAB"
		sys.exit()
	if len(sys.argv) == 4:
		in_name1  = sys.argv[1]
		out_name  = sys.argv[2]
		tab_sep   = sys.argv[3]
		if tab_sep == "TAB":
			Seqs_Extractor(in_name1, out_name, tab_sep)
		if tab_sep != "TAB":
			print "Last argument must be TAB"
			sys.exit()
### THE END ###
