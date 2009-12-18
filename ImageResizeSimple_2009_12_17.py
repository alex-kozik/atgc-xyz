#!/usr/bin/python

########################
# COPYRIGHT 2004       #
# Alexander Kozik      #
# http://www.atgc.org/ #
# akozik@atgc.org      #
########################

def Image_Drobilka(in_name, out_name, x_size, y_size):

	print in_name
	print out_name
	print x_size
	print y_size

	im = Image.open(in_name)
	width, height = im.size
	print in_name, width, height

	im = im.resize((x_size, y_size),Image.ANTIALIAS)
	im = im.filter(ImageFilter.SHARPEN)

	im.save(out_name, im.format)


# import math
# import re
import sys
import string
import Image
import ImageFilter
if __name__ == "__main__":
	if len(sys.argv) <= 4 or len(sys.argv) > 5:
		print "Program usage: "
		print "[input_file] [output_file] [X_Size] [Y_Size]"
		print "Script resizes an image"
		exit
	if len(sys.argv) == 5:
		in_name   = sys.argv[1]
		out_name  = sys.argv[2]
		x_size    = int(sys.argv[3])
		y_size    = int(sys.argv[4])
		
		if in_name != out_name:
			Image_Drobilka(in_name, out_name, x_size, y_size)
		else:
			print "Output should have different name than Input"
			exit
