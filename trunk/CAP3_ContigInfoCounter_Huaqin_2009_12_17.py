#!/usr/bin/python
#########################################################################################################
# Author: Huaqin Xu (huaxu@ucdavis.edu)
# Supervisor: Alexander Kozik (akozik@atgc.org)
# Date: Sep. 7 2006
# Description:
#
# This python script summrizes contigs by genotype or user defined type.
#
# =======================================================================================================
# Input file
# Contig file format:
# --- Input files contains three fields: ContigID, # of Sequences and Sequence String,
#	 which are delimited by tab. Sequences in sequence string are delimited by '|',
#	and each sequence contains sequenceID, oritention, start_postion and end_position.
#
# --- Examples	
#   [ContigID]   [No.of Sequneces]  [Sequences String]   	 
#        |              |                   |
#   UCO2_Contig1878	3	HAN.DY917364.CDS+(1,513)|HAR.EE609702.CDS+(1,333)|HAN.AJ318286.CDS+(298,627)
#			
#   [Sequence String] -> HAN.DY917364.CDS+(1,513)|HAR.EE609702.CDS+(1,333)|HAN.AJ318286.CDS+(298,627)
#                         |				   |				    |
#                 	Type1				  Type2			   Type1
#
# ---------------------------------------------------------------------------------
# Output file format:
# 
#    [ContigID] 	[No. of Type1/HAN] [No. of Type2/HAR] ... [No. of Sequences] [No. of Types]
#         |        	|                      |                   |         		 |	
#  UCO2_Contig1872 	2			     1			 3			 2	
#
##########################################################################################################

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
def getPreType(prelines, typeLen):
	global logf

	pretype = []
	linecount = len(prelines)
	for l in range(linecount):
		if prelines[l] != '\n':
			pretype.append(prelines[l].strip())
	pretype.sort()
	print pretype
	return pretype

def getType(flines, typeLen):

	type = []
	linecount = len(flines)
	for l in range(linecount):
		# check for empty lines and incorrect field numbers
		if flines[l] != '\n' and flines[l].count('\t')==2:
			flines[l].rstrip()	
			fields = flines[l].split('\t')
			contigs = fields[2].split('|')
			for c in contigs:
				atype = c[0:typeLen]
				if not(atype in type):
					type.append(atype)
	type.sort()
	print type
	return type

def compareType(pretype, type, opt):
	global logf

	undefinedtype=[x for x in pretype if x not in type]
	if(len(undefinedtype)!=0):
		logf.write("Prefix not found in contig file:\n" + "\t".join(undefinedtype)+"\n")

	if(opt == 1): # strict search
		curtype=[x for x in pretype if x in type]
	else:
		curtype=type
	print curtype
	return curtype

	
def countType(flines, curtype, type, typeLen):
	global outf
	global logf
	global logcount
	global linecount

	notinlist=[x for x in type if x not in curtype]
	if(len(notinlist) != 0):
		outf.write("Contig ID\t" + "\t".join(curtype)+ "\tOther\tTotal Seq\tNo. of Diff Prefix\n")
	else:
		outf.write("Contig ID\t" + "\t".join(curtype)+ "\tTotal Seq\tNo. of Diff Prefix\n")

	for l in range(linecount):

		# check for empty lines and incorrect field numbers
		if flines[l] != '\n' and flines[l].count('\t')==2:
			flines[l].rstrip() 
			fields = flines[l].split('\t')

			# Check for the consistence between sequence number and sequences string
			if fields[2].count('|') == int(fields[1])-1:
				contigs = fields[2].split('|')
				prefix = [x[0:typeLen] for x in contigs]
				countcur = [str(prefix.count(y)) for y in curtype]
				countother = [str(prefix.count(z)) for z in type if z not in curtype]
				countall = [y for y in countcur+countother if y != '0']
				if(len(notinlist) !=0):
					other = "\t"+str(sum([prefix.count(z) for z in type if z not in curtype]))+"\t"
				else:
					other = "\t"
				outf.write(fields[0]+"\t"+"\t".join(countcur)+other+fields[1]+"\t"+str(len(countall))+"\n")
			else:
				logf.write("Warning: Skip line #%s due to inconsistent sequence numbers.\n\t%s\n" %(l+1,flines[l]))
		else:
			logcount += 1
			logf.write("Warning: Skip line #%s due to empty or wrong format.\n" %(l+1))

#----------------------------- main ------------------------------------------------------
# ---------- get input file name and construct output file name and open files -----

# ---------- Read from contig file -----
s = raw_input("Enter the CONTIG file name: ")	
if s != "":
	ifile = s
else:
	print 'Empty input file name!'
	raw_input("\n\nPress the enter key to exit.")
	sys.exit(0)
inf=open_file(ifile,'r')

lens = raw_input("Enter the Length of Contig Prefix(Default: 3): ")
if lens != "":
	typeLen = int(lens)
else:
	typeLen = 3

try:
	flines = inf.readlines()
except:
	print 'Failed to read from: ', ifile
	sys.exit(1)

type=getType(flines,typeLen)
curtype=type

# ---------- Read from prefix file -----
t = raw_input("Enter the CONTIG PREFIX LIST file name(Hit Enter if no prefix file): ")	
if t != "":
	tfile = t
	pref=open_file(tfile,'r')
	try:
		prelines = pref.readlines()
	except:
		print 'Failed to read from: ', prefile
		sys.exit(1)

	pretype=getPreType(prelines, type)
	pref.close()
	print "Enter the search option of prefix: \n"
	print "1. Ignore the prefix which does not in the config file.\n"
	print "2. Search all the prefixes in the prefix file.\n"
	opt = raw_input("Your Choice(Deault: 1): ")
	if  opt != "":
		opt = int(opt)
	else:
		opt = 1
	curtype=compareType(pretype, type, opt)

ofile=ifile+'.out'
lfile=ifile+'.log'

outf=open_file(ofile,'w')
logf = open_file(lfile,'w')
 
# ---------- Loop through all the lines in the file -----
linecount = len(flines)
logcount=0
countType(flines, curtype, type, typeLen) 

# ---------- Print messages for user to find output -----
print 'Done... Total %s lines, skip %s lines' %(linecount,logcount)
print 'Please find output in file "%s", error messages in file "%s"' %(ofile,lfile)

inf.close()
outf.close()
logf.close()

