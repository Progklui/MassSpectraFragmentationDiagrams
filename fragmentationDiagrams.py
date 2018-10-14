# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 17:45:11 2018

@author: Florian Kluibenschedl
@e-mail: florian.kluibenschedl@live.de

Program for analysis and creation of fragmentation diagrams in mass spectrometry out of .csv files

"""

import os
import time

from tkinter import filedialog

import pandas as pd

import numpy as np
from numpy import trapz

from scipy.signal import savgol_filter
from sklearn.svm import SVR

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import axes3d
import pickle as pl

xMin = 15
xMax = 30
stepWidth = 1

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
        #x = np.arange(15,30,1)
        x = np.arange(xMin, xMax, stepWidth)

        plt.plot(x, data_to_draw.intensity, label = i + ' Da')

    plt.suptitle(plant+' - '+category+'-'+catabolite+fragmentation_mode)
    plt.title(version)
    plt.xlabel('normalised collision energy (in %)')
    plt.ylabel('intensity (arbitrary unit)')
    plt.legend()

    ax.set_ylim(ymin=0)
    #ax.set_xlim([0,96])
    #ax.set_xlim([20,44])
    #ax.set_xlim([15,29])
    ax.set_xlim([xMin,xMax-stepWidth])

    directory = 'diagrams_output/'+plant+'/'+category+'/'+catabolite+'/'+time+'/'+fragmentation_mode+'/'+version+'/'
    diag_name = directory+catabolite+fragmentation_mode+'-'+version

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


choice = '200'

while choice != '0':
    print("---------------------")
    print("create diagram    <1>")
    print("view diagram      <2>")
    print("calc. derivatives <3>")
    print("total ion current <4>")
    print("Exit              <0>")

    choice = input("Enter: ")

    if choice == '1':
        print(" ")

        time = input("time of measurement: ")
        filename = input("filename (.csv file - without last number): ")

        plant = input("plant: ")
        category = input("catabolite type: ")
        catabolite = input("fragmented mass: ")
        fragmentation_mode = input("fragmentation mode: ")

        catabolites_string = input("[M]-fragments of above catabolite: ")
        catabolites = catabolites_string.split(",")

        highest_value_overall = 0
        ms_info_overall = int(catabolites[0])

        xMin = int(input("minimum collision energy: "))
        xMax = int(input("maximum collision energy: "))
        stepWidth = int(input("step width: "))

        versions = input("number of versions: ")

        print("<<info - close window for next to appear>>")

        i = 1
        while i <= int(versions):
            filepath = 'RawFiles/'+time+'/'+plant+'/'+filename+str(i)+'.csv'

            version = 'Version'+str(i)

            print('...'+version)
            plot_diag(catabolites, plant, category, version, catabolite, fragmentation_mode)

            i = i+1

    if choice == '2':
        pathname = filedialog.askopenfilename(title = "Select file",filetypes = (("pickle files","*.pickle"),("all files","*.*")))
        fig = pl.load(open(pathname, 'rb'))

        fig.show()

    if choice == '3':
        pathname = filedialog.askopenfilename(title = "Select file",filetypes = (("pickle files","*.pickle"),("all files","*.*")))
        fig_1 = pl.load(open(pathname, 'rb'))

        dataframe = pd.DataFrame()

        lines = 3
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

        dx = dataframe.iloc[1,0] - dataframe.iloc[0,0]
        y = dataframe.iloc[:,1]

        dydx = np.gradient(y, dx)
        print(dydx)

    if choice == '4':
        print(" ")

        time = input("time of measurement: ")
        filename = input("filename (.csv file - without last number): ")

        plant = input("plant: ")
        category = input("catabolite type: ")
        catabolite = input("fragmented mass: ")
        fragmentation_mode = input("fragmentation mode: ")

        xMin = int(input("minimum collision energy: "))
        xMax = int(input("maximum collision energy: "))
        stepWidth = int(input("step width: "))

        # filepath = filedialog.askopenfilename(title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))

        versions = input("number of versions: ")

        print("<<info - close window for next to appear>>")

        i = 1
        while i <= int(versions):
            filepath = 'RawFiles/'+time+'/'+plant+'/'+filename+str(i)+'.csv'

            version = 'Version'+str(i)
            print('...'+version)

            data = pd.io.parsers.read_csv(filepath)

            highest_value_continuation = 0
            index = 0
            scan = 0

            sums = {'scan': [scan],
                    'sumIntensity': [highest_value_continuation]}

            data_sum = pd.DataFrame(sums)

            for index, row in data.iterrows():
                scan_new = row['scan']

                if scan_new == scan:
                    highest_value_new = row['intensity']

                    highest_value_continuation = highest_value_continuation + highest_value_new
                else:
                    sums = {'scan': [scan],
                            'sumIntensity': [highest_value_continuation]}

                    data_sum = data_sum.append(pd.DataFrame(sums))

                    scan = scan_new
                    highest_value_continuation = 0

            data_sum = data_sum.iloc[2:]

            fig = plt.figure()

            ax = plt.axes()
            ax.yaxis.grid()

            x = np.arange(xMin,xMax,stepWidth)

            plt.plot(x, data_sum.sumIntensity)

            plt.suptitle(plant+'-'+category+'-'+catabolite+fragmentation_mode+"_TIC")
            plt.title(version)
            plt.xlabel("normalised collision energy (in %)")
            plt.ylabel("total intensity (arbitrary unit)")

            ax.set_ylim(ymin=0)
            ax.set_xlim([xMin,xMax-stepWidth])

            directory = 'diagrams_output/'+plant+'/'+category+'/'+catabolite+'/'+time+'/'+fragmentation_mode+'/'+version+'/'
            diag_name = directory+catabolite+fragmentation_mode+'_TIC'

            if not os.path.exists(directory):
                os.makedirs(directory)

            plt.savefig(diag_name+'.png')
            pl.dump(fig, open(diag_name+'.pickle','wb'))

            fig.show()

            i = i+1

input("Press <Enter> to exit!")

#date = '14092018'
#plant = 'Cj'
#category = 'NCC'
#version = 'Version1'

#fragmentation_mode = 'CID+w'
#catabolite = '645'
#filename = '645CID+wunscaled'

#pathname = 'diagrams_output/'+plant+'/'+category+'/'+catabolite+'/'+date+'/'+fragmentation_mode+'/'+version+'/'+filename+'.pickle'
#pathname = 'diagrams_output/'+plant+'/'+category+'/'+catabolite+'/'+date+'/'+fragmentation_mode+'/'+version+'/'+filename+'.pickle'
