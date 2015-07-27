#!/usr/bin/tclsh

##############################################################
#                                                            #
#                 Tcl/Tk  HAPLO  PARSER                      #
#              COPYRIGHT, Alexander Kozik                    #
#                     October 2014                           #
#                                                            #
##############################################################

	proc Range_Finder {argv} {

		set f_in_1 [open [lindex $argv 0]     "r"]
		set f_out1 [open [lindex $argv 1].log "w"]
		set f_out2 [open [lindex $argv 1].out "w"]

		# DUMMY TEST #
		set x_test [lindex $argv 2]
		if { $x_test != "Range" } {
			set mooba 'booba'
			exit
		}

		global data_array
		set c 1
		# LOAD DATA INTO MEMORY #
		while {[gets $f_in_1 t] >= 0} {
			set data_line  [split $t "\t"]
			set scaffold_ID [lindex $data_line 0]
			set coords_X   [lindex $data_line 1]
			set column_N   [lindex $data_line 2]
			set group_ID   [lindex $data_line 3]
			set genotype   [lindex $data_line 4]
			set data_array($c) "$scaffold_ID\t$coords_X\t$column_N\t$group_ID\t$genotype"
			puts -nonewline "$c - "
			incr c
		}
		###########################################################
		puts "                                                    "
		puts " ================================================== "
		set r [ expr $c - 1 ]
		###########################################################
		set q 1
		set A A
		set B B
		while { $q <= $r } {
			if { $q >= 6 } {
				set q1 [expr $q - 0]
				set q2 [expr $q - 1]
				set q3 [expr $q - 2]
				set p1 [expr $q - 3]
				set p2 [expr $q - 4]
				set p3 [expr $q - 5]
				set current_data1  $data_array($q1)
				set current_data2  $data_array($q2)
				set current_data3  $data_array($q3)
				set previous_line1 $data_array($p1)
				set previous_line2 $data_array($p2)
				set previous_line3 $data_array($p3)
				set index_data_Q1 [split $current_data1  "\t"]
				set index_data_P1 [split $previous_line1 "\t"]
				set index_data_Q2 [split $current_data2  "\t"]
				set index_data_P2 [split $previous_line2 "\t"]
				set index_data_Q3 [split $current_data3  "\t"]
				set index_data_P3 [split $previous_line3 "\t"]
				# CURRENT DATA #
				set sid_Q1 [lindex $index_data_Q1 0]
				set snp_Q1 [lindex $index_data_Q1 1]
				set ril_Q1 [lindex $index_data_Q1 2]
				set trn_Q1 [lindex $index_data_Q1 3]
				set dna_Q1 [lindex $index_data_Q1 4]
				#
				set sid_Q2 [lindex $index_data_Q2 0]
				set snp_Q2 [lindex $index_data_Q2 1]
				set ril_Q2 [lindex $index_data_Q2 2]
				set trn_Q2 [lindex $index_data_Q2 3]
				set dna_Q2 [lindex $index_data_Q2 4]
				#
				set sid_Q3 [lindex $index_data_Q3 0]
				set snp_Q3 [lindex $index_data_Q3 1]
				set ril_Q3 [lindex $index_data_Q3 2]
				set trn_Q3 [lindex $index_data_Q3 3]
				set dna_Q3 [lindex $index_data_Q3 4]
				# PREVIOUS LINE #
				set sid_P1 [lindex $index_data_P1 0]
				set snp_P1 [lindex $index_data_P1 1]
				set ril_P1 [lindex $index_data_P1 2]
				set trn_P1 [lindex $index_data_P1 3]
				set dna_P1 [lindex $index_data_P1 4]
				#
				set sid_P2 [lindex $index_data_P2 0]
				set snp_P2 [lindex $index_data_P2 1]
				set ril_P2 [lindex $index_data_P2 2]
				set trn_P2 [lindex $index_data_P2 3]
				set dna_P2 [lindex $index_data_P2 4]
				#
				set sid_P3 [lindex $index_data_P3 0]
				set snp_P3 [lindex $index_data_P3 1]
				set ril_P3 [lindex $index_data_P3 2]
				set trn_P3 [lindex $index_data_P3 3]
				set dna_P3 [lindex $index_data_P3 4]
				## CASE AAABBB ##
				if { $sid_Q1 == $sid_P3 && $ril_Q1 == $ril_P3 && $trn_Q1 == $trn_P3 && $dna_Q1 == $A && $dna_Q2 == $A && $dna_Q3 == $A && $dna_P1 == $B && $dna_P2 == $B && $dna_P3 == $B} {
					puts $index_data_P1
					puts $index_data_Q3
					puts $f_out1 "$index_data_P3 *** $index_data_P1"
					puts $f_out1 "$index_data_Q3 *** $index_data_Q1"
					set trn_L [expr $snp_Q3 - $snp_P1 + 1 ]
					puts $f_out2 "$sid_Q1\t$snp_P1\t$snp_Q3\t$trn_L\t$dna_P1\t$dna_Q3\t$ril_Q1\t$trn_Q1\tAAABBB"
				}
				## CASE BBBAAA ###
				if { $sid_Q1 == $sid_P3 && $ril_Q1 == $ril_P3 && $trn_Q1 == $trn_P3 && $dna_Q1 == $B && $dna_Q2 == $B && $dna_Q3 == $B && $dna_P1 == $A && $dna_P2 == $A && $dna_P3 == $A} {
					puts $index_data_P1
					puts $index_data_Q3
					puts $f_out1 "$index_data_P3 *** $index_data_P1"
					puts $f_out1 "$index_data_Q3 *** $index_data_Q1"
					set trn_L [expr $snp_Q3 - $snp_P1 + 1 ]
					puts $f_out2 "$sid_Q1\t$snp_P1\t$snp_Q3\t$trn_L\t$dna_P1\t$dna_Q3\t$ril_Q1\t$trn_Q1\tBBBAAA"
				}
				if { $sid_Q1 == $sid_P3 && $ril_Q1 != $ril_P3 } {
					puts " .                                                    . "
					puts $f_out1 " .                                                    . "
				}
				if { $sid_Q1 != $sid_P3 } {
					puts " ====================================================== "
					puts $f_out1 " ====================================================== "
					puts $f_out2 " ====================================================== "
				}
			}
			incr q
		}
		###########################################################
		close $f_in_1
		close $f_out1
		close $f_out2
		###########################################################
	}

#### MAIN BODY #####

puts "$argc arguments entered"

if {$argc != 3} {

	puts "   Program usage:   "
	puts "   TclHaploFragment.tcl  \[input_haplo_table\], \[output\], \[Range\]   "

} else {
	puts $argv
	Range_Finder $argv
}

####  THE END  ####

