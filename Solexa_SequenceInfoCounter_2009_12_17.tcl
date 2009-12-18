#!/usr/bin/tcl

proc Sort_Table {argv} {

    set f_in1 [open [lindex $argv 0] "r"]
    set q_len [lindex $argv 1]
    set f_out [open [lindex $argv 2] "w"]

    global q_array_all
    global q_array_a
    global q_array_t
    global q_array_g
    global q_array_c
    global q_array_n
    global q_array_x
    global q_array_z

    ### HEADER OUT FILE ###

    puts $f_out "\#\tA_abs\tT_abs\tG_abs\tC_abs\tN_abs\tX_abs\tZ_abs\tALL_abs\t\*\*\*\tALL_sum\t\*\*\*\tA_fr\tT_fr\tG_fr\tC_fr\tATGC\tAT\tGC\tNXZ\tALL_fr"

    ####### SET ZERO FOR DATAPOINTS ######

    set q 0
    while { $q < $q_len } {
	set q_array_all($q) 0
	set q_array_a($q)   0
	set q_array_t($q)   0
	set q_array_g($q)   0
	set q_array_c($q)   0
	set q_array_n($q)   0
	set q_array_x($q)   0
	set q_array_z($q)   0
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
		if { $current_q == "T" } {
                        incr q_array_t($k)
                }
		if { $current_q == "G" } {
                        incr q_array_g($k)
                }
		if { $current_q == "C" } {
                        incr q_array_c($k)
                }
		if { $current_q == "N" } {
                        incr q_array_n($k)
                }
		if { $current_q == "X" } {
                        incr q_array_x($k)
                }
		if { $current_q == "*" } {
                        incr q_array_z($k)
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

	set a_fract [expr int(round($q_array_a($n)*100.00/$q_array_all($n)))]
	set t_fract [expr int(round($q_array_t($n)*100.00/$q_array_all($n)))]
	set g_fract [expr int(round($q_array_g($n)*100.00/$q_array_all($n)))]
	set c_fract [expr int(round($q_array_c($n)*100.00/$q_array_all($n)))]
	set n_fract [expr int(round($q_array_n($n)*100.00/$q_array_all($n)))]
	set x_fract [expr int(round($q_array_x($n)*100.00/$q_array_all($n)))]
	set z_fract [expr int(round($q_array_z($n)*100.00/$q_array_all($n)))]

	set q_sum [expr $q_array_a($n) + $q_array_t($n) + $q_array_g($n) + $q_array_c($n) + $q_array_n($n) + $q_array_x($n) + $q_array_z($n)]

	set atgc_sum [expr $q_array_a($n) + $q_array_t($n) + $q_array_g($n) + $q_array_c($n)]
	set nxz_sum  [expr $q_array_n($n) + $q_array_x($n) + $q_array_z($n)]

	set at_sum [expr $q_array_a($n) + $q_array_t($n)]
	set gc_sum [expr $q_array_g($n) + $q_array_c($n)]

	set all_fract [expr int(round($q_sum*100.00/$q_array_all($n)))]

	set at_fract [expr int(round($at_sum*100.00/$q_array_all($n)))]
	set gc_fract [expr int(round($gc_sum*100.00/$q_array_all($n)))]

	set atgc_fract [expr int(round($atgc_sum*100.00/$q_array_all($n)))]
	set nxz_fract [expr int(round($nxz_sum*100.00/$q_array_all($n)))]

	puts $f_out "$n\t$q_array_a($n)\t$q_array_t($n)\t$q_array_g($n)\t$q_array_c($n)\t$q_array_n($n)\t$q_array_x($n)\t$q_array_z($n)\t$q_array_all($n)\t\*\*\*\t$q_sum\t\*\*\*\t$a_fract\t$t_fract\t$g_fract\t$c_fract\t$atgc_fract\t$at_fract\t$gc_fract\t$nxz_fract\t$all_fract"
	puts "$n\t$q_array_a($n)\t$q_array_t($n)\t$q_array_g($n)\t$q_array_c($n)\t$q_array_n($n)\t$q_array_x($n)\t$q_array_z($n)\t$q_array_all($n)\t\*\*\*\t$q_sum\t\*\*\*\t$a_fract\t$t_fract\t$g_fract\t$c_fract\t$atgc_fract\t$at_fract\t$gc_fract\t$nxz_fract\t$all_fract"
	incr n
    }

    close $f_out
    puts ""
    puts "DONE"
}

if {$argc != 3} {
    puts "Program usage:"
    puts "Sequence_File, Total_Length, output_file"
} else {
    Sort_Table $argv
}

