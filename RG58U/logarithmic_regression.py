#########################################################################
#                                                                       #
#   The goal of this program is to approach the curve made by the       #
#   attenuations according to the frequencies with a curve fit method.  #
#                                                                       #
#   This programm is coded in Python language and needs special         #
#   libraries to work. Especially Numpy, Matplotlib and Scipy           #
#   libraries are necessary and the programm can't work without them.   #
#                                                                       #
#########################################################################



# IMPORTS ---------------------------------------------------------------

#########################################################################
#                                                                       #
#   We first import the necessary libraries like mentionned.            #
#                                                                       #
#########################################################################


from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# FUNCTIONS -------------------------------------------------------------

#########################################################################
#                                                                       #
#   We then need a few functions to ease up the rest of the programm.   #
#                                                                       #
#########################################################################

def file_reading(nom):
    '''
    This function just reads the contents of a txt file and put them into a list of the lines.
    '''
    file=open(nom,'r')
    t=file.readlines()
    file.close()
    return t

def file_translator(nom):
    '''
    This function reads a file setup a certain way :
    frequency
    attenuation
    frequency
    attenuation
    ....
    The goal of this function is to order them into two seperate lists and then return them
    '''
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

def equation_fit(x,a,b,c,d,e):
    '''
    This function serves as a container of the model fucntion that we want to make fit with the data
    '''
    return a*x**4+b*x**3+c*x**2+d*x+e

def researcher_fit(x):
    '''
    This function is the associated reasercher curve that can be found within the study.
    '''
    return -np.log(-1.7*10**(-9)*x+0.9928)/18.6

# MAIN PROGRAM ----------------------------------------------------------

#########################################################################
#                                                                       #
#   We then code the main programm and use all that we defined above.   #
#                                                                       #
#########################################################################


# We first use the two first functions above to obtain a list of frequencies and a list of attenuations
list_frequencies,list_attenuations=file_translator('attenuations.txt')
# We then generate two arrays : one of pulsations and another of freqencies
pulsations=2*np.pi*np.array(list_frequencies)
attenuations=np.array(list_attenuations)

# We then use Scipy curve_fit method applied on the data, giving a set of initial values for the coefficients mentionned
# in the equation_fit fucntion above.
popt,pcov=curve_fit(equation_fit,pulsations,attenuations,p0=(-1.0,0.0,1.0*10**(-9),1.0,1.0),maxfev=8000)

# Since the adapted coefficients are containes inside popt, we extract them all
a=popt[0]
print('a = ',a)
b=popt[1]
print('b = ',b)
c=popt[2]
print('c = ',c)
d=popt[3]
print('d = ',d)
e=popt[4]
print('e = ',e)

# We then plot the data using the newly found curve fit function.
x_frequencies=np.linspace(0,50*10**6,num=3000)
x_pulsations=2*np.pi*x_frequencies
y_attenuations=equation_fit(x_pulsations,a,b,c,d,e)

pdf_save=True
plt.rcParams.update({'font.size': 21})

if pdf_save:
    # If pdf_save is True, then we create a pdf called 'RG58U_pdf.pdf' containing all the values
    with PdfPages('RG58U_pdf.pdf') as pdf:
        fig = plt.figure(figsize=(11.69,8.27))
        plt.plot(x_frequencies/(10**6),y_attenuations,'r',label='fitted curve')
        plt.plot(pulsations/(2*np.pi*10**6),attenuations,'x',label = 'data')
        plt.plot(x_frequencies/(10**6),researcher_fit(2*np.pi*x_frequencies),'b',label='researcher curve')
        plt.xlabel('frequency (MHz)')
        plt.ylabel('attenuation coefficients')
        plt.legend()
        plt.grid()
        pdf.savefig(fig)
        plt.close()

else:
    # If pdf_save is False, we then just plot the values calculated just above
    plt.plot(x_frequencies/(10**6),y_attenuations,'r',label='fitted curve')
    plt.plot(pulsations/(2*np.pi*10**6),attenuations,'x',label = 'data')
    plt.plot(x_frequencies/(10**6),researcher_fit(2*np.pi*x_frequencies),'b',label='researcher curve')
    plt.xlabel('frequency (MHz)')
    plt.ylabel('attenuation coefficients')
    plt.legend()
    plt.grid()
    plt.show()
