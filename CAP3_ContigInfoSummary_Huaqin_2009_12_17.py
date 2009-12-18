#!/usr/bin/python
##################################################################################
# Author: Huaqin Xu (huaxu@ucdavis.edu)
# Supervisor: Alexander Kozik (akozik@atgc.org)
# Date: June. 19 2006
# Description:
#
# This python script extracts individual sequences from the contigs input data file. 
#
# =================================================================================
# Input file format:
# --- Input files contains three fields: ContigID, # of Sequences and Sequence String,
#	 which are delimited by tab. Sequences in sequence string are delimited by '|',
#	and each sequence contains sequenceID, oritention, start_postion and end_position.
#
# --- Examples	
#   [ContigID]   [No.of Sequneces]  [Sequences String]   	 
#        |              |                   |
#   CLL_S1_Contig7      2     CLLX10035.b1_E13.ab1+(1,831)|CLLX9783.b1_N21.ab1+(16,831)
#			
#   [Sequence String] -> CLLX10035.b1_E13.ab1+(1,831)|CLLX9783.b1_N21.ab1+(16,831)
#                          /                 |       |                       /   \
#                   [SequenceID]    [Oritention][Delimiter]     [Start_position][End_position] 
#
# ---------------------------------------------------------------------------------
# Output file format:
# 
#    [ContigID] [No. of Sequences] [SequenceID] [Oritention] [Start_position] [End_position]
#         |        |                     |            |           |             |
#  CLL_S1_Contig7  2          CLLX10035.b1_E13.ab1    +           1            831
#  CLL_S1_Contig7  2          CLLX9783.b1_N21.ab1     +           16           831
#
######################################################################################

import sys
import re

# ---------------------------functions ------------------------------------------------
# -------------------------------------------------------------------------------------
def open_file(file_name, mode):
	try:
		the_file = open(file_name, mode)
	except(IOError), e:
		print "Unable to open the file", file_name, "Ending program.\n", e
		raw_input("\n\nPress the enter key to exit.")
		sys.exit(0)
	else:
		return the_file

# -------------------------------------------------------------------------------------
def getcontig(aline):
	global outf
	global logf
	global l
	global logcount
	fields = aline.split('\t')
	contigcount = int(fields[1])

	# Check for the consistence between sequence number and sequences string
	if fields[2].count('|') == contigcount-1:
		contigs = fields[2].split('|')
		for c in contigs:

			#construct pattern to retrieve info from sequence
			pattern="([A-Za-z0-9._]+)([+-])\(([0-9]+),([0-9]+)\)"
			if(re.search(pattern,c)==None):
				logcount += 1
				logf.write("#Warning: Skip line #%s due to wrong format.\n\t%s\n" %(l+1,aline))
				break
			else:
				m=re.match(pattern,c)
				outf.write(';'.join((fields[0],fields[1],m.group(1),m.group(2),m.group(3),m.group(4)))+'\n')
	
	else:
		logcount += 1
		logf.write("Warning: Skip line #%s due to inconsistent sequence numbers.\n\t%s\n" %(l+1,aline))


#----------------------------- main ------------------------------------------------------
# ----- get input file name and construct output file name and open files -----
s = raw_input("Enter the SOURCE file name: ")	
if s != "":
	ifile = s
else:
	print 'Empty input file name!'
	raw_input("\n\nPress the enter key to exit.")
	sys.exit(0)
	
ofile=ifile+'.out'
lfile=ifile+'.log'

inf=open_file(ifile,'r')
outf=open_file(ofile,'w')
logf = open_file(lfile,'w')

# ----- Read from input files -----
try:
	flines = inf.readlines()
except:
	print 'Failed to read from: ', ifile
	sys.exit(1)
 
linecount = len(flines)
logcount=0

# ----- Loop through all the lines in the file -----
for l in range(linecount):

	# check for empty lines and incorrect field numbers
	if flines[l] != '\n' and flines[l].count('\t')>=2:
		flines[l].rstrip() 
		getcontig(flines[l])
	else:
		logcount += 1
		logf.write("Warning: Skip line #%s due to empty or wrong format.\n" %(l+1))

# ----- Print messages for user to find output -----
print 'Done... Total %s lines, skip %s lines' %(linecount,logcount)
print 'Please find output in file "%s", error messages in file "%s"' %(ofile,lfile)

inf.close()
outf.close()
logf.close()

