#!/usr/bin/tclsh

##############################################################
#                                                            #
#                 Tcl/Tk  HAPLO  PARSER                      #
#              COPYRIGHT, Alexander Kozik                    #
#                       June 2014                            #
#                                                            #
##############################################################

	proc Haplo_Parsing {argv} {

		##########################################
		# set hetero_case "TRUE"
		set hetero_case "FALSE"
		##########################################
		set f_in   [open [lindex $argv 0]     "r"]
		
		set f_out1 [open [lindex $argv 1].log "w"]
		set f_out2 [open [lindex $argv 1].axb "w"]
		set f_out3 [open [lindex $argv 1].aub "w"]
		set f_out4 [open [lindex $argv 1].tmp "w"]
		
		set s_above  [lindex $argv 2]
		set s_middle [lindex $argv 3]
		set s_below  [lindex $argv 4]
		set f_column [lindex $argv 5]
		set n_scores [lindex $argv 6]

		# OFF BY 1 #
		set f_column [expr $f_column - 1]
		set l_column [expr $n_scores + $f_column - 1]

		global id_array
		global data_array

		set l 1
		set c 1
		set depth [expr $s_above + $s_middle + $s_below]

		# LOAD DATA INTO MEMORY #
		while {[gets $f_in t] >= 0} {
			set data_line  [split $t "\t"]
			set current_id [lindex $data_line 0]
			if {$l == 1} {
				set id_list [lappend id_list $current_id]
				set id_array($current_id) $c
				set data_array($current_id,$c) $data_line
				incr c
			} else {
				set already_there [lsearch -exact $id_list $current_id]
				if {$already_there < 0} {
					set id_list [lappend id_list $current_id]
					set c 1
				}
				set id_array($current_id) $c
				set data_array($current_id,$c) $data_line
				incr c
			}
			incr l
		}
	# DATA ANALYSIS #
	set n 1
	set m 1
	
	foreach id $id_list {
		set d $id_array($id)
		if {$d >= $depth} {
			
			set p 1
				while {$p <= [ expr $d - $depth + 1 ] } {
					########################
					set haplo_diff_AB 0
					set haplo_diff_BA 0
					# # # # # #  # # # # # #
					set haplo_diff_HB 0
					set haplo_diff_BH 0
					set haplo_diff_HA 0
					set haplo_diff_AH 0
					# # # # # #  # # # # # #
					# set haplo_diff_AHBB  0
					# set haplo_diff_AAHB  0
					# set haplo_diff_BHAA  0
					# set haplo_diff_BBHA  0
					########################
					set haplo_diff_AUB  0
					set haplo_diff_BUA  0
					set haplo_diff_ABB  0
					set haplo_diff_AAB  0
					set haplo_diff_BBA  0
					set haplo_diff_BAA  0
					########################
					set q 1
					set s $f_column
					#########################################################
					# set haplo_diff_Hom [expr $haplo_diff_AB + $haplo_diff_BA]
					# set haplo_diff_Het [expr $haplo_diff_HB + $haplo_diff_BH + $haplo_diff_HA + $haplo_diff_AH]
					# set haplo_diff_All [expr $haplo_diff_Hom + $haplo_diff_Het]
					set diff_coords_S  [lindex $data_array($id,[expr $p + 2]) 1]
					set diff_coords_M  [lindex $data_array($id,[expr $p + 3]) 1]
					set diff_coords_E  [lindex $data_array($id,[expr $p + 3]) 2]
					set transit_length [expr $diff_coords_E - $diff_coords_S + 1]
					set transit_length_M [expr $diff_coords_E - $diff_coords_M + 1]
					#########################################################
					while {$s <= $l_column} {
						set s1 [lindex $data_array($id,[expr $p + 0]) $s]
						set s2 [lindex $data_array($id,[expr $p + 1]) $s]
						set s3 [lindex $data_array($id,[expr $p + 2]) $s]
						set s4 [lindex $data_array($id,[expr $p + 3]) $s]
						set s5 [lindex $data_array($id,[expr $p + 4]) $s]
						set s6 [lindex $data_array($id,[expr $p + 5]) $s]
						###########################
						# COLUMN N HUMAN FRIENDLY #
						set s_off_1 [ expr $s + 1 ]
						###########################
						if { $depth == 6 } {
							### puts $f_out4 "$id $p $q *** $s1 $s2 $s3 $s4 $s5 $s6"
							########################
							#       HAPLO SCAN     #
							if { $s1 == "A" && $s2 == "A" && $s3 == "A" && $s4 == "B" && $s5 == "B" && $s6 == "B" } {
								incr haplo_diff_AB
								puts $f_out4 "$id\t$diff_coords_S\t$diff_coords_E\t$s_off_1\t_AxB_"
							}
							if { $s1 == "B" && $s2 == "B" && $s3 == "B" && $s4 == "A" && $s5 == "A" && $s6 == "A" } {
								incr haplo_diff_BA
								puts $f_out4 "$id\t$diff_coords_S\t$diff_coords_E\t$s_off_1\t_BxA_"
							}
							########################
							if { $s1 == "U" && $s2 == "U" && $s3 == "U" && $s4 == "B" && $s5 == "B" && $s6 == "B" } {
								incr haplo_diff_HB
							}
							if { $s1 == "B" && $s2 == "B" && $s3 == "B" && $s4 == "U" && $s5 == "U" && $s6 == "U" } {
								incr haplo_diff_BH
							}
							if { $s1 == "U" && $s2 == "U" && $s3 == "U" && $s4 == "A" && $s5 == "A" && $s6 == "A" } {
								incr haplo_diff_HA
							}
							if { $s1 == "A" && $s2 == "A" && $s3 == "A" && $s4 == "U" && $s5 == "U" && $s6 == "U" } {
								incr haplo_diff_AH
							}
							######################## NOT IN USE ########################################################
							# if { $s1 == "A" && $s2 == "A" && $s3 == "U" && $s4 == "B" && $s5 == "B" && $s6 == "B" } {}
							#	incr haplo_diff_AHBB
							# {}
							# if { $s1 == "A" && $s2 == "A" && $s3 == "A" && $s4 == "U" && $s5 == "B" && $s6 == "B" } {}
							#	incr haplo_diff_AAHB
							# {}
							# if { $s1 == "B" && $s2 == "B" && $s3 == "U" && $s4 == "A" && $s5 == "A" && $s6 == "A" } {}
							# 	incr haplo_diff_BHAA
							# {}
							# if { $s1 == "B" && $s2 == "B" && $s3 == "B" && $s4 == "U" && $s5 == "A" && $s6 == "A" } {}
							#	incr haplo_diff_BBHA
							# {}
							######################## XXXXXXXXX #########################################################
						}
						########################
						if { $depth == 7 } {
							set s7 [lindex $data_array($id,[expr $p + 6]) $s]
							### puts $f_out4 "$id $p $q *** $s1 $s2 $s3 $s4 $s5 $s6 $s7"
							# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
							if { $s1 == "A" && $s2 == "A" && $s3 == "A" && $s4 == "B" && $s5 == "B" && $s6 == "B" && $s7 == "B"} {
								incr haplo_diff_ABB
							}
							if { $s1 == "A" && $s2 == "A" && $s3 == "A" && $s4 == "A" && $s5 == "B" && $s6 == "B" && $s7 == "B"} {
								incr haplo_diff_AAB
							}
							if { $s1 == "B" && $s2 == "B" && $s3 == "B" && $s4 == "B" && $s5 == "A" && $s6 == "A" && $s7 == "A"} {
								incr haplo_diff_BBA
							}
							if { $s1 == "B" && $s2 == "B" && $s3 == "B" && $s4 == "A" && $s5 == "A" && $s6 == "A" && $s7 == "A"} {
								incr haplo_diff_BAA
							}
							# # # # # 
							if { $s1 == "A" && $s2 == "A" && $s3 == "A" && $s4 == "U" && $s5 == "B" && $s6 == "B" && $s7 == "B"} {
								incr haplo_diff_AUB
								puts $f_out4 "$id\t$diff_coords_M\t$diff_coords_E\t$s_off_1\t_AUB_"
							}
							if { $s1 == "B" && $s2 == "B" && $s3 == "B" && $s4 == "U" && $s5 == "A" && $s6 == "A" && $s7 == "A"} {
								incr haplo_diff_BUA
								puts $f_out4 "$id\t$diff_coords_M\t$diff_coords_E\t$s_off_1\t_BUA_"
							}
							# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
						}
						########################
						incr q
						incr s
					}
					puts -nonewline .
					### puts $f_out4 "  - - - - - - - - - - -  "
					########################################
					set haplo_diff_Hom [expr $haplo_diff_AB + $haplo_diff_BA]
					set haplo_diff_Het [expr $haplo_diff_HB + $haplo_diff_BH + $haplo_diff_HA + $haplo_diff_AH]
					set haplo_diff_All [expr $haplo_diff_Hom + $haplo_diff_Het]
					# set diff_coords_S  [lindex $data_array($id,[expr $p + 2]) 1]
					# set diff_coords_M  [lindex $data_array($id,[expr $p + 3]) 1]
					# set diff_coords_E  [lindex $data_array($id,[expr $p + 3]) 2]
					# set transit_length [expr $diff_coords_E - $diff_coords_S + 1]
					# set transit_length_M [expr $diff_coords_E - $diff_coords_M + 1]
					########################################
					if { $haplo_diff_All >= 1 && $depth == 6 } {
						##############################################################
						puts " >>> $id  $p  Hom:$haplo_diff_Hom  Het:$haplo_diff_Het <<< "
						if { $haplo_diff_Hom >= 1 } {
							puts $f_out2 ">-+=XXXXXXXXXXXXXXXXXXX=+-<"
							set H_mark "XXX"
						}
						if { $haplo_diff_Hom == 0 && $hetero_case == "TRUE"} {
							puts $f_out2 ">-+=HHHHHHHHHHHHHHHHHHH=+-<"
							set H_mark "HHH"
						}
						##########################################
						if { $hetero_case == "TRUE" } {
							puts $f_out1 "$id\t$diff_coords_S\t$diff_coords_E\t$transit_length\t\#\t$haplo_diff_All\t\#\t$haplo_diff_Hom\t$haplo_diff_Het\t###\t$haplo_diff_AB\t$haplo_diff_BA\t$H_mark"
							puts $f_out2 $data_array($id,[expr $p + 0])
							puts $f_out2 $data_array($id,[expr $p + 1])
							puts $f_out2 $data_array($id,[expr $p + 2])
							puts $f_out2 $data_array($id,[expr $p + 3])
							puts $f_out2 $data_array($id,[expr $p + 4])
							puts $f_out2 $data_array($id,[expr $p + 5])
							}
						if { $hetero_case == "FALSE" && $haplo_diff_Hom > 0 } {
							puts $f_out1 "$id\t$diff_coords_S\t$diff_coords_E\t$transit_length\t\#\t$haplo_diff_AB\t$haplo_diff_BA\t###\t$haplo_diff_Hom\t$H_mark"
							puts $f_out2 $data_array($id,[expr $p + 0])
							puts $f_out2 $data_array($id,[expr $p + 1])
							puts $f_out2 $data_array($id,[expr $p + 2])
							puts $f_out2 $data_array($id,[expr $p + 3])
							puts $f_out2 $data_array($id,[expr $p + 4])
							puts $f_out2 $data_array($id,[expr $p + 5])
						}
					}
					########################################
					if { $haplo_diff_AUB > 0 || $haplo_diff_BUA > 0 } {
						set homo_trans_test [expr $haplo_diff_ABB + $haplo_diff_AAB + $haplo_diff_BBA + $haplo_diff_BAA]
						set haplo_diff_U [expr $haplo_diff_AUB + $haplo_diff_BUA] 
						if { $homo_trans_test == 0 } {
							set H_mark "III"
							puts " >>> $id  $p  Trans:$haplo_diff_U <<< "
							puts $f_out1 "$id\t$diff_coords_M\t$diff_coords_E\t$transit_length_M\t\#\t$haplo_diff_AUB\t$haplo_diff_BUA\t###\t$haplo_diff_U\t$H_mark"
							# # # # # # # # # # # # # # # # # # # # # #
							puts $f_out3 ">-+=IIIIIIIIIIIIIIIIIII=+-<"
							puts $f_out3 $data_array($id,[expr $p + 0])
							puts $f_out3 $data_array($id,[expr $p + 1])
							puts $f_out3 $data_array($id,[expr $p + 2])
							puts $f_out3 $data_array($id,[expr $p + 3])
							puts $f_out3 $data_array($id,[expr $p + 4])
							puts $f_out3 $data_array($id,[expr $p + 5])
							puts $f_out3 $data_array($id,[expr $p + 6])
						}
					}
					########################################
					incr p
				}
				### puts $f_out4 " +=< $id  :  $d >=+ "
				### puts $f_out4 "                    "
				### puts $f_out4 " ++++++++++++++++++ "
				puts " <= "
				puts " += $id  :  $d =+ "
			}
		}
	}

#### MAIN BODY #####

puts "$argc arguments entered"

if {$argc != 7} {

	puts "   Program usage:   "
	puts "   TclHaploParser.tcl  \[input\], \[output\], \[Scores_Above(3)\], \[Scores_Middle(1)\], \[Scores_Below(3)\], \[Scores_First_Column(5)\], \[Number_of_Score_Columns(115)\]   "

} else {
	puts $argv
	Haplo_Parsing $argv
}

####  THE END  ####

