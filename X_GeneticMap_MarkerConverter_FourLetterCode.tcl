#!/usr/bin/tcl

proc Process_Tables {argv} {

    set f_in1 [open [lindex $argv 0] "r"]
    set f_in2 [open [lindex $argv 1] "r"]
    set f_out [open [lindex $argv 2] "w"]

    global conv_array

    ####### READ CONVERSION ID INFO TABLE INTO MEMORY #######
    set l 0
    while { [gets $f_in1 current_line] >= 0 } {
	set current_data     [split   $current_line "\t"]
	set current_old_id   [lindex  $current_data 0]
	set current_new_id   [lindex  $current_data 1]
	set conv_array($current_new_id) $current_old_id
	incr l
	set k_mod [expr fmod($l,100)]
	if { $k_mod == 0 } {
		puts " $l  $current_old_id  $current_new_id "
	}
    }
    close $f_in1
    puts " $l  ID PAIRS WERE LOADED "
    after 2000

    ####### READ CEL FILE WITH DATA TO EXTRACT #######
    set k 0
    set m 0
    while {[gets $f_in2 current_line] >= 0} {

	set current_data [split   $current_line "\t"]
	set current_id   [lindex  $current_data 1]

	set current_4X [string range $current_id 0 3]

	set query_id [info exists conv_array($current_4X)]
	if {$query_id == 0} {
		puts "  $current_id  WAS NOT FOUND !!!  *** $k LINES  "
		set old_id "XXX_XXX_XXX"
	    incr m
	}
	if {$query_id == 1} {
		puts "  $current_id  WAS     FOUND +++  *** $k LINES  "
		set old_id $conv_array($current_4X)
	}
        puts $f_out "$current_line\t***\t$old_id"
	incr k
    }

    puts "$m DATAPOINT OUT OF $k WERE NOT EXTRACTED"

    close $f_in2
    close $f_out
    puts ""
    puts "DONE"
}

if {$argc != 3} {
    puts "Program usage:"
    puts "ConversionTable, MAP_Table_Tab, output_file"
} else {
    Process_Tables $argv
}

