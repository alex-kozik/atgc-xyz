#!/usr/bin/python

########################
# COPYRIGHT 2004       #
# Alexander Kozik      #
# http://www.atgc.org/ #
# akozik@atgc.org      #
########################

def Image_Resize(in_type, out_type, x_size, y_size):

	print in_type
	print out_type
	print x_size
	print y_size

	# all_cats = glob.glob("*" + "." + in_type)

	all_cats = glob.glob("*")

	print all_cats

	for cat in all_cats:

		in_name = cat
		in_name_fixed = re.sub(' ', "", in_name)
		cat_split = in_name_fixed.split(".")
		cat_len = len(cat_split)
		cats_tail = cat_split[cat_len-1]
		print cats_tail
		cats_tail = cats_tail.lower()
		if cats_tail == in_type:
			out_name1 = in_name_fixed[0:-4] + '.' + out_type
			out_name2 = in_name_fixed[0:-4] + '.small.' + out_type
			print out_name1 + '\t' + out_name2

			im = Image.open(in_name)
			width, height = im.size
			print in_name, width, height

			x_size_new = width
			y_size_new = height

			if width > x_size or height > y_size:

				if width >= height:
					z_comp   = x_size*1.0/width
				if height > width:
					z_comp   = y_size*1.0/height

				x_size_new = int(round(width*z_comp))
				y_size_new = int(round(height*z_comp))

			print im.format, im.mode
			im = im.convert("RGB")
			im.save("processed_images/" + out_name1, "JPEG")
			im = im.resize((x_size_new, y_size_new),Image.ANTIALIAS)
			# im.save("processed_images/" + out_name2, im.format)
			im.save("processed_images/" + out_name2, "JPEG")

		else:
			print cats_tail + '\t' + "SKIPPED"

	print "DONE!"

import re
import sys
import glob
import Image

if __name__ == "__main__":
	if len(sys.argv) <= 4 or len(sys.argv) > 5:
		print "Program usage: "
		print "[input_type] [output_type] [X_Size] [Y_Size]"
		print "Script resizes image(s)"
		print "processed images will be written into directory \"processed_images\""
		sys.exit()
	if len(sys.argv) == 5:
		in_type   = sys.argv[1]
		out_type  = sys.argv[2]
		x_size    = int(sys.argv[3])
		y_size    = int(sys.argv[4])
		
		Image_Resize(in_type, out_type, x_size, y_size)
