#!/usr/bin/tcl

proc Process_Tables {argv} {

    set f_in1 [open [lindex $argv 0] "r"]
    set f_in2 [open [lindex $argv 1] "r"]
    set f_out [open [lindex $argv 2] "w"]

    global id_array

    ####### READ LIST OF IDs #######
    set l 0
    while { [gets $f_in2 current_line] >= 0 } {
	set current_data [split   $current_line "\t"]
	set current_id      [lindex  $current_data 0]
	set id_array($current_id) $current_id
	incr l
	puts "$current_id\t***\t$l"
    }
    close $f_in2

    ####### READ LOCUS FILE #######
    set k 0
    set m 0
    set n 0
    while {[gets $f_in1 current_line] >= 0} {
	set current_data [split   $current_line "\t"]
	set current_spp    [lindex  $current_data 0]

	set query_bin [info exists id_array($current_spp)]
	if {$query_bin == 0} {
	    puts "  $current_spp  WAS NOT EXTRACTED ???  *** $k LINES  "
	    incr m
	}
	if {$query_bin == 1} {
	    puts "  $current_spp  WAS     EXTRACTED !!!  *** $k LINES  "
	    puts $f_out $current_line
	    incr n
	}
	incr k
    }

    puts "$m DATAPOINT OUT OF $k WERE NOT EXTRACTED"

    puts "$n  MARKERS WERE EXTRACTED"

    close $f_in1
    close $f_out
    puts ""
    puts "DONE"
}

if {$argc != 3} {
    puts "Program usage:"
    puts "Locus_File, List_of_IDs, output_file"
} else {
    Process_Tables $argv
}

