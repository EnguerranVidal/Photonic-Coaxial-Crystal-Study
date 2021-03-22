#########################################################################
#                                                                       #
#   The goal of this program is to manage the frequencies that will     #
#   be used in the study of the response of the model to the attack     #
#   of Gaussian packets.                                                #
#   We need easy management of these frequencies so that once the       #
#   This programm is coded in Python language and needs special         #
#   libraries to work.                                                  #
#                                                                       #
#########################################################################



# IMPORTS ---------------------------------------------------------------

#########################################################################
#                                                                       #
#   We first import the necessary libraries like mentionned.            #
#                                                                       #
#########################################################################

import numpy as np

# FUNCTIONS -------------------------------------------------------------

#########################################################################
#                                                                       #
#   This code is containing only functions that can be used easily      #
#   by the user without the need for a script.                          #
#                                                                       #
#########################################################################
  
def read_float_file(file_name):
    '''
    This function takes as input a file name and returns the float contents of the file
    in a ordered list.
    '''
    content=[]
    with open(file_name,'r') as file:
        LINES=file.readlines()
        N=len(LINES)
        for i in range(N):
            content.append(float(LINES[i]))
        file.close()
    return content

def write_float_file(file_name,content):
    '''
    This function takes as input a file name and some content in a list then writes the content
    of this list into the file mentionned, deleting all previous content of the file in the process.
    '''
    N=len(content)
    with open(file_name,'w') as file:
        for i in range(N):
            file.write(str(float(content[i]))+'\n')
        file.close()


def initial_frequencies(fi=5*10**6,ff=50*10**6,N=91):
    '''
    This function writes the initial frequencies studied in our Gaussian packets study
    ( one every 0.5 MHz starting from 5 MHz and finishing at 50 MHz )
    '''
    F=np.linspace(fi,ff,num=int(N))
    write_float_file('frequencies.txt',F)

def add_frequency(new_frequency):
    '''
    This function lets us add a frequency in the file by reading all the previous content, storing it,
    adding the frequency at the end of the obtained list( and checking for any duplicate ) and
    rewriting all the content of the file, closing it afterwards.
    '''
    frequencies=read_float_file('frequencies.txt')
    if new_frequency not in frequencies:
        frequencies.append(new_frequency)
        write_float_file('frequencies.txt',frequencies)
    else:
        print("frequency already in file, not added once more")
