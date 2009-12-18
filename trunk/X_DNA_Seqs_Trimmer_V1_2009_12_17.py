#!/usr/bin/python

########################
# COPYRIGHT 2003       #
# Alexander Kozik      #
# http://www.atgc.org/ #
# akozik@atgc.org      #
########################

def Seqs_Drobilka(in_name, out_name, seq_type):

	print in_name + ' ' + out_name

	in_file  = open(in_name,  "rb")
	out_file = open(out_name, "wb")
	out_stat = open(out_name + '.stat', "wb")
	out_tab  = open(out_name + '.tab', "wb")
	out_trm  = open(out_name + '.trimmed', "wb")

	seqs_body_array = {}	# ARRAY WITH SEQUENCES
	seqs_head_array = {}	# ARRAY WITH HEADERS

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

	while 1:
		t = in_file.readline()
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
				atgc_fract = round(atgc_fract)
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
			# print seqs_len
			if have_seqs != "":
				out_file.write('>' + proper_id + ' ' + good_name + '\n')
				out_file.write(have_seqs + '\n')
				####  END OF SUB_SEQ  ####
				out_tab.write(proper_id + '\t' + `seqs_len` + '\t' + have_seqs + '\n')
				##########################
				seqs_body_array[proper_id] = have_seqs
				seqs_head_array[proper_id] = good_name
				##########################
				break
		if '\n' in t:
			t = t[:-1]
		if '\r' in t:
			t = t[:-1]

		fasta_match = t[0:1]
		if fasta_match == ">":
			gi_test = t[0:4]
			if gi_test == ">gi|":
				# print gi_test
				descr_line = t
				descr_line = re.sub("^>gi\|", "", descr_line)
				descr_line = re.sub("\|", '\t', descr_line, 1)
				# print line_counter
				line_counter += 1
			else:
				descr_line = t
				descr_line = re.sub("^>", "", descr_line)
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
				atgc_fract = round(atgc_fract)
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
				# print seqs_len
				if have_seqs != "":
					out_file.write('>' + proper_id + ' ' + good_name + '\n')
					out_file.write(have_seqs + '\n')
					####  END OF SUB_SEQ  ####
					out_tab.write(proper_id + '\t' + `seqs_len` + '\t' + have_seqs + '\n')
					##########################
					seqs_body_array[proper_id] = have_seqs
					seqs_head_array[proper_id] = good_name
					##########################
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
	atgc_fract_tot = round(atgc_fract_tot)
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

	#################################################################
	###    TRIMMING 
	for item in fasta_id_array:
		try:
			seq_head = seqs_head_array[item]
			sequence = seqs_body_array[item]
			#########################################
			sequence = re.sub("^t{1,}", "", sequence)		# REMOVE ALL "t" FROM LEFT
			sequence = re.sub("^T{10,}", "", sequence)		# REMOVE ALL "T" FROM LEFT
			sequence = re.sub("^[ATGCNX]{1,30}t{1,}", "", sequence)	# REMOVE ALL "t" FROM LEFT
			sequence = re.sub("^[ATGCNX]{1,30}T{10,}", "", sequence)
			sequence = re.sub("^X{1,}", "", sequence)		# REMOVE ALL "X" FROM LEFT
			sequence = re.sub("^[ATGCNX]{1,30}X{1,}", "", sequence)	# REMOVE ALL "X" FROM LEFT
			sequence = re.sub("^[ATGCNX]{1,30}X{1,}", "", sequence) # REMOVE ALL "X" FROM LEFT AGAIN
			sequence = re.sub("^[ATGCNX]{1,30}t{1,}", "", sequence) # REMOVE ALL "t" FROM LEFT AGAIN
			sequence = re.sub("^[ATGCNX]{1,30}T{10,}", "", sequence)
			sequence = re.sub("X.*", "", sequence)			# REMOVE ALL "X" FROM RIGHT
			sequence = re.sub("a{20,}.*", "", sequence)		# REMOVE ALL "a" FROM RIGHT
			sequence = re.sub("A{20,}.*", "", sequence)
			sequence = re.sub("^N{1,}", "", sequence)		# REMOVE ALL "N" FROM LEFT
			sequence = re.sub("N{1,}$", "", sequence)		# REMOVE ALL "N" FROM RIGHT
			sequence = re.sub("A{10,}[ATGCN][ATGCN][ATGCN][ATGCN][ATGCN][ATGCN]$", "", sequence)
			sequence = re.sub("N{1,}[ATGCN]{1,5}$", "", sequence)
			sequence = re.sub("^[ATGCN]{1,5}N{1,}", "", sequence)
			#########################################
			seq_len  = len(sequence)
			if seq_len >= 100:
				#########################################
				out_trm.write('>' + item + ' ' + seq_head + '\n')
				out_trm.write(sequence + '\n')
				#########################################
		except:
			print item + " DOES NOT EXIST"

	in_file.close()
	out_file.close()
	out_stat.close()
	out_tab.close()
	out_trm.close()

import math
import re
import sys
import string
if __name__ == "__main__":
	if len(sys.argv) <= 3 or len(sys.argv) > 4:
		print ""
		print "Program usage: "
		print "input_file output_file DNA/prot"
		print "Script trims sequences after masking"
		print "and generates tab-delimited file for mySQL db"
		print ""
		sys.exit()
	if len(sys.argv) == 4:
		in_name  = sys.argv[1]
		out_name = sys.argv[2]
		seq_type = sys.argv[3]
		if in_name != out_name:
			Seqs_Drobilka(in_name, out_name, seq_type)
		else:
			print "Output should have different name than Input"
			sys.exit()

