#!/usr/bin/python

########################
# COPYRIGHT 2004       #
# Alexander Kozik      #
# http://www.atgc.org/ #
# akozik@atgc.org      #
########################

def Seqs_Processing(in_name, out_name, seq_type, min_L, max_N, min_A, min_T, min_G, min_C, max_MA, max_MT, max_MG, max_MC, anc_L, max_GC, min_GC, mask, all_hits, mask_char, trim):

	print in_name + ' ' + out_name

	print "min L: " + ' ' + `min_L`
	print "max N: " + ' ' + `max_N`
	print "min A: " + ' ' + `min_A`
	print "min T: " + ' ' + `min_T`
	print "min G: " + ' ' + `min_G`
	print "min C: " + ' ' + `min_C`
	print "max MA:" + ' ' + `max_MA`
	print "max MT:" + ' ' + `max_MT`
	print "max MG:" + ' ' + `max_MG`
	print "max MC:" + ' ' + `max_MC`
	print "word L:" + ' ' + `anc_L`
	print "max GC:" + ' ' + `max_GC`
	print "min GC:" + ' ' + `min_GC`
	print "mask:"   + ' ' +  mask
	print "char:"   + ' ' +  mask_char
	print "trim:"   + ' ' +  trim

	in_file  = open(in_name,  "rb")
	out_file = open(out_name + '.all',  "wb")          # ALL FASTA
	out_good = open(out_name + '.good', "wb")          # GOOD FASTA
	out_bad  = open(out_name + '.bad',  "wb")          # BAD FASTA
	out_stat = open(out_name + '.stat.gc', "wb")       # STAT FILE (GC CONTENT)
	out_dinc = open(out_name + '.stat.ncompl', "wb")   # STAT FILE (DINUCL COMPLEXITY)
	out_tab1 = open(out_name + '.tab.all', "wb")       # ALL TAB FILE
	out_tab2 = open(out_name + '.tab.good', "wb")      # GOOD TAB FILE
	out_tab3 = open(out_name + '.tab.bad', "wb")       # BAD TAB FILE
	if mask == "mask":
		out_mask = open(out_name + '.good.masked', "wb")      # GOOD FASTA MASKED
		out_mask_list = open(out_name + '.masked.list', "wb") # GOOD MASKED LIST

	mask_seqs_array = {}
	mask_desc_array = {}
	mask_lib_array  = {}
	compl_fract     = {}     # COMPLEXITY ARRAY
	mask_seqs_list  = []
	compl_list = ["AA","AT","AG","AC","TA","TT","TG","TC","GA","GT","GG","GC","CA","CT","CG","CC"]

	out_dinc.write("SEQ_ID" + '\t')
	for dinc in compl_list:
		if dinc != "CC":
			out_dinc.write(dinc + '\t')
		if dinc == "CC":
			out_dinc.write(dinc + '\n')

	if seq_type == "DNA":
		out_stat.write("#SEQ_ID" + '\t' + "LENGTH" + '\t' + " A " + '\t' + " T " + '\t' + \
				" G " + '\t' + " C " + '\t' + "AT" + '\t' + "GC" + '\t' \
				+ "ATGC" + '\t' + " N " + '\t' + " X " + '\n')
	if seq_type == "prot":
		out_stat.write("#SEQ_ID" + '\t' + "LENGTH" + '\t' + \
				" A " + '\t' + " B " + '\t' + \
				" C " + '\t' + " D " + '\t' + \
				" E " + '\t' + " F " + '\t' + \
				" G " + '\t' + " H " + '\t' + \
				" I " + '\t' + " J " + '\t' + \
				" K " + '\t' + " L " + '\t' + \
				" M " + '\t' + " N " + '\t' + \
				" O " + '\t' + " P " + '\t' + \
				" Q " + '\t' + " R " + '\t' + \
				" S " + '\t' + " T " + '\t' + \
				" U " + '\t' + " V " + '\t' + \
				" W " + '\t' + " X " + '\t' + \
				" Y " + '\t' + " Z " + '\n')

	fasta_id_array = []
	line_counter = 0
	have_seqs = ""
	proper_id = ""
	my_seqs = []
	tot_len = 0
	a_tot = 0
	b_tot = 0
	c_tot = 0
	d_tot = 0
	e_tot = 0
	f_tot = 0
	g_tot = 0
	h_tot = 0
	i_tot = 0
	j_tot = 0
	k_tot = 0
	l_tot = 0
	m_tot = 0
	n_tot = 0
	o_tot = 0
	p_tot = 0
	q_tot = 0
	r_tot = 0
	s_tot = 0
	t_tot = 0
	u_tot = 0
	v_tot = 0
	w_tot = 0
	x_tot = 0
	y_tot = 0
	z_tot = 0

	### MAIN LOOP ###
	while 1:
		t = in_file.readline()
		### ALMOST THE END ###
		if t == '':
			###  SUB_SEQ FUNCTION  ###
			have_seqs = "".join(my_seqs)
			seqs_len = len(have_seqs)
			###   STRING PROCESSING   ###
			if seqs_len != 0:
				have_seqs = "".join(my_seqs)
				seqs_len = len(have_seqs)
				tot_len = tot_len + seqs_len
				if seqs_len == 0:
					seqs_len = 1
				###   STRING PROCESSING   ###
				abc_up = have_seqs.upper()
				##########################
				###
				a_count = abc_up.count("A")
				a_tot = a_tot + a_count
				###
				b_count = abc_up.count("B")
				b_tot = b_tot + b_count
				###
				c_count = abc_up.count("C")
				c_tot = c_tot + c_count
				###
				d_count = abc_up.count("D")
				d_tot = d_tot + d_count
				###
				e_count = abc_up.count("E")
				e_tot = e_tot + e_count
				###
				f_count = abc_up.count("F")
				f_tot = f_tot + f_count
				###
				g_count = abc_up.count("G")
				g_tot = g_tot + g_count
				###
				h_count = abc_up.count("H")
				h_tot = h_tot + h_count
				###
				i_count = abc_up.count("I")
				i_tot = i_tot + i_count
				###
				j_count = abc_up.count("J")
				j_tot = j_tot + j_count
				###
				k_count = abc_up.count("K")
				k_tot = k_tot + k_count
				###
				l_count = abc_up.count("L")
				l_tot = l_tot + l_count
				###
				m_count = abc_up.count("M")
				m_tot = m_tot + m_count
				###
				n_count = abc_up.count("N")
				n_tot = n_tot + n_count
				###
				o_count = abc_up.count("O")
				o_tot = o_tot + o_count
				###
				p_count = abc_up.count("P")
				p_tot = p_tot + p_count
				###
				q_count = abc_up.count("Q")
				q_tot = q_tot + q_count
				###
				r_count = abc_up.count("R")
				r_tot = r_tot + r_count
				###
				s_count = abc_up.count("S")
				s_tot = s_tot + s_count
				###
				t_count = abc_up.count("T")
				t_tot = t_tot + t_count
				###
				u_count = abc_up.count("U")
				u_tot = u_tot + u_count
				###
				v_count = abc_up.count("V")
				v_tot = v_tot + v_count
				###
				w_count = abc_up.count("W")
				w_tot = w_tot + w_count
				###
				x_count = abc_up.count("X")
				x_tot = x_tot + x_count
				###
				y_count = abc_up.count("Y")
				y_tot = y_tot + y_count
				###
				z_count = abc_up.count("Z")
				z_tot = z_tot + z_count
				###
				a_fract = round((a_count*100.00/seqs_len),2)
				b_fract = round((b_count*100.00/seqs_len),2)
				c_fract = round((c_count*100.00/seqs_len),2)
				d_fract = round((d_count*100.00/seqs_len),2)
				e_fract = round((e_count*100.00/seqs_len),2)
				f_fract = round((f_count*100.00/seqs_len),2)
				g_fract = round((g_count*100.00/seqs_len),2)
				h_fract = round((h_count*100.00/seqs_len),2)
				i_fract = round((i_count*100.00/seqs_len),2)
				j_fract = round((j_count*100.00/seqs_len),2)
				k_fract = round((k_count*100.00/seqs_len),2)
				l_fract = round((l_count*100.00/seqs_len),2)
				m_fract = round((m_count*100.00/seqs_len),2)
				n_fract = round((n_count*100.00/seqs_len),2)
				o_fract = round((o_count*100.00/seqs_len),2)
				p_fract = round((p_count*100.00/seqs_len),2)
				q_fract = round((q_count*100.00/seqs_len),2)
				r_fract = round((r_count*100.00/seqs_len),2)
				s_fract = round((s_count*100.00/seqs_len),2)
				t_fract = round((t_count*100.00/seqs_len),2)
				u_fract = round((u_count*100.00/seqs_len),2)
				v_fract = round((v_count*100.00/seqs_len),2)
				w_fract = round((w_count*100.00/seqs_len),2)
				x_fract = round((x_count*100.00/seqs_len),2)
				y_fract = round((y_count*100.00/seqs_len),2)
				z_fract = round((z_count*100.00/seqs_len),2)
				###
				at_fract = a_fract + t_fract
				gc_fract = g_fract + c_fract
				atgc_fract = a_fract + t_fract + g_fract + c_fract
				atgc_fract = round(atgc_fract,2)
				### STRING ###
				a_fract = str(a_fract) 
				b_fract = str(b_fract) 
				c_fract = str(c_fract) 
				d_fract = str(d_fract) 
				e_fract = str(e_fract) 
				f_fract = str(f_fract) 
				g_fract = str(g_fract) 
				h_fract = str(h_fract) 
				i_fract = str(i_fract) 
				j_fract = str(j_fract) 
				k_fract = str(k_fract) 
				l_fract = str(l_fract) 
				m_fract = str(m_fract) 
				n_fract = str(n_fract) 
				o_fract = str(o_fract) 
				p_fract = str(p_fract) 
				q_fract = str(q_fract) 
				r_fract = str(r_fract) 
				s_fract = str(s_fract) 
				t_fract = str(t_fract) 
				u_fract = str(u_fract) 
				v_fract = str(v_fract) 
				w_fract = str(w_fract) 
				x_fract = str(x_fract) 
				y_fract = str(y_fract) 
				z_fract = str(z_fract) 

				at_fract = str(at_fract)
				gc_fract = str(gc_fract)
				atgc_fract = str(atgc_fract)
				###
				if seq_type == "DNA":
					out_stat.write(proper_id + '\t' + `seqs_len` + '\t' + a_fract + '\t' + t_fract + '\t' + \
							g_fract + '\t' + c_fract + '\t' + at_fract + '\t' + gc_fract + '\t' \
							+ atgc_fract + '\t' + 'N: ' + n_fract + '\t' + 'X: ' + x_fract + '\n')
				if seq_type == "prot":
					out_stat.write(proper_id + '\t' + `seqs_len` + '\t' + \
							a_fract + '\t' + b_fract + '\t' + \
							c_fract + '\t' + d_fract + '\t' + \
							e_fract + '\t' + f_fract + '\t' + \
							g_fract + '\t' + h_fract + '\t' + \
							i_fract + '\t' + j_fract + '\t' + \
							k_fract + '\t' + l_fract + '\t' + \
							m_fract + '\t' + n_fract + '\t' + \
							o_fract + '\t' + p_fract + '\t' + \
							q_fract + '\t' + r_fract + '\t' + \
							s_fract + '\t' + t_fract + '\t' + \
							u_fract + '\t' + v_fract + '\t' + \
							w_fract + '\t' + x_fract + '\t' + \
							y_fract + '\t' + z_fract + '\n')
			### STRING PROCESSING END ###

			#############################
			#  DINUCLEOTIDE COMPLEXITY  #

			for dinc in compl_list:
				compl_fract[dinc] = 0

			j = 0
			i = 0
			mooba = "WHATEVER"
			while j < seqs_len-1:
				n_pair = have_seqs[j:j+2]
				try:
					compl_fract[n_pair] = compl_fract[n_pair] + 1
					i = i + 1
				except:
					booba = mooba
				j = j + 1

			if i == 0:
				i = 1

			out_dinc.write(proper_id + '\t')
			for dinc in compl_list:
				if dinc != "CC":
					out_dinc.write(str(round(compl_fract[dinc]*100.0/i,2)) + '\t')
				if dinc == "CC":
					out_dinc.write(str(round(compl_fract[dinc]*100.0/i,2)) + '\n')

			#     END OF COMPLEXITY     #
			#############################

			# print seqs_len
			gc_fract = float(gc_fract)
			n_fract  = float(n_fract)
			if seqs_len >= min_L and gc_fract <= max_GC and gc_fract >= min_GC and n_fract <= max_N:
				out_good.write('>' + proper_id + ' ' + good_name + '\n')
				out_good.write(have_seqs + '\n')
				out_tab2.write(proper_id + '\t' + `seqs_len` + '\t' + have_seqs + '\n')
				mask_seqs_array[proper_id] = have_seqs
				mask_desc_array[proper_id] = good_name
				mask_lib_array[proper_id] = []
				mask_seqs_list.append(proper_id)
			if seqs_len < min_L or gc_fract > max_GC or gc_fract < min_GC or n_fract > max_N:
				out_bad.write('>' + proper_id + ' ' + good_name + '\n')
				out_bad.write(have_seqs + '\n')
				out_tab3.write(proper_id + '\t' + `seqs_len` + '\t' + have_seqs + '\n')
			if have_seqs != "":
				out_file.write('>' + proper_id + ' ' + good_name + '\n')
				out_file.write(have_seqs + '\n')
				out_tab1.write(proper_id + '\t' + `seqs_len` + '\t' + have_seqs + '\n')
				break
		if '\n' in t:
			t = t[:-1]
		if '\r' in t:
			t = t[:-1]

		### FIND THE SEQUENCE ###
		fasta_match = t[0:1]
		if fasta_match == ">":
			gi_test = t[0:4]
			if gi_test == ">gi|":
				# print gi_test
				descr_line = t
				###   REPLACE ALL TABS WITH WHITESPACES   ###
				descr_line = re.sub('\t', " ", descr_line)
				#############################################
				descr_line = re.sub("^>gi\|", "", descr_line)
				descr_line = re.sub("\|", '\t', descr_line, 1)
				# print line_counter
				line_counter += 1
			else:
				descr_line = t
				###   REPLACE ALL TABS WITH WHITESPACES   ###
				descr_line = re.sub('\t', " ", descr_line)
				#############################################
				descr_line = re.sub("^>", "", descr_line)
				descr_line = re.sub("\|", " ", descr_line, 1)
				descr_line = re.sub(" ", '\t', descr_line, 1)
				# print line_counter
				line_counter = line_counter + 1
			good_head = string.split(descr_line, '\t')[0]
			try:
				long_tail = string.split(descr_line, '\t')[1]
			except:
				long_tail = ""
			###############################
			dupl_status = "GOOD"
			###############################
			if good_head in fasta_id_array:
				dupl_status = "BAD"
				running_text = "\
\n\n  Ooops... ID duplication  \n\n  check input for duplications  \n\n\n ID: " + good_head + "\n\n\n"
				print running_text
				###
				### INSERT TKINTER TEXT MESSAGE BOX
				###
				break
			fasta_id_array.append(good_head)
			print `line_counter` + '\t' + good_head
			if line_counter != 1:
				###  SUB_SEQ FUNCTION  ###
				have_seqs = "".join(my_seqs)
				seqs_len = len(have_seqs)
				tot_len = tot_len + seqs_len
				if seqs_len == 0:
					seqs_len = 1
				###   STRING PROCESSING   ###
				abc_up = have_seqs.upper()
				#############################
				###
				a_count = abc_up.count("A")
				a_tot = a_tot + a_count
				###
				b_count = abc_up.count("B")
				b_tot = b_tot + b_count
				###
				c_count = abc_up.count("C")
				c_tot = c_tot + c_count
				###
				d_count = abc_up.count("D")
				d_tot = d_tot + d_count
				###
				e_count = abc_up.count("E")
				e_tot = e_tot + e_count
				###
				f_count = abc_up.count("F")
				f_tot = f_tot + f_count
				###
				g_count = abc_up.count("G")
				g_tot = g_tot + g_count
				###
				h_count = abc_up.count("H")
				h_tot = h_tot + h_count
				###
				i_count = abc_up.count("I")
				i_tot = i_tot + i_count
				###
				j_count = abc_up.count("J")
				j_tot = j_tot + j_count
				###
				k_count = abc_up.count("K")
				k_tot = k_tot + k_count
				###
				l_count = abc_up.count("L")
				l_tot = l_tot + l_count
				###
				m_count = abc_up.count("M")
				m_tot = m_tot + m_count
				###
				n_count = abc_up.count("N")
				n_tot = n_tot + n_count
				###
				o_count = abc_up.count("O")
				o_tot = o_tot + o_count
				###
				p_count = abc_up.count("P")
				p_tot = p_tot + p_count
				###
				q_count = abc_up.count("Q")
				q_tot = q_tot + q_count
				###
				r_count = abc_up.count("R")
				r_tot = r_tot + r_count
				###
				s_count = abc_up.count("S")
				s_tot = s_tot + s_count
				###
				t_count = abc_up.count("T")
				t_tot = t_tot + t_count
				###
				u_count = abc_up.count("U")
				u_tot = u_tot + u_count
				###
				v_count = abc_up.count("V")
				v_tot = v_tot + v_count
				###
				w_count = abc_up.count("W")
				w_tot = w_tot + w_count
				###
				x_count = abc_up.count("X")
				x_tot = x_tot + x_count
				###
				y_count = abc_up.count("Y")
				y_tot = y_tot + y_count
				###
				z_count = abc_up.count("Z")
				z_tot = z_tot + z_count
				###
				a_fract = round((a_count*100.00/seqs_len),2)
				b_fract = round((b_count*100.00/seqs_len),2)
				c_fract = round((c_count*100.00/seqs_len),2)
				d_fract = round((d_count*100.00/seqs_len),2)
				e_fract = round((e_count*100.00/seqs_len),2)
				f_fract = round((f_count*100.00/seqs_len),2)
				g_fract = round((g_count*100.00/seqs_len),2)
				h_fract = round((h_count*100.00/seqs_len),2)
				i_fract = round((i_count*100.00/seqs_len),2)
				j_fract = round((j_count*100.00/seqs_len),2)
				k_fract = round((k_count*100.00/seqs_len),2)
				l_fract = round((l_count*100.00/seqs_len),2)
				m_fract = round((m_count*100.00/seqs_len),2)
				n_fract = round((n_count*100.00/seqs_len),2)
				o_fract = round((o_count*100.00/seqs_len),2)
				p_fract = round((p_count*100.00/seqs_len),2)
				q_fract = round((q_count*100.00/seqs_len),2)
				r_fract = round((r_count*100.00/seqs_len),2)
				s_fract = round((s_count*100.00/seqs_len),2)
				t_fract = round((t_count*100.00/seqs_len),2)
				u_fract = round((u_count*100.00/seqs_len),2)
				v_fract = round((v_count*100.00/seqs_len),2)
				w_fract = round((w_count*100.00/seqs_len),2)
				x_fract = round((x_count*100.00/seqs_len),2)
				y_fract = round((y_count*100.00/seqs_len),2)
				z_fract = round((z_count*100.00/seqs_len),2)
				###
				at_fract = a_fract + t_fract
				gc_fract = g_fract + c_fract
				atgc_fract = a_fract + t_fract + g_fract + c_fract
				atgc_fract = round(atgc_fract,2)
				### STRING ###
				a_fract = str(a_fract) 
				b_fract = str(b_fract) 
				c_fract = str(c_fract) 
				d_fract = str(d_fract) 
				e_fract = str(e_fract) 
				f_fract = str(f_fract) 
				g_fract = str(g_fract) 
				h_fract = str(h_fract) 
				i_fract = str(i_fract) 
				j_fract = str(j_fract) 
				k_fract = str(k_fract) 
				l_fract = str(l_fract) 
				m_fract = str(m_fract) 
				n_fract = str(n_fract) 
				o_fract = str(o_fract) 
				p_fract = str(p_fract) 
				q_fract = str(q_fract) 
				r_fract = str(r_fract) 
				s_fract = str(s_fract) 
				t_fract = str(t_fract) 
				u_fract = str(u_fract) 
				v_fract = str(v_fract) 
				w_fract = str(w_fract) 
				x_fract = str(x_fract) 
				y_fract = str(y_fract) 
				z_fract = str(z_fract) 

				at_fract = str(at_fract)
				gc_fract = str(gc_fract)
				atgc_fract = str(atgc_fract)
				###
				if seq_type == "DNA":
					out_stat.write(proper_id + '\t' + `seqs_len` + '\t' + a_fract + '\t' + t_fract + '\t' + \
							g_fract + '\t' + c_fract + '\t' + at_fract + '\t' + gc_fract + '\t' \
							+ atgc_fract + '\t' + 'N: ' + n_fract + '\t' + 'X: ' + x_fract + '\n')
				if seq_type == "prot":
					out_stat.write(proper_id + '\t' + `seqs_len` + '\t' + \
							a_fract + '\t' + b_fract + '\t' + \
							c_fract + '\t' + d_fract + '\t' + \
							e_fract + '\t' + f_fract + '\t' + \
							g_fract + '\t' + h_fract + '\t' + \
							i_fract + '\t' + j_fract + '\t' + \
							k_fract + '\t' + l_fract + '\t' + \
							m_fract + '\t' + n_fract + '\t' + \
							o_fract + '\t' + p_fract + '\t' + \
							q_fract + '\t' + r_fract + '\t' + \
							s_fract + '\t' + t_fract + '\t' + \
							u_fract + '\t' + v_fract + '\t' + \
							w_fract + '\t' + x_fract + '\t' + \
							y_fract + '\t' + z_fract + '\n')
				### STRING PROCESSING END ###

				#############################
				#  DINUCLEOTIDE COMPLEXITY  #

				for dinc in compl_list:
					compl_fract[dinc] = 0
					# print dinc

				j = 0
				i = 0
				mooba = "WHATEVER"
				while j < seqs_len-1:
					n_pair = have_seqs[j:j+2]
					# print n_pair
					try:
						compl_fract[n_pair] = compl_fract[n_pair] + 1
						# print n_pair
						i = i + 1
					except:
						booba = mooba
					j = j + 1

				if i == 0:
					i = 1

				out_dinc.write(proper_id + '\t')
				for dinc in compl_list:
					if dinc != "CC":
						out_dinc.write(str(round(compl_fract[dinc]*100.0/i,2)) + '\t')
					if dinc == "CC":
						out_dinc.write(str(round(compl_fract[dinc]*100.0/i,2)) + '\n')

				#     END OF COMPLEXITY     #
				#############################

				# print seqs_len
				gc_fract = float(gc_fract)
				n_fract  = float(n_fract)
				if seqs_len >= min_L and gc_fract <= max_GC and gc_fract >= min_GC and n_fract <= max_N:
					out_good.write('>' + proper_id + ' ' + good_name + '\n')
					out_good.write(have_seqs + '\n')
					out_tab2.write(proper_id + '\t' + `seqs_len` + '\t' + have_seqs + '\n')
					mask_seqs_array[proper_id] = have_seqs
					mask_desc_array[proper_id] = good_name
					mask_lib_array[proper_id] = []
					mask_seqs_list.append(proper_id)
				if seqs_len < min_L or gc_fract > max_GC or gc_fract < min_GC or n_fract > max_N:
					out_bad.write('>' + proper_id + ' ' + good_name + '\n')
					out_bad.write(have_seqs + '\n')
					out_tab3.write(proper_id + '\t' + `seqs_len` + '\t' + have_seqs + '\n')
				if have_seqs != "":
					out_file.write('>' + proper_id + ' ' + good_name + '\n')
					out_file.write(have_seqs + '\n')
					out_tab1.write(proper_id + '\t' + `seqs_len` + '\t' + have_seqs + '\n')
				##########################
			# out_file.write('>' + good_head + ' ' + `line_counter` + ' ' + long_tail + '\n')
			have_seqs = ""
			my_seqs = []
		if fasta_match != ">" and fasta_match != "" and dupl_status == "GOOD":
			proper_id = good_head
			good_name = long_tail
			# have_seqs += t
			my_seqs.append(t)

	a_fract_tot = round((a_tot*100.00/tot_len),2)
	b_fract_tot = round((b_tot*100.00/tot_len),2)
	c_fract_tot = round((c_tot*100.00/tot_len),2)
	d_fract_tot = round((d_tot*100.00/tot_len),2)
	e_fract_tot = round((e_tot*100.00/tot_len),2)
	f_fract_tot = round((f_tot*100.00/tot_len),2)
	g_fract_tot = round((g_tot*100.00/tot_len),2)
	h_fract_tot = round((h_tot*100.00/tot_len),2)
	i_fract_tot = round((i_tot*100.00/tot_len),2)
	j_fract_tot = round((j_tot*100.00/tot_len),2)
	k_fract_tot = round((k_tot*100.00/tot_len),2)
	l_fract_tot = round((l_tot*100.00/tot_len),2)
	m_fract_tot = round((m_tot*100.00/tot_len),2)
	n_fract_tot = round((n_tot*100.00/tot_len),2)
	o_fract_tot = round((o_tot*100.00/tot_len),2)
	p_fract_tot = round((p_tot*100.00/tot_len),2)
	q_fract_tot = round((q_tot*100.00/tot_len),2)
	r_fract_tot = round((r_tot*100.00/tot_len),2)
	s_fract_tot = round((s_tot*100.00/tot_len),2)
	t_fract_tot = round((t_tot*100.00/tot_len),2)
	u_fract_tot = round((u_tot*100.00/tot_len),2)
	v_fract_tot = round((v_tot*100.00/tot_len),2)
	w_fract_tot = round((w_tot*100.00/tot_len),2)
	x_fract_tot = round((x_tot*100.00/tot_len),2)
	y_fract_tot = round((y_tot*100.00/tot_len),2)
	z_fract_tot = round((z_tot*100.00/tot_len),2)

	###
	at_fract_tot = a_fract_tot + t_fract_tot
	gc_fract_tot = g_fract_tot + c_fract_tot
	atgc_fract_tot = a_fract_tot + t_fract_tot + g_fract_tot + c_fract_tot
	atgc_fract_tot = round(atgc_fract_tot,2)
	### STRING ###
	a_fract_tot = str(a_fract_tot) 
	b_fract_tot = str(b_fract_tot) 
	c_fract_tot = str(c_fract_tot) 
	d_fract_tot = str(d_fract_tot) 
	e_fract_tot = str(e_fract_tot) 
	f_fract_tot = str(f_fract_tot) 
	g_fract_tot = str(g_fract_tot) 
	h_fract_tot = str(h_fract_tot) 
	i_fract_tot = str(i_fract_tot) 
	j_fract_tot = str(j_fract_tot) 
	k_fract_tot = str(k_fract_tot) 
	l_fract_tot = str(l_fract_tot) 
	m_fract_tot = str(m_fract_tot) 
	n_fract_tot = str(n_fract_tot) 
	o_fract_tot = str(o_fract_tot) 
	p_fract_tot = str(p_fract_tot) 
	q_fract_tot = str(q_fract_tot) 
	r_fract_tot = str(r_fract_tot) 
	s_fract_tot = str(s_fract_tot) 
	t_fract_tot = str(t_fract_tot) 
	u_fract_tot = str(u_fract_tot) 
	v_fract_tot = str(v_fract_tot) 
	w_fract_tot = str(w_fract_tot) 
	x_fract_tot = str(x_fract_tot) 
	y_fract_tot = str(y_fract_tot) 
	z_fract_tot = str(z_fract_tot) 

	at_fract_tot = str(at_fract_tot)
	gc_fract_tot = str(gc_fract_tot)
	atgc_fract_tot = str(atgc_fract_tot)
	###

	if seq_type == "DNA":
		out_stat.write("#TOTAL" + '\t' + `tot_len` + '\t' + a_fract_tot + '\t' + t_fract_tot + '\t' + \
				g_fract_tot + '\t' + c_fract_tot + '\t' + at_fract_tot + '\t' + gc_fract_tot + '\t' \
				+ atgc_fract_tot + '\t' + 'N: ' + n_fract_tot + '\t' + 'X: ' + x_fract_tot + '\n')
	if seq_type == "prot":
		out_stat.write("#TOTAL" + '\t' + `tot_len` + '\t' + \
				a_fract_tot + '\t' + b_fract_tot + '\t' + \
				c_fract_tot + '\t' + d_fract_tot + '\t' + \
				e_fract_tot + '\t' + f_fract_tot + '\t' + \
				g_fract_tot + '\t' + h_fract_tot + '\t' + \
				i_fract_tot + '\t' + j_fract_tot + '\t' + \
				k_fract_tot + '\t' + l_fract_tot + '\t' + \
				m_fract_tot + '\t' + n_fract_tot + '\t' + \
				o_fract_tot + '\t' + p_fract_tot + '\t' + \
				q_fract_tot + '\t' + r_fract_tot + '\t' + \
				s_fract_tot + '\t' + t_fract_tot + '\t' + \
				u_fract_tot + '\t' + v_fract_tot + '\t' + \
				w_fract_tot + '\t' + x_fract_tot + '\t' + \
				y_fract_tot + '\t' + z_fract_tot + '\n')

	### MASKING ###
	if mask == "mask" and trim != "trim":
		# hit_id_array = {}
		all_hits_f = open(all_hits, "rb")
		while 1:
			r = all_hits_f.readline()
			if r == '':
				break
			if '\n' in r:
				r = r[:-1]
			if '\r' in r:
				r = r[:-1]
			# print r
			r = string.split(r, '\t')
			rl = len(r)
			m_dir = "FOR"
			if rl == 18:
			# if rl == 14:
				id  = r[0]
				mid = r[1]
				hit_direction = r[9]
				vr  = int(r[10])
				vl  = int(r[11])
				if vl < vr:
					ml = vl
					mr = vr
					m_dir = "FOR"
				if vl > vr:
					ml = vr
					mr = vl
					m_dir = "REV"
				mlmr = [ml,mr]
				mask_len = mr - ml + 1
				# hit_id_array[id] = mlmr
				# print id + '\t' + `ml` + '\t' + `mr` + '\t' + `m_dir` \
				#		+ '\t' + `vl` + '\t' + `vr` + '\t' + 'len: ' +  `mask_len`
				# print hit_id_array[id]
				try:
					my_seqs = mask_seqs_array[id]
					my_sub  = my_seqs[ml:mr]
					ms_sub  = mask_char*(mask_len - 1)
					### POLY_A CASE ###
					if mid == "poly_A" and hit_direction == "+/+":
						ms_sub = "a"*(mask_len - 1)
					if mid == "poly_A" and hit_direction == "+/-":
						ms_sub = "t"*(mask_len - 1)
					### END OF POLY_A ###
					if my_sub != ms_sub:
						# print my_sub
						# print ms_sub
						my_seqs = my_seqs.replace(my_sub, ms_sub)
						if mid not in mask_lib_array[id]:
							# mask_lib_array[id] = mask_lib_array[id].append(mid)
							mask_lib_array[id].append(mid)
						mask_seqs_array[id] = my_seqs
						print "APPLYING MASKING FOR SEQUENCE: " + id
						# print my_seqs
					if my_sub == ms_sub:
						# print "ALREADY MASKED"
						# print my_sub
						continue
					
				except:
					# print "SEQS IS OK, NO MASKING FOR: " + id
					continue

		for item in mask_seqs_list:
			mask_flag = "FALSE"
			proper_id  = item
			good_name  = mask_desc_array[proper_id]
			masked_seq = mask_seqs_array[proper_id]
			mx_count   = masked_seq.count(mask_char)
			masked_lib = mask_lib_array[proper_id]
			# masked_lib_len = range(len(masked_lib))
			masked_str = ""
			if masked_lib != []:
				# print masked_lib
				mask_flag = "TRUE"
				for crap in masked_lib:
					# print crap
					masked_str = masked_str + ' ' + crap
			if mask_flag == "TRUE":
				out_mask.write('>' + proper_id + ' ' + good_name + ' [MASKED: ' + masked_str + ']' + '\n')
				out_mask.write(masked_seq + '\n')
				out_mask_list.write(proper_id + '\t' + masked_str + '\t' + `mx_count` + '\n')
			if mask_flag == "FALSE":
				out_mask.write('>' + proper_id + ' ' + good_name + '\n')
				out_mask.write(masked_seq + '\n')


	if mask == "mask" and trim == "trim":
		print "CAN NOT DO MASKING WITH TRIMMING"

	in_file.close()
	out_file.close()
	out_good.close()
	out_bad.close()
	out_stat.close()
	out_tab1.close()
	out_tab2.close()
	out_tab3.close()
	out_dinc.close()
	if mask == "mask" and trim != "trim":
		all_hits_f.close()
		out_mask.close()
		out_mask_list.close()

	print ""
	print " PROCESSING DONE "
	print ""

###### MAIN BODY ######

import math
import re
import sys
import string
if __name__ == "__main__":
	if len(sys.argv) <= 20 or len(sys.argv) > 21:
		print "Program usage: "
		print "[input_file] [output_file] [DNA/prot] [min len] [max N] [min A] [min T] [min G] [min C] [max MA] [max MT] [max MG] [max MC] [anc L] [max GC] [min GC] [MASK] [ALL_HITS] [MASK_CHAR] [TRIM]"
		print "f_in f_out DNA 60 12 20 20 20 20 2 2 2 2 4 80 20 mask all_hits X trim"
		print "Script counts \"ATGC\" content in FASTA file and sorts sequences according to quality"
		exit
	if len(sys.argv) == 21:
		in_name   =     sys.argv[1]
		out_name  =     sys.argv[2]
		seq_type  =     sys.argv[3]
		min_L     = int(sys.argv[4])
		max_N     = int(sys.argv[5])
		min_A     = int(sys.argv[6])
		min_T     = int(sys.argv[7])
		min_G     = int(sys.argv[8])
		min_C     = int(sys.argv[9])
		max_MA    = int(sys.argv[10])
		max_MT    = int(sys.argv[11])
		max_MG    = int(sys.argv[12])
		max_MC    = int(sys.argv[13])
		anc_L     = int(sys.argv[14])
		max_GC    = int(sys.argv[15])
		min_GC    = int(sys.argv[16])
		mask      =     sys.argv[17]
		all_hits  =     sys.argv[18]
		mask_char =     sys.argv[19]
		trim      =     sys.argv[20]

		if min_A < 10:
			print "Poly A must be >= than 10"
			sys.exit()
		if min_T < 10:
			print "Poly T must be >= than 10"
			sys.exit()
		if min_G < 10:
			print "Poly G must be >= than 10"
			sys.exit()
		if min_C < 10:
			print "Poly C must be >= than 10"
			sys.exit()
		# if min_A/max_MA < 10 or min_T/max_MT < 10 or min_G/max_MG < 10 or min_C/max_MC < 10:
		#	print "Only 10% or less mismatch allowed"
		#	sys.exit()
		if anc_L < 4:
			print "Word size must be >= 4"
			sys.exit()
		if in_name != out_name:
			Seqs_Processing(in_name, out_name, seq_type, min_L, max_N, min_A, min_T, min_G, min_C, max_MA, max_MT, max_MG, max_MC, anc_L, max_GC, min_GC, mask, all_hits, mask_char, trim)
		else:
			print "Output should have different name than Input"
			sys.exit()
###### THE END ######
