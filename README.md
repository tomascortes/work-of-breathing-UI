# work-of-breathing-UI
Software for obtaining PTP (Pressure-time product, a measure of breathing effort) values from respiratory data. Specifically, from Pes (esophageal pressure) and EAdi (electrical activity of the diaphragm) data obtained from patients with mechanical ventilatory assistance. Includes a user interface, displaying input signals and estimation of points of interest (start and end of inspiration).
 
# PTP estimation
The starting points for computing the Pes integral are computed by first finding the inflection points of the curve. The inflection points are estimated as the intersection points of two smoothed versions of the original curve (using a gaussian filter with two different user-inputted sigma values). Then the starting points are obtained as the first local peak before each inflection point. 
 
The ending points of the Pes integral are computed as the points in which each Edi cycle reaches 75% of its amplitude after the cycle's peak. The starting points of each Edi cycle are estimated in the same way as the Pes's starting points.
 
The PTP for each inspiration cycle is finally computed as the area over the Pes curve from each Pes's starting point to the next ending point.
 
# Installation
You need [Link text Here](https://www.python.org/) installed

To easily install the libraries you can execute (double click) the  file package_installer.py. This will install all extra liabraries, you need to do it just once.
This install the libraries in [dependencies](#dependencies)
# Info
The small and big smoothing parameter can´t be the same

#Integration
The integration is calculated like:
in 1 second we have 100 samples, so to obtain the area 
[picture]
We rest the top square to the sample and the diference 
is calculated like  
```
(max_val*len_cycle - sum(data[start_cycle:end_cycle]))/100
```
### Input
Input data must consist of an excel file with a worksheet with the name: **Resumen para análisis**, in which the two first columns contain the synchronized (same length) EAdi and Pes data, in that order. Data values are read starting from the second row.
### Interface usage
After executing main.py, the user interface will pop up. Choose the input file with *Abrir archivo* button and then press *Continuar*. If everything worked right you should see both signals (Edi and Pes) shown in interactive graphs.
 
You can now press _Calcular_ to compute and visualize the points of interest based on the smoothing values *Suavizado pequeño* and *Suavizado grande* (values shown at the right of input text boxes are the default values. You can also visualize the smoothed curves used in inflection point estimation by checking off the *Mostrar curva de suavizado* checkbox).
### Output
You can use de *Exportar datos* button to generate output. The output consists of an excel file located at _/calculated_data_ folder, which will be automatically created in the same location as the executable file. The output file can be identified by the input file's name and a timestamp corresponding to it's time of creation. This excel file contains a worksheet with the name "results'', in which there are 10 columns:

* 
    * Datapoint 0 corresponds to the first datapoint of the input signals, datapoint 1 corresponds to the second, and so forth, there are 100 Datapoints in one second)
    * When output start with _t_ like _t_start_pes->75%_ it means that the value in in seconds. Under the assumption that the signal frequency is 100 data points per second).

* _n cycle_: Inspiration cycle identifier. The same number is shown in the interactive graphs.
* _integral value pes_: PTP value estimated for that inspiration cycle.
* _integral value edi_: PTP value estimated for that inspiration cycle.
* _start pes_: Datapoint used as starting point when computing the Pes integral .
* _start edi_: Datapoint considered the starting point for the Edi cycle.
* _point 75%_: Datapoint where the x curve reaches 75% when it goes down.
* _t start pes->75%_: Time elapsed from _start_pes_ to _point_75%_
* _t start pes-> start edi_: Time elapsed from _start_pes_ to _start_edi_.
* _t start edi -> 75%_: Time elapsed from _start_edi_ to _point_75%_.
* _t start edi -> peak edi_:  Time elapsed from _start_edi_ to maximun value of the cycle
* _t start edi -> end edi_:Time elapsed from _start_edi_ to the start of the next cycle
* _edi Amplitude_: Amplitude of the cycle in the edi curve
* _pes Amplitude_: Amplitude of the cycle in the pes curve

## dependencies
PyQt5
openpyxl
matplotlib
scipy
Excecute main.py