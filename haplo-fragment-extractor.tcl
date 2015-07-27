#!/usr/bin/tclsh

##############################################################
#                                                            #
#                 Tcl/Tk  HAPLO  PARSER                      #
#              COPYRIGHT, Alexander Kozik                    #
#                       July 2014                            #
#                                                            #
##############################################################

	proc Haplo_Extractor {argv} {

		set f_in_1 [open [lindex $argv 0]     "r"]
		set f_in_2 [open [lindex $argv 1]     "r"]
		
		set f_out1 [open [lindex $argv 2].log "w"]
		set f_out2 [open [lindex $argv 2].out "w"]

		# DUMMY TEST #
		set x_test [lindex $argv 3]
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
			set data_array($c) "$current_id\t$coords_L\t$coords_R"
			puts -nonewline "$c - "
			incr c
		}
		###########################################################
		puts "                                                    "
		puts " ================================================== "
		set r [ expr $c - 1 ]
		###########################################################
		set m 1
		set q 1
		while {[gets $f_in_2 h] >= 0} {
			set haplo_data [split $h "\t"]
			set cid [lindex $haplo_data 0]
			set pid [lindex $haplo_data 1]
			set q 1
			while { $q <= $r } {
				set current_range $data_array($q)
				set index_data [split $current_range "\t"]
				set qid [lindex $index_data 0]
				set lid [lindex $index_data 1]
				set rid [lindex $index_data 2]
				if { $cid == $qid && $pid >= $lid && $pid <= $rid } {
					puts $f_out2 $haplo_data
				}
				incr q
			}
			incr m
			set m_mod [expr fmod($m,100000)]
			if { $m_mod == 0 } {
				puts $m 
			}
		}
		###########################################################
		close $f_in_1
		close $f_in_2
		close $f_out1
		close $f_out2
		###########################################################
	}

#### MAIN BODY #####

puts "$argc arguments entered"

if {$argc != 4} {

	puts "   Program usage:   "
	puts "   TclHaploFragment.tcl  \[input_coords\], \[input_data\], \[output\], \[Range\]   "

} else {
	puts $argv
	Haplo_Extractor $argv
}

####  THE END  ####



