#########################################################################
#                                                                       #
#   The goal of this program is to calculate the locations of center    #
#   of masses of gaussian packets on oscilloscope scopes, obtaining     #
#   the group velocity of the packet through our coaxial model by       #
#   calculating the differences between the center of mass of the       #
#   input packet and the center of mass of the output packet.           #
#   This position delay will be expressed as a velocity, giving us      #
#   the group velocity of the Gaussian packet through the model.        #
#                                                                       #
#   This programm is coded in Python language and needs special         #
#   libraries to work. Especially Numpy, Matplotlib, Os and Csv         #
#   libraries are necessary and the programm can't work without         #
#   them.                                                               #
#                                                                       #
#########################################################################



# IMPORTS ---------------------------------------------------------------

#########################################################################
#                                                                       #
#   We first import the necessary libraries like mentionned.            #
#                                                                       #
#########################################################################

import csv
import numpy as np
import matplotlib.pyplot as plt
import os



# FUNCTIONS -------------------------------------------------------------

#########################################################################
#                                                                       #
#   We then need a few functions to easy up the rest of the programm.   #
#                                                                       #
#########################################################################

def file_extension(file_name):
    ''' This function gives the extension of the file.
        Example : file01.txt ---> txt
    '''
    file=file_name.split('.')
    return file[1]

def name_file(file_name):
    ''' This function gives the name of the file without the extension.
        Example : file01.txt ---> file01
    '''
    file=file_name.split('.')
    return file[0]

def trapeze_method(X,Y):
    ''' From two lists X and Y with Y = f(X), calculate an approximation of the area below the curve of f
        on the interval [ X[0] , X[-1] ] by using the trapezes method of integral calculation.
    '''
    assert len(X)==len(Y)
    dX=X[1]-X[0]
    N=len(X)
    S=0
    for i in range(N-1):
        S=S+(Y[i+1]+Y[i])*dX/2 # We each time add a little trapeze between X[i+1] and X[i]
    return S
 
def is_file(file_name):
    ''' This function returns True if the input is a file. It does that by checking for extensions which
        directories don't have'''
    file=file_name.split('.')
    if len(file)==2:
        return True
    else:
        return False
    
def signal_centroid(X,Y):
    ''' This function returns the x position of the centroid of a signal inputes through the Y list of points
        associated with X. '''
    assert len(X)==len(Y)
    XY=X*abs(Y)
    ES=trapeze_method(X,abs(Y))
    tES=trapeze_method(X,XY)
    center=tES/ES
    return center
            
def constant(name):
    ''' This function returns a wanted known constant value by giving its name '''
    if name=='c':
        return 299792458



# MAIN PROGRAM ----------------------------------------------------------

#########################################################################
#                                                                       #
#   We then code the main programm and use all that we defined above.   #
#                                                                       #
#########################################################################

# We first need to specify the directory where all the scopes ( that are in a csv format ) are located
input_directory="C://Users//engue/Desktop/scopes"

# We then open a new file where all the group velocities will be stored once calculated
time_delay_file=open('speeds_in_c.txt','w')
# We then scan the directory mentionned for any object, be it files or other directories
files_list = os.listdir(input_directory)

Speeds=[]
files_number=len(files_list)
for i in range(files_number):
    csv_file_name=files_list[i]
    if is_file(csv_file_name) and file_extension(csv_file_name)=='csv': # We check if it is a csv format file
        print(csv_file_name)
        # We then create the name of a file that will contain all the values in the csv by using the name of the csv file
        # And we also load all the values and infos of the csv into this new txt file
        txt_file_name=name_file(csv_file_name)+'.txt'
        with open(txt_file_name, "w") as my_output_file:
            with open(csv_file_name, "r") as my_input_file:
                [ my_output_file.write(" ".join(row)+'\n') for row in csv.reader(my_input_file)]
        my_output_file.close()
        # Once the file txt done, we read all its lines
        txt_file=open(txt_file_name,'r')
        LINES=txt_file.readlines()
        txt_file.close()
        # We get rid of useless lines ( the first and second one )
        LINES.pop(0)
        LINES.pop(0)
        # Then we retrieve the values of the X coordinates and the CH1 and CH2 values, getting them
        # into the Y1 and Y2 lists
        n_lines=len(LINES)
        X=[]
        Y1=[]
        Y2=[]
        for j in range(n_lines):
            line=LINES[j].split()
            if len(line)==3:
                X.append(float(line[0]))
                Y1.append(float(line[1]))
                Y2.append(float(line[2]))
        # We transform the obtained lists into arrays
        X=np.array(X)
        Y1=np.array(Y1)
        Y2=np.array(Y2)
        # We obtain the center of masses of each Gaussian packet by using the signal_centroid() function defined above
        t1=signal_centroid(X,Y1)
        t2=signal_centroid(X,Y2)
        # We then get the difference between the two
        time_delay=abs(t1-t2)
        # We then convert it into the group velocities by calculating the speed associated with this time delay when
        # the signal go through our 120 m long coaxial photonic cristal
        speed=(120/time_delay)/constant('c')
        Speeds.append(speed)
        # We then write this speed in the file 'speeds_in_c.txt' opened at the very beginning
        time_delay_file.write(str(speed)+'\n')
# Once all the scopes read and the speeds obtained we close the file, saving all the speeds in the process
time_delay_file.close()
