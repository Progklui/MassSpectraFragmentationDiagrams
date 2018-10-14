# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 16:13:27 2018

@author: Florian Kluibenschedl
@e-mail: florian.kluibenschedl@live.de

Program for converting .mzXML files into .csv files with the purpose to be able to generate fragementation diagramms. 

"""

# Imports - these are bound to the emzed area
from pyopenms import *
import pandas as pd

dataframe = pd.DataFrame()

"""
Setting of parameters - very important - keep in accordance with file structur!!
"""

# general file information - be aware of strings - must remain in 'xxxx' format
date = '28092018'
plant = 'Wein'
filename = 'LCMS_Wein_PQD_28092018'
compound_to_analyse = '777PQD'
version = 'Version4'

# scan numbers - begin and end - out of XCalibur

beginID = 1788
endID = 1803

"""
This part is handling the extraction of the desired part! - so far no modifications needed in usual workflow
"""

# Specifying file types and preparation for reading file
filemzXML = '.mzXML'
fileCsv = '.csv'

filename_input = 'RawFiles/'+date+'/'+plant+'/'+filename+filemzXML
filename_output = 'RawFiles/'+date+'/'+plant+'/'+filename+'_'+compound_to_analyse+'-'+version+fileCsv

expXML = MSExperiment()
MzXMLFile().load(filename_input, expXML)

# starting to extract desired area of file - filtering!
index = beginID
#index = int(filter(str.isdigit, beginID))

mzList = []
intensityList = []

#while index <= int(filter(str.isdigit, endID)):
while index <= endID:
    specInspected = expXML[index]
    mz, intensity = specInspected.get_peaks()
    
    #if index == int(filter(str.isdigit, beginID)):
    if index == beginID:
        d = {'scan': index,
         'intensity': intensity,
         'm': mz}
        
        dataframe = pd.DataFrame(d)
        
    d = {'scan': index,
         'intensity': intensity,
         'm': mz}
    
    dataframe = dataframe.append(pd.DataFrame(d))
    
    index += 1

dataframe.to_csv(filename_output)

"""
Some comments follow in the following section and code parts for further development.
"""

"""
This would be an option for using time values instead of IDs but not so exact!!

beginID = 0
endID = 0

beginTime = 270
endTime = 602

for spec in expXML:
    if spec.getRT() >= beginTime and spec.getRT() <= (beginTime + 1):
        beginID = spec.getNativeID()
        
    if spec.getRT() >= endTime and spec.getRT() <= (endTime + 1):
        endID = spec.getNativeID()

# it is also possible to set beginID and endID here, because scan number can be read out with XCalibur!!
"""