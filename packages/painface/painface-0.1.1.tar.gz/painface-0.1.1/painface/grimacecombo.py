#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 12:33:13 2021

@author: rahulpatel
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
import statistics
import os
import shutil
from subprocess import call 
import datetime 
import csv
import itertools

def fau_combos():
#create list of all FAU combos
    orbitals = [0,1,2]
    nose = [0,1,2]
    whiskers = [0,1,2]
    ears = [0,1,2]
    cheeks = [0,1,2]
    # result contains all possible combinations.
    combinations = list(itertools.product(orbitals,nose,ears,whiskers,cheeks))
    #combinations
    import re
    commas_removed = []
    for i in combinations:
        original_string = str(i)
        newstring = re.sub(",", "", original_string)
        pattern = re.compile(r'\s+')
        newstring = re.sub(pattern, '', newstring)
        newstring = newstring[1:]
        newstring = newstring[:-1]
        commas_removed.append(newstring)
    return commas_removed


def AU_grimace(threshold, start, stop):
    commas_removed = fau_combos()
    threshold = int(threshold) #change as necessary 
    thres_string = str(threshold)
    start = int(start)#change start time
    stop = int(stop) #change end time 
    directory = os.getcwd()
    direc= os.listdir(directory)
    to_process=[]
    for file in direc:
        if file[-7:]== ('sAU.csv'):
            to_process.append(file)
    print ("Files to process:")
    print (to_process)        
    print ("There are " +str(len(to_process))+ " csv files to be processed. Would you like to continue?")
    answer= input("Y or N: ")
    answer=answer.upper()
    if answer==("Y"):
        print ("Processing Files.")
        #with open(data_log, 'a+') as file:
            #writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            #writer.writerow(["File_Name",'UseableFrame%','UseableFramesFromFirst10Minutes','AverageTotalGrimaceScore','AvgEyeScore','AvgEarScore','AvgNoseScore','AvgWhiskerScore', 'AvgCheekScore', 'AverageGrimaceScoreFirst10Min',str('AverageGrimaceScore'+thres_string+'frames'),'SampledEyeScore','SampledEarScore','SampledNoseScore','SampledWhiskerScore','SampledCheekScore','Process_Time'])
        count = 0
        for _csv in to_process:
            FileName = _csv
            csvname = FileName
            filename = csvname[:-4]
            comboname = str(filename +'_AutoSampledWholeVideoFramesCombinations.xlsx')
            #begin_time = datetime.datetime.now()
            df = pd.read_csv(_csv)
            AUcsv = df[(df.AUScored == 5)]
            total_frames = len(AUcsv)
            df = AUcsv
            #print(total_frames)
            if total_frames >= threshold:
                fiveFAU = df[df['Timestamp(x)'].between(start, stop)]
                sampled_5FAU = fiveFAU.sample(n = threshold)
                count_series = sampled_5FAU.groupby(['Orbital','Nose','Ears', 'Whiskers', 'Cheek']).size()
                sampled_FAUs = count_series.to_frame(name = 'Count').reset_index()
                sampled_FAUs['Percentage']= ((sampled_FAUs['Count']/threshold)*100)
                sampled_FAUs['Orbital'] = sampled_FAUs["Orbital"].astype(int) 
                sampled_FAUs['Nose'] = sampled_FAUs["Nose"].astype(int) 
                sampled_FAUs['Ears'] = sampled_FAUs["Ears"].astype(int) 
                sampled_FAUs['Whiskers'] = sampled_FAUs["Whiskers"].astype(int) 
                sampled_FAUs['Cheek'] = sampled_FAUs["Cheek"].astype(int) 
                sampled_FAUs['Combo(ONEWC)'] = sampled_FAUs['Orbital'].astype(str) + sampled_FAUs['Nose'].astype(str) + sampled_FAUs['Ears'].astype(str) + sampled_FAUs['Whiskers'].astype(str) + sampled_FAUs['Cheek'].astype(str)
                averages = []
                sizes = []
                for i in commas_removed:
                    combination = i
                    group = sampled_FAUs.loc[sampled_FAUs['Combo(ONEWC)'] == i]
                    size = len(group)
                    average = group["Percentage"].mean()
                    #print(i)
                    #print(size)
                    #print(average)
                    averages.append(average)
                    sizes.append(size)
                    # print(len(averages))
                    # print(len(commas_removed))
                df1 = pd.DataFrame(columns=commas_removed)
                df1.loc[len(df)] = averages
                df2 = df1
                df2.insert(0, "FileName", [comboname], True)
                df2.columns = df1.columns.astype(str)
                df2.to_excel(comboname,header= True)
                
            else:
                pass
            count += 1
            print (str(count)+"/"+str(len(to_process))+" files converted.")
                

# location = str('/Users/rahulpatel/OneDrive - University of North Carolina at Chapel Hill/Zylka/PainFace/Data/WhiteMousePaper/DrugScreen/Combos/Saline_base')
# os.chdir(location)
# direc= os.listdir(location)
# directory_combo_grimace_analysis(direc)

