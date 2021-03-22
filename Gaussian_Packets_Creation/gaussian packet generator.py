#########################################################################
#                                                                       #
#   The goal of this program is to generate a Gaussian packet of a      #
#   certain frequency in a csv format which is readable by the GBF      #
#   used in our experiments with the coaxial photonic cristal model.    #
#   The frequencies are taken from a seperate file containing the       #
#   ones we carefully chose.                                            #
#                                                                       #
#   This programm is coded in Python language and needs special         #
#   libraries to work. Especially Numpy, Matplotlib and Csv libraries   #
#   are necessary and the programm can't work without them.             #  
#                                                                       #
#########################################################################



# IMPORTS ---------------------------------------------------------------

#########################################################################
#                                                                       #
#   We first import the necessary libraries like mentionned.            #
#                                                                       #
#########################################################################

import numpy as np
import matplotlib.pyplot as plt
import csv

# FUNCTIONS -------------------------------------------------------------

# We need a few fucntions to generate the packets

def Gauss_function(x,mu,sigma):
    '''
    This function generates a Gaussian function ( bell function ) on a x interval or x value
    '''
    return (1/(sigma*np.sqrt(2*np.pi)))*np.exp(-(x-mu)**2/(2*sigma**2))

def create_file_Gaussian(fw,f0,width,fGBF,Amplitude,name):
    '''
    This function creates a csv file containing a Gaussian packet. The packet is put in the middle of an interval
    of a length of 1/fw by calculationg the product between a Gaussian function and a sin fucntion with a
    period of 1/f0. The Gaussian function is put at a mean of 0 and with a certain width.
    The name of the csv file is given by the user.
    
    The Gaussian packet is created with a number of points generated specifically for the sampling
    frequency of the GBF expected to read the file.
    '''
    N=int(fGBF/fw)
    Tw=1/fw
    X=np.linspace(-Tw/2,Tw/2,num=N)
    Sinusoid=np.sin(2*np.pi*f0*X)
    Gaussian=Gauss_function(X,0,width)
    G0=Gauss_function(0,0,width)
    Y=Gaussian*Amplitude*Sinusoid/G0
    with open(name, 'w', newline='') as csvfile:
        float_writer = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(N):
            float_writer.writerow([str(Y[i])])

def name(f,i,n):
    '''
    This function's goal is to generate a name for the Gaussian packets file.
    The name contains the frequency but also an index for more accurate management of the files.
    '''
    i_str=str(i)
    n_str=str(n)
    len_i=len(i_str)
    len_n=len(n_str)
    if len_i<len_n:
        num='0'*(len_n-len_i)+i_str
    else:
        num=i_str
    return "Gaussian_Packet_"+num+"_"+str(f)+".csv"


# We first mention the Gaussian packet outer frequency ( the frequency at which the packest will appear )
fw=10000

# We then need to mention the sampling frequency of the GBF and the width of the Gaussian packets
width=4*10**(-6)
fGBF=200*10**6

# We then extract the frequencies we want from the 'frequencies.txt' file containing them all
frequencies=[]
with open('frequencies.txt','r') as file:
    LINES=file.readlines()
    N=len(LINES)
    for k in range(N):
        frequencies.append(float(LINES[k]))
    file.close()

# Then we use all the functions defined above to generate a csv file for every frequency extracted just above
N=len(frequencies)
for i in range(int(N)):
    create_file_Gaussian(fw,frequencies[i],width,fGBF,10,name(frequencies[i],i,1000))
