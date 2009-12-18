#!/usr/bin/tcl

proc Insert_Dummy_Marker {argv} {

    set f_in1 [open [lindex $argv 0] "r"]
    set f_in2 [open [lindex $argv 1] "r"]
    set f_out [open [lindex $argv 2] "w"]
    set max_n [lindex $argv 3]

    set m 1
    set k 1
    while {[gets $f_in1 current_line1] >= 0} {
	set lgr [lindex [split $current_line1 "\t"] 15]
	set grt [lindex [split $current_line1 "\t"] 16]
	set ndt [lindex [split $current_line1 "\t"] 17]
	set xgr [lindex [split $current_line1 "\t"] 24]
	set mid [lindex [split $current_line1 "\t"] 25]
	set sca [lindex [split $current_line1 "\t"] 27]
	set scb [lindex [split $current_line1 "\t"] 28]
	set pos [lindex [split $current_line1 "\t"] 31]
	set mhd [string range $mid 0 3]
	set scx [expr $sca + $scb]
	set msc [expr $max_n - $scx]
	if { $msc < 10 } {
	    set msd "0$msc"
	}
	if { $msc >= 10 } {
	    set msd "$msc"
	}
	# puts $f_out "$lgr\t$mid\t$pos\t*\t$sca\t$scb\t$scx\t$mhd\t+++\t$mid"
	puts $f_out "$lgr\t$mhd\t$msd\t$mid\t$pos\t*\t$sca\t$scb\t$scx\t+++\t$mid\t$grt\t$ndt\t$xgr"
	set f_in2 [open [lindex $argv 1] "r"]
	while { [gets $f_in2 current_line2] >= 0 } {
	    set sid [lindex [split $current_line2 "\t"] 0]
	    set pid [lindex [split $current_line2 "\t"] 1]
	    set shd [string range $sid 0 3]
	    if { $pid == $mid && $sid != $pid } {
		# puts $f_out "$lgr\t$sid\t$pos\t*\t$sca\t$scb\t$scx\t$shd\t---\t$mid"
		puts $f_out "$lgr\t$shd\t$msd\t$sid\t$pos\t*\t$sca\t$scb\t$scx\t---\t$mid\t$grt\t$ndt\t$xgr"
		puts -nonewline "$k\t"
		incr k
	    }
	}
	close $f_in2
	puts $m
	incr m
    }

    close $f_in1
    close $f_out
    puts ""
    puts "DONE"
}

if {$argc != 4} {
    puts "Program usage:"
    puts "TreeClust_File, Redundant_Table, output_file, max_score"
} else {
    Insert_Dummy_Marker $argv
}
