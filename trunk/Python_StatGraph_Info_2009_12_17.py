#!/usr/bin/python

def Seqs_Count(in_name, out_name, min_val, max_val, column_n):

	print "INPUT FILE:  " + in_name
	print "OUTPUT FILE: " + out_name
	print "MIN VALUE:   " + `min_val`
	print "MAX VALUE:   " + `max_val`
	print "COLUMN No:   " + `column_n`

	column_n = column_n - 1

	in_file  = open(in_name,  "rb")
	out_file = open(out_name, "wb")

	prm_count = 0
	id_list = []
	tot_value = {}

	k = min_val
	while k <= max_val:
		tot_value[k] = 0
		k = k + 1

	# print tot_value[1]
	# print tot_value[100]

	while 1:
		t = in_file.readline()
		if t == '':
			break
		if '\n' in t:
			t = t[:-1]
		if '\r' in t:
			t = t[:-1]
		t = t.split('\t')
		####
		comment_contr = "".join(t)
		if comment_contr[0:1] != "#":
			cur_value = t[column_n]
			cur_value = float(cur_value)
			cur_value = int(cur_value)
			prm_count = prm_count + 1
			# print comment_contr[0:1]
			print `prm_count` + '\t' + `cur_value`
			if cur_value >= max_val:
				cur_value = max_val
			if cur_value <= min_val:
				cur_value = min_val
			tot_value[cur_value] = tot_value[cur_value] + 1

	k = min_val
	dummy = "="
	while k <= max_val:
		# val_pcnt = int(round(tot_value[k]*100.00/prm_count))
		val_pcnt = round((tot_value[k]*100.00/prm_count),4)
		val_pcnt_int = int(round(val_pcnt*10.00))
		dummy_length = dummy*val_pcnt_int
		val_pcnt = str(val_pcnt)
		print `k` + '\t' + `tot_value[k]` + '\t' + val_pcnt + '\t' + dummy_length
		out_file.write(`k` + '\t' + `tot_value[k]` + '\t' + val_pcnt + '\t' + dummy_length + '\n')
		k = k + 1

	in_file.close()
	out_file.close()


import math
import re
import sys
import string
if __name__ == "__main__":
	if len(sys.argv) <= 5 or len(sys.argv) > 6:
		print "Program usage: "
		print "input_file output_file min_val max_val column_n"
		exit
	if len(sys.argv) == 6:
		in_name   = sys.argv[1]
		out_name  = sys.argv[2]
		min_val   = sys.argv[3]
		max_val   = sys.argv[4]
		column_n  = sys.argv[5]
		min_val   = int(min_val)
		max_val   = int(max_val)
		column_n  = int(column_n)
		Seqs_Count(in_name, out_name, min_val, max_val, column_n)

