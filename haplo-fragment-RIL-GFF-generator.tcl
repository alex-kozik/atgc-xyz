#!/usr/bin/tclsh

##############################################################
#                                                            #
#                 Tcl/Tk  HAPLO  PARSER                      #
#              COPYRIGHT, Alexander Kozik                    #
#                    December 2014                           #
#                                                            #
##############################################################

	proc Haplo_Extractor {argv} {

		set f_in_1 [open [lindex $argv 0]     "r"]
		set f_in_2 [open [lindex $argv 1]     "r"]
		set f_in_3 [open [lindex $argv 2]     "r"]
		
		set f_out1 [open [lindex $argv 3].gff "w"]
		set f_out2 [open [lindex $argv 3].out "w"]

		# DUMMY TEST #
		set x_test [lindex $argv 4]
		if { $x_test != "Range" } {
			set mooba 'booba'
			exit
		}

		global data_array
		set c 1
		# LOAD DATA INTO MEMORY #
		while {[gets $f_in_1 t] >= 0} {
			set data_line  [split $t "\t"]
			set current_id [lindex $data_line 0]
			set coords_L   [lindex $data_line 1]
			set coords_R   [lindex $data_line 2]
			set column_N   [lindex $data_line 3]
			set group_ID   [lindex $data_line 4]
			set data_array($c) "$current_id\t$coords_L\t$coords_R\t$column_N\t$group_ID"
			puts -nonewline "$c - "
			incr c
		}
		###########################################################
		global conversion_array
		# LOAD DATA INTO MEMORY #
		while {[gets $f_in_2 r] >= 0} {
			set conv_line [split $r "\t"]
			set column_id [lindex $conv_line 0]
			set ril_id    [lindex $conv_line 1]
			set conversion_array($column_id) $ril_id
		}
		###########################################################
		puts "                                                    "
		puts " ================================================== "
		set r [ expr $c - 1 ]
		set column_offset 1
		###########################################################
		set m 1
		set q 1
		while {[gets $f_in_3 h] >= 0} {
			set haplo_data [split $h " "]
			set cid [lindex $haplo_data 0]
			set pid [lindex $haplo_data 1]
			set q 1
			while { $q <= $r } {
				set current_range $data_array($q)
				set index_data [split $current_range "\t"]
				set qid [lindex $index_data 0]
				set lid [lindex $index_data 1]
				set rid [lindex $index_data 2]
				set col [lindex $index_data 3]
				set trn [lindex $index_data 4]
				if { $cid == $qid && $pid >= $lid && $pid <= $rid } {
					set ril [expr $col + $column_offset]
					set genotype_call [lindex $haplo_data $ril]
					set real_ril $conversion_array($col)
					set pid_off_1 [expr $pid + 1]
					puts $f_out1 "$cid\tX_Region\t$real_ril\t$pid\t$pid_off_1\t\.\t\.\t\.\tName\=$genotype_call\;"
					# puts $f_out2 "$cid\t$pid\t$col\t$trn\t$genotype_call"
					puts $f_out2 "$cid\t$pid\t$real_ril\t$trn\t$genotype_call"
				}
				incr q
			}
			incr m
			set m_mod [expr fmod($m,1000)]
			if { $m_mod == 0 } {
				puts $m 
			}
		}
		###########################################################
		close $f_in_1
		close $f_in_2
		close $f_in_3
		close $f_out1
		close $f_out2
		###########################################################
	}

#### MAIN BODY #####

puts "$argc arguments entered"

if {$argc != 5} {

	puts "   Program usage:   "
	puts "   TclHaploFragment.tcl  \[input_coords\], \[column_conversion_table\], \[input_data\], \[output\], \[Range\]   "

} else {
	puts $argv
	Haplo_Extractor $argv
}

####  THE END  ####

