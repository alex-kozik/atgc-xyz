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

    #TUPLES
    MATCH_TUPLE = ()
    MATCH_TUPLE_LIST = []
    OUTPUT_TUPLE = ()
    OUTPUT_TUPLE_LIST = []
    FASTA_TUPLE =()
    FASTA_TUPLE_LIST =[]
    FASTA_MATCH_TUPLE = ()
    FASTA_MATCH_TUPLE_LIST = []
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
            print id

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


##Error Checking
#########################################################################################################################################

    #Input file

    counter = 1
    length = sum(len(ID_LIST))
    
    #This can be short circuited
    #for i
    #list[i] in ID_list...
    print "Checking for redundant Id's"
    for i in range(0,len(ID_LIST)):
        print `i`
        for j in range(i+1,len(ID_LIST)):

            if counter % 100000 == 0:
                print counter, " of ", length
            counter = counter +1

            if (i == j):
                continue
            else:
                if (ID_LIST[i] == ID_LIST[j]):
                    print "This Id", ID_LIST[i] ,"has been found in the file more than once, this file cannot contain redundant Id's\n"
                    log_error = True
                    log_string = "This Id " + ID_LIST[i] + " has been found in the file more than once, this file cannot contain redundant Id's"
                    LOG_LIST.append(log_string)

    #Newline


    if (os.name == 'nt'):
        _newline = '\r\n'
    elif (os.name == 'mac'):
        _newline = '\r'
    else:
        _newline = '\n'



##Find REdundancy
#############################################################################################################################################


    #index through sequence list and look for redundant sequences 
    #if found store in MATCH_LIST. format
    #MATCH_LIST[#][0] = a, MATCH_LIST[#][1] = b
    #the sequence a was found in b

    counter = 1
    length = sum(len(SEQUENCE_LIST))
    print "Checking for redundant sequences"
    for i in range(0,len(SEQUENCE_LIST)):
        print `i`
        for j in range(i+1, len(SEQUENCE_LIST)):
            tempi = SEQUENCE_LIST[i]
            tempj = SEQUENCE_LIST[j]


            if counter % 200000 == 0:
                print counter, " of ", length
            counter = counter +1


            #match_tuple = copy_id, master_id, perfect_match?, from,  to,  copy_sequence,  master_sequence

            #perfect match
            if (tempi == tempj):
                MATCH_TUPLE = ID_LIST[i], ID_LIST[j], "True", '1', repr(len(tempi)) , tempi,  tempj
                MATCH_TUPLE_LIST.append(MATCH_TUPLE)
                match_flag = True
                continue

            #partial finds

            #j found in i    
            if (tempi.find(tempj) >= 0):
                MATCH_TUPLE = ID_LIST[j], ID_LIST[i], "False", repr( (tempi.find(tempj) +1) ), repr( tempi.find(tempj) + 1 + len(tempj) ) ,tempj , tempi
                MATCH_TUPLE_LIST.append(MATCH_TUPLE)
                match_flag = True
                continue
                
            #i found in j
            if (tempj.find(tempi) >= 0):
                MATCH_TUPLE = ID_LIST[i], ID_LIST[j], "False", repr( (tempj.find(tempi) +1) ), repr( tempj.find(tempi)+ 1 + len(tempi) ), tempi,  tempj
                MATCH_TUPLE_LIST.append(MATCH_TUPLE)
                match_flag = True
                continue

        if (match_flag != True):
            FASTA_TUPLE = ID_LIST[i], tempi
            FASTA_TUPLE_LIST.append(FASTA_TUPLE)

        match_flag = False


##Find Clusters 
#############################################################################################################################################

    #elements which aren't clusters are not found on the other side(MATCH_TUPLE_LIST[i][1]) of this list. 


    for i in range(0,len(MATCH_TUPLE_LIST)):
        CLUSTER_MATCH_LIST.append(MATCH_TUPLE_LIST[i][0])

    #elements in MATCH_TUPLE_LIST[i][1] which are not in CLUSTER_MATCH_LIST are clusters 


    for i in range(0,len(MATCH_TUPLE_LIST)):
        print `i`
        if (MATCH_TUPLE_LIST[i][1] not in CLUSTER_MATCH_LIST):

            #if the element is in the CLUSTER_LIST than that cluster has already been found.


            if (MATCH_TUPLE_LIST[i][1] not in CLUSTER_LIST):
                CLUSTER_LIST.append(MATCH_TUPLE_LIST[i][1])

    #find cluster subsets
    for i in range (0,len(CLUSTER_LIST)):
        print `i`
        for j in range (0,len(MATCH_TUPLE_LIST)):
            if (CLUSTER_LIST[i] == MATCH_TUPLE_LIST[j][1]):
                cluster_counter = cluster_counter + 1
                if (MATCH_TUPLE_LIST[j][2] == True):
                    perfect_matches = perfect_matches + 1
                master_len = len( MATCH_TUPLE_LIST[j][6] )

                
        #MATCH_TUPLE_LIST[j][5] == copy sequence ,,  MATCH_TUPLE_LIST[j][6] == master sequence
        #  CLUSTER_ID,  SEQUENCE_ID,  PERFERCT_MATCH?, NUMBER_OF_MATCHES,  FROM,  TO, LENGTH_OF_CURRENT_SEQUENCE, NODE_NUMBER
        FASTA_MATCH_TUPLE = CLUSTER_LIST[i], perfect_matches, cluster_counter
        
        FASTA_MATCH_TUPLE_LIST.append(FASTA_MATCH_TUPLE)
        OUTPUT_TUPLE = CLUSTER_LIST[i], CLUSTER_LIST[i],  "Master_Sequence", repr(cluster_counter + 1 ), '1', repr( master_len), repr(master_len), repr(i+1)
        OUTPUT_TUPLE_LIST.append(OUTPUT_TUPLE)


        for j in range (0,len(MATCH_TUPLE_LIST)):
            if (CLUSTER_LIST[i] == MATCH_TUPLE_LIST[j][1]):            
                OUTPUT_TUPLE = CLUSTER_LIST[i], MATCH_TUPLE_LIST[j][0],  MATCH_TUPLE_LIST[j][2], repr( cluster_counter +1 ), MATCH_TUPLE_LIST[j][3], MATCH_TUPLE_LIST[j][4], repr(len(MATCH_TUPLE_LIST[j][6])), repr(i +1)
                OUTPUT_TUPLE_LIST.append(OUTPUT_TUPLE)

        perfect_matches = 0
        cluster_counter = 0
         
        

##Create output file
#############################################################################################################################################
            
    #create output files with .quality extension
    try:
        file_output = open(output_file + ".xls",  "wbU")
    except:
        print "Could not create quality1 output file", output_file, "Check file permissions and Close all open excel files"
        return


    #Create Table headers
    file_output.write("CLUSTER_ID")
    file_output.write("\t")
    file_output.write("EST_ID")
    file_output.write("\t")
    file_output.write("Full_Overlap")
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
        print `i`
        for j in range(0,len(OUTPUT_TUPLE_LIST[i])):
            file_output.write(OUTPUT_TUPLE_LIST[i][j])
            file_output.write("\t")
        file_output.write(_newline)
    file_output.close()



    try:
        file_output2 = open(output_file + ".fasta",  "wbU")
    except:
        print "Could not create quality1 output file", output_file, "Check file permissions and Close all open excel files"
        return


    for i in range(0, len(FASTA_TUPLE_LIST)):
        print `i`

        if (FASTA_TUPLE_LIST[i][0] in CLUSTER_LIST):
            for j in range(0, len(FASTA_MATCH_TUPLE_LIST)):
                if (FASTA_MATCH_TUPLE_LIST[j][0] == FASTA_TUPLE_LIST[i][0]):
                    file_output2.write(FASTA_TUPLE_LIST[i][0])
                    file_output2.write('\t')
                    file_output2.write("[ FULL:")
                    file_output2.write(repr(FASTA_MATCH_TUPLE_LIST[j][1]))
                    file_output2.write(' ]\t')
                    file_output2.write("[ PART:")
                    file_output2.write(repr(FASTA_MATCH_TUPLE_LIST[j][2]))
                    file_output2.write(' ]')
                    file_output2.write(_newline)
                    file_output2.write(FASTA_TUPLE_LIST[i][1])
                    file_output2.write(_newline)
                                       
        else :      
            file_output2.write(FASTA_TUPLE_LIST[i][0])
            file_output2.write('\t')
            file_output2.write("[ FULL:0 ]  [ PART:0 ]")
            file_output2.write(_newline)
            file_output2.write(FASTA_TUPLE_LIST[i][1])
            file_output2.write(_newline)

    file_output2.close()




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
