#!/usr/bin/tcl

proc Process_Tables {argv} {

    set f_in1 [open [lindex $argv 0] "r"]
    set f_out [open [lindex $argv 1] "w"]
    set n_mod [lindex $argv 2]

    global xy_coord_array

    ####### READ SEQ INFO TABLE INTO MEMORY #######
    set l 0
    while { [gets $f_in1 current_line] >= 0 } {
	set current_data [split   $current_line "\t"]
	set k_mod [expr fmod($l,$n_mod)]
	if { $k_mod == 0 } {
		puts $l
		# puts $f_out $current_data
		puts $f_out $current_line
	}
	incr l
    }
    close $f_in1

    puts ""
    puts "DONE"
}

if {$argc != 3} {
    puts "Program usage:"
    puts "file_to_process, output_file, n_mod"
} else {
    Process_Tables $argv
}

