#!/usr/bin/python
#################################################################################
# Author: Lutz Froenicke(lfroenicke@ucdavis.edu)
# Date: Oct.16 2013; last update: Dec.13 2013
#================================================================================
# Description:
#    This script converts the group counts into group haplotypes with the GroupHaplotyper script. After this haplotyping is performed per-scaffold  and per-sample:
#    The script provides output of all data and of data filtered per-scaffold.
#    Scaffolds with a higher percentage of missing data than the cutoff value will be removed from the "filtered"
#    output file and written instead to the "removed data" output file.
#
# Notes: The haplotyping thresholds are hardcoded in the script and should be edited at the top of the script.
#       -- B/A ratio between "min" and "max" --> resulting call: heterozygous
#       -- B/A ratio between smaller than or equal to "min" --> resulting call: A
#       -- B/A ratio between bigger than or equal to "max" --> resulting call: B
#       -- if heterozygous calls more than the sum of A and B calls --> resulting call: heterozygous
#       -- if missing data point number higher than the sum of A and B and het calls --> resulting call: missing  
# 
# Outputs:
#    The script generates an outputfile with all scaffolds and two additional with filtered data
#    with the prefixes 'htyped-flt-' (for scaffolds passingthe test) and 'htyped-rem-' (for scaffolds  failing the test).
#    Filtering is done according the precentage of missing data

# Usage:
#   python  06-ScaffoldHaplotyper.py  chunked-clean-genotype-table.tsv  number_of_samples  max-percentage_of_missing_data &
# Example: for 88 samples and a 10% cutoff threshold:
#   python 06-ScaffoldHaplotyper.py  genotype-table.tsv  88  10 &

#####################################################

import csv, os, sys
from os.path import basename, splitext
from itertools import islice

# The haplotyping thresholds to be edited
min = 0.25
max = 4

######################################################
#count in cells
def genotype(Vcnt, Ccnt, Mcnt, Ucnt):
    Vcnt = float(Vcnt)
    Ccnt = float(Ccnt)
    Mcnt = float(Mcnt)
    Ucnt = float(Ucnt)
    GT = ""
    if Vcnt == Ccnt == 0:
        GT = "-"
    elif Vcnt == 0:
        GT = "A"
    elif Ccnt == 0:
        GT = "B"
    elif min <= Vcnt / Ccnt <= max:    # thresholds for typing as heterozygous
        GT = "U"
    elif Vcnt / Ccnt <  min:
        GT = "A"
    elif Vcnt / Ccnt > max:
        GT = "B"
    if Vcnt < Ucnt and Ccnt < Ucnt:  # previously:  if Vcnt + Ccnt <= Ucnt:
        GT = "U"
    if Vcnt + Ccnt + Ucnt < Mcnt:
        GT = "-"
    GTL = [GT]
    return GTL
######################################################
def countrow(gt, samples, cutoff):
    C = ''
    max = samples * cutoff * 0.01
    Gcnt = gt.count("A") + gt.count("B") + gt.count("U")
    Mcnt = gt.count("-")
#    if Mcnt == 0:
#        Mcnt = 1
#    if Gcnt == 0:
#        Gcnt = 0.05
    if Mcnt >= max:
        C = 'F'
    return C
######################################################
######################################################
#count genotype
def genotypesum(x):
    cnt_N = list(x).count('-')
    cnt_A = list(x).count('A')
    cnt_B = list(x).count('B')
    cnt_U = list(x).count('U')
    return [cnt_A, cnt_B, cnt_N, cnt_U]

######################################################


infile = sys.argv[1]
samples = int(sys.argv[2])
cutoff = float(sys.argv[3])

infbase = splitext(basename(infile))[0]
outfile = 'htyped-' + infbase + '.tsv'
foutfile = 'htyped-flt-' + str(cutoff)  + '-' + infbase + '.tsv'
remoutfile = 'htyped-rem-' + str(cutoff)  + '-' + infbase + '.tsv'

tsvin = open(infile,'rb')
tsvout = open(outfile, 'wb')
tsvfout = open(foutfile, 'wb')
remout = open(remoutfile, 'wb')

tsvinreader = csv.reader(tsvin, delimiter='\t')
tsvoutwriter = csv.writer(tsvout, delimiter='\t')
tsvfoutwriter = csv.writer(tsvfout, delimiter='\t')
remoutwriter = csv.writer(remout, delimiter='\t')

allSc = 0
filSc = 0
remSc = 0


for row in tsvinreader:
    if row == [] or row[0] == '':
        gtresult = row
        # tsvoutwriter.writerow(gtresult)
    else:
        gtresult = [row[0]] + [row[1]] + [row[2]] + [row[3]]
        for x in range(1,samples + 1):
            gtresult = gtresult + genotype(row[x*4+1], row[x*4], row[x*4+2], row[x*4+3])   #
        flag = countrow(gtresult[4:], samples, cutoff)
        if flag == 'F':
            remoutwriter.writerow(gtresult)
            remSc = remSc + 1
        else:
            tsvfoutwriter.writerow(gtresult)
            filSc = filSc + 1
    tsvoutwriter.writerow(gtresult)
    allSc = allSc + 1



print "\n\n"
print "All Scaffolds: " + str(allSc)
print "Scaffolds passing filter: " + str(filSc)
print "Removed Scaffolds: " + str(remSc)

