#########################################################################
#                                                                       #
#   The goal of this program is to plot the group velocities            #
#   calculated by the center_masses programm.                           #
#   The goal is also to create a pdf version of the plot created        #
#   here.                                                               #
#                                                                       #
#   This programm is coded in Python language and needs special         #
#   libraries to work. Especially Numpy and Matplotlib libraries are    #
#   necessary and the programm can't work without them.                 #                                                            #
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
from matplotlib.backends.backend_pdf import PdfPages

def read_float_file(file_name):
    ''' This function takes a file_name as input and ouputs the float contents of the file
        in a ordered list
    '''
    content=[]
    with open(file_name,'r') as file:
        LINES=file.readlines()
        N=len(LINES)
        for i in range(N):
            content.append(float(LINES[i]))
        file.close()
    return content

# We first need to read the file containing the previously calculated group velocities
speeds=read_float_file('speeds_in_c.txt')
print(speeds)
# We then do the same to a file containing all the associated frequencies of the Gaussian packets
# that attacked the coaxial photonic cristal model
frequencies=read_float_file('frequencies.txt')
print(frequencies)
# We get two lists that we convert into arrays
speeds=np.array(speeds)
frequencies=np.array(frequencies)
# We also create a array containing only ones ( to simulate a limit line : the sped of light )
line=np.ones_like(frequencies)

# We define this pdf_save variable to determine what how the user wants to continue
pdf_save=True

if pdf_save:
    # If pdf_save is True, then we save the figure containing the data in a pdf version
    with PdfPages('GroupVelocities.pdf') as pdf:
        fig = plt.figure(figsize=(11.69,8.27))
        plt.plot(frequencies/(10**6),speeds,'x',label='data')
        plt.plot(frequencies/(10**6),line,'r',label='light speed')
        plt.xlabel('frequencies (MHz)')
        plt.ylabel('group velocity ( in units of c )')
        plt.legend()
        plt.grid()
        pdf.savefig(fig)
        plt.close()

else:
    # If pdf_save is False, then we just plot the data like normal without saving it.
    plt.plot(frequencies/(10**6),speeds,'x',label='data')
    plt.plot(frequencies/(10**6),line,'r',label='light speed')
    plt.xlabel('frequencies (MHz)')
    plt.ylabel('group velocity ( in units of c )')
    plt.legend()
    plt.grid()
    plt.show()
