#!/usr/bin/tcl

proc Sort_GenoType {argv} {

    set f_in1 [open [lindex $argv 0] "r"]
    set f_in2 [open [lindex $argv 1] "r"]
    set f_out [open [lindex $argv 2] "w"]
    set map_column_n [lindex $argv 3]

    set l 1
    set uni_length 0
    while { [gets $f_in2 current_line] >= 0 } {
	set current_data [split $current_line "\t"]
	set data_length  [llength $current_data]
	if { $l == 6 } {
	    set uni_length $data_length
	}
	if { $uni_length == $data_length && $l >= 6 } {
	    puts "LENGTH IS OK: $data_length"
	}
	if { $uni_length != $data_length && $l >= 6 } {
	    puts "LENGTH IS BAD"
	    puts "CHECK LINE: $current_line"
	    break
	}
	if { [lindex $current_data 0] == ";" || [lindex $current_data 0] == ";;" || [lindex $current_data 0] == ";;;" } {
		puts $f_out $current_line
	}
	incr l
	puts " $l  DATA LINES "
    }

    close $f_in2

    set k 1
    while {[gets $f_in1 current_line1] >= 0} {
	# set id1 [lindex [split $current_line1 "\t"] 1]
	set id1 [lindex [split $current_line1 "\t"] $map_column_n]
	set f_in2 [open [lindex $argv 1] "r"]
	while { [gets $f_in2 current_line2] >= 0 } {
	    set id2 [lindex [split $current_line2 "\t"] 0]
	    if { $id1 == $id2 } {
		puts $f_out $current_line2
		puts -nonewline "$k\t"
		incr k
	    }
	}
	close $f_in2
	puts " $k LINES PROCESSED - OUT OF $l "
    }

    close $f_in1
    close $f_out
    puts ""
    puts "DONE"
}

if {$argc != 4} {
    puts "Program usage:"
    puts "Map_File, GenoType_Raw_Data, output_file, map_column_n"
} else {
    Sort_GenoType $argv
}
