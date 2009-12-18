#!/usr/bin/tcl

proc Insert_Dummy_Marker {argv} {

    set f_in1 [open [lindex $argv 0] "r"]
    set f_in2 [open [lindex $argv 1] "r"]
    set f_out [open [lindex $argv 2] "w"]

    set n 1
    set m 1
    set k 1
    while {[gets $f_in1 current_line1] >= 0} {
	set lgr [lindex [split $current_line1 "\t"] 0]
	set mid [lindex [split $current_line1 "\t"] 1]
	set pos [lindex [split $current_line1 "\t"] 2]
	set c_4 [lindex [split $current_line1 "\t"] 3]
	set c_5 [lindex [split $current_line1 "\t"] 4]
	puts $f_out "$lgr\t$mid\t$pos\t$c_4\t$c_5\t+++\t$mid\t\*\t$n"
	incr n
	set f_in2 [open [lindex $argv 1] "r"]
	while { [gets $f_in2 current_line2] >= 0 } {
	    set sid [lindex [split $current_line2 "\t"] 0]
	    set pid [lindex [split $current_line2 "\t"] 1]
	    if { $pid == $mid && $sid != $pid } {
		# incr n
		puts $f_out "$lgr\t$sid\t$pos\t$c_4\t$c_5\t---\t$mid\t\*\t$n"
		puts -nonewline "$k\t"
		incr k
		incr n
	    }
	}
	close $f_in2
	puts "$m\t*\t$n"
	incr m
    }

    close $f_in1
    close $f_out
    puts ""
    puts "DONE"
}

if {$argc != 3} {
    puts "Program usage:"
    puts "Map_File, Redundant_Table, output_file"
} else {
    Insert_Dummy_Marker $argv
}
