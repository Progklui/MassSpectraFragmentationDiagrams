# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 16:13:27 2018

@author: Florian Kluibenschedl
@e-mail: florian.kluibenschedl@live.de

Program for converting .mzXML files into .csv files with the purpose to be able to generate fragementation diagramms. 

"""

from pyopenms import *
import pandas as pd

dataframe = pd.DataFrame()

date = '28092018'
plant = 'Wein'
filename = 'LCMS_Wein_PQD_28092018'
compound_to_analyse = '777PQD'
version = 'Version4'

beginTime = 270
endTime = 602

filemzXML = '.mzXML'
fileCsv = '.csv'
#filename_input = 'Kuerbis_Experiment21082017_Analyse24082017_Reaktion10min_Bindungskinetik_RT3635-3670.mzXML'
#filename_output = 'Kuerbis_Experiment21082017_Analyse24082017_Reaktion10min_Bindungskinetik_RT3635-3670_633CID.csv'

filename_input = 'RawFiles/'+date+'/'+plant+'/'+filename+filemzXML
filename_output = 'RawFiles/'+date+'/'+plant+'/'+filename+'_'+compound_to_analyse+'-'+version+fileCsv

expXML = MSExperiment()
MzXMLFile().load(filename_input, expXML)

beginID = 0
endID = 0

for spec in expXML:
    if spec.getRT() >= beginTime and spec.getRT() <= (beginTime + 1):
        beginID = spec.getNativeID()
        
    if spec.getRT() >= endTime and spec.getRT() <= (endTime + 1):
        endID = spec.getNativeID()

# it is also possible to set beginID and endID here, because scan number can be read out with XCalibur!!

#beginID = 157
#endID = 330

beginID = 1788
endID = 1803

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