"""
Venn Helpers to create vennPlots used in the report
"""
import os 
import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import numpy as np
import pandas as pd
import math
import utils as vennUtils



"""
Actual Plots
"""

def checkLeftRigtSubset(api1_df, api2_df, filename = None):    
    result_dict = dict()

    for file in api1_df.File.unique():
        result_dict[file] = {'left': [], 'right': []}
        print(file)
        ## Test Right for file
        left_lst = vennUtils.getSide(file, api1_df, api2_df, direction = 'left')
        right_lst = vennUtils.getSide(file, api1_df, api2_df, direction = 'right')

        i = vennUtils.getSingleInMulti(api2_df, api1_df, left_lst)
        result_dict[file]['left'] = [i, len(left_lst)-i]
        i = vennUtils.getSingleInMulti(api1_df, api2_df, right_lst)
        result_dict[file]['right'] = [i, len(right_lst)-i]

    fig, axes = plt.subplots(figsize=(18,8),nrows=3, ncols=3)
    fig.tight_layout() 

    i = 0
    for file in result_dict.keys():
        row_i = math.floor((i)/3) 
        col_i = i % 3
        l1 =  result_dict[file]['left']
        l2 =  result_dict[file]['right']
        plotdata = pd.DataFrame({
            "Subset": [l1[0], l2[0]],
            "NotSubset":[l1[1], l2[1]]
            }, 
            index=["Left", "Right"]
        )
        plotdata.plot(ax=axes[row_i,col_i], kind='bar', stacked=True)
        title = os.path.basename(file).split('.')[1]
        axes[row_i,col_i].title.set_text(title)
        i = i +1
    fig.suptitle("Venn of names that match only 1 Sense.ID")
    fig.subplots_adjust(top=0.88)
    if filename is not None:
        fig.savefig(filename)
    
    

def VennComparePerfect(api1_df, api2_df, filename = None):
    plt.rcParams["figure.figsize"] = (20,10)
    N = len(api1_df.File.unique())
    i = 0
    row = 3
    col = 3
    for file in api1_df.File.unique():
        i = i+1
        lst1 = api1_df.query("File == @file").query("N_IDS == 1").Name.to_list()
        lst2 = api2_df.query("File == @file").query("N_IDS == 1").Name.to_list()
        NMATCH = 0
        for name in vennUtils.intersection(lst1, lst2):
            S1 = api1_df.query("File == @file").query("Name == @name").Sense_ID
            S2 = api2_df.query("File == @file").query("Name == @name").Sense_ID
            if S1.to_list()[0][0] == S2.to_list()[0][0]:
                NMATCH = NMATCH+1

        plt.subplot(row, col, i)
        vennUtils.vennFromLst(lst1, lst2)
        f = os.path.basename(file).split('.')[1]
        txt = "{} PerfectMatch = {}"
        title = txt.format(f, NMATCH)    
        plt.title(title)
    plt.suptitle("Venn of names that match only 1 Sense.ID")
    #plt.figure(figsize = (20,20))
    if filename is not None:
        plt.savefig(filename, bbox_inches='tight')

def plotVenn1(df1, df2, width = 20, height =  10, filename = None):
    plt.rcParams["figure.figsize"] = (width, height)
    N = len(df1.File.unique())
    i = 0
    row = 3
    col = 3
    for file in df1.File.unique():
        i = i+1
        lst1 = df1.query("File == @file").Name.to_list()
        lst2 = df2.query("File == @file").Name.to_list()    
        plt.subplot(row, col, i)
        vennUtils.vennFromLst(lst1, lst2)
        f = os.path.basename(file).split('.')[1]
        txt = "{}"
        title = txt.format(f,0)    
        plt.title(title)
    plt.suptitle("Venn of names that returned from API")
    if filename is not None:
        plt.savefig(filename, bbox_inches='tight')

def p1():
    plt.rcParams["figure.figsize"] = (20,10)
    # Data for plotting
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)

    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
           title='About as simple as it gets, folks')
    ax.grid()
    return(plt)