#!/usr/bin/python

def DFS_procedure(current_adj_item):

	global adj_array
	global already_done
	global group_count
	global dfs_counter
	global working_group
	global group_depth
	global node_count
	global node_array

	print "DFS" + '\t' + `dfs_counter`

	for key in adj_array:
		current_adj_list = adj_array[key]
		current_adj_len = len(current_adj_list)
		if current_adj_item in current_adj_list:
			q = 0
			while q <= (current_adj_len - 1):
				current_adj_item1 = current_adj_list[q]
				# print `q` + '\t' + current_adj_item1
				if current_adj_item1 in already_done:
					go_to_dfs = 0
				# if current_adj_item1 not in already_done:
				try:
					node_test = node_array[current_adj_item1]
				except:
					node_array[current_adj_item1] = 1
					already_done.append(current_adj_item1)
					node_count = node_count + 1
					if current_adj_item1 not in working_group:
						working_group.append(current_adj_item1)
					go_to_dfs = 1
					DFS_procedure(current_adj_item1)
					dfs_counter = dfs_counter + 1
					print "DFS" + '\t' + `dfs_counter`
					group_depth = dfs_counter
				q = q + 1


def Seqs_Cluster(in_name, out_name, exp_cut, bit_cut, idn_cut, ovr_cut):

	print "INPUT FILE:  " + in_name
	print "OUTPUT FILE: " + out_name
	print "EXP CUTOFF:  " + `exp_cut`
	print "BITS CUTOFF: " + `bit_cut`
	print "IDNT CUTOFF: " + `idn_cut`
	print "OVRL CUTOFF: " + `ovr_cut`

	in_file  = open(in_name,  "rb")
	out_file1 = open(out_name + '.all_pairs', "wb")
	out_file2 = open(out_name + '.adj_list', "wb")
	out_file3 = open(out_name + '.group_info', "wb")

	global id_list
	global id_array
	global pair_matrix_array
	global adj_array
	global already_done
	global group_count
	global dfs_counter
	global working_group
	global group_depth
	global node_count
	global node_array

	prm_count = 0
	id_list = []
	id_array = {}
	node_array = {}
	matrix_array = {}
	pairs_array  = {}
	adj_array    = {}
	pair_matrix_array = {}
	pair_matrix_count = 0
	already_done = []
	group_count = 0
	pair_counter = 0

	### READ ALL HITS FILE ###

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
		id_a = t[0]
		id_b = t[1]
		# if id_a not in id_list:
		try:
			id_test = id_array[id_a]
		except:
			id_array[id_a] = 1
			id_list.append(id_a)
		if id_b != 'no_hits_found':
			exp  = int(t[2])
			bit  = round(float(t[3]))
			idn  = int(t[4])
			ovr  = int(t[6])
			aln  = t[9]

			if aln == "PRM":
				prm_count = prm_count + 1
				line_tick_update = math.fmod(prm_count, 1000)
				if line_tick_update == 0:
					print prm_count
				# if id_a not in id_list:
				#	id_list.append(id_a)
				# if id_b not in id_list:
				try:
					id_test = id_array[id_b]
				except:
					id_array[id_b] = 1
					id_list.append(id_b)
				if exp >= exp_cut and bit >= bit_cut and idn >= idn_cut and ovr >= ovr_cut:
					pair_counter = pair_counter + 1
					current_pair = [id_a, id_b]
					pairs_array[pair_counter] = current_pair
					matrix_values = [exp, bit, idn, ovr]
					matrix_array[id_a,id_b] = matrix_values

	# print id_list
	print "------------------------------"
	print "FOUND " + `len(id_list)` + " UNIQ IDs"
	print "------------------------------"

	r = 0

	### CREATE NON-REDUNDANT MATRIX ###

	for key in pairs_array:
		id_a = pairs_array[key][0]
		id_b = pairs_array[key][1]
		try:
			# cur_exp1 = round(float(matrix_array[id_a,id_b][0]))
			# cur_bit1 = round(float(matrix_array[id_a,id_b][1]))
			# cur_idn1 = round(float(matrix_array[id_a,id_b][2]))
			# cur_ovr1 = round(float(matrix_array[id_a,id_b][3]))
			cur_exp1 = int(matrix_array[id_a,id_b][0])
			cur_bit1 = round(float(matrix_array[id_a,id_b][1]))
			cur_idn1 = int(matrix_array[id_a,id_b][2])
			cur_ovr1 = int(matrix_array[id_a,id_b][3])
			query1 = 1
			print key
			# print `key` + '\t' + id_a + '\t' + id_b + '\t' + `cur_exp1` + \
			#		'\t' + `cur_bit1` + '\t' + `cur_idn1` + '\t' + `cur_ovr1`
			# print pairs_array[key]
		except:
			print "ALREADY PROCESSED"
			query1 = 0

		try:
			# cur_exp2 = round(float(matrix_array[id_b,id_a][0]))
			# cur_bit2 = round(float(matrix_array[id_b,id_a][1]))
			# cur_idn2 = round(float(matrix_array[id_b,id_a][2]))
			# cur_ovr2 = round(float(matrix_array[id_b,id_a][3]))
			cur_exp2 = int(matrix_array[id_b,id_a][0])
			cur_bit2 = round(float(matrix_array[id_b,id_a][1]))
			cur_idn2 = int(matrix_array[id_b,id_a][2])
			cur_ovr2 = int(matrix_array[id_b,id_a][3])
			r = r + 1
			# print `r` + " REVERSE PAIR FOUND"
			query2 = 1
		except:
			# print "NO REVERSE PAIR FOUND"
			query2 = 0

		if query1 == 1 and query2 == 0 and cur_exp1 >= exp_cut and cur_bit1 >= bit_cut and \
					cur_idn1 >= idn_cut and cur_ovr1 >= ovr_cut and \
					id_a != id_b:
			out_file1.write(id_a + '\t' + id_b + '\t' + `cur_exp1` + '\t' + \
				`cur_bit1` + '\t' + `cur_idn1` + '\t' + `cur_ovr1` + '\n')
			pair_matrix_count = pair_matrix_count + 1
			current_matrix_pair = [id_a, id_b]
			pair_matrix_array[id_a,id_b] = current_matrix_pair
			### NEED TO UNSET ARRAY
			try:
				del matrix_array[id_a,id_b]
			except:
				print "ALREADY REMOVED"

		if query1 == 1 and query2 == 1 and id_a != id_b:
			# if cur_exp1 >= cur_exp2:
			if cur_idn1 >= cur_idn2:
				# print "CASE 1"
				if cur_exp1 >= exp_cut and cur_bit1 >= bit_cut and \
					cur_idn1 >= idn_cut and cur_ovr1 >= ovr_cut:
					out_file1.write(id_a + '\t' + id_b + '\t' + `cur_exp1` + '\t' + \
						`cur_bit1` + '\t' + `cur_idn1` + '\t' + `cur_ovr1` + '\n')
					pair_matrix_count = pair_matrix_count + 1
					current_matrix_pair = [id_a, id_b]
					pair_matrix_array[id_a,id_b] = current_matrix_pair
					### NEED TO UNSET ARRAY
					try:
						del matrix_array[id_a,id_b]
						del matrix_array[id_b,id_a]
					except:
						print "ALREADY REMOVED"
			# if cur_exp1 < cur_exp2:
			if cur_idn1 < cur_idn2:
				# print "CASE 2"
				if cur_exp2 >= exp_cut and cur_bit2 >= bit_cut and \
					cur_idn2 >= idn_cut and cur_ovr2 >= ovr_cut:
					out_file1.write(id_b + '\t' + id_a + '\t' + `cur_exp2` + '\t' + \
					`cur_bit2` + '\t' + `cur_idn2` + '\t' + `cur_ovr2` + '\n')
					pair_matrix_count = pair_matrix_count + 1
					current_matrix_pair = [id_b, id_a]
					pair_matrix_array[id_b,id_a] = current_matrix_pair
					### NEED TO UNSET ARRAY
					try:
						del matrix_array[id_a,id_b]
						del matrix_array[id_b,id_a]
					except:
						print "ALREADY REMOVED"

	out_file1.close()
	print "-------------------------------------"
	print `pair_matrix_count` + " PAIRS IN REDUNDANT MATRIX"
	print "-------------------------------------"
	print "BEGIN CLUSTERING"

	# l = 0
	# for item in id_list:
	#	l = l + 1
	#	print `l` + '\t' + item

	item_count = 0
	id_list.sort()
	### CREATE ADJACENCY LIST ###
	for item in id_list:
		item_count = item_count + 1
		print `item_count` + '\t' + item

		item_list = [item]
		for key in pair_matrix_array:
			id_a = pair_matrix_array[key][0]
			id_b = pair_matrix_array[key][1]
			if id_a == item:
				item_list.append(id_b)
			if id_b == item:
				item_list.append(id_a)
		adj_array[item] = item_list
		item_string = " ".join(item_list)
		out_file2.write(item_string + '\n')

	out_file2.close()

	### GROUP ANALYSIS ###
	node_count = 0
	for item in id_list:
		# if item not in already_done:
		try:
			node_test = node_array[item]
		except:
			node_array[item] = 1
			group_count = group_count + 1
			already_done.append(item)
			node_count = node_count + 1
			working_group = [item]
			current_adj_list = adj_array[item]
			current_adj_len = len(current_adj_list)

			q = 0
			while q <= (current_adj_len - 1):
				current_adj_item = current_adj_list[q]
				# print `q` + '\t' + current_adj_item
				if current_adj_item in already_done:
					go_to_dfs = 0
				# if current_adj_item not in already_done:
				try:
					node_test = node_array[current_adj_item]
				except:
					node_array[current_adj_item] = 1
					already_done.append(current_adj_item)
					node_count = node_count + 1
					if current_adj_item not in working_group:
						working_group.append(current_adj_item)
					go_to_dfs = 1
					dfs_counter = 0
					# print 'Processing Group:  ' + `group_count`
					DFS_procedure(current_adj_item)
				q = q + 1
			# if item not in already_done:
			#	already_done.append(item)
			working_group.sort()
			# print working_group
			print 'Processing Group:  ' + `group_count`
			print 'Number of processed nodes:  ' + `node_count`
			i = 0
			for element in working_group:
				current_adj_list1 = adj_array[element]
				current_adj_len1 = len(current_adj_list1)
				current_group_len1 = len(working_group)
				if i == 0:
					out_file3.write(element + '\t' + `(current_adj_len1 - 1)` + '\t' \
						+ `current_group_len1` + '\t' + `group_count` + '\t' + '*****' + '\n')
				if i != 0:
					out_file3.write(element + '\t' + `(current_adj_len1 - 1)` + '\t' \
						+ `current_group_len1` + '\t' + `group_count` + '\t' + '\n')
				i = i + 1
	print '======================'
	# print already_done
	print len(already_done)
	print `group_count` + '\t' + 'GROUPS FOUND'
	print '======================'
	in_file.close()
	# out_file1.close()
	# out_file2.close()
	out_file3.close()

import math
import re
import sys
import string
import time
if __name__ == "__main__":
	if len(sys.argv) <= 6 or len(sys.argv) > 7:
		print "Program usage: "
		print "input_file output_file exp_cut bit_cut idn_cut ovr_cut"
		exit
	if len(sys.argv) == 7:
		in_name  = sys.argv[1]
		out_name = sys.argv[2]
		exp_cut  = sys.argv[3]
		bit_cut  = sys.argv[4]
		idn_cut  = sys.argv[5]
		ovr_cut  = sys.argv[6]
		exp_cut = float(exp_cut)
		bit_cut = float(bit_cut)
		idn_cut = float(idn_cut)
		ovr_cut = float(ovr_cut)

		sys.setrecursionlimit(10000)

		Seqs_Cluster(in_name, out_name, exp_cut, bit_cut, idn_cut, ovr_cut)

