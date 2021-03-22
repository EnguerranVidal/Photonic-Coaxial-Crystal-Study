import numpy as np

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
