#!/usr/bin/python
##################################################################################
# Author: Huaqin Xu (huaxu@ucdavis.edu)
# Supervisor: Alexander Kozik (akozik@atgc.org)
# Date: Oct.12. 2009
# Description:
#
# This python script splits file by prefix and count the match information. 
#
# =================================================================================
# input arguments:
#	1.input file.
#	2.size of prefix
#	3.output suffix ("_dummy_split.tab")
#		  
# Output: split files.
#
######################################################################################

import sys
import re
import array
import os
from math import *
from os.path import exists, join, basename, splitext


# ---------------------------functions ------------------------------------------------
# ---------------- Open and read file functions ---------------------------------------
def open_file(file_name, mode):
	if file_name == "":
		print 'Empty input file name!'
		raw_input("\nPress the enter key to exit.")
		sys.exit(0)

	try:
		the_file = open(file_name, mode)
	except(IOError), e:
		print "Unable to open the file", file_name, "Ending program.\n", e
		raw_input("\nPress the enter key to exit.")
		sys.exit(0)
	else:
		return the_file

def read_file(afile):
	try:
		flines = afile.readlines()
	except:
		print 'Failed to read from: ', afile
		sys.exit(0)
	else:
		return flines




# ------------------- get Data to be displyed------------------------------------
def getData(lines):
	global query
	global prefix
	global content
	global header
	
	delimiter="\t"
	datalen=len(lines)
	if(datalen == 0):
		print "Empty Data file!"
		sys.exit(0)
	colcount=lines[0].count(delimiter)+1
	header = lines[0]
	query=[]
	content={}
	
	aq = 'x'
	for l in range(1, datalen):

	# check for empty lines and incorrect field numbers
		if lines[l] != '\n':
			if lines[l].count(delimiter)==colcount-1:
				arow=lines[l].rstrip().split(delimiter)
				if(arow[0][0:prefix] != aq):
					aq = arow[0][0:prefix]
					query.append(aq)
					content[aq] = []
				
				content[aq].append(arow)				
			
			else:
				print "Error: Line #%s has inconsistent number of columns.\n" %(l+1)
				sys.exit(0)
		else:
			print "Skip an empty line at #%s.\n" %(l+1)



# ------------------- print table -------------------
def printtable(aq):
	global content
	global header
	
	outf.write(header)
	for line in content[aq]:
		outf.write("\t".join(line)+"\n")
	lines = len(content[aq])
	
	totallen = header.count("\t")
	mismatch = []
	for j in range(1, totallen+1):
		sum = map(lambda i:i[j], content[aq])  # get all letters in j position
		unisum = dict(map(lambda k:(k,1), sum)).keys() # get unique letters in j position
		unisum.sort()
		if(len(unisum)==2 and unisum[0] != '-') or (len(unisum)>2):
			mismatch.append(str(j))
	
	sumstring = aq+"\t"+str(lines)+"\t"+str(len(mismatch))+"\t["+" ".join(mismatch)+"]"+"\n"
	sumf.write(sumstring)			


#----------------------------- main ------------------------------------------------------

# ----- get options and file names and open files -----
if len(sys.argv) == 4:
	infile=sys.argv[1]
	prefix=int(sys.argv[2])
	suffix=sys.argv[3]
else: 
	print len(sys.argv)
	print 'Usage: [1]infile, [2]size of prefix [3]suffix'
	sys.exit(1) 


inf=open_file(infile,'r')
inlines = read_file(inf)
infilebase = splitext(basename(infile))[0]
getData(inlines)

sumfile= infilebase + "_summary" + suffix
sumf = open_file(sumfile,'w')


for q in query:
#	print content[q].count("\n")
	if(len(content[q])>1):
		outfile= q + suffix
		outf=open_file(outfile,'w')	
		printtable(q)

	else:
		print "Skip an file at q.\n" 
		
		