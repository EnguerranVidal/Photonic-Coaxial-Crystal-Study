from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def file_reading(nom):
    file=open(nom,'r')
    t=file.readlines()
    file.close()
    return t

def file_translator(nom):
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


list_frequencies,list_attenuations=file_translator('attenuations.txt')
frequencies=np.array(list_frequencies)
pulsations=2*np.pi*np.array(list_frequencies)
attenuations=np.array(list_attenuations)


def equation_fit(X,a,b,c,d,e,f,g,sigma):
    Y=np.zeros_like(X)
    N=len(Y)
    for i in range(N):
        if X[i]<sigma:
            Y[i]=a*np.arctan(b*X[i]+g)+c
        else:
            Y[i]=d*X[i]**2+e*X[i]+f
    return Y

def researcher_fit(x):
    return -np.log(-1.3*10**(-9)*x+0.9328)/31.5

popt,pcov=curve_fit(equation_fit,frequencies,attenuations,p0=(1.0,10**(-7),1.0,1,1.0,0.025,50*10**6,44*10**6),maxfev=800000)

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
f=popt[5]
print('f = ',f)
g=popt[6]
print('g = ',g)
sigma=popt[7]
print('sigma = ',sigma)


x_frequencies=np.linspace(0,50*10**6,num=3000)
x_pulsations=2*np.pi*x_frequencies
y_attenuations=equation_fit(x_frequencies,a,b,c,d,e,f,g,sigma)

pdf_save=False
plt.rcParams.update({'font.size': 21})

if pdf_save:
    with PdfPages('RG59U_pdf.pdf') as pdf:
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
    plt.plot(x_frequencies/(10**6),y_attenuations,'r',label='fitted curve')
    plt.plot(pulsations/(2*np.pi*10**6),attenuations,'x',label = 'data')
    plt.plot(x_frequencies/(10**6),researcher_fit(2*np.pi*x_frequencies),'b',label='researcher curve')
    plt.xlabel('frequency (MHz)')
    plt.ylabel('attenuation coefficients')
    plt.legend()
    plt.grid()
    plt.show()
