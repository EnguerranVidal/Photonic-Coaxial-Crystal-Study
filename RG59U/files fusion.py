import numpy as np
import csv


def csv2txt(csv_file,txt_file):
    with open(txt_file, "w") as my_output_file:
        with open(csv_file, "r") as my_input_file:
            [ my_output_file.write(" ".join(row)+'\n') for row in csv.reader(my_input_file)]
        my_output_file.close()

def name_file(file_name):
    file=file_name.split('.')
    return file[0]

def txt_extraction_3columns(file):
    F=[]
    Ain=[]
    Aout=[]
    with open(file,'r') as file:
        LINES=file.readlines()
        LINES.pop(0)
        n=len(LINES)
        for i in range(n):
            line=LINES[i].split(';')
            print(line)
            F.append(float(line[0]))
            Ain.append(float(line[1]))
            Aout.append(float(line[2]))
    return F,Ain,Aout

def write_file_list(file,data_list):
    file=open(file,'w')
    n=len(data_list)
    for i in range(n):
        file.write(str(data_list[i])+'\n')
    file.close()
        
def files_fusion(new_file):
    csv_file=new_file
    txt_file=name_file(csv_file)+'.txt'
    csv2txt(csv_file,txt_file)
    F,Ain,Aout=txt_extraction_3columns(txt_file)
    write_file_list('frequencies.txt',F)
    write_file_list('input amplitudes.txt',Ain)
    write_file_list('output amplitudes.txt',Aout)
        


files_fusion('RG59.csv')
