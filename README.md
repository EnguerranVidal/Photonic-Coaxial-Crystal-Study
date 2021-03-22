# Analysis and characterization of a photonic crystal made with coaxial cables

This instrumentation project was realized by Nina Moëllo, Maxime Thumin and Enguerran Vidal during a study bureau mandatory for our bachelor degree third year under the supervision of M. Hassan SABBAH. It consisted of a peer-review like project where we had to characterize a complicated set of juxtaposed coaxial cables made in such a way tat they model a photonic crystal (these crystal usually cost around hundreds of thousands of dollars to manufacture, so a simpler way to get the same properties in order to study them is a major improvement). That is what the original paper was about ( see [Original Paper.pdf](https://github.com/EnguerranVidal/Photonic-Coaxial-Crystal-Study/blob/main/Original%20Paper.pdf) ). The results of our study as well as all the theoretical and practicle aspects can be found in much greater details in our final documents : [Final_Document-compressed.pdf](https://github.com/EnguerranVidal/Photonic-Coaxial-Crystal-Study/blob/main/Final_Document-compressed.pdf).

This project is copyright prtotected under the MIT License ( see [LICENSE](https://github.com/EnguerranVidal/Photonic-Coaxial-Crystal-Study/blob/main/LICENSE) ).

## Repository contents :

### FOLDERS :
This repository contains 4 folders that each represent a branch of the huge coding work this project needed in order to succeed :

- **[Gaussian_Packets_Creation](https://github.com/EnguerranVidal/Photonic-Coaxial-Crystal-Study/tree/main/Gaussian_Packets_Creation)** : this folcer contains the .py files that were needed in this project in order to automatically create a huge series of Gaussian packets as .csv files ( and therefore usable by our Low-Frequency Generator - GBF in French ). It therefore needed a way to add new frequencies to a .txt file ( [frequencies.txt](https://github.com/EnguerranVidal/Photonic-Coaxial-Crystal-Study/blob/main/Gaussian_Packets_Creation/frequencies.txt) ) and then generate many csv files from it ([gaussian packet generator.py](https://github.com/EnguerranVidal/Photonic-Coaxial-Crystal-Study/blob/main/Gaussian_Packets_Creation/gaussian%20packet%20generator.py) ).

- **[RG58U](https://github.com/EnguerranVidal/Photonic-Coaxial-Crystal-Study/tree/main/RG58U)** : This folder contains the codes and data usedto characterize an homogenous RG-58-U coaxial cable, especially its attenuation and a polynomial fit used to model it.

- **[RG59U](https://github.com/EnguerranVidal/Photonic-Coaxial-Crystal-Study/tree/main/RG59U)** : Pretty much the same contents as [RG58U](https://github.com/EnguerranVidal/Photonic-Coaxial-Crystal-Study/tree/main/RG58U) but for a an homogenous RG-59-U coaxial cable and a first degree interpolation made to model it.

- **[Scopes_Reading](https://github.com/EnguerranVidal/Photonic-Coaxial-Crystal-Study/tree/main/Scopes_Reading)** : This folder contains the code used to read scopes form the output oscilloscope and get the centroids of the input and output Gaussian packets in order to extract the group packet velocities at each frequency.

### FILES :
The repository also holds a few important files :

- **[Figures Creator.py](https://github.com/EnguerranVidal/Photonic-Coaxial-Crystal-Study/blob/main/Figures%20Creator.py)** : this .py file holds the theoretical model of our coaxial photonic crystal made using the attenuations measured in the [RG58U](https://github.com/EnguerranVidal/Photonic-Coaxial-Crystal-Study/tree/main/RG58U) and [RG59U](https://github.com/EnguerranVidal/Photonic-Coaxial-Crystal-Study/tree/main/RG59U) tasks and an object-oriented class code. It then plots the article daa, our own data as well as the results of the model.


- **[multipage_pdf.pdf](https://github.com/EnguerranVidal/Photonic-Coaxial-Crystal-Study/blob/main/multipage_pdf.pdf)** : PDF output from [Figures Creator.py](https://github.com/EnguerranVidal/Photonic-Coaxial-Crystal-Study/blob/main/Figures%20Creator.py) holding the plots that can be seen in our [Final Document](https://github.com/EnguerranVidal/Photonic-Coaxial-Crystal-Study/blob/main/Final_Document-compressed.pdf).




