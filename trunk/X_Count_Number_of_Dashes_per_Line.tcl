#!/usr/bin/tcl

proc Process_Tables {argv} {

    set f_in1  [open [lindex $argv 0] "r"]
    set f_out  [open [lindex $argv 1] "w"]
    set n_char [lindex $argv 2]

    if {$n_char == "DASH"} {
	set c_char "-"
    }

    ####### PROCESS FILE LINE BY LINE #######
    set l 0
    while { [gets $f_in1 current_line] >= 0 } {
	set line_length [string length $current_line]
	set trimmed_string $current_line
	### HARD CODED REGEXP ###
	regsub -all {\-} $trimmed_string "" trimmed_string
	#########################
	set trim_length [string length $trimmed_string]
	set string_diff [expr $line_length - $trim_length]
	puts "$string_diff\t$l"
	puts $f_out "$string_diff\t$l"
	incr l
    }
    close $f_in1
    close $f_out

    puts ""
    puts "DONE"
}

if {$argc != 3} {
    puts "Program usage:"
    puts "file_to_process, output_file, DASH"
} else {
    Process_Tables $argv
}

