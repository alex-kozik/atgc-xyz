def redundant(input_file, output_file):


    #variables
    seq_end = 0
    carrot_loc = 0
    rows = 0
    temp_int = 0
    score_len = 0
    log_error = False
    log_string = ''
    cluster_counter = 0
    perfect_matches = 0
    match_flag = False
    fast_flag = True
    cleaning_flag = True
    #LISTS
    ID_LIST = []
    SEQUENCE_LIST = []
    CLUSTER_LIST = []
    LOG_LIST = []
    TEMP_LIST = []
    TEMP_SCORE_LIST = []
    CLUSTER_MATCH_LIST = []
    USED_IDS = []
    CLUSTER_TUPLE_LIST = []
    PERFECT_MATCH_LIST =[]
    CLUSTER_ORDER = []
    CLUSTER_ORDER_LIST = []
    #TUPLES
    MATCH_TUPLE = ()
    MATCH_LIST = []
    OUTPUT_TUPLE = ()
    OUTPUT_TUPLE_LIST = []
    FASTA_TUPLE =()
    FASTA_TUPLE_LIST =[]
    FASTA_MATCH_TUPLE = ()
    FASTA_MATCH_TUPLE_LIST = []
    DISTANCE_TUPLE_LIST=[]
    #TIMING VARIABLE
    timer = timeit.Timer()
    begin = timer.timer()



#Functions
##################################################################################################################

    def sum(n):
        count = 0
        for i in range(1, n):
            count= i + count
        return count



#Data Extraction
##################################################################################################################


    #INPUT FILE


    print "\nOpening and Checking Input File\n"

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
    t1 = timer.timer()
    #formatting file
    try:
        while cleaning_flag == True:
            cleaning_flag = False
                
            while line.find('\t') > 0:
                cleaning_flag = True
                line = line.replace('\t',' ')
            while line.find('  ') > 0:
                cleaning_flag = True
                line = line.replace('  ',' ')
            while line.find('\r') > 0:
                cleaning_flag = True
                line = line.replace('\r', '\n')
            while line.find('\n\n') > 0:
                cleaning_flag = True
                line = line.replace('\n\n', '\n')
            while line.find('\n \n') > 0:
                cleaning_flag = True
                line = line.replace('\n \n', '\n')
            while (line[0] == '\n'  or  line [0] == ' '):
                cleaning_flag = True
                line = line.lstrip('\n')
                line = line.lstrip()
            while (line[-1] == '\n'  or  line[-1] == ' '):
                cleaning_flag = True
                line = line.rstrip()
                line = line.rstrip('\n')
        #added to end of file to simplify parsing
        line = line + '\n'#end of file

        carrots = line.count('>')
        carrot_counter = 1
        found_counter = 0
        #Extraction of id and sequence            
        while line.find('>', carrot_loc) >= 0:

            if carrot_counter % 300 == 0:
                print carrot_counter, " of ", carrots
            carrot_counter = carrot_counter +1

            carrot_loc = line.find('>',carrot_loc)

            if fast_flag == True:            
                id_space = line.find(' ', carrot_loc)#space after id
                if id_space == -1:
                    fast_flag = False
            id_end = line .find('\n', carrot_loc)#if no space then newline after id

            #determines where the end of the id is. 
            #done by finding nearest space or newline and then determines which is closer
            if ( (id_space == -1) or (id_end - id_space) < 0 ):
                id = line[carrot_loc + 1:id_end]
            else:
                id = line[carrot_loc + 1:id_space]
            #id's are stored in this master list
            ID_LIST.append(id)

            #looks for the begining of the next id
            #this will also points to the end of the sequence
            seq_end = line.find('>' , id_end)
            carrot_loc = seq_end

            #sequence is extracted 
            if seq_end > 0:
                sequence = line[id_end + 1: seq_end]
            else: 
                sequence = line[id_end + 1:len(line)-1]
                SEQUENCE_LIST.append(sequence)
                rows = rows + 1
                break
            #sequences are stored in this master list
            SEQUENCE_LIST.append(sequence)
            rows = rows + 1
        text_file.close()
        t2 = timer.timer()
        print "File was scanned in %.2f seconds\n" %(t2-t1)
        
    except:
        print "Error occured while reading data from file, Script probably encountered an unexpected format error."
        print "Error encountered was" , sys.exc_info()[0]
        return
    #line is not used again deleted to free memory
    line =''

#List Formatting
#################################################################################################################


    
    #formatting data
    #all spaces and \n characters are removed from the sequences
    for i in range(0, len(SEQUENCE_LIST)):
        temp_string = SEQUENCE_LIST[i]
        while temp_string.find(' ') > 0: 
            temp_string = temp_string.replace(' ','')
        while temp_string.find('\n') > 0:
            temp_string = temp_string.replace('\n', '')
       
        TEMP_LIST.append(temp_string)
    SEQUENCE_LIST = TEMP_LIST
    TEMP_LIST = []


#########################################################################################################################################
    #Newline

    if (os.name == 'nt'):
        _newline = '\r\n'
    elif (os.name == 'mac'):
        _newline = '\r'
    else:
        _newline = '\n'


##Error Checking
#########################################################################################################################################

##    counter = 1
##    length = sum(len(ID_LIST))
##    
##    #This can be short circuited
##    #for i
##    ##list[i] in ID_list...
##    print "Checking for redundant Id's"
##    for i in range(0,len(ID_LIST)):
##        for j in range(i+1,len(ID_LIST)):
##
##            if counter % 500000 == 0:
##                print counter, " of ", length
##            counter = counter +1
##
##            if (i == j):
##                continue
##            else:
##                if (ID_LIST[i] == ID_LIST[j]):
##                    print "This Id", ID_LIST[i] ,"has been found in the file more than once, this file cannot contain redundant Id's\n"
##                    log_error = True
##                    log_string = "This Id " + ID_LIST[i] + " has been found in the file more than once"
##                    LOG_LIST.append(log_string)
##
##    if LOG_LIST != []:
##        try:
##            file_output2 = open(output_file + ".error",  "wbU")
##        except:
##            print "Could not create", output_file, ".error.\n\nCheck file permissions and Close all open excel files"
##            return
##        for i in range(0,len(LOG_LIST)):
##            file_output2.write(LOG_LIST[i])
##            file_output2.write(_newline)
##        file_output2.close()
##        
##        end = timer.timer()
##        print "Total Execution time: %.2f seconds" %(end - begin)
##        print "PROGRAM DID NOT EXIT SUCCESFULLY\nCHECK ERROR FILE."
##        return




##Find REdundancy
#############################################################################################################################################


    #index through sequence list and look for redundant sequences 
    #if found store in MATCH_LIST. format
    #MATCH_LIST[#][0] = a, MATCH_LIST[#][1] = b
    #the sequence a was found in b

    counter = 1
    length = sum(len(SEQUENCE_LIST))
    print "\n\nChecking for redundant sequences\n\n"
    for i in range(0,len(SEQUENCE_LIST)):
	print counter
        for j in range(i+1, len(SEQUENCE_LIST)):

            tempi = SEQUENCE_LIST[i]
            tempj = SEQUENCE_LIST[j]

            if tempi == '':
                break
            if tempj =='':
                continue

            
            if counter % 500000 == 0:
                print counter, " of ", length
            counter = counter +1


            #match_tuple = copy_id, master_id, perfect_match?, from,  to,  copy_sequence,  master_sequence

            #perfect match
            if (tempi == tempj):
                MATCH_TUPLE = ID_LIST[i], ID_LIST[j], "True", '1', str(len(tempi)) , tempi,  tempj
                MATCH_LIST.append(MATCH_TUPLE)
                if ID_LIST[i] not in USED_IDS:
                    USED_IDS.append(ID_LIST[i])
                if ID_LIST[j] not in USED_IDS:
                    USED_IDS.append(ID_LIST[j])
                continue

            #partial finds

            #j found in i    
            if (tempi.find(tempj) >= 0):
                MATCH_TUPLE = ID_LIST[j], ID_LIST[i], "False", str( (tempi.find(tempj) +1) ), str( tempi.find(tempj)+  len(tempj) ) ,tempj , tempi
                MATCH_LIST.append(MATCH_TUPLE)
                if ID_LIST[i] not in USED_IDS:
                    USED_IDS.append(ID_LIST[i])
                if ID_LIST[j] not in USED_IDS:
                    USED_IDS.append(ID_LIST[j])
                continue
                
            #i found in j
            if (tempj.find(tempi) >= 0):
                MATCH_TUPLE = ID_LIST[i], ID_LIST[j], "False", str( (tempj.find(tempi) +1) ), str( tempj.find(tempi)+  len(tempi) ), tempi,  tempj
                MATCH_LIST.append(MATCH_TUPLE)
                if ID_LIST[i] not in USED_IDS:
                    USED_IDS.append(ID_LIST[i])
                if ID_LIST[j] not in USED_IDS:
                    USED_IDS.append(ID_LIST[j])
                continue

##Find Clusters 
#############################################################################################################################################

    #elements which aren't clusters are not found on the other side(MATCH_LIST[i][1]) of this list. 
    for i in range(0,len(MATCH_LIST)):
        CLUSTER_MATCH_LIST.append(MATCH_LIST[i][0])


    #elements in MATCH_LIST[i][1] which are not in CLUSTER_MATCH_LIST are clusters 
    for i in range(0,len(MATCH_LIST)):
        if (MATCH_LIST[i][1] not in CLUSTER_MATCH_LIST):

            #if the element is in the CLUSTER_LIST than that cluster has already been found.

            if (MATCH_LIST[i][1] not in CLUSTER_LIST):
                CLUSTER_LIST.append(MATCH_LIST[i][1])

    

    #find cluster subsets
    for i in range (0,len(CLUSTER_LIST)):
        CLUSTER_ORDER.append(CLUSTER_LIST[i])
	print i
        for j in range (0,len(MATCH_LIST)):
            if (CLUSTER_LIST[i] == MATCH_LIST[j][1]):
                CLUSTER_ORDER.append(MATCH_LIST[j][0])                           
                cluster_counter = cluster_counter + 1
                if (MATCH_LIST[j][2] == "True"):
                    perfect_matches = perfect_matches + 1
                master_len = len(MATCH_LIST[j][6])
                DISTANCE_TUPLE = CLUSTER_LIST[i], "\t[1:", str(len(MATCH_LIST[j][6])), ']\t', MATCH_LIST[j][0],'\t[', str(MATCH_LIST[j][3]),':', str(MATCH_LIST[j][4]),']\t'
                DISTANCE_TUPLE_LIST.append(DISTANCE_TUPLE)
        CLUSTER_ORDER_LIST.append(CLUSTER_ORDER)
        CLUSTER_ORDER = []
                
        #MATCH_LIST[j][5] == copy sequence ,,  MATCH_LIST[j][6] == master sequence
        #  CLUSTER_ID,  SEQUENCE_ID,  PERFECT_MATCH, NUMBER_OF_MATCHES,  FROM,  TO, LENGTH_OF_CURRENT_SEQUENCE, NODE_NUMBER
        for k in range(0,len(ID_LIST)):
            if CLUSTER_LIST[i] == ID_LIST[k]:
                cluster_sequence = SEQUENCE_LIST[k]

        FASTA_MATCH_TUPLE = CLUSTER_LIST[i], str(perfect_matches), str(cluster_counter- perfect_matches), cluster_sequence
        

        CLUSTER_TUPLE_LIST.append(FASTA_MATCH_TUPLE)
        OUTPUT_TUPLE = CLUSTER_LIST[i], CLUSTER_LIST[i],  "Master_Sequence", str(cluster_counter + 1 ), '1', str(master_len), str(master_len), str(i+1)
        OUTPUT_TUPLE_LIST.append(OUTPUT_TUPLE)


        for j in range (0,len(MATCH_LIST)):
            if (CLUSTER_LIST[i] == MATCH_LIST[j][1]):            
                OUTPUT_TUPLE = CLUSTER_LIST[i], MATCH_LIST[j][0],  MATCH_LIST[j][2], str( cluster_counter +1 ), MATCH_LIST[j][3], MATCH_LIST[j][4], str(len(MATCH_LIST[j][6])), str(i +1)
                OUTPUT_TUPLE_LIST.append(OUTPUT_TUPLE)

        perfect_matches = 0
        cluster_counter = 0
        cluster_sequence = ''
         
        

##Create output file
#############################################################################################################################################
            
    #create output files with .quality extension
    #create the excel file
    if len(OUTPUT_TUPLE_LIST) > 0:
        try:
            file_output = open(output_file + ".xls",  "wbU")
        except:
            print "Could not create the Excel table", output_file, ".xls \n\nCheck file permissions and Close all open Excel files"
            return


        #Create Table headers
        file_output.write("CLUSTER_ID")
        file_output.write("\t")
        file_output.write("EST_ID")
        file_output.write("\t")
        file_output.write("MS_Type")
        file_output.write("\t")
        file_output.write("Perfect_Match")
        file_output.write("\t")
        file_output.write("Number_of_Seqs")
        file_output.write("\t")
        file_output.write("From")
        file_output.write("\t")
        file_output.write("To")
        file_output.write("\t")
        file_output.write("Total_Len")
        file_output.write("\t")
        file_output.write("Node")
        file_output.write(_newline)

        
        for i in range(0, len(OUTPUT_TUPLE_LIST)):
	    print i
            for j in range(0,len(OUTPUT_TUPLE_LIST[i])):
                if (j==2):

                    if OUTPUT_TUPLE_LIST[i][2] == "Master_Sequence":
                        file_output.write("Master")
                        file_output.write('\t')
                        file_output.write('True')
                        file_output.write('\t')

                    elif OUTPUT_TUPLE_LIST[i][2] == "True":
                        file_output.write("Slave")
                        file_output.write('\t')
                        file_output.write('True')
                        file_output.write('\t')
                        
                    else:
                        file_output.write("Slave")
                        file_output.write('\t')
                        file_output.write('False')
                        file_output.write('\t')
                else:                    
                    file_output.write(OUTPUT_TUPLE_LIST[i][j])
                    file_output.write("\t")
            file_output.write(_newline)

        file_output.close()


            
        try:
            file_output2 = open(output_file + ".fasta",  "wbU")
        except:
            print "Could not create", output_file, ".fasta.\n\nCheck file permissions and Close all open excel files"
            return

        for i in range(0,len(ID_LIST)):
            if (ID_LIST[i] not in USED_IDS) :
                file_output2.write('>')
                file_output2.write(ID_LIST[i])
                file_output2.write('  ')
                file_output2.write("[ FULL:0 ]  [ PART:0 ]")
                file_output2.write(_newline)
                file_output2.write(SEQUENCE_LIST[i])
                file_output2.write(_newline)
                                           

        for i in range(0, len(CLUSTER_TUPLE_LIST)):
            file_output2.write('>')
            file_output2.write(CLUSTER_TUPLE_LIST[i][0])
            file_output2.write('  ')
            file_output2.write("[ FULL:")
            file_output2.write(str(CLUSTER_TUPLE_LIST[i][1]))
            file_output2.write(' ]  ')
            file_output2.write("[ PART:")
            file_output2.write(str(CLUSTER_TUPLE_LIST[i][2]))
            file_output2.write(' ]')
            file_output2.write(_newline)
            file_output2.write(CLUSTER_TUPLE_LIST[i][3])
            file_output2.write(_newline)

        file_output2.close()


        try:
            file_output2 = open(output_file + ".group_info",  "wbU")
        except:
            print "Could not create", output_file, ".group_info.\n\nCheck file permissions and Close all open excel files"
            return

        counting = 1

        for i in range(0,len(ID_LIST)):
            if ID_LIST[i] not in USED_IDS:
                file_output2.write(ID_LIST[i])
                file_output2.write('\t')
                file_output2.write(str(counting))
                file_output2.write('\t')
                file_output2.write("-")
                file_output2.write(_newline)
                counting = counting + 1
        for i in range(0,len(OUTPUT_TUPLE_LIST)):

            file_output2.write(str(OUTPUT_TUPLE_LIST[i][1]))
            file_output2.write('\t')
            file_output2.write( str( int(OUTPUT_TUPLE_LIST[i][7]) + counting - 1))
            file_output2.write('\t')
            if OUTPUT_TUPLE_LIST[i][0] == OUTPUT_TUPLE_LIST[i][1]:
                file_output2.write("Master")
            else:
                file_output2.write("Slave")
            file_output2.write(_newline)

            
        file_output2.close()


        try:
            file_output2 = open(output_file + ".distance_info",  "wbU")
        except:
            print "Could not create", output_file, ".distance_info.\n\nCheck file permissions and Close all open excel files"
            return
        for i in range(0,len(DISTANCE_TUPLE_LIST)):
            for j in range(0,len(DISTANCE_TUPLE_LIST[i])):
                
                file_output2.write(DISTANCE_TUPLE_LIST[i][j])



            file_output2.write(_newline)

        file_output2.close()


        try:
            file_output2 = open(output_file + ".cluster_order",  "wbU")
        except:
            print "Could not create", output_file, ".cluster_order.\n\nCheck file permissions and Close all open excel files"
            return
        for i in range(0,len(CLUSTER_ORDER_LIST)):
            for j in range(0,len(CLUSTER_ORDER_LIST[i])):
                
                file_output2.write(CLUSTER_ORDER_LIST[i][j])

                if j != len(CLUSTER_ORDER_LIST[i]):
                    file_output2.write('  ')


            file_output2.write(_newline)

        file_output2.close()

        
    else:
        print "\n\nNo Matches were found.\n\nNo output file was created.\n\n"



    end = timer.timer()
    print "Total Execution time: %.2f seconds" %(end - begin)
    print "Program Exited Sucessfully"    
    return



import os
import sys
import string
import timeit
if __name__ == "__main__":
        
    if len(sys.argv) <= 2 or len(sys.argv) > 3:
        print "Program usage: "
        print "Input-File, Output-File"
	exit
    else:
        input_file = sys.argv[1]
	output_file = sys.argv[2]
        redundant(input_file, output_file)
