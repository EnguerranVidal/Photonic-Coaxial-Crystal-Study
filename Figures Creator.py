#########################################################################
#                                                                       #
#   The goal of this program is to modelize the coaxial photonic        #
#   cristal using a matrix solving method to retrieve the theoretical   #
#   curves contained in the original study of Alain Haché and           #
#   Abderrahim Slimani that was the base of our Study Bureau.           #
#   We also wish to get all data taken from our own experiments and     #
#   the article to compare them by plotting them.                       #
#                                                                       #
#                                                                       #
#   This programm is coded in Python language and needs special         #
#   libraries to work. Especially Numpy and Matplotlib libraries are    #
#   necessary and the programm can't work without them.                 #
#                                                                       #
#########################################################################



# IMPORTS ---------------------------------------------------------------

#########################################################################
#                                                                       #
#   We first import the necessary libraries like mentionned.            #
#                                                                       #
#########################################################################

import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


# CLASSES ---------------------------------------------------------------

#########################################################################
#                                                                       #
#   We create a Python Object modelizing a certain medium.              #
#                                                                       #
#########################################################################


class Medium():
    '''
    The Medium class creates a certain medium and saves up its specifics useful for the rest
    of the program.

    Parameters :
    
    - length : length of the medium ( default value = None )
    - impedance : electrical impedance of the medium ( default value = None )
    - phase_velocity : the phase velocity of electical waves in the medium ( default value = None )
    - attenuation_function : a function of lineic attenuation depending on the pulsation of the electrical wave inside the medium ( default value = None )
    - name : the designated name of the medium ( default value = None ) 

    Attributes :
    
    - length : length of the medium
    - impedance : electrical impedance of the medium
    - phase_velocity : the phase velocity of electical waves in the medium
    - attenuation_function : a function of lineic attenuation depending on the pulsation of the electrical wave inside the medium
    - name : the designated name of the medium
    
    Fonctions :

    - none
    
    '''
    def __init__(self,length=None,impedance=None,phase_velocity=None,attenuation_function=None,name=None):
        self.length=length
        self.impedance=impedance
        self.phase_velocity=phase_velocity
        self.attenuation_function=attenuation_function
        self.name=name

#########################################################################
#                                                                       #
#   We create a Python Object modelizing the all photonic cristal       #
#   coaxial model and easing the calculations of the theroetical        #
#   values and curves.                                                  #
#                                                                       #
#########################################################################

class Multi_Layered_Media_Model():
    '''
    The Multi_Layered_Media_Model class creates a coaxial photonic cristal model and lets you decide the layout of layers and their specifics.
    

    Parameters :
    
    - layers : defines the medium that will be used to create the layers layout, input a list of Medium Objects ( default value = [] )
    - build_mode : defines how the layers defined just before will be used to create the layout.
                  Two values can be used :
                  . 'direct_define' : layout is created by directly putting the layers as given
                  . 'alternation' : layout is created by putting the layers given on a periodic system
    - n_alternation : number of periods of layouts using the layers given ( default value = None )
    - input_medium : defines an input medium for the model ( default value = None )
    - output_medium : defines an output medium for the model ( default value = None )

    Attributes :
    
    - layers : the layout of the layers, contains Medium objects
    - base_layers : base layers used in the creation of the layout
    - build_mode : defines how the base layers were used in the creation of the model
    - n_alternation : number of periods of layouts using the layers given ( default value = None )
    - input_medium : input medium for the model
    - output_medium : output medium for the model

    - pulsations : contains the pulsations range on which further calculations are done
    - c_transmissions : contains the complex values of transmissions done on the pulsations range
    - c_reflections : contains the reflections ratio done on the pulsations range
    - phases : contains the arguments of the c_transmissions ( phases )
    - phase_shifts : contains the phase shifts done on the pulsations range
    - refraction_indexes : contains the rafraction indexes calculated on the pulsations range
    - wave_numbers : contains the wave numbers calculated on the pulsations range
    - group_velocities : contains the group velocities calculated on the pulsations range
    
    Fonctions :

    - __str__ : lets the user use the print() function directly to get the layout of the model
    - total_length : calculates the total length of the coaxial model
    - overall_transmission : calculates and returns the c_transmissions and c_reflections ( calculates the transfer function )
    - overall_phases : gets the arguments of the complex transmissions and return them ( calculates the phases )
    - overall_phase_shifts : calculates the phase shifts using the phases
    - overall_refraction_indexes : calculates the refraction indexes using previous data
    - overall_wave_numbers : calculates the wave numbers using previous data
    - overall_group_velocities : calculates the group velocities using previous data
    
    '''
    def __init__(self,layers=[],build_mode='direct_define',n_alternation=None,input_medium=None,output_medium=None):
        # Function that initialize the model and constructs the layout based on the base layers given and the building mode given
        if build_mode=='alternation':
            # If build_mode is ' alteration', we take the base layers and repeat them as many as n_alternation
            assert type(layers)==list and len(layers)!=0
            self.base_layers=layers
            n=n_alternation
            k=len(layers)
            self.layers=[]
            for i in range(n):
                for j in range(k):
                    self.layers.append(self.base_layers[j])
            assert len(self.layers)==len(self.base_layers)*n

        if build_mode=='direct_define':
            # If build_mode is ' direct_define', the layers layout is a direct copy of the base layers
            self.base_layers=layers
            self.layers=layers
        # We then define other variables using the inputs of the initialization
        self.n_layers=len(self.layers)
        self.n_alternation=n_alternation
        self.input_medium=input_medium
        self.output_medium=output_medium
        
        # Saved values for later calculations, made in None variables at first
        self.pulsations=None
        self.c_trannsmissions=None
        self.c_reflections=None
        self.phases=None
        self.phase_shifts=None
        self.refraction_indexes=None
        self.wave_numbers=None
        self.group_velocities=None
        

        
    def __str__(self):
        # As mentionned above, prints out the layout of the model
        string='Coaxial Model = | '
        for i in range(self.n_layers):
            string=string+str(self.layers[i].name)+' | '
        return string
    
    def total_length(self):
        # As mentionne above, gives the total length of the model
        d=0
        for i in range(len(self.layers)):
            d=d+self.layers[i].length
        return d
    
    def overall_transmission(self,w):
        # As mentionned above, calculates the transfer function values for a given pulsation range ( given with w )
        # We first verify that we have a input and output medium as the methode used needs one
        assert self.input_medium!=None ;" No Input Medium defined "
        assert self.output_medium!=None ;" No Output Medium defined "
        t=1
        r=1
        # We calculate the transmission and reflection ratio based on the formulas derived from the matrix modelization of the model
        for k in range(self.n_layers): # k : calculation index
            i=(self.n_layers-1)-k      # i : medium index in the model
            # Calculation for the last medium of the model layout ( first one to be studied --> k=0 )
            if k==0: 
                LayerH=self.layers[i-1]# Layer H : previous layer
                LayerI=self.layers[i] # Layer I : studied layer
                LayerJ=self.output_medium # Layer J : layer just after
                # Each time we calculate the different 
                t1plus=transmission(LayerH,LayerI)
                t2plus=transmission(LayerI,LayerJ)
                t1minus=transmission(LayerI,LayerH)
                r1plus=reflection(LayerH,LayerI)
                r2plus=reflection(LayerI,LayerJ)
                r1minus=reflection(LayerI,LayerH)
                D=LayerI.length
                k=LayerI.attenuation_function(w)
                phase_shift=w*D/LayerI.phase_velocity
                t=(t1plus*t2plus*np.exp(1j*phase_shift-k*D))/(1-r1minus*r2plus*np.exp(2j*phase_shift-2*k*D))
                r=r1plus+(t1plus*t1minus*r2plus*np.exp(2j*phase_shift-2*k*D))/(1-r1minus*r2plus*np.exp(2j*phase_shift-2*k*D))
            # Calculation for the first medium of the model layout ( last one to be studied --> k=n_layers-1 )
            elif k==self.n_layers-1:
                LayerH=self.input_medium
                LayerI=self.layers[i]
                LayerJ=self.layers[i+1]
                t1plus=transmission(LayerH,LayerI)
                t2plus=t
                t1minus=transmission(LayerI,LayerH)
                r1plus=reflection(LayerH,LayerI)
                r2plus=r
                r1minus=reflection(LayerI,LayerH)
                D=LayerI.length
                k=LayerI.attenuation_function(w)
                phase_shift=w*D/LayerI.phase_velocity
                t=(t1plus*t2plus*np.exp(1j*phase_shift-k*D))/(1-r1minus*r2plus*np.exp(2j*phase_shift-2*k*D))
                r=r1plus+(t1plus*t1minus*r2plus*np.exp(2j*phase_shift-2*k*D))/(1-r1minus*r2plus*np.exp(2j*phase_shift-2*k*D))
            # Calculation for the rest of the layers
            else:
                LayerH=self.layers[i-1]
                LayerI=self.layers[i]
                LayerJ=self.layers[i+1]
                t1plus=transmission(LayerH,LayerI)
                t2plus=t
                t1minus=transmission(LayerI,LayerH)
                r1plus=reflection(LayerH,LayerI)
                r2plus=r
                r1minus=reflection(LayerI,LayerH)
                D=LayerI.length
                k=LayerI.attenuation_function(w)
                phase_shift=w*D/LayerI.phase_velocity
                t=(t1plus*t2plus*np.exp(1j*phase_shift-k*D))/(1-r1minus*r2plus*np.exp(2j*phase_shift-2*k*D))
                r=r1plus+(t1plus*t1minus*r2plus*np.exp(2j*phase_shift-2*k*D))/(1-r1minus*r2plus*np.exp(2j*phase_shift-2*k*D))
        # We store the values of the results and return them to the user as well
        self.c_transmissions=t
        self.r_transmissions=r
        self.pulsations=w
        return t,r

    def overall_phases(self):
        # We extract the phases by calculating the arguments of the transmissions that are imaginary values
        self.phases=np.arctan(self.c_transmissions.imag/self.c_transmissions.real)
        return self.phases
    
    def overall_phase_shifts(self):
        # We calculate the phase shifts by adding 180° each time the phases go from +180° to -180°,if we reason in degrees.
        # Here we reason in radians
        phase_shifts=np.zeros_like(self.phases)
        m=0
        for i in range(self.phases.shape[0]):
            if i!=0 and self.phases[i-1]==abs(self.phases[i-1]) and self.phases[i]==-abs(self.phases[i]):
                m=m+1
            phase_shifts[i]=self.phases[i]+m*np.pi
        self.phase_shifts=phase_shifts
        return phase_shifts

    def overall_refraction_indexes(self):
        # We calculate the refraction indexes using the phase shifts calculated just above, we then store the velues
        indexes=(self.phase_shifts*constant('c'))/(self.total_length()*self.pulsations)
        self.refraction_indexes=indexes
        return indexes

    def overall_wave_numbers(self):
        # We calculate the wave numbers using the dispersion relation and storing those values
        numbers=(self.refraction_indexes*self.pulsations)/constant('c')
        N=numbers.shape[0]
        k0=0.314
        for i in range(N):
            k=numbers[i]
            while k>=k0:
                k=2*k0-abs(k)
                k=abs(k)
            numbers[i]=k
        self.wave_numbers=numbers
        return numbers

    def overall_group_velocities(self):
        # We calculate the group velocities on the pulsation range and store the values
        dw=self.pulsations[1]-self.pulsations[0]
        dndw=np.gradient(self.refraction_indexes,dw) #np.gradient() is a finite derivative method so that we can get dn/dw
        self.group_velocities=constant('c')/(self.refraction_indexes+self.pulsations*dndw)
        return self.group_velocities



# FUNCTIONS -------------------------------------------------------------

#########################################################################
#                                                                       #
#   We then need a few other needed functions used above.               #
#                                                                       #
#########################################################################


# The new attenuations that we mesured and modelized or interpolized to get rough estimates

# For the RG58U cable, we did a curve fit on the data taken from our measurements and got the following expression
attenuation_RG58U=lambda w : -3.7881791187642735*10**(-36)*(w**4)+2.735326073454789*10**(-27)*(w**3)-6.367690393696193*10**(-19)*(w**2)+1.0397790765150726*10**(-10)*w+0.0012431624352975269
# It essentially is a fourth degree polynom with coefficients best adapted to the data fed to the program that came up with them

# For the RG59U cable, we sadly couldn't make a curve fit, the fucntio being to difficult to modelize simply
# We are then forced to do a simple but rough first degree interpolation ( meaning we draw lines between the data points and use that as a makeshift function )

def attenuation_RG59U(w):
    list_frequencies,list_attenuations=txt_file_translator('RG59U frequencies-attenuations.txt')
    frequencies=np.array(list_frequencies)
    pulsations=2*np.pi*np.array(list_frequencies)
    attenuations=np.array(list_attenuations)
    return np.interp(w,pulsations,attenuations)

def file_reading(nom):
    file=open(nom,'r')
    t=file.readlines()
    file.close()
    return t

def txt_file_translator(nom):
    t=file_reading(nom)
    n=len(t)
    images=[]
    labels=[]
    for i in range(n):
        if i%2==0:
            image=float(t[i])
            images.append(image)
        else:
            label=float(t[i])
            labels.append(label)
    return images,labels

def csv2txt(csv_file_name,txt_file_name):
    ''' Transforms a csv file into a txt file ( easier to read in Python ) '''
    with open(txt_file_name, "w") as my_output_file:
        with open(csv_file_name, "r") as my_input_file:
            [ my_output_file.write(" ".join(row)+'\n') for row in csv.reader(my_input_file)]
    my_output_file.close()


def standarization(txt_file_name):
    ''' Focuses on getting floats into an anglophone syntax ( basically , --> . )'''
    with open(txt_file_name,"r")as file:
        LINES=file.readlines()
        file.close()
    N=len(LINES)
    for i in range(N):
        line=str(LINES[i])
        line=line.replace(' ','.')
        LINES[i]=line
    with open(txt_file_name,"w")as file:
        for j in range(N):
            file.write(LINES[j])

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

def transmission(medium1,medium2):
    ''' calculates the transmission ratio from a medium1 to a medium2'''
    z1=medium1.impedance
    z2=medium2.impedance
    return (2*z1)/(z1+z2)

def reflection(medium1,medium2):
    ''' calculates the reflection ratio from a medium1 to a medium2'''
    z1=medium1.impedance
    z2=medium2.impedance
    return (z1-z2)/(z1+z2)

    
def constant(name):
    ''' returns constants from a given name in SI units'''
    if name=='c':
        return 299792458




# MAIN PROGRAM ----------------------------------------------------------

#########################################################################
#                                                                       #
#   We then code the main programm and use all that we defined above.   #
#                                                                       #
#########################################################################


# We first create the frequency/ pulsation range up to 50 MHz
frequencies=np.linspace(1,50*10**6,num=100000)
impulsions=2*np.pi*frequencies

# We the, define the 4 media used in the model ( input, output, RG58U and RG59U )
Input=Medium(impedance=50,name='GBF')
Output=Medium(impedance=50,name='Termination')

RG58U=Medium(length=5,impedance=50,
             phase_velocity=0.66*constant('c'),
             attenuation_function=attenuation_RG58U,
             name='RG58U')
RG59U=Medium(length=5,impedance=75,
             phase_velocity=0.66*constant('c'),
             attenuation_function=attenuation_RG59U,
             name='RG59U')

# We the use the Multi_Layered_Media_Model class to create the coaxial model
Coaxial=Multi_Layered_Media_Model(layers=[RG59U,RG58U],
                                  build_mode='alternation',
                                  n_alternation=12,
                                  input_medium=Input,
                                  output_medium=Output)

# We finally calculate all the theroetical values by calling all the functions attached to the model
c_transmissions,c_reflections=Coaxial.overall_transmission(impulsions)
transmissions,reflections=abs(c_transmissions),abs(c_reflections)

phases=Coaxial.overall_phases()
phases_shifts=Coaxial.overall_phase_shifts()

indexes=Coaxial.overall_refraction_indexes()
numbers=Coaxial.overall_wave_numbers()
velocities=Coaxial.overall_group_velocities()

# We print some useful informations like the model layout and the total length
print(Coaxial)
print('Model total length : ',Coaxial.total_length(),' m')

# We then need the useful data to plot them with the theoreatical curves
#-------------- Article data ----------------#
# TRANSMISSIONS
csv2txt('Transmissions article.csv','Transmissions article.txt')
standarization('Transmissions article.txt')
LINES=file_reading('Transmissions article.txt')
AT_Frequencies=[]
AT_Transmissions=[]
LINES.pop(0)
N=len(LINES)
for i in range(N):
    if len(LINES[i])>0:
        line=LINES[i].split(';')
        AT_Frequencies.append(float(line[0])*10**(6))
        AT_Transmissions.append(float(line[1]))
AT_Frequencies=np.array(AT_Frequencies)
AT_Transmissions=np.array(AT_Transmissions)
#DISPERSION RELATION
csv2txt('Dispersion Relation article.csv','Dispersion Relation article.txt')
standarization('Dispersion Relation article.txt')
LINES=file_reading('Dispersion Relation article.txt')
AK_Frequencies=[]
AK_WaveNumbers=[]
LINES.pop(0)
N=len(LINES)
for i in range(N):
    if len(LINES[i])>0:
        line=LINES[i].split(';')
        AK_Frequencies.append(float(line[0])*10**(6)/(2*np.pi))
        AK_WaveNumbers.append(float(line[1]))
AK_Frequencies=np.array(AK_Frequencies)
AK_WaveNumbers=np.array(AK_WaveNumbers)
#GROUP VELOCITIES
csv2txt('Group Velocities article.csv','Group Velocities article.txt')
standarization('Group Velocities article.txt')
LINES=file_reading('Group Velocities article.txt')
AS_Frequencies=[]
AS_Speeds=[]
LINES.pop(0)
N=len(LINES)
for i in range(N):
    if len(LINES[i])>0:
        line=LINES[i].split(';')
        AS_Frequencies.append(float(line[0])*10**(6))
        AS_Speeds.append(float(line[1]))
AS_Frequencies=np.array(AS_Frequencies)
AS_Speeds=np.array(AS_Speeds)
#-------------- Experimental data ----------------#
# TRANSMISSIONS
csv2txt('Composite Cable Experimental Transmissions.csv','Composite Cable Experimental Transmissions.txt')
standarization('Composite Cable Experimental Transmissions.txt')
LINES=file_reading('Composite Cable Experimental Transmissions.txt')
ET_Frequencies=[]
ET_Transmissions=[]
LINES.pop(0)
LINES.pop(0)
N=len(LINES)
for i in range(N):
    if len(LINES[i])>0:
        line=LINES[i].split(';')
        ET_Frequencies.append(float(line[0])*10**(6))
        ET_Transmissions.append(float(line[2])/float(line[1]))
ET_Frequencies=np.array(ET_Frequencies)
ET_Transmissions=np.array(ET_Transmissions)
# GROUP VELOCITIES
ES_Speeds=read_float_file('Composite Cable Experimental Group Velocities.txt')
ES_Frequencies=read_float_file('Composite Cable Experimental Group Velocities Frequencies.txt')
ES_Speeds=np.array(ES_Speeds)
ES_Frequencies=np.array(ES_Frequencies)

pdf_save=True
plt.rcParams.update({'font.size': 21})

if pdf_save:
    # If pdf_save is True, then we create a pdf called multipage_pdf.pdf containing all the values
    with PdfPages('multipage_pdf.pdf') as pdf:
        #------------------TRANSMISSIONS-----------------#
        # Transmission theoretical
        fig = plt.figure(figsize=(11.69,8.27))
        plt.plot(frequencies/(10**6),transmissions,'k',label='Theoretical curve')
        plt.yscale("log")
        plt.xlabel('frequency (MHz)')
        plt.ylabel('| t |')
        plt.grid()
        plt.legend()
        pdf.savefig(fig)
        plt.close()
        
        # Transmission experimental
        fig = plt.figure(figsize=(11.69,8.27))
        plt.plot(ET_Frequencies/(10**6),ET_Transmissions,'gx',label='Experimental data')
        plt.yscale("log")
        plt.xlabel('frequency (MHz)')
        plt.ylabel('| t |')
        plt.grid()
        plt.legend()
        pdf.savefig(fig)
        plt.close()

        # Transmission experimental+theoretical
        fig = plt.figure(figsize=(11.69,8.27))
        plt.plot(frequencies/(10**6),transmissions,'k',label='Theoretical curve')
        plt.plot(ET_Frequencies/(10**6),ET_Transmissions,'gx',label='Experimental data')
        plt.yscale("log")
        plt.xlabel('frequency (MHz)')
        plt.ylabel('| t |')
        plt.grid()
        plt.legend()
        pdf.savefig(fig)
        plt.close()

        # Transmission article
        fig = plt.figure(figsize=(11.69,8.27))
        plt.plot(AT_Frequencies/(10**6),AT_Transmissions,'rx',label='Article data')
        plt.yscale("log")
        plt.xlabel('frequency (MHz)')
        plt.ylabel('| t |')
        plt.grid()
        plt.legend()
        pdf.savefig(fig)
        plt.close()

        # Transmission article+experimental+theoretical
        fig = plt.figure(figsize=(11.69,8.27))
        plt.plot(frequencies/(10**6),transmissions,'k',label='Theoretical curve')
        plt.plot(ET_Frequencies/(10**6),ET_Transmissions,'gx',label='Experimental data')
        plt.plot(AT_Frequencies/(10**6),AT_Transmissions,'rx',label='Article data')
        plt.yscale("log")
        plt.xlabel('frequency (MHz)')
        plt.ylabel('| t |')
        plt.grid()
        plt.legend()
        pdf.savefig(fig)
        plt.close()

        # Transmission article+experimental
        fig = plt.figure(figsize=(11.69,8.27))
        plt.plot(ET_Frequencies/(10**6),ET_Transmissions,'gx',label='Experimental data')
        plt.plot(AT_Frequencies/(10**6),AT_Transmissions,'rx',label='Article data')
        plt.yscale("log")
        plt.xlabel('frequency (MHz)')
        plt.ylabel('| t |')
        plt.grid()
        plt.legend()
        pdf.savefig(fig)
        plt.close()

        fig = plt.figure(figsize=(11.69,8.27))
        plt.plot(frequencies/(10**6),(phases*360)/(2*np.pi),'k',label='Theoretical curve')
        plt.xlabel('frequency (MHz)')
        plt.ylabel('phases (°)')
        plt.grid()
        plt.legend()
        pdf.savefig(fig)
        plt.close()

        fig = plt.figure(figsize=(11.69,8.27))
        plt.plot(frequencies/(10**6),(phases_shifts*360)/(2*np.pi),'k',label='Theoretical curve')
        plt.xlabel('frequency (MHz)')
        plt.ylabel('phase shifts (°)')
        plt.grid()
        plt.legend()
        pdf.savefig(fig)
        plt.close()

        fig = plt.figure(figsize=(11.69,8.27))
        plt.plot(frequencies/(10**6),indexes,'k',label='Theoretical curve')
        plt.xlabel('frequency (MHz)')
        plt.ylabel('refraction index')
        plt.grid()
        plt.legend()
        pdf.savefig(fig)
        plt.close()
        
        #------------------DISPERSION RELATION-----------------#
        # Dispersion relation theoretical
        fig = plt.figure(figsize=(11.69,8.27))
        plt.plot(numbers,frequencies/(10**6),'k',label='Theoretical curve')
        plt.ylabel('frequency (MHz)')
        plt.xlabel('k ( m^-1)')
        plt.grid()
        plt.legend()
        pdf.savefig(fig)
        plt.close()

        # Dispersion relation article+theoretical
        fig = plt.figure(figsize=(11.69,8.27))
        plt.plot(numbers,frequencies/(10**6),'k',label='Theoretical curve')
        plt.plot(AK_WaveNumbers,AK_Frequencies/(10**6),'rx',label='Article data')
        plt.ylabel('frequency (MHz)')
        plt.xlabel('k ( m^-1)')
        plt.grid()
        plt.legend()
        pdf.savefig(fig)
        plt.close()

        #------------------GROUP VELOCITIES-----------------#
        # Group velocities theoretical
        fig = plt.figure(figsize=(11.69,8.27))
        plt.plot(frequencies/(10**6),velocities/constant('c'),'k',label='Theoretical curve')
        plt.ylabel('group velocity ( in units of c )')
        plt.xlabel('frequency (MHz)')
        plt.grid()
        plt.legend()
        pdf.savefig(fig)
        plt.close()

        # Group velocities experimental
        fig = plt.figure(figsize=(11.69,8.27))
        plt.plot(ES_Frequencies/(10**6),ES_Speeds,'gx',label='Experimental data')
        plt.ylabel('group velocity ( in units of c )')
        plt.xlabel('frequency (MHz)')
        plt.grid()
        plt.legend()
        pdf.savefig(fig)
        plt.close()

        # Group velocities experimental+theoretical
        fig = plt.figure(figsize=(11.69,8.27))
        plt.plot(frequencies/(10**6),velocities/constant('c'),'k',label='Theoretical curve')
        plt.plot(ES_Frequencies/(10**6),ES_Speeds,'gx',label='Experimental data')
        plt.ylabel('group velocity ( in units of c )')
        plt.xlabel('frequency (MHz)')
        plt.grid()
        plt.legend()
        pdf.savefig(fig)
        plt.close()

        # Group velocities article+experimental
        fig = plt.figure(figsize=(11.69,8.27))
        plt.plot(ES_Frequencies/(10**6),ES_Speeds,'gx',label='Experimental data')
        plt.plot(AS_Frequencies/(10**6),AS_Speeds,'rx',label='Article data')
        plt.ylabel('group velocity ( in units of c )')
        plt.xlabel('frequency (MHz)')
        plt.grid()
        plt.legend()
        pdf.savefig(fig)
        plt.close()

        # Group velocities article+experimental+theoretical
        fig = plt.figure(figsize=(11.69,8.27))
        plt.plot(frequencies/(10**6),velocities/constant('c'),'k',label='Theoretical curve')
        plt.plot(ES_Frequencies/(10**6),ES_Speeds,'gx',label='Experimental data')
        plt.plot(AS_Frequencies/(10**6),AS_Speeds,'rx',label='Article data')
        plt.ylabel('group velocity ( in units of c )')
        plt.xlabel('frequency (MHz)')
        plt.grid()
        plt.legend()
        pdf.savefig(fig)
        plt.close()


        
else:
    # If pdf_save is False, we then just plot the values calculated earlier
    fig=plt.figure() # We define the figure

    ax1=fig.add_subplot(131)
    ax1.plot(frequencies/(10**6),transmissions)
    plt.yscale("log")
    plt.xlabel('frequency (MHz)')
    plt.ylabel('| t |')

    ax2=fig.add_subplot(132)
    ax2.plot(numbers,frequencies/(10**6))
    plt.ylabel('frequency (MHz)')
    plt.xlabel('k ( m^-1 )')

    ax3=fig.add_subplot(133)
    ax3.plot(frequencies/(10**6),velocities/constant('c'))
    plt.ylabel('group velocity ( units of c )')
    plt.xlabel('frequency (MHz)')

    plt.show()# We show the figure
             
    
