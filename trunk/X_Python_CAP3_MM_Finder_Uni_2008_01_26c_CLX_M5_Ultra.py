#!/usr/bin/python
###########################################
# Author: Brian Chan (birdchan@ucdavis.edu)
# Supervisor: Alexander Kozik (akozik@atgc.org)
# Date: February 27 2004
# Modified by A.Kozik March 2007
# Description:
#
# This script finds mismatches in the CAP3 alignments
#
# Notation: [something]* means "something" can appear
#    many times. {something}* means the same.
#
# =========================================
#
# Input file format:
#
#    {
#               .    :    .    :    .    :
#     seq1      XAAAAAAAAT-TTTTGTTTT-TTTTT
#     seq2      AAAAA-AAATTTTTTTTTTT-TTTTT
#               --------------------------
#     Contig_1  NAAAAAAAAT-TTTTGTTTT-TTTTT
#    }*
#
# =========================================
#
# Mismatches are defined as follows:
#
#    This is an exception, not a mismatch
#      if seq[i] == "X" and contig[i] == "N"
#      For example, at position 1
#
#    This is a deletion
#      if contig[i] != "-" and seq[i] == "-"
#      For example, at position 6
#
#    This is an insertion
#      if contig[i] == "-" and seq[i] != "-"
#      For example, at position 11
#
#    This is a substitution
#      if contig[i] != "-" and seq[i] != "-" and contig[i] != seq[i]
#      For example, at position 16
#
# ==========================================
#
# Output file format:
#
#    {Contig_i  seqName   MM_info}*
#
# MM_info is defined as follows:
#    "no polymorphism found" | [index:[D|I|S]]*
#
# For the sample input file, the output would be
#    Contig1  seq1   no polymorphism found
#    Contig1  seq2   6:D|11:I|16:S
#
#
############################################

import sys
import string
from string import *
from string import rstrip
import re

############################################
# global
seqNameMaxLength = 22

############################################

class seqClass:

	def __init__(self, name):
		self.name = name
		self.seq = ""
	def setSeq(self, subSeq):
		self.seq = subSeq
	def getName(self):
		return self.name
	def getSeq(self):
		return self.seq
	def charAt(self, pos):
		if len(self.seq) > pos:
			return self.seq[pos]
		else:
			return " "    # the genes on the right should be " "
	def print_info(self):
		str = ""
		str = self.name
		num_sp = len(self.name)
		for i in range( seqNameMaxLength-num_sp ):
			str = str + " "
		str = str + self.seq + "\n"
		print str
	def output_info(self):
		output_string(self.name)
		num_sp = len(self.name)
		for i in range( seqNameMaxLength-num_sp ):
			output_string(" ")
		output_string(self.seq + "\n")

#------------------------------

class seqInfo:

	def __init__(self):
		self.seqName = ""
		self.infoStr = ""
	def setSeqName(self, seqName):
		self.seqName = seqName
	def appendInfoStr(self, info):
		if len(self.infoStr) != 0:   # have sth
			self.infoStr = self.infoStr + "|" + info
		else:                        # have nothing
			self.infoStr = info
	def getInfoStr(self):
		if len( self.infoStr ) != 0:
			return self.infoStr
		else:
			return "no polymorphism found"

#------------------------------

class seqHeapClass:

	def __init__(self):
		self.seqList = []
		self.seqNum = 0
		self.contig_ID = ""
	def set_contig_ID(self, line):
		contig_str, white_spaces = split(line)
		self.contig_ID = contig_str
	def get_contig_ID(self):
		return self.contig_ID
	def find_seq_index(self, name):
		for i in range(len(self.seqList)):
			if self.seqList[i].getName() == name:
				return i
		return -1
	def readinSeq(self, name, subSeq):
		# insert a new seq
		newSeq = seqClass(name)   # make a new empty seq
		newSeq.setSeq( subSeq.upper() )   # put stuff into it
		self.seqList.append(newSeq)
		self.seqNum = self.seqNum + 1
	def clear(self):
		self.seqList = []
		self.seqNum = 0
	def print_info(self):
		print self.get_contig_ID()
		for l in self.seqList:
			l.print_info()
	def output_info(self):
		subseq_info_list = []     # list of the seq_info objs
		for i in range(self.seqNum):  # initialization
			subSeq_info = seqInfo()
			# subSeq_info.setSeqName( self.seqList[i].getName() )
			subseq_info_list.append( subSeq_info )
		total_len = len( self.seqList[ self.seqNum-1 ].getSeq() )
		contig_index = self.seqNum - 1

		### Alex Kozik 2007 03 21 ###
		ContigID_out2 = self.get_contig_ID()
		fp_out2.write(ContigID_out2 + '\t' + " *** CONTIG_INFO_START *** " + '\n')
		FindMM_Status = "FALSE"
		gap_in_contig = "FALSE"
		# Current_Position_out2 = 1
		Current_Position_out2 = 0
		Gap_Adjusted     = 0

		for col in range(total_len):   # from index [0] to the end
			FindMM_Status = "FALSE"
			gap_in_contig = "FALSE"
			col_num = col+1  # bio != CS
			# Current_Position_out2 = 1
			#################### COUNT FOR ALL INDELs AND SNPs 
			All_Count_out2   = 0
			Del_Count_out2   = 0
			Ins_Count_out2   = 0
			Sub_Count_out2   = 0
			#################### COUNT PER GENOTYPE FOR INDELs AND SNPs 
			Type_A_Count     = 0
			Type_B_Count     = 0
			Type_X_Count     = 0
			#################### COUNT FOR ALL LETTERS
			Type_A_Count_All = 0
			Type_B_Count_All = 0
			Type_X_Count_All = 0
			#################### GENOTYPE A
			seq_A_count_A    = 0
			seq_A_count_T    = 0
			seq_A_count_G    = 0
			seq_A_count_C    = 0
			seq_A_count_N    = 0
			seq_A_count_d    = 0
			#################### GENOTYPE B
			seq_B_count_A    = 0
			seq_B_count_T    = 0
			seq_B_count_G    = 0
			seq_B_count_C    = 0
			seq_B_count_N    = 0
			seq_B_count_d    = 0
			####################  ANY GENOTYPE 
			seq_X_count_A    = 0
			seq_X_count_T    = 0
			seq_X_count_G    = 0
			seq_X_count_C    = 0
			seq_X_count_N    = 0
			seq_X_count_d    = 0
			all_cons_mm_count = 0
			####################
			# Gap_Adjusted     = 0
			# Num_of_Seqs      = self.seqNum
			Num_of_Seqs_in_Align = 0
			for row in range( self.seqNum - 1 ):   # for each seq
				current_seq_id = self.seqList[row].getName()
				# print current_seq_id
				# seq_genotype = get_genotype_3LC(current_seq_id)
				seq_genotype = get_genotype_9LC_lact(current_seq_id)
				#        CALL FOR FIND GENOTYPE FUNCTION     ###
				# BINARY SYSTEM - ONLY TWO GENOTYPES ALLOWED ###
				# MODIFY FOR YOUR PARTICULAR SYSTEM OF PREFIXES
				# seq_genotype = get_genotype_9LC_cich(current_seq_id)
				# print seq_genotype
				con_ch = self.seqList[contig_index].charAt(col)
				seq_ch = self.seqList[row].charAt(col)
				# all_cons_mm_count = 0
				# seq_ch == " " ? skip, coz not in range
				if seq_ch == " ":
					continue
				# if seq_ch == "X" and contig_ch == "N", not MM
				if seq_ch == "X" and con_ch == "N":
					continue
				if seq_ch != " ":
					Num_of_Seqs_in_Align = Num_of_Seqs_in_Align + 1
					if seq_genotype == "_A_":
						Type_A_Count_All = Type_A_Count_All + 1
					if seq_genotype == "_B_":
						Type_B_Count_All = Type_B_Count_All + 1
					# if seq_genotype != "_A_" or seq_genotype != "_B_":
					if seq_genotype != "_A_" and seq_genotype != "_B_":
						Type_X_Count_All = Type_X_Count_All + 1
					# if seq_ch != con_ch:
					#	all_cons_mm_count = all_cons_mm_count + 1
				if con_ch == "-" and row == 0:
					gap_in_contig = "TRUE"
					Gap_Adjusted = Gap_Adjusted + 1
				# deletion
				if con_ch != "-" and seq_ch == "-":
					all_cons_mm_count = all_cons_mm_count + 1
					num = "%d" % col_num
					subseq_info_list[row].appendInfoStr(num+":D")
					FindMM_Status = "TRUE"
					Del_Count_out2 = Del_Count_out2 + 1
					All_Count_out2 = All_Count_out2 + 1
					if seq_genotype == "_A_":
						Type_A_Count = Type_A_Count + 1
					if seq_genotype == "_B_":
						Type_B_Count = Type_B_Count + 1
					if seq_genotype != "_A_" or seq_genotype != "_B_":
						Type_X_Count = Type_X_Count + 1
				# insertion
				if con_ch == "-" and seq_ch != "-":
					all_cons_mm_count = all_cons_mm_count + 1
					num = "%d" % col_num
					subseq_info_list[row].appendInfoStr(num+":I")
					FindMM_Status = "TRUE"
					Ins_Count_out2 = Ins_Count_out2 + 1
					All_Count_out2 = All_Count_out2 + 1
					if seq_genotype == "_A_":
						Type_A_Count = Type_A_Count + 1
					if seq_genotype == "_B_":
						Type_B_Count = Type_B_Count + 1
					if seq_genotype != "_A_" or seq_genotype != "_B_":
						Type_X_Count = Type_X_Count + 1
				# substitution
				if con_ch != "-" and seq_ch != "-" and con_ch != seq_ch:
					all_cons_mm_count = all_cons_mm_count + 1
					num = "%d" % col_num
					subseq_info_list[row].appendInfoStr(num+":S")
					FindMM_Status = "TRUE"
					Sub_Count_out2 = Sub_Count_out2 + 1
					All_Count_out2 = All_Count_out2 + 1
					if seq_genotype == "_A_":
						Type_A_Count = Type_A_Count + 1
					if seq_genotype == "_B_":
						Type_B_Count = Type_B_Count + 1
					if seq_genotype != "_A_" or seq_genotype != "_B_":
						Type_X_Count = Type_X_Count + 1
				###########################################
				###   GENOTYPE _A_   ###
				if seq_ch == "A" and seq_genotype == "_A_":
					seq_A_count_A = seq_A_count_A + 1
				if seq_ch == "T" and seq_genotype == "_A_":
                                        seq_A_count_T = seq_A_count_T + 1
				if seq_ch == "G" and seq_genotype == "_A_":
                                        seq_A_count_G = seq_A_count_G + 1
				if seq_ch == "C" and seq_genotype == "_A_":
                                        seq_A_count_C = seq_A_count_C + 1
				if seq_ch == "N" and seq_genotype == "_A_":
                                        seq_A_count_N = seq_A_count_N + 1
				if seq_ch == "-" and seq_genotype == "_A_":
                                        seq_A_count_d = seq_A_count_d + 1
				###   GENOTYPE _B_   ###
				if seq_ch == "A" and seq_genotype == "_B_":
                                        seq_B_count_A = seq_B_count_A + 1
                                if seq_ch == "T" and seq_genotype == "_B_":
                                        seq_B_count_T = seq_B_count_T + 1
                                if seq_ch == "G" and seq_genotype == "_B_":
                                        seq_B_count_G = seq_B_count_G + 1
                                if seq_ch == "C" and seq_genotype == "_B_":
                                        seq_B_count_C = seq_B_count_C + 1
                                if seq_ch == "N" and seq_genotype == "_B_":
                                        seq_B_count_N = seq_B_count_N + 1
				if seq_ch == "-" and seq_genotype == "_B_":
                                        seq_B_count_d = seq_B_count_d + 1
				###    ANY GENOTYPE  ###
				if seq_ch == "A":
                                        seq_X_count_A = seq_X_count_A + 1
                                if seq_ch == "T":
                                        seq_X_count_T = seq_X_count_T + 1
                                if seq_ch == "G":
                                        seq_X_count_G = seq_X_count_G + 1
                                if seq_ch == "C":
                                        seq_X_count_C = seq_X_count_C + 1
                                if seq_ch == "N":
                                        seq_X_count_N = seq_X_count_N + 1
                                if seq_ch == "-":
                                        seq_X_count_d = seq_X_count_d + 1
				###########################################
			Current_Position_out2 = Current_Position_out2 + 1

		### Alex Kozik 2007 03 21 ###
			if gap_in_contig == "TRUE":
				fp_out4.write(ContigID_out2 + '\tGAP_POS: ' + `Current_Position_out2` + '\n')

			if FindMM_Status == "TRUE":
				Poly_Status = " - * * * - "
				Sequence_End_Warning = " DEEP_ENOUGH "
				if Current_Position_out2 <= 60 or Current_Position_out2 >= (total_len-60):
					Sequence_End_Warning = " CLOSE_TO_EDGE " 
				MM_Fraction = ((All_Count_out2*1.00)/Num_of_Seqs_in_Align)
				MM_Fraction_str = str(round(MM_Fraction,2))
				genotype_ratio_class = "_NN_"

				Poly_Status = GetPolyClass(Num_of_Seqs_in_Align,All_Count_out2,Type_A_Count_All,Type_B_Count_All,Type_A_Count,Type_B_Count)

				if (Type_A_Count_All - Type_A_Count) == 0 and Type_A_Count != 0:
					genotype_ratio_class = "_AA_"
				if (Type_B_Count_All - Type_B_Count) == 0 and Type_B_Count != 0:
					genotype_ratio_class = "_BB_"
				if Type_A_Count != 0 and Type_B_Count != 0:
					genotype_ratio_class = "_AB_"
				if Type_A_Count_All == 0:
					genotype_ratio_class = "__B_"
				if Type_B_Count_All == 0:
					genotype_ratio_class = "_A__"

				### WRITE DATA TO FILEs ###
				### DATA FOR ALL GENOTYPES ###
				fp_out5.write(ContigID_out2 + '\t' + `Current_Position_out2` + '\t' \
					+ `seq_X_count_A` + ':' + `seq_X_count_T` + ':' \
					+ `seq_X_count_G` + ':' + `seq_X_count_C` + ':' \
					+ `seq_X_count_N` + ':' + `seq_X_count_d` + '\t' \
					+ `Num_of_Seqs_in_Align` + '\t' + con_ch + '\n')

				### DECEMBER 2007 12
				# poly_x_status = "GOOD"

				all_mm_list = [seq_X_count_A, seq_X_count_T, seq_X_count_G, seq_X_count_C, seq_X_count_N, seq_X_count_d]
				all_mm_list.sort()
				second_largest_mm = all_mm_list[4]
				second_largest_fr = (second_largest_mm*1.0)/Num_of_Seqs_in_Align
				second_largest_fr_string = str(round(second_largest_fr,2))

				second_largest_fr_status = "*****"
				if second_largest_fr >= 0.25:
					second_largest_fr_status = "**+**"

				if second_largest_fr >= 0.30:
					second_largest_fr_status = "*+*+*"

				if second_largest_fr >= 0.40:
					second_largest_fr_status = "*+++*"

				second_largest_status = "-------"

				if second_largest_mm >= 3:
					second_largest_status = "-+-+-+-"
				if second_largest_mm >= 4:
					second_largest_status = "+-+-+-+"
				if second_largest_mm >= 5:
					second_largest_status = "+-+++-+"
				if second_largest_mm >= 6:
					second_largest_status = "+++-+++"
				if second_largest_mm >= 7:
					second_largest_status = "+++++++"

				all_cons_mm_count_fr = (all_cons_mm_count*1.0)/Num_of_Seqs_in_Align
				all_cons_mm_count_fr_string = str(round(all_cons_mm_count_fr,2))

				all_cons_mm_count_fr_status = "====="

				if all_cons_mm_count_fr >= 0.25:
					all_cons_mm_count_fr_status = "==X=="
				if all_cons_mm_count_fr >= 0.50:
					all_cons_mm_count_fr_status = "=X=X="
				if all_cons_mm_count_fr >= 0.75:
					all_cons_mm_count_fr_status = "=XXX="

				Num_of_Seqs_in_Align_status = "  -  "
				if Num_of_Seqs_in_Align >=  8:
					Num_of_Seqs_in_Align_status = "  +  "
				if Num_of_Seqs_in_Align >= 10:
					Num_of_Seqs_in_Align_status = " + + "

				### DECEMBER 2007 12 - it was a bug in poly_x STATUS
				# if seq_X_count_A == 1 or seq_X_count_T == 1 or seq_X_count_G == 1 or seq_X_count_C == 1 or seq_X_count_N == 1 or seq_X_count_d == 1:
				#	poly_x_status = "NOT GOOD"
				poly_x_status = "NOT GOOD"
				if all_cons_mm_count >= 2 and Num_of_Seqs_in_Align >=4:
					poly_x_status = "GOOD"

				# print poly_x_status

				if poly_x_status == "GOOD":
					fp_out6.write(ContigID_out2 + '\t' + `Current_Position_out2` + '\t' \
						+ `seq_X_count_A` + ':' + `seq_X_count_T` + ':' \
						+ `seq_X_count_G` + ':' + `seq_X_count_C` + ':' \
						+ `seq_X_count_N` + ':' + `seq_X_count_d` + '\t' \
						+ `Num_of_Seqs_in_Align` + '\t' + con_ch + '\t' \
						+ second_largest_status + '\t' + `second_largest_mm` + '\t' \
						+ second_largest_fr_status + '\t' + second_largest_fr_string + '\t' \
						+ all_cons_mm_count_fr_status + '\t' + all_cons_mm_count_fr_string + '\t' \
						+ Num_of_Seqs_in_Align_status + '\t' + `all_cons_mm_count` + '\n')

				### DATA FOR BINARY SYSTEM - TWO GENOTYPES ONLY ###
				if Type_X_Count_All == 0:
					fp_out2.write(ContigID_out2 + ' | ALL:' + `All_Count_out2` + ' | DEL:' + `Del_Count_out2` + ' | INS:' \
						+ `Ins_Count_out2` + ' | SUB:' + `Sub_Count_out2` + ' | POS:' + `Current_Position_out2` \
						+ ' | ALN:' + `Num_of_Seqs_in_Align` + ' | FRC:' + MM_Fraction_str + ' | ' \
						+ Poly_Status + ' | ' + Sequence_End_Warning \
						+ ' | ' + genotype_ratio_class + ' | GT_A:' + `Type_A_Count_All` \
						+ ' | GT_B:' + `Type_B_Count_All` + ' | A/B:' \
						+ `Type_A_Count` + '/' + `Type_B_Count` + ' | GAP_ADJ:' + `Gap_Adjusted` \
						+ ' | [A]_ATGCN:' + `seq_A_count_A` + ':' + `seq_A_count_T` + ':' \
						+ `seq_A_count_G` + ':' + `seq_A_count_C` + ':' + `seq_A_count_N` + ':' + `seq_A_count_d` \
						+ ' | [B]_ATGCN:' + `seq_B_count_A` + ':' + `seq_B_count_T` + ':' \
                                                + `seq_B_count_G` + ':' + `seq_B_count_C` + ':' + `seq_B_count_N` \
						+ ':' + `seq_B_count_d` + ' | CONS:' + con_ch + '\n')
					fp_out3.write(ContigID_out2 + '\t' + `All_Count_out2` + '\t' + `Del_Count_out2` + '\t' \
						+ `Ins_Count_out2` + '\t' + `Sub_Count_out2` + '\t' + `Current_Position_out2` \
						+ '\t' + `Num_of_Seqs_in_Align` + '\t' + MM_Fraction_str + '\t' \
						+ Poly_Status + '\t' + Sequence_End_Warning \
						+ '\t' + genotype_ratio_class + '\t' + `Type_A_Count_All` \
						+ '\t' + `Type_B_Count_All` + '\t' \
						+ `Type_A_Count` + '\t' + `Type_B_Count` + '\t' + `Gap_Adjusted` + '\t' \
						+ `seq_A_count_A` + ':' + `seq_A_count_T` + ':' \
                                                + `seq_A_count_G` + ':' + `seq_A_count_C` + ':' + `seq_A_count_N` + ':' + `seq_A_count_d` \
                                                + '\t' + `seq_B_count_A` + ':' + `seq_B_count_T` + ':' \
                                                + `seq_B_count_G` + ':' + `seq_B_count_C` + ':' + `seq_B_count_N` \
                                                + ':' + `seq_B_count_d` + '\t' + con_ch + '\n')

			real_adj_position = Current_Position_out2-Gap_Adjusted
			fp_out7.write(ContigID_out2 + '\t' + `Current_Position_out2` + '\t' \
					+ '[' + `Gap_Adjusted` + ']' + '\t' + `real_adj_position` + '\t' \
					+ `seq_X_count_A` + ':' + `seq_X_count_T` + ':' \
					+ `seq_X_count_G` + ':' + `seq_X_count_C` + ':' \
					+ `seq_X_count_N` + ':' + `seq_X_count_d` + '\t' \
					+ `Num_of_Seqs_in_Align` + '\t' + con_ch + '\t' + `all_cons_mm_count` \
					+ '\t' + '***' + '\t' + `Type_A_Count_All` + ' | ' + `Type_B_Count_All` + '\n')

		# output info to output file
		for i in range( self.seqNum-1 ):
			""" # this debugging part prints out len( consensus_line )
			n = len( self.seqList[contig_index].getSeq() )
			s = "%d" % n
			output_string( s + "\t" )
			"""
			output_string( self.get_contig_ID() + "\t" )
			output_string( self.seqList[i].getName() + "\t" )
			output_string( subseq_info_list[i].getInfoStr() + "\n" )

		### Alex Kozik 2007 03 21 ###
		fp_out2.write(ContigID_out2 + '\t' + " *** CONTIG_INFO_END *** " + '\n')

############################################
# global

debug_01 = 1       # print out line info

fp_in = 0          # file pointer for input
fp_out = 0         # file pointer for output

seqHeap = seqHeapClass()  # the obj that stores everything within a contig

############################################

def check_contigs_info():
	global fp_in
	lines = fp_in.readlines()
	if not lines:
		print "No input in the input file"
		sys.exit(0)   # if no input, exit
	i = 0  # the line index, starting from the top

	# jump to the next contig section
	i = line_num_string(lines, i, ".    :")
	next_contig_index = line_num_string(lines, i+1, ".    :")

	while i < len(lines)-1:

		global seqRow
		global seqHeap
		seqRow = 0
		seqHeap.clear()

		while i <= next_contig_index:
			line = get_line(lines, i)
			if is_seq_data_line(line) == 1:
				if debug_01 == 1:
					print "line ", i, " is a seq_data_line"
				do_seq_data(line)
			elif is_consensus_line(line) == 1:
				if debug_01 == 1:
					print "line ", i, " is a consensus_line"
				do_consensus(line)
			elif is_blank_line(line) == 1:
				if debug_01 == 1:
					print "line ", i, " is a blank line"
			i = i + 1   # go to the next line

		# show what we got
		#seqHeap.print_info()

		# output data into output file
		seqHeap.output_info()

		# jump to the next contig section
		i = line_num_string(lines, i-1, ".    :")
		next_contig_index = line_num_string(lines, i+1, ".    :")


# -----------------------------------------

def GetPolyClass(Num_of_Seqs_in_Align,All_Count_out2,Type_A_Count_All,Type_B_Count_All,Type_A_Count,Type_B_Count):

	got_status = "FALSE"

	Poly_Status = " - ** - "

	# if Num_of_Seqs_in_Align <= 3 and Type_A_Count_All !=0 and Type_B_Count_All != 0:
	if Num_of_Seqs_in_Align >= 2 and (Type_A_Count_All - Type_A_Count) == 0 and Type_A_Count >= 1:
		Poly_Status = " _WEAK_ "
		got_status = "TRUE"

	if Num_of_Seqs_in_Align >= 2 and (Type_B_Count_All - Type_B_Count) == 0 and Type_B_Count >= 1:
                Poly_Status = " _WEAK_ "
                got_status = "TRUE"

	if Num_of_Seqs_in_Align >= 4 and (Type_A_Count_All - Type_A_Count) == 0 and Type_A_Count >= 2:
		Poly_Status = " MEDIUM "
		got_status = "TRUE"

	if Num_of_Seqs_in_Align >= 4 and (Type_B_Count_All - Type_B_Count) == 0 and Type_B_Count >= 2:
		Poly_Status = " MEDIUM "
		got_status = "TRUE"

        if Num_of_Seqs_in_Align >= 6 and (Type_A_Count_All - Type_A_Count) == 0 and Type_A_Count >= 3 :
                Poly_Status = " STRONG "
		got_status = "TRUE"

        if Num_of_Seqs_in_Align >= 6 and (Type_B_Count_All - Type_B_Count) == 0 and Type_B_Count >= 3 :
                Poly_Status = " STRONG "
		got_status = "TRUE"

	if Num_of_Seqs_in_Align >= 8 and (Type_A_Count_All - Type_A_Count) == 0 and Type_A_Count >= 4 :
                Poly_Status = " _DREAM_ "
		got_status = "TRUE"

        if Num_of_Seqs_in_Align >= 8 and (Type_B_Count_All - Type_B_Count) == 0 and Type_B_Count >= 4 :
                Poly_Status = " _DREAM_ "
		got_status = "TRUE"

	###################################################
	# if got_status == "FALSE":
	#	if (Type_A_Count_All - Type_A_Count) != 0 and Type_A_Count != 0:
	#		Poly_Status = "_MIXT_A__"
	#	if (Type_B_Count_All - Type_B_Count) != 0 and Type_B_Count != 0:
        #        	Poly_Status = "_MIXT__B_"
	#	if (Type_A_Count_All - Type_A_Count) != 0 and Type_A_Count and (Type_B_Count_All - Type_B_Count) != 0 and Type_B_Count != 0:
	#		Poly_Status = "_MIXT_AB_"
	###################################################

	return Poly_Status

def get_genotype_3LC(est_sequence_id):
	seq_prefix = est_sequence_id[0:3]
	# print seq_prefix
	seq_genotype = "_X_"
	if seq_prefix == "QGA" or seq_prefix == "QGB" or seq_prefix == "QGC" or seq_prefix == "QGD" or seq_prefix == "QGI" or seq_prefix == "CLS":
		seq_genotype = "_A_"
	if seq_prefix == "QGE" or seq_prefix == "QGF" or seq_prefix == "QGG" or seq_prefix == "QGH" or seq_prefix == "QGJ" or seq_prefix == "CLR":
		seq_genotype = "_B_"
	return seq_genotype

def get_genotype_9LC_lact(est_sequence_id):
	seq_prefix = est_sequence_id[0:3]
	# seq_prefix = est_sequence_id[0:9]
	# print seq_prefix
	seq_genotype = "_X_"
	if seq_prefix == "LST" or seq_prefix == "CLS":
		seq_genotype = "_A_"
	if seq_prefix == "LSR":
		seq_genotype = "_B_"
	return seq_genotype

### GET GENOTYPE FUNCTION ###
### MODIFY ACCORDINGLY TO YOUR CUSTOM SYSTEM OF PREFIXES ###

def get_genotype_9LC_cich(est_sequence_id):
	seq_prefix = est_sequence_id[0:9]
	seq_genotype = "_X_"
	if seq_prefix == "Cich_inty":
		seq_genotype = "_A_"
	if seq_prefix == "Cich_endi":
		seq_genotype = "_B_"
	return seq_genotype

def get_line(lines, index):
	line = lines[index]
	line = rstrip(line)   # get rid of \n
	return line

def line_num_string(lines, index, pattern):   # stop at the matched line
	i = index
	while 1:
		if i >= len(lines):
			return len(lines)-1
		line = get_line(lines, i)
		if find(line, pattern) != -1:
			break
		i = i + 1
	return i

def output_string(str):
	global fp_out
	fp_out.write(str)

def is_x_line(line, x):
	if find(line, x) != -1:
		return 1
	return 0

def is_seq_data_line(line):
	if not is_consensus_line(line) and len(line) > 0 and line[0] != " ":
		return 1
	else:
		return 0

def is_consensus_line(line):
	global consensus_pattern
	# return is_x_line(line, "Contig")
	return is_x_line(line, consensus_pattern)

def is_blank_line(line):
	if len(line) == 0:
		return 1
	return 0

def do_seq_data(line):
	# the seq name and the whole seq
	global seqNameMaxLength
	seqName = line[0:seqNameMaxLength]
	seqName = split(seqName)
	seqName = seqName[0]
	seq = line[seqNameMaxLength:len(line)]
	# store the seq
	global seqHeap
	seqHeap.readinSeq(seqName, seq)

def do_consensus(line):
	# read consensus line
	global seqHeap
	global seqNameMaxLength
	seqName = line[0:seqNameMaxLength]   # the consensus name (contig)
	seqName = split(seqName)
	seqName = seqName[0]
	seq = line[seqNameMaxLength:len(line)]
	seqHeap.readinSeq(seqName, seq)
	seqHeap.set_contig_ID(line)


############################################
# main

# ask for input
# if sys.argv[1] != "":
# input_filename = sys.argv[1]
# else:

s = raw_input("Enter the SOURCE file name: ")
input_filename = s

s = raw_input("Enter the DESTINATION file name: ")
output_filename = s

# checking input
if input_filename == output_filename:
	print "input file is the same as output file"
	sys.exit(0)

global consensus_pattern
s = raw_input("Enter the CONSENSUS_ID pattern: ")
consensus_pattern = s

global fp_out2
global fp_out3
global fp_out4
global fp_out5
global fp_out6
global fp_out7

# open the input and output file
print "read data from the input file", input_filename, "..."
fp_in = open(input_filename, "rb")
fp_out = open(output_filename, "wb")
fp_out2 = open(output_filename + '.bin.stat', "wb")
fp_out3 = open(output_filename + '.bin.mysql', "wb")
fp_out4 = open(output_filename + '.gaps', "wb")
fp_out5 = open(output_filename + '.mm_info.all', "wb")
fp_out6 = open(output_filename + '.mm_info.good', "wb")
fp_out7 = open(output_filename + '.seqs.coverage', "wb")
check_contigs_info()
fp_in.close()
fp_out.close()
fp_out2.close()
fp_out3.close()
fp_out4.close()
fp_out5.close()
fp_out6.close()
fp_out7.close()

