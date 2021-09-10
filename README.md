# work-of-breathing-UI
Software that alows you to obtain the value of the integration that representes the work of breathing. Providing a UI

Interface created with Qt designer 
# dependencies
PyQt5
openpyxl
xlrd
matplotlib

# Usage
Excecute main.py
# Info
The small and big smoothing parameter can´t be the same

#Integration
The integration is calculated like:
in 1 second we have 100 samples, so to obtain the area 
[picture]
We rest the top square to the sample and the diference 
is calculated like  
(max_val*len_cycle - sum(data[start_cycle:end_cycle]))/100