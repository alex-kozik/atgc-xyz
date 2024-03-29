#!/usr/bin/python
import csv, os, sys
from os.path import basename, splitext
##################################################################################
"""
Authors: Lutz Froenicke(lfroenicke@ucdavis.edu) and Huaqin Xu (huaxu@ucdavis.edu)
Date: Aug.15 2013; last updated Aug.29 2013
Description:

This python script sums the occurences of SNP consensus calls and variant calls
(i.e. [,.] or [ATCG|atcg]) in mpileup files for each SNP.
It also converts the count results into a genotype table.
An additional 'cleaned' genotype table from which SNPs with obvious artifacts are removed
is generated if the option '1' is applied.
=================================================================================
input arguments:
	1.input file.
	2.number of sample
	3.opt: cleaned (1) or not cleaned(0)
Note:
 The following thresholds per SNP are hard-coded in the script, but can be easily edited:
 - if more than one sample displays an indel in the alignment, the SNP will be removed;
   the data point containing the indel will be set to 'missing data' in any case.
 - if data for more than 80% of the samples are missing (M), the SNP will be removed.
 - if more than 50% of the called genotypes are heterozygous (U), the SNP will be removed.
 - if the genotyping data are very skewed (minor allele frequency < 10%), the SNP will be removed.

Output:
- a "parsed_" file (conversion of the mpileup file into counts for consensus and variant calls)-
- a "GTcounts_"  file (count of genotytes per SNP)
- a "genotyped_" file (providing a genotype for per RIL for each SNP
- and if option is 1: additionaly a "cleanedGTs_" file  (SNPs with severly skewed genotype data have been filtered out)

The GTcounts file lists for each SNP: scaffold, position, sum of Us, sum of As, sum of Bs, sum of "-"s (missing data), A/B call ratio, flags (indicating the reasons to filter this SNP - please see above).
"""
######################################################################################
# count in cells
def countcell(cnt, pu):
    global flag
    Vcnt = pu.count("a") + pu.count("A") + pu.count("c") + pu.count("C") +pu.count("t") + pu.count("T") + pu.count("g") + pu.count("G")
    Ccnt = pu.count(",") + pu.count(".")
    if int(cnt) != Vcnt + Ccnt:
        Vcnt = 0
        Ccnt = 0
        flag = flag + 1
    C = [Vcnt, Ccnt]    
    return C

#convert count number to genotype
def genotype(C):    
    Vcnt = float(C[0])
    Ccnt = float(C[1])

    GT = ""
    if Vcnt == Ccnt == 0:
        GT = "-"
    elif Vcnt == 0:
        GT = "A"
    elif Ccnt == 0:
        GT = "B"
    elif 0.2 <= Vcnt / Ccnt <= 5:
        GT = "U"
    elif Vcnt / Ccnt < 0.2:
        GT = "A"
    elif Vcnt / Ccnt > 5:
        GT = "B"    
    return [GT]

#clean up genotype table by genotype count
def genotypecount(row, samples):
    U = row.count("U")
    A = row.count("A")
    B = row.count("B")
    M = row.count("-")
    S = U + A + B
    R = ""

    F = ""
    if M > 0.8 * samples :    # Snps with more than 80% missing data points are flagged
        F = F + "M"
    ### if U > 0.5 * S :    # raised the cutoff threshold from 5% of the sample number (in versions prior to r63), to 50% of genoytpes fo rflagging SNPs of unexpected heterozygosity
    if U > 0.1 * S :
        F = F + "U"
    if A == 0 or B == 0:  #  monotypic SNPs are flagged
        F = F + "Y"
    if A != 0 and B != 0 :
        R = round((A/float(B)), 2)
    if R < 0.1 or R > 9:   #  SNPs with severely skewed genotype ratios (e.g. MAF less than 10%) are flagged
        F = F + "X"

    C = [U, A, B, M, R, F]
    return C

######################################################

# ----- get options and file names and open files -----
if len(sys.argv) == 4:
    infile = sys.argv[1]
    samples = int(sys.argv[2])
    opt = int(sys.argv[3])
else: 
    print len(sys.argv)
    print 'Usage: [1]infile, [2]num of samples, [3]opt: 0 or 1'
    sys.exit(1)
    
if samples <0:
    print "The number of samples must be a positive integer."
    sys.exit(1)

infbase = splitext(basename(infile))[0]
outfile1 = 'parsed_' + infbase + '.tsv'
outfile2 = 'genotyped_' + infbase + '.tsv'

tsvin = open(infile,'rb')
tsvout1 = open(outfile1, 'wb')
tsvout2 = open(outfile2, 'wb')

tsvinreader = csv.reader(tsvin, delimiter='\t')
tsvoutwriter1 = csv.writer(tsvout1, delimiter='\t')
tsvoutwriter2 = csv.writer(tsvout2, delimiter='\t')

if opt == 1:
    outfile3 = 'cleanedGTs_' + infbase + '.tsv'
    outfile4 = 'GTcounts_' + infbase + '.tsv'
    tsvout3 = open(outfile3, 'wb')
    tsvout4 = open(outfile4, 'wb')
    tsvoutwriter3 = csv.writer(tsvout3, delimiter='\t')
    tsvoutwriter4 = csv.writer(tsvout4, delimiter='\t')

# ------ loop through each line to count ocurrence -------

for row in tsvinreader:
    if len(row) != (samples+1)*3 :
        print "Unmatched number of samples"
        sys.exit(0)
        
    cntresult = [row[0]] + [row[1]]
    gtresult = [row[0]] + [row[1]]
    flag = 0
    for x in range(1,samples+1):
        Cnt = countcell(row[x*3] , row[x*3+1])
        cntresult = cntresult + Cnt   # countcell has two input values: cnt and teh cell with the genotypes
        gtresult = gtresult + genotype(Cnt)
    
    ##### updated 8/27/2013
    if flag > 1:
        cntresult = [row[0]] + [row[1]] + [0]*samples*2  # fill the whole row with [0,0]
    #####
        
    tsvoutwriter1.writerow(cntresult)
    tsvoutwriter2.writerow(gtresult)
    
    if opt == 1:
        gtcnt = [row[0]] + [row[1]]
        gtcnt = gtcnt + genotypecount(gtresult, samples) #get genotype count
        tsvoutwriter4.writerow(gtcnt)
        if gtcnt[7] == '':             # write to cleanGT file if genotype count is good
            tsvoutwriter3.writerow(gtresult)


    

