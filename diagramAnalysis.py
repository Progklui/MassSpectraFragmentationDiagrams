import pickle as pl
from tkinter import filedialog
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

choice = '200'

while choice != '0':
    print(" ")
    print("view diagram      <1>")
    print("calc. derivatives <2>")
    print("total ion current <3>")
    print("Exit              <0>")
    print(" ")

    choice = input("Enter: ")

    if choice == '1':
        pathname = filedialog.askopenfilename(title = "Select file",filetypes = (("pickle files","*.pickle"),("all files","*.*")))
        fig = pl.load(open(pathname, 'rb'))

        fig.show()
    if choice == '2':
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

    if choice == '3':
        filepath = filedialog.askopenfilename(title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))

        data = pd.io.parsers.read_csv(filepath)

        print(data)

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

        x = np.arange(15,30,1)

        plt.plot(x, data_sum.sumIntensity)

        plt.title("total ion current")
        plt.xlabel("scan id")
        plt.ylabel("total intensity (arbitrary unit)")

        ax.set_ylim(ymin=0)
        ax.set_xlim([15,29])

        fig.show()

#date = '14092018'
#plant = 'Cj'
#category = 'NCC'
#version = 'Version1'

#fragmentation_mode = 'CID+w'
#catabolite = '645'
#filename = '645CID+wunscaled'

#pathname = 'diagrams_output/'+plant+'/'+category+'/'+catabolite+'/'+date+'/'+fragmentation_mode+'/'+version+'/'+filename+'.pickle'
#pathname = 'diagrams_output/'+plant+'/'+category+'/'+catabolite+'/'+date+'/'+fragmentation_mode+'/'+version+'/'+filename+'.pickle'

input("Press <Enter> to exit!")
