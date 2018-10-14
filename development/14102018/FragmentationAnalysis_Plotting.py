
# coding: utf-8

# # Programm for generating fragmentation diagrams in mass spectrometry

# ## Function filtering data from .csv file - returns plottable pandas documents

# In[1]:


def prepare_data(ms_info):
    global filepath

    data = pd.io.parsers.read_csv(filepath)

    data.drop(data[data.m > (ms_info + 2)].index, inplace=True)
    data.drop(data[data.m < (ms_info - 1)].index, inplace=True)

    #data.intensity = savgol_filter(data.intensity, 23, 6, mode='wrap')
    #data.intensity = savgol_filter(data.intensity, 21, 7, mode='nearest')

    global highest_value_overall
    global ms_info_overall
    highest_value = 0
    scan = 0
    index = 0

    d = {'scan': [scan],
         'intensity': [highest_value]}

    data_new = pd.DataFrame(d)
    data_new_scaled = pd.DataFrame(d)

    for index, row in data.iterrows():
        scan_new = row['scan']

        if scan_new == scan:
            highest_value_new = row['intensity']

            if highest_value_new > highest_value:
                highest_value = highest_value_new
        else:
            d = {'scan': [scan],
                 'intensity': [highest_value]}

            data_new = data_new.append(pd.DataFrame(d))

            scan = scan_new
            highest_value = 0

    data_new = data_new.iloc[2:]

    data_new.intensity = savgol_filter(data_new.intensity, 11, 6, mode='nearest')

    if ms_info < ms_info_overall:
        data_new['intensity'].iloc[0] = 0

    for index, row in data_new.iterrows():
        highest_value = row['intensity']

        if highest_value >= highest_value_overall:
                highest_value_overall = highest_value

    for i, row in data_new.iterrows():
        scan = row['scan']
        highest_value = row['intensity']

        d = {'scan': [scan],
             'intensity': [(highest_value/highest_value_overall)*100]}

        data_new_scaled = data_new_scaled.append(pd.DataFrame(d))

    data_new_scaled = data_new_scaled.iloc[2:]

    if ms_info < ms_info_overall:
        data_new_scaled['intensity'].iloc[0] = 0

    return data_new, data_new_scaled


# ## Function plotting the final pandas documents and saving copies

# In[2]:


def plot_diag(catab, plant, category, version, catabolite, fragmentation_mode):

    global time

    fig_1 = plt.figure(1)

    ax = plt.axes()
    ax.yaxis.grid()

    overall_length = 0

    dataframe = pd.DataFrame()
    dataframe_scaled = pd.DataFrame()

    for i in catab:
        data_to_draw, data_to_draw_scaled = prepare_data(int(i))

        length = data_to_draw.scan.size

        if length > overall_length:
            overall_length = length

    for i in catab:
        data_to_draw, data_to_draw_scaled = prepare_data(int(i))

        length = data_to_draw.scan.size
        #x = np.arange(0, (length/(overall_length+1)*100), ((length/(overall_length+1)*100)/length))
        #x = np.arange(0, ((length/overall_length)*100), (((length/overall_length)*100)/length))
        #x = np.arange(20,45,1)
        #x = np.arange(0,100,4)
        x = np.arange(15,30,1)

        plt.plot(x, data_to_draw.intensity, label = i + ' Da')

    plt.title(plant+' - '+category+'-'+catabolite+fragmentation_mode)
    plt.xlabel('normalised collision energy (in %)')
    plt.ylabel('intensity (arbitrary unit)')
    plt.legend()

    ax.set_ylim(ymin=0)
    #ax.set_xlim([0,96])
    #ax.set_xlim([20,44])
    ax.set_xlim([15,29])

    directory = 'diagrams_output/'+plant+'/'+category+'/'+catabolite+'/'+time+'/'+fragmentation_mode+'/'+version+'/'
    diag_name = directory+catabolite+fragmentation_mode+'unscaled'

    if not os.path.exists(directory):
        os.makedirs(directory)

    lines = len(catab)
    index = 0

    while index <= lines - 1:
        data = fig_1.axes[0].lines[index].get_data()

        if index == 0:
            dataframe_two = pd.DataFrame(data[0])
            dataframe = pd.concat([dataframe, dataframe_two], axis=1)

            dataframe_two = pd.DataFrame(data[1])
            dataframe = pd.concat([dataframe, dataframe_two], axis=1)
        else:
            dataframe_two = pd.DataFrame(data[1])
            dataframe = pd.concat([dataframe, dataframe_two], axis=1)

        index = index + 1

    dataframe.to_csv(diag_name+'.csv')
    plt.savefig(diag_name+'.png')
    pl.dump(fig_1, open(diag_name+'.pickle','wb'))

    plt.show()


# ### main imports

# In[3]:


import os
import time

import numpy as np
from numpy import trapz

import pandas as pd

from scipy.signal import savgol_filter
from sklearn.svm import SVR

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d
import pickle as pl


# ### setting constants and file path

# In[4]:


#time = time.strftime("%d%m%Y") # should be in accordance with date of measure - if not, change it!
time = '28092018'
plantname = 'Wein'

filename = 'LCMS_Wein_PQD_28092018_777PQD-Version3'
filepath = 'RawFiles/'+time+'/'+plantname+'/'+filename+'.csv'

version = 'Version3'


plant = input("Specify plant: ")
category = input("Specify catabolite type: ")
catabolite = input("Specify fragmented mass: ")
fragmentation_mode = input("Specify fragmentation mode: ")

catabolites_string = input("Specify [M]-fragments of above catabolite: ")
catabolites = catabolites_string.split(",")

highest_value_overall = 0
ms_info_overall = int(catabolites[0])


# In[6]:


plot_diag(catabolites, plant, category, version, catabolite, fragmentation_mode)
