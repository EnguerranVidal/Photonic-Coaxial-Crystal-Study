#########################################################################
#                                                                       #
#   The goal of this program is to calculate the attenuation            #
#   coefficients from input amplitudes and output amplitudes and        #
#   storing these values into a new txt file for further use.           #
#                                                                       #
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

# MAIN PROGRAM ----------------------------------------------------------

# We first extract the frequencies and the associated input amplitudes and
# output amplitudes and open a new file called 'output amplitudes.txt' to store the
# newly calculated attenuations
frequencies_file=open('frequencies.txt','r')
input_amplitudes_file=open('input amplitudes.txt','r')
output_amplitudes_file=open('output amplitudes.txt','r')
file=open('attenuations.txt','w+')
frequencies=frequencies_file.readlines()
input_amplitudes=input_amplitudes_file.readlines()
output_amplitudes=output_amplitudes_file.readlines()
print(input_amplitudes)
attenuations=[]
n=len(input_amplitudes)
D=101
# We then for each frequency calculate the attenuation and then write it up into the new file
for i in range(n):
    frequencies[i]=float(frequencies[i])
    input_amplitudes[i]=float(input_amplitudes[i])
    output_amplitudes[i]=float(output_amplitudes[i])
    file.write(str(frequencies[i])+'\n')
    file.write(str((-np.log(output_amplitudes[i]/input_amplitudes[i]))/D)+'\n')
input_amplitudes_file.close()
output_amplitudes_file.close()
frequencies_file.close()
file.close()
