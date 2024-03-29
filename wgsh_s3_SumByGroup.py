#!/usr/bin/python
##################################################################################
# Author: Lutz Froenicke(lfroenicke@ucdavis.edu) and Huaqin Xu (huaxu@ucdavis.edu)
# Date: Aug.16 2013; last update: Dec.13 2013
#================================================================================
# Description:
#   This python script summarize the genotype data for groups of SNPs along the reference sequence.  
# 
# input arguments:
#   1.input file: genotyped file or grouped genotyped file.
#   2.num
#     -- when opt is l(summarize by line), num = # of lines to group/# of lines to wrap up at the end of each scaffold, for example 100/20;
#        if summarize by scaffold ID: num = 0/0;
#     -- when opt is b(summarize by block), num = the position range to summarize, for example: 100000
#   3.opt:
#     -- l: summarize by defined line number or by scaffold ID
#     -- b: summarize by position range.
#   4.format:
#     -- f: first run
#     -- s: second run               
#     note: after first run, the script can take the result file as the input file to run the second time.
#           Thus, this input file will have two extra blank lines between groups and two extra columns of end position & # of SNPs per group)
#           b option does not support second run.
#  
# Output: summary files.
#       Format: SNP group | start position | end position | # of SNPs in group | # of 'A' | # of 'B' | # of '-' | # of 'U' |......
#
# Usage:
#   python 03-SumByGroup.py genotyped_file num opt format
# Example:
#   python 03-SumByGroup.py cleaned-genotype-table.tsv 60/20 l f
#   python 03-SumByGroup.py cleaned-genotype-table.tsv 0/0 l f
#   python 03-SumByGroup.py test.tsv 100000 b f
#
######################################################################################

import csv, os, sys, timeit, math
from os.path import basename, splitext
from itertools import islice


######################################################
#count genotype
def genotypesum(x):
    cnt_N = list(x).count('-')
    cnt_A = list(x).count('A')
    cnt_B = list(x).count('B')
    cnt_U = list(x).count('U')
    return [cnt_A, cnt_B, cnt_N, cnt_U] 
    
######################################################

start = timeit.default_timer()

# ----- get options and file names and open files -----
if len(sys.argv) == 5:
    infile = sys.argv[1]
    opt = sys.argv[3]
    format = sys.argv[4]
else: 
    print len(sys.argv)
    print 'Usage: [1]infile, [2]# of lines(bases) to sum/# of lines to round up, [3]opt: l or b, [4]format: f or s'
    sys.exit(1) 

if format == 's' and opt == 'b':
    print 'b option can not use with s option!'
    sys.exit(0)

infbase = splitext(basename(infile))[0]
if opt == 'l':
    if sys.argv[2].index('/') != -1:
        cnt = int(sys.argv[2].split("/")[0])
        endlimit = int(sys.argv[2].split("/")[1])
    else:
        print 'Please specify # of lines to sum/# of lines to wrap up !'
        sys.exit(0)
    outfile = 'sumByL_' + infbase + '.tsv'
else:
    cnt = int(sys.argv[2])
    outfile = 'sumByB_' + infbase + '.tsv'    

# ----- count the number of lines for each scaffold -------
tsvid = open(infile,'rb')
tsvidreader = csv.reader(tsvid, delimiter='\t')

rowlist = []
first = 1
SNPcount = 0 # num of SNPs per scaffold or num of SNPs in position range
cutoff = cnt

for row in tsvidreader:
    if row == [] or row == '\n':
        continue
    if (len(row)<2 and len(row)>0) or row[0] == '': # ignore "I" line
        continue
    if first == 1:
        curid = row[0]
        first = 0
        rowlen = len(row)
        
    if row[0] != curid:  # next scaffold
        rowlist = rowlist + [[curid, SNPcount]]
        SNPcount = 0
        curid = row[0]
        if opt == 'b':    
            cutoff = cnt

    if opt == 'l':
        SNPcount = SNPcount + 1     # count num of SNPs in scaffold group
    else:
        if int(row[1]) <= cutoff:
            SNPcount = SNPcount +1  # count num of SNPs in position range
        else: 
            rowlist = rowlist + [[curid, SNPcount]]
            cutoff = cutoff+cnt
            SNPcount = 0
            while int(row[1]) > cutoff:
                rowlist = rowlist + [[curid, SNPcount]]
                cutoff = cutoff+cnt                    
            SNPcount = 1  
                
rowlist = rowlist + [[curid, SNPcount]]

tsvid.close()

# ----- main: count the occurance of 'A','B','-' --------

tsvin = open(infile,'rb')
tsvout = open(outfile, 'wb')
tsvinreader = csv.reader(tsvin, delimiter='\t')
tsvoutwriter = csv.writer(tsvout, delimiter='\t')

if format == 'f': 
    s = 2   # id and position columns
else:
    s = 4   # id, start, end, and count columns

if opt == 'l':
    for alist in rowlist:
        id = alist[0]
        SNPlines = alist[1]
        print id + ":" + str(SNPlines)
        if cnt > 0:  #sum by the predefined number
            if SNPlines < cnt:
                loopcnt = 0
                endline = SNPlines%cnt                
            elif SNPlines%cnt > endlimit:
                loopcnt = SNPlines/cnt
                endline = SNPlines%cnt 
            else: 
                loopcnt = SNPlines/cnt-1
                endline = cnt + SNPlines%cnt
  
            for m in range(loopcnt): # loop by each cnt-100 lines
                total = []
                cnt_lines = list(islice(tsvinreader, cnt))  # get cnt-100 lines
                posStart = cnt_lines[0][1]
                if format == 'f':
                    posEnd = cnt_lines[cnt-1][1]
                    sumcnt = cnt
                else:
                    posEnd = cnt_lines[cnt-1][2]
                    sumcnt = sum(int(z) for z in zip(*cnt_lines)[s-1])
                for x in zip(*cnt_lines)[s:]:            # convert to list of columns and count
                    total = total + genotypesum(x)      
                tsvoutwriter.writerow([id]+ [posStart] + [posEnd] + [sumcnt] + total)
            
            # get the rest of lines 
            total = []
            cnt_lines = list(islice(tsvinreader, endline))
            posStart = cnt_lines[0][1]
            if format == 'f':
                posEnd = cnt_lines[endline-1][1]
                sumcnt = endline
            else:
                posEnd = cnt_lines[endline-1][2]
                sumcnt = sum(int(z) for z in zip(*cnt_lines)[s-1])

            for x in zip(*cnt_lines)[s:]:
                total = total + genotypesum(x)       
            tsvoutwriter.writerow([id]+ [posStart] + [posEnd] + [sumcnt] + total)
            tsvoutwriter.writerow([])
            tsvoutwriter.writerow([])
            if format != 'f':
                blank_lines = list(islice(tsvinreader, 2))
            
        else: # sum by each scaffold
            total = []
            cnt_lines = list(islice(tsvinreader, SNPlines))
            posStart = cnt_lines[0][1]
            if format == 'f':
                posEnd = cnt_lines[SNPlines-1][1]
                sumcnt = SNPlines
            else:
                posEnd = cnt_lines[SNPlines-1][2]
                sumcnt = sum(int(z) for z in zip(*cnt_lines)[s-1])

            for x in zip(*cnt_lines)[s:]:
                total = total + genotypesum(x)       
            tsvoutwriter.writerow([id]+ [posStart] + [posEnd] + [sumcnt] + total)
            if format != 'f':
                blank_lines = list(islice(tsvinreader, 2))
            
else:     
    id = 'first' # first scaffold

    for rlist in rowlist: # loop by position range for each scaffold
        if rlist[0] != id: # New scaffold
            if id != 'first': # print two extra lines at the end of previous scaffold if it is not the first one
                tsvoutwriter.writerow([id]+ [posStart] + [posEnd] + [sumcnt] + total)    
                tsvoutwriter.writerow([])
                tsvoutwriter.writerow([])
            posStart = 0
            posEnd = 0
        else:
            posEnd = (int(posEnd/cnt)+1)*cnt        
            tsvoutwriter.writerow([id]+ [posStart] + [posEnd] + [sumcnt] + total)
            
        id = rlist[0]
        SNPlines = rlist[1]
        print id + ":" + str(SNPlines)        
        total = []
        if SNPlines != 0:            
            cnt_lines = list(islice(tsvinreader, SNPlines))  # get lines by range
            posStart = (int(cnt_lines[0][1])/cnt)*cnt+1      
            posEnd = int(cnt_lines[SNPlines-1][1])      
            sumcnt = SNPlines
            for x in zip(*cnt_lines)[s:]:               # convert to list of columns and count
                total = total + genotypesum(x)
                
        else:      # no data in this range
            posStart = posEnd +1
            sumcnt = 0
            total = [0]*(rowlen-s)*4
                       
    tsvoutwriter.writerow([id]+ [posStart] + [posEnd] + [sumcnt] + total) # print last block

stop = timeit.default_timer()
print stop - start 

