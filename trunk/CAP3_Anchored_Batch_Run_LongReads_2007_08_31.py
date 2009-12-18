#/usr/bin/python

####################################################
#
# Author: Brian	Chan (birdchan@ucdavis.edu)
# Supervisor : Alex Kozik (akozik@atgc.org)
#
####################################################

####################################################
# importing the	libraries

import sys
import os
from string import *
from string import atof
from math import log10
from string import strip
from string import split

####################################################
# global 

fp_ESTs	= 0
fp_QLTs = 0
fp_info	= 0
filename_out_fasta = "x-out.fasta.temp"       # temp fasta file for each contig
filename_out_qualt = "x-out.fasta.temp.qual"  # temp quality file for each contig
finalCAP3File = "x-out.BIG.cap3"
finalContigFile = "x-out.BIG.contig"
finalClipFile = "x-out.BIG.clipInfo"
finalSingletFile = "x-out.BIG.singlet"
errorLogFile = "x-out.error.log"
CAP3TempFile = filename_out_fasta + ".cap.out"

####################################################
# obj

class contig_info_bank_class:

	def __init__(self):
		self.seqSet = {}     # set of sequences
		self.qltSet = {}     # set of qualities
		self.contigInfoSet = {}    # contig info set
	def storeSeqInfo(self, sn, sb):
		if self.seqSet.has_key(sn):
			print sn + " has already been read !!!\n"
		else:
			self.seqSet[sn] = sb
	def storeQltInfo(self, sn, sb):
		if self.qltSet.has_key(sn):
			print sn + " has already been read !!!\n"
		else:
			self.qltSet[sn] = sb
	# def storeContigInfo(self, contigName, seqName, numOfSeq):
	def storeContigInfo(self, contigName, seqName):
		if self.contigInfoSet.has_key(contigName):
			self.contigInfoSet[contigName].append(seqName)
		else:
			self.contigInfoSet[contigName] = []
			self.contigInfoSet[contigName].append(seqName)
	def printSeqAll(self):    # print out the seqs
		self.seqSet
	def printContigInfoAll(self):    # print out the contig info
		print self.contigInfoSet
	def outputSeqsToCAP3File(self, contigName):
		mySeqSet = self.contigInfoSet[contigName]
		global filename_out_fasta
		global filename_out_qualt
		fp_out_fasta = open(filename_out_fasta, "wb")
		fp_out_qualt = open(filename_out_qualt, "wb")
		for i in range(len(mySeqSet)):
			seqName = mySeqSet[i]
			seqBody = self.seqSet[seqName]
			qltBody = self.qltSet[seqName]
			s = ">" + seqName + "\n" + seqBody + "\n"
			q = ">" + seqName + "\n" + qltBody + "\n"
			fp_out_fasta.write(s)
			fp_out_qualt.write(q)
		fp_out_fasta.close()
		fp_out_qualt.close()
	def outputInfoToClipFile(self):
		global filename_out_fasta
		global finalClipFile
		clipFilename = filename_out_fasta + ".cap.info"
		os.system("cat " + clipFilename + " >> " + finalClipFile)
	def outputInfoToSingletFile(self):
		global filename_out_fasta
		global finalSingletFile
		singletFilename = filename_out_fasta + ".cap.singlets"
		os.system("cat " + singletFilename + " >> " + finalSingletFile)
	def runCAP3onEachContig(self):
		global filename_out_fasta
		global CAP3TempFile
		for contigName in self.contigInfoSet:
			self.outputSeqsToCAP3File(contigName)
			print "\n============================"
			print "Executing CAP3..."
			# os.system("../bin/cap3 " + filename_out_fasta + " > " + CAP3TempFile)
			#################################################################################
			###          CAP3   EXECUTION                                                 ###
			os.system("../bin/cap3 " + filename_out_fasta + " -o 80 -p 90 > " + CAP3TempFile)
			#################################################################################
			print "Done with CAP3 on the contig " + contigName
			self.restoreContigIDsForBigContig(contigName)
			self.restoreContigIDsForBigCAP3(contigName)
			self.outputInfoToClipFile()
			self.outputInfoToSingletFile()
	def restoreContigIDsForBigCAP3(self, contigName):
		global CAP3TempFile
		global finalCAP3File
		# constructing something like the following
		# cat cap3Temp | sed 's/Contig 1/QGA12345/' >> BIG.cap3
		#os.system("cat " + CAP3TempFile + " | sed 's/Contig 1/" + contigName + "/' >> " + finalCAP3File)
		# output contig to the final CAP3 file with original contigName
		fp_finalCAP3File = open(finalCAP3File, "a+")
		fp_tempCAP3File = open(CAP3TempFile, "r")
		lines = fp_tempCAP3File.readlines()
		fp_tempCAP3File.close()
		for i in range( len(lines) ):
			line = lines[i]
			list_line = line.split()
			if len(list_line) == 4 and list_line[1] == "Contig":
				contigNum = int( list_line[2] )
				print line
				print "Contig " + str( contigNum )
				if contigNum == 1:
					# line = line.replace("Contig " + str(contigNum), contigName)
					line = line.replace("Contig " + str(contigNum), contigName + "_" + str(contigNum) )
					# print "replaced"
					print_message = "renamed " + `contigNum`
					print print_message
				else:
					# line = line.replace("Contig " + str(contigNum), contigName + "_" + str(contigNum-1) )
					line = line.replace("Contig " + str(contigNum), contigName + "_" + str(contigNum) )
					# print "replaced 2"
					print_message = "renamed " + `contigNum`
					print print_message
			fp_finalCAP3File.write(line)
		fp_finalCAP3File.close()

	def restoreContigIDsForBigContig(self, contigName):
		# count how many contig(s) we get back from CAP3
		global filename_out_fasta
		global finalSingletFile
		filename_fasta_contig = filename_out_fasta + ".cap.contigs"
		fp_fasta_contig = open(filename_fasta_contig, "rb")
		lines = fp_fasta_contig.readlines()	  # read all input lines
		fp_fasta_contig.close()
		if not lines:      # all are singlets
			os.system("cat " + filename_out_fasta + ".cap.singlets >> " + finalSingletFile)
			print "all singlets... saved to error log file"
			list_singlets = os.popen("grep \"^>\" " + filename_out_fasta + ".cap.singlets", "r").readlines()
			# append each to the error log file
			fp_error = open(errorLogFile, "a+")
			for s in list_singlets:
				seqName = s[1:]
				seqName = strip(seqName)
				fp_error.write(seqName + " not assembled in contig " + contigName + "\n")
			fp_error.close()
			return
		end_index = len(lines)
		i = 0  # the line index, starting from the top
		count = 0  # num of contig(s)
		contigBody = ""
		contigBodySet = []
		while i<len(lines):        # keep reading the lines
			line = getLine(lines, i)
			if find(line, ">") == 0:   # if it's a contig name
				count = count + 1
				if contigBody != "":
					contigBodySet.append(contigBody)
				contigBody = ""
			else:
				contigBody = contigBody + line
			i = i+1
		contigBodySet.append(contigBody)

		# output contig info to the final collection with original contigName
		global finalContigFile
		fp_finalContigFile = open(finalContigFile, "a+")
		for i in range(count):
			if i == 0:
				# contigName_str = contigName
				contigName_str = contigName + "_" + str(i+1)
			else:
				# contigName_str = contigName + "_" + str(i)
				contigName_str = contigName + "_" + str(i+1)
			s = ">" + contigName_str + "\n" + contigBodySet[i] + "\n"
			fp_finalContigFile.write(s)


		fp_finalContigFile.close()


####################################################
# functions

def main_routine():

	# init the contig info bank
	contig_info_bank = contig_info_bank_class()
	read_ESTs_file(contig_info_bank)
	read_QLTs_file(contig_info_bank)
	read_info_file(contig_info_bank)
	contig_info_bank.runCAP3onEachContig()

def read_info_file(contig_info_bank):

	global fp_info
	lines = fp_info.readlines()	  # read all input lines
	if not lines:
		print "No input	in the info file"
		sys.exit(0)  # if no input, exit
	end_index = len(lines)
	i = 0  # the line index, starting from the top

	while i<len(lines):        # keep reading the lines
		line = getLine(lines, i)
		current_list = line.split('\t')
		# seqName = current_list[1]
		# contigName = current_list[0]
		seqName = current_list[0]
		contigName = current_list[1]
		# seqName, tagN, contigName, numOfSeq = split(line)
		# contig_info_bank.storeContigInfo(contigName, seqName, numOfSeq)
		contig_info_bank.storeContigInfo(contigName, seqName)
		i = i+1

	contig_info_bank.printContigInfoAll()

def read_ESTs_file(contig_info_bank):

	global fp_ESTs
	lines = fp_ESTs.readlines()	  # read all input lines
	if not lines:
		print "No input	in the EST file"
		sys.exit(0)  # if no input, exit
	end_index = len(lines)
	i = 0  # the line index, starting from the top

	while i<len(lines):        # keep reading the lines
		line = getLine(lines, i)
		seqName, seqLength, seqBody = split(line)
		contig_info_bank.storeSeqInfo(seqName, seqBody)
		i = i+1

def read_QLTs_file(contig_info_bank):

	global fp_QLTs
	lines = fp_QLTs.readlines()
	if not lines:
		print "No input in the EST file"
		sys.exit(0)  # if no input, exit
	end_index = len(lines)
	i = 0  # the line index, starting from the top
	while i<len(lines):
		line = getLine(lines, i)
		seqName, qltBody = split(line,"\t")
		contig_info_bank.storeQltInfo(seqName, qltBody)
		i = i+1

def getLine(lines, index):
	line = lines[index]
	line = line[0:len(line)-1]   # rid of \n
	return line

####################################################
# main

s = raw_input("Please input the EST filename: ")
#filename_in_ESTs = "Test_ESTs.input1"
filename_in_ESTs = s
filename_in_QLTs = filename_in_ESTs + ".qual"

s = raw_input("Please input the info filename: ")
#filename_in_info = "Test_Info.input2"
filename_in_info = s

# get file handlers
fp_ESTs	= open(filename_in_ESTs, "rb")
fp_QLTs = open(filename_in_QLTs, "rb")
fp_info	= open(filename_in_info, "rb")

# make directory for the hmmer files
"""
if not os.path.exists(pfam_seqs_dirname):
	os.mkdir(pfam_seqs_dirname)
"""

main_routine()

fp_ESTs.close()
fp_info.close()

