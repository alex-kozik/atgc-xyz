#!/usr/bin/tcl

proc Sort_Table {argv} {

    set f_in1 [open [lindex $argv 0] "r"]
    set q_len [lindex $argv 1]
    set f_out [open [lindex $argv 2] "w"]

    global q_array_all
    global q_array_a
    global q_array_b
    global q_array_c
    global q_array_d
    global q_array_f
    global q_array_x

    ### HEADER OUT FILE ###

    puts $f_out "\#\tA_abs\tB_abs\tC_abs\tD_abs\tF_abs\tX_abs\tALL_abs\t\*\*\*\tABCD\tALL_sum\t\*\*\*\tA_fr\tB_fr\tC_fr\tD_fr\tF_fr\tX_fr\tALL_fr\t\*\*\*\tABCD_fr\tFX_fr\tALL_fr"

    ####### SET ZERO FOR DATAPOINTS ######

    set q 0
    while { $q < $q_len } {
	set q_array_all($q) 0
	set q_array_a($q)   0
	set q_array_b($q)   0
	set q_array_c($q)   0
	set q_array_d($q)   0
	set q_array_f($q)   0
	set q_array_x($q)   0
	incr q
    }

    ####### READ TABLE INTO MEMORY #######
    set l 1
    while { [gets $f_in1 current_line] >= 0 } {
	set current_line [string toupper $current_line]
	set current_data [split   $current_line ""]
	set data_length  [llength $current_data]
	set k 0
	if { [lindex $current_data 0] != ">" && $data_length >= 24 } {
	    while { $k < $data_length } {
		set current_q   [lindex  $current_data $k]
		incr q_array_all($k)
		if { $current_q == "A" } {
			incr q_array_a($k)
		}
		if { $current_q == "B" } {
                        incr q_array_b($k)
                }
		if { $current_q == "C" } {
                        incr q_array_c($k)
                }
		if { $current_q == "D" } {
                        incr q_array_d($k)
                }
		if { $current_q == "F" } {
                        incr q_array_f($k)
                }
		if { $current_q == "X" } {
                        incr q_array_x($k)
                }
		incr k 
	    }
	    incr l
	    set l_mod [expr fmod($l,1000)]
	    if { $l_mod == 0 } {
		puts " ...  $l  ... "
		puts $current_data
	    }
	}
    }
    close $f_in1

    set n 0
    while { $n < $q_len } {

	set abcd_sum [expr $q_array_a($n) + $q_array_b($n) + $q_array_c($n) + $q_array_d($n)]
	set fx_sum   [expr $q_array_f($n) + $q_array_x($n)]

	### FRACTION CALCULATION ###
	set a_fract [expr int(round($q_array_a($n)*100.00/$q_array_all($n)))]
	set b_fract [expr int(round($q_array_b($n)*100.00/$q_array_all($n)))]
	set c_fract [expr int(round($q_array_c($n)*100.00/$q_array_all($n)))]
	set d_fract [expr int(round($q_array_d($n)*100.00/$q_array_all($n)))]
	set f_fract [expr int(round($q_array_f($n)*100.00/$q_array_all($n)))]
	set x_fract [expr int(round($q_array_x($n)*100.00/$q_array_all($n)))]

	set abcd_fract [expr int(round($abcd_sum*100.00/$q_array_all($n)))]
	set fx_fract [expr int(round($fx_sum*100.00/$q_array_all($n)))]

	set q_sum [expr $q_array_a($n) + $q_array_b($n) + $q_array_c($n) + $q_array_d($n) + $q_array_f($n) + $q_array_x($n)]

	set all_fract [expr int(round($q_sum*100.00/$q_array_all($n)))] 

	puts $f_out "$n\t$q_array_a($n)\t$q_array_b($n)\t$q_array_c($n)\t$q_array_d($n)\t$q_array_f($n)\t$q_array_x($n)\t$q_array_all($n)\t\*\*\*\t$abcd_sum\t$q_sum\t\*\*\*\t$a_fract\t$b_fract\t$c_fract\t$d_fract\t$f_fract\t$x_fract\t$all_fract\t\*\*\*\t$abcd_fract\t$fx_fract\t$all_fract"
	puts "$n\t$q_array_a($n)\t$q_array_b($n)\t$q_array_c($n)\t$q_array_d($n)\t$q_array_f($n)\t$q_array_x($n)\t$q_array_all($n)\t\*\*\*\t$abcd_sum\t$q_sum\t\*\*\*\t$a_fract\t$b_fract\t$c_fract\t$d_fract\t$f_fract\t$x_fract\t$all_fract\t\*\*\*\t$abcd_fract\t$fx_fract\t$all_fract"
	incr n
    }

    close $f_out
    puts ""
    puts "DONE"
}

if {$argc != 3} {
    puts "Program usage:"
    puts "Quality_File, Total_Length, output_file"
} else {
    Sort_Table $argv
}

