#!/usr/bin/tcl

proc Search_Seqs { argv } {

    global fragm_array

    set f_in1 [open [lindex $argv 0] "r"]
    set f_in2 [open [lindex $argv 1] "r"]
    set f_out [open [lindex $argv 2] "w"]
    set f_sql [open [lindex $argv 3] "w"]
    set xsearch  [lindex $argv 4]

    if {$xsearch != "SEARCH"} {
	set oo 1
	while {$oo <= 10000} {
	    puts " BAD BAD BAD ... $oo "
	    after 1000
	    incr oo
	}
    }

    ### AFFY PROBE FILE
    set k 1
    while {[gets $f_in1 current_line] >= 0} {
	set current_data [split $current_line "\t"]
	set fr  [lindex $current_data 0] 
	# set fr  [lindex $current_data 1]
	set fragm_array($k) [string toupper $fr]
	set data_array($k) $current_line
	set k_mod [expr fmod($k,10000)]
	if {$k_mod == 0} {
	    puts "$k\t$fr"
	}
	incr k
    }
    set n [expr $k - 1]

    puts "STEP 1 DONE"
    after 2000

    set id_list ""

    ### DNA FILE 
    set m 1
    while {[gets $f_in2 current_line] >= 0} {
	set current_data [split $current_line "\t"]
	set id  [lindex $current_data 0]
	set seq_len [lindex $current_data 1]
	set seq [lindex $current_data 2]
	set seq_array($id) [string toupper $seq]
	set already_done [lsearch -exact $id_list $id]
	#####
	if {$seq_len >= 100} {
		#####
		if {$already_done < 0} {
	    		set id_list [lappend id_list $id]
		}
		if {$already_done >= 0} {
	    		puts "========================="
	    		puts " DUPLICATION ... FOR $id "
	    		puts "========================="
	    		after 5000
	    		puts ""
		}
		set m_mod [expr fmod($m,100)]
		if {$m_mod == 0} {
	    		puts "$m\t$id"
		}
		incr m
	}
    }

    puts "STEP 2 DONE"
    puts "$m  SEQUENCES LOADED"
    after 5000

    set l 1
    while { $l <= $n } {
	set q 0
	set u 0
	set t 0
	set dupl_status "_UNKNOWN_"
	set found_list ""
	set found_ids  ""
	set step [string length $fragm_array($l)]
	# puts "$l\t$fragm_array($l)"
	foreach id $id_list {
	    set t 0
	    while { $t < [string length $seq_array($id)] } {
		set find_me [string first $fragm_array($l) $seq_array($id) $t]
		if { $find_me != -1 } {
		    incr q
		    set t [expr $find_me + $step]
		    # puts "$l\t$fragm_array($l)\t$id\t$find_me\t$q"
		    # set found_list [lappend found_list $id]
		    set find_me1 [expr $find_me + 1]
		    set found_list [lappend found_list " \[$id\:$find_me1\] "]
		    set already_done [lsearch -exact $found_ids $id]
		    if {$already_done < 0} {
			set found_ids [lappend found_ids $id]
		    }
		    # set dupl_status "DUPLICATED" 
		}
		if { $find_me == -1 } {
		    set t [string length $seq_array($id)]
		}
	    }
	}
	set u [llength $found_ids]
	if {$q == 1} {
	    set dupl_status "SINGLETON"
	}
	if {$q > 1 && $u == 1} {
            set dupl_status "DUPL_CASE1"
        }
	if {$q > 1 && $u > 1 && $q == $u} {
            set dupl_status "DUPL_CASE2"
        }
	if {$q > 1 && $u > 1 && $q != $u} {
	    set dupl_status "DUPL_CASE3"
	}
	puts "$l\t$fragm_array($l)\t$q\t$u\t$dupl_status"
	puts $f_out "$l\t$data_array($l)\t\*\*\*\t$q\t$u\t\*\*\*\t$found_list\t\*\*\*\t$dupl_status"

	#####
	if { $dupl_status != "_UNKNOWN_" } {
		set h 1
		foreach match_list $found_list {
			puts $f_sql "$l\t$data_array($l)\t\*\*\*\t$match_list\t$dupl_status\t$q\t$u\t$h"
			incr h
		}
	}
	#####

	incr l
	set q 0
    }

    puts "STEP 3 DONE"
    after 1000

    close $f_in1
    close $f_in2
    close $f_out
    close $f_sql
}

puts "$argc arguments entered"

if {$argc != 5} {
	puts ""
	puts "Program usage:"
	puts "f_in1\(fr_db\)  f_in2\(seq_db\)  f_out  f_sql  SEARCH"
} else {
	puts ""
	puts $argv
	Search_Seqs $argv
}



### THE END ###
