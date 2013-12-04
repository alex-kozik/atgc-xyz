#!/usr/bin/python

######################################################
# AUTHORS:                                           #
#     Lutz Froenicke lutz.fr@gmail.com               #
#     Huaqin Xu xhuaqin@gmail.com                    #
#     Alexander Kozik akozik@gmail.com               #
######################################################

import csv, os, sys
from os.path import basename, splitext

#####################################################
''' 

STANDARD / BASIC / ORIGINAL HAPLO-CALL RULE:
 * see details under genotype_SR function *
This script converts the group counts into group haplotypes with the GroupHaplotyper script.
The haplotyping thresholds are hardcoded in the script and should be edited there at the top of the script.
If the B/A call ratio is between 0.2 and 5, the group is typed as heterozygous;
If it is lower than 0.2 the haplotype is set to A; if it is bigger than 5, the haplotype is set to B.
If the rate of missing data is greater, the 90% the group is typed as missing data.
If the number of het calls is equal or greater than the sum of A calls and B calls, the haplotype is set to heterozygous.

Usage: python  04-GroupHaplotyper.py  chunked-clean-genotype-table.tsv  number-of-samples genotype-call-rule 
e.g:   python  04-GroupHaplotyper.py  genotype-table.tsv  88 SR 

EXPERIMENTAL HAPLO-CALL RULE:
 * see details under genotype_XR function *
CUSTOMIZED TO HANDLE DATA WITH LOW NUMBER OF SNPs PER GROUP/BLOCK

'''

######################################################
#                        SR BEGIN                    #
# B/A ratio between "min" and "max" --> resulting call: heterozygous
# B/A ratio between smaller than or equal to "min" --> resulting call: A
# B/A ratio between bigger than or equal to "max" --> resulting call: B

min_SR = 0.2
max_SR = 5.0

######################################################
#count in cells
def genotype_SR(groupsize, Vcnt, Ccnt, Mcnt, Ucnt):
	Vcnt = float(Vcnt)
	Ccnt = float(Ccnt)
	Mcnt = float(Mcnt)
	Ucnt = float(Ucnt)
	gs = int(groupsize)

	GT = ""
	if Vcnt == Ccnt == 0:
		GT = "-"
	elif Vcnt == 0:
		GT = "A"
	elif Ccnt == 0:
		GT = "B"
	elif min_SR <= Vcnt / Ccnt <= max_SR:    # thresholds for typing as heterozygous
		GT = "U"
	elif Vcnt / Ccnt <  min_SR:
		GT = "A"
	elif Vcnt / Ccnt > max_SR:
		GT = "B"
	if Vcnt < Ucnt and Ccnt < Ucnt:      # previously: "if Vcnt + Ccnt < Ucnt:"  or  "if Vcnt + Ccnt <= Ucnt:"  
		GT = "U"
	if Mcnt > 0.9 * gs:
		GT = "-"
	GTL = [GT]
	return GTL
#                        SR END                      #
######################################################

######################################################
#                        XR BEGIN                    #

# CUTOFF RATIO FOR A-B SCORES #
min_XR =  0.05

#  CUTOFF RATIO FOR U SCORES  #
min_UR = 0.10

# CUTOFF FOR LOW NUMBER OF SCORES #
low__data_cutoff = 25
# med__data_cutoff = 50
# high_data_cutoff = 100

def genotype_XR(groupsize, Vcnt, Ccnt, Mcnt, Ucnt):
	Vcnt = float(Vcnt)
	Ccnt = float(Ccnt)
	Mcnt = float(Mcnt)
	Ucnt = float(Ucnt)
	gs = int(groupsize)

	GT = "X"
	##############################
	### RANGE 1 - BELOW CUTOFF ###
	if gs < low__data_cutoff:
		GT = "?"
		### CASE 0-0-X ###
		if Vcnt == 0 and Ccnt == 0 and Ucnt == 0:
			GT = "-"
		if Vcnt == 0 and Ccnt == 0 and Ucnt >  0:
			GT = "U"
		### CASE A-0-X ###
		if Vcnt == 0 and Ccnt >  0 and Ucnt == 0:
			GT = "A"
		if Vcnt == 0 and Ccnt >  0 and Ucnt >  0:
			GT = "U"
		### CASE 0-B-X ###
		if Vcnt >  0 and Ccnt == 0 and Ucnt == 0:
			GT = "B"
		if Vcnt >  0 and Ccnt == 0 and Ucnt >  0:
			GT = "U"
		### CASE A-B-X ###
		if Vcnt >  0 and Ccnt >  0 and Ucnt == 0:
			GT = "U"
		if Vcnt >  0 and Ccnt >  0 and Ucnt >  0:
			GT = "U"
	##############################
	### RANGE 2 - ABOVE CUTOFF ###
	if gs >= low__data_cutoff:
		GT = "?"
		### CASE 0-0-X ###
		if Vcnt == 0 and Ccnt == 0 and Ucnt == 0:
			GT = "-"
		if Vcnt == 0 and Ccnt == 0 and Ucnt >  0:
			GT = "U"
		### CASE A-0-X ###
		if Vcnt == 0 and Ccnt >  0 and Ucnt == 0:
			GT = "A"
		if Vcnt == 0 and Ccnt >  0 and Ucnt >  0:
			GT = "A"
			if Ucnt/Ccnt > min_UR:
				GT = "U"
		### CASE 0-B-X ###
		if Vcnt >  0 and Ccnt == 0 and Ucnt == 0:
			GT = "B"
		if Vcnt >  0 and Ccnt == 0 and Ucnt >  0:
			GT = "B"
			if Ucnt/Vcnt > min_UR:
				GT = "U"
		### CASE A-B-X WITHOUT U ###
		if Vcnt >  0 and Ccnt >  0 and Ucnt == 0:
			if Vcnt == Ccnt:
				GT = "U"
			if Vcnt < Ccnt:
				GT = "U"
				if Vcnt/Ccnt < min_XR:
					GT = "A"
			if Vcnt > Ccnt:
				GT = "U"
				if Ccnt/Vcnt < min_XR:
					GT = "B"
		### CASE A-B-X  WITH U   ###
		if Vcnt >  0 and Ccnt >  0 and Ucnt >  0:
			if Vcnt == Ccnt:
				GT = "U"
			if Vcnt < Ccnt:
				GT = "U"
				if Vcnt/Ccnt < min_XR:
					GT = "A"
			if Vcnt > Ccnt:
				GT = "U"
				if Ccnt/Vcnt < min_XR:
					GT = "B"
			if Ucnt/(Vcnt+Ccnt) > min_UR:
				GT = "U"
	###############################
	### TOO MANY MISSING SCORES ###
	if Mcnt > 0.9 * gs:
		GT = "-"
	GTL = [GT]
	return GTL
#                        XR END                      #
######################################################

#############
# MAIN BODY #
#############

script_version = "2013_12_03"

if len(sys.argv) != 4:
	print ""
	print " arguments: "
	print " 1 - input file "
	print " 2 - number of samples "
	print " 3 - genotype call rule: SR or XR "
	print "     genotype rule shoud be SR or XR: "
	print "     SR - standard rule "
	print "     XR - experimental / custom rule "
	print ""
	sys.exit()

if len(sys.argv) == 4:
	genotype_rule = sys.argv[3]
	if genotype_rule != "SR" and genotype_rule != "XR":
		print ""
		print " genotype rule shoud be SR or XR: "
		print " SR - standard rule "
		print " XR - experimental / custom rule "
		print ""
		sys.exit()
	infile = sys.argv[1]
	samples = int(sys.argv[2])
	#############################
	# INPUT - OUTPUT FILE NAMES #
	###############################
	infbase = splitext(basename(infile))[0]
	outfile = 'hpt-' + genotype_rule + '-' + script_version + '-' + infbase + '.tsv'
	tsvin = open(infile,'rb')
	tsvout = open(outfile, 'wb')
	tsvinreader = csv.reader(tsvin, delimiter='\t')
	tsvoutwriter = csv.writer(tsvout, delimiter='\t')

	#############################################
	# READ INPUT FILE AND RUN GENOTYPE ANALYSIS #
	#############################################
	for row in tsvinreader:
		if row == []:
			gtresult = row
		else:
			gtresult = [row[0]] + [row[1]] + [row[2]] + [row[3]]
			for x in range(1,samples + 1):
				if genotype_rule == "SR":
					gtresult = gtresult + genotype_SR(row[3], row[x*4+1], row[x*4], row[x*4+2], row[x*4+3])
				if genotype_rule == "XR":
					gtresult = gtresult + genotype_XR(row[3], row[x*4+1], row[x*4], row[x*4+2], row[x*4+3])
		tsvoutwriter.writerow(gtresult)
########################
#        THE END       #
########################

