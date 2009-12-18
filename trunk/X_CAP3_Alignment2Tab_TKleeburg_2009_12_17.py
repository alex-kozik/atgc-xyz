def cap3_alignment(input_file, output_file):


    #Newline

    if (os.name == 'nt'):
        _newline = '\r\n'
        _seperator = '\\'
    elif (os.name == 'mac'):
        ##I think thats what the seperator will look like in mac 
        _newline = '\r'
        _seperator = ':'
    else:
        _newline = '\n'
        _seperator = '/'


    print _seperator
    #variables
    id_count = 0
    fast_flag = True
    cleaning_flag = True
    tab ='\t'
    #LISTS
    ID_LIST = []
    SEQUENCE_LIST = []
    FILES = []
    FILE_NAMES = []
    #TIMING VARIABLE
    timer = timeit.Timer()
    begin = timer.timer()

    path = os.getcwd()

    try:
        dirty_files = glob.glob(path + _seperator + dir + _seperator + '*')
    except:
        print "An Error was Encountered while trying to read from the directory"
        print "Make sure that the directory is in your current path and the name is correct." 
        print "Error encountered was" , sys.exc_info()[0]
        return
    
    if dirty_files == []:
        print "There were no files in the path given"
        print "Make sure that the directory is in your current path and the name is correct." 
        return

    for i in range(0,len(dirty_files)):
        if os.path.isfile(dirty_files[i]):
            FILES.append(dirty_files[i])

    for i in range(0,len(FILES)):
        temp = FILES[i].split(_seperator)
        temp = temp[-1]
        FILE_NAMES.append(temp[:temp.find('.')])



    try:
        file_output = open(output_file + ".txt",  "wbU")
    except:
        print "An error occured while trying to create the output file\n\n", output_file, "Could not be created\n\nCheck file permissions and Close all open instances of the file"
        return
    


#Data Extraction
##################################################################################################################


    #INPUT FILE

    for input_file in FILES:
            
        #try to open file
        try:
            text_file = open(input_file)
        except:
                print "DID NOT FIND FILE:  " + input_file
                print sys.exc_info()[0]
                return
        #try to read total file    

        try:
            line = text_file.read()
        except:
            print "FILE COULD NOT BE READ, CHECK FILE FORMAT"
            print sys.exc_info()[0]
            return

        #try to extract data
#        try:
        if True:
            line = line.rstrip('\n')
            line = line.split('\n')
            #the contig is at the bottom of the file
            contig = line[-1][22:len(line[-1])]
	    contig_id = line[-1][:21]
	    contig_id = contig_id[:contig_id.find(' ')]
	    print contig_id
            #all sequences but contig
            for i in range(1,len(line)-1):
                if line[i].find(len(contig)*'-') >=0:
		    # print partial_id
		    # print contig
                    break

                partial_id = line[i][0:22]
		# print partial_id
                partial_id = partial_id[:partial_id.find(' ')]
                if ( (partial_id[-1] == '-') or  (partial_id[-1] == '+')):
                    orientation = partial_id[-1]
                    file_output.write(partial_id[:-1])
                else:

                    orientation = '?'
                    file_output.write(partial_id)
		    ### DEBUG PRINTING ###
		    print partial_id

                #sequence_id
		### DEBUG PRINTING ###
		print partial_id
                file_output.write(tab)
                file_output.write(orientation)
                file_output.write(tab)

                
                partial_sequence = line[i][22:len(line[i])]
                if partial_sequence.startswith(' '):
                    partial_sequence = partial_sequence.replace(' ','-')
                    file_output.write(partial_sequence + (len(contig)-len(partial_sequence))*'-')
                    file_output.write(_newline)
                else:
                    file_output.write(partial_sequence + (len(contig)-len(partial_sequence))*'-')
                    file_output.write(_newline)
                    
                    
            # file_output.write(FILE_NAMES[id_count])
            file_output.write(contig_id)
            id_count = id_count + 1
            file_output.write(tab)
            file_output.write('*')
            file_output.write(tab)
            file_output.write(contig)
            file_output.write(_newline)
            print "=================================================================================="
            text_file.close()
                        
            
##        except:
##            print "Error occured while reading data from file, Script probably encountered an unexpected format error."
##            print "Error encountered was" , sys.exc_info()[0]
##            return
##



    #ends program
    end = timer.timer()
    print "Total Execution time: %.2f seconds" %(end - begin)
    print "Program Exited Sucessfully"    
    return

import os
import sys
import string
import timeit
import glob

if __name__ == "__main__":
        
    if len(sys.argv) <= 2 or len(sys.argv) > 3:
        print "Program usage: "
        print "Directory, Output-File"
	exit
    else:
        dir = sys.argv[1]
	output_file = sys.argv[2]
        cap3_alignment(dir, output_file)

