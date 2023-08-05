#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 12:33:13 2021

@author: rahulpatel
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os 
import shutil
from subprocess import call 
import datetime 
import csv
import statistics
import scipy
from scipy.stats import skew 
from scipy.stats import kurtosis

# Create folder for csv

def batch_grimace(threshold, begin, end, auThreshold):
    directory = os.getcwd()
    os.chdir(directory)
    direc= os.listdir(directory)
    #print(directory)
    thres = threshold #change as necessary 
    start = int(begin) #time
    stop = int(end) #time
    timeframe = str(str(start) + '(s)_'+ str(stop) + '(s)')
    #threshold_name = str(thres + 'frames')
    to_process=[]
    if((auThreshold <1) or (auThreshold >5)):
        print ("Invalid action unit threshold. Value must be between 1 and 5.")
        exit()
    for file in direc:
        print(file)
        if file[-4:]== ('.csv'):
            to_process.append(file)
    print ("Files to process:")
    print (to_process)        
    print ("There are " +str(len(to_process))+ " csv files to be processed. Would you like to continue?")
    answer= input("Y or N: ")
    answer=answer.upper()
    if answer==("Y"):
        print ("Processing Files.")
        with open('data_log.csv', 'a+') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["File_Name",'UseableFrame%','UseableFramesFromFirst10Minutes','AverageTotalGrimaceScore','AverageGrimaceScoreFirst10Min','AverageGrimaceScore300Frames','%0s','%1s','%2s','%3s','%4s','%5s','%6s','%7s','%8s','%9s','%10s','WholeVideoSkew','SampledSkew','Threshold','TimeFrame','Process_Time'])
            count = 0
            for _csv in to_process:
                FileName = _csv
                begin_time = datetime.datetime.now()
                df = pd.read_csv(_csv)
                #df['Nose'] = df['Nose'].replace([1], 2)
                #df['NewTotalGrimaceScore']= df.iloc[:, 2:6].sum(axis=1)
                df.columns = df.columns.str.replace(' ', '')
                total_frames = len(df)
#=============================================================================
                AUcsv = df[(df.AUScored >= auThreshold)]  
                AUs = len(AUcsv)
                AUs = int(AUs)
                
                if AUs == 0:
                    #pass
                    scores = [0,1,2,3,4,5,6,7,8,9,10]
                    UseableFrames = str(0)
                    total_grimace_score = str('na')
                    useableframes_first_ten_min = str('na')
                    useableframes_first_ten_min = str('na')   
                    ten_min_grimace_score = str("na")
                    grimace_score_threehundred_frames = str('na')
                    TotalGrimaceSum = str("na")
                    First_Ten_Min_GrimaceSum = str('na')
                    Sampled_First_Ten_Min_GrimaceSum = str('na')
                    Sampled_First_Ten_Min_GrimaceSkew = str('na')
                    whole_video_skew = str('na')
                    Sampled_video_skew = str('na')
                    whole_video_kurtosis = str('na')
                    per0s = str('na') #percent of 0s
                    per1s = str('na')
                    per2s = str('na')
                    per3s = str('na')
                    per4s = str('na')
                    per5s = str('na')
                    per6s = str('na')
                    per7s = str('na')
                    per8s = str('na')
                    per9s = str('na')
                    per10s = str('na')
                    count += 1
                    end_time = datetime.datetime.now()
                    file_process_time = (end_time - begin_time)
                    with open('data_log.csv', 'a') as file:
                        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        writer.writerow([f'{FileName}',f'{UseableFrames}',f'{useableframes_first_ten_min}', f'{total_grimace_score}',f'{ten_min_grimace_score}',f'{grimace_score_threehundred_frames}',f'{per0s}', f'{per1s}',f'{per2s}',f'{per3s}', f'{per4s}',f'{per5s}',f'{per6s}',f'{per7s}',f'{per8s}',f'{per9s}',f'{per10s}', f'{whole_video_skew}',f'{Sampled_video_skew}',f'{thres}',f'{timeframe}',f'{file_process_time}'])
#=============================================================================
                if AUs > 0:
                    AUcsv['Cheek'] = AUcsv['Cheek'].replace([-1], '0')
                    AUcsv['Nose'] = AUcsv['Nose'].replace([-1], '0')
                    AUcsv['Orbital'] = AUcsv['Orbital'].replace([-1], '0')
                    AUcsv['Ears'] = AUcsv['Ears'].replace([-1], '0')
                    AUcsv['Whiskers'] = AUcsv['Whiskers'].replace([-1], '0')
                    AUcsv[['Orbital', 'Nose', 'Ears', 'Whiskers', 'Cheek']] = AUcsv[['Orbital', 'Nose', 'Ears', 'Whiskers', 'Cheek']].astype(int)
                    column_names = ['Orbital', 'Nose', 'Ears', 'Whiskers', 'Cheek']
                    AUcsv['NewTotalGrimaceScore']= AUcsv[column_names].sum(axis=1)
                    #path = '/Users/rahulpatel/OneDrive - University of North Carolina at Chapel Hill/Zylka/PainFace/Data/C57/FrontFacingOptimization/Test'
                    file = FileName[:-4] + ("_4PlusAU.csv")
                    #file_final = (path+file)
                    AUcsv.to_csv(file, sep=',', index=False) 
                    #AUcsv.to_csv(path+'greenl.csv')
                    UseableFrames = str((AUs/total_frames)*100)
                    total_grimace_score = AUcsv['NewTotalGrimaceScore'].mean()
                    column = AUcsv.loc[:,'NewTotalGrimaceScore']
                    whole_video_column = column.values
                    whole_video_skew = (skew(whole_video_column))
                    AU_first_ten_min = AUcsv[AUcsv['Timestamp(x)'].between(start, stop)] #0-10min, change as needed
                    useableframes_first_ten_min = int(len(AU_first_ten_min))
                    useableframes_calc_first_ten_min = str((useableframes_first_ten_min/AUs)*100)
                    scores = [0,1,2,3,4,5,6,7,8,9,10]
                    if useableframes_first_ten_min >= thres:
                        ten_min_grimace_score = AU_first_ten_min['NewTotalGrimaceScore'].mean()
                        frames_from_first_ten_min = AU_first_ten_min.sample(n = thres) #collecting 300 frames, change as needed
                        sampled_column = frames_from_first_ten_min.loc[:,'NewTotalGrimaceScore']
                        sampled_video_column = sampled_column.values
                        Sampled_video_skew = (skew(sampled_video_column))
                        storage = []
                        for i in scores:
                            column = frames_from_first_ten_min.loc[:,'NewTotalGrimaceScore']
                            column_values = column.values
                            if i in column_values:
                                score = frames_from_first_ten_min['NewTotalGrimaceScore'].value_counts(normalize=True)[i]
                                storage.append(score)
                                #print(score)
                            else:
                                storage.append('n/a')
                                #print('n/a')
                        scores_freq2 = pd.DataFrame(storage)#, columns =[scores])
                        scores_freq3 = scores_freq2.transpose()
                        per0s = str(scores_freq3.iloc[0][0])
                        per1s = str(scores_freq3.iloc[0][1])
                        per2s = str(scores_freq3.iloc[0][2])
                        per3s = str(scores_freq3.iloc[0][3])
                        per4s = str(scores_freq3.iloc[0][4])
                        per5s = str(scores_freq3.iloc[0][5])
                        per6s = str(scores_freq3.iloc[0][6])
                        per7s = str(scores_freq3.iloc[0][7])
                        per8s = str(scores_freq3.iloc[0][8])
                        per9s = str(scores_freq3.iloc[0][9])
                        per10s = str(scores_freq3.iloc[0][10])
                        grimace_score_threehundred_frames = frames_from_first_ten_min['NewTotalGrimaceScore'].mean()
                        TotalGrimaceSum = AUcsv['NewTotalGrimaceScore'].sum()
                        First_Ten_Min_GrimaceSum = AU_first_ten_min['NewTotalGrimaceScore'].sum()
                        Sampled_First_Ten_Min_GrimaceSum = frames_from_first_ten_min['NewTotalGrimaceScore'].sum()
                    if useableframes_first_ten_min < thres:
                        scores = [0,1,2,3,4,5,6,7,8,9,10]
                        storage = []
                        for i in scores:
                            column = AU_first_ten_min.loc[:,'NewTotalGrimaceScore']
                            column_values = column.values
                            if i in column_values:
                                score = AU_first_ten_min['NewTotalGrimaceScore'].value_counts(normalize=True)[i]
                                storage.append(score)
                                #print(score)
                            else:
                                storage.append('n/a')
                                #print('n/a')
                        scores_freq2 = pd.DataFrame(storage)#, columns =[scores])
                        scores_freq3 = scores_freq2.transpose()
                        per0s = str(scores_freq3.iloc[0][0])
                        per1s = str(scores_freq3.iloc[0][1])
                        per2s = str(scores_freq3.iloc[0][2])
                        per3s = str(scores_freq3.iloc[0][3])
                        per4s = str(scores_freq3.iloc[0][4])
                        per5s = str(scores_freq3.iloc[0][5])
                        per6s = str(scores_freq3.iloc[0][6])
                        per7s = str(scores_freq3.iloc[0][7])
                        per8s = str(scores_freq3.iloc[0][8])
                        per9s = str(scores_freq3.iloc[0][9])
                        per10s = str(scores_freq3.iloc[0][10])
                        sampled_column = AU_first_ten_min.loc[:,'NewTotalGrimaceScore']
                        sampled_video_column = sampled_column.values
                        Sampled_video_skew = (skew(sampled_video_column))
                        ten_min_grimace_score = AU_first_ten_min['NewTotalGrimaceScore'].mean() 
                        grimace_score_threehundred_frames = str('na')
                        TotalGrimaceSum = AUcsv['NewTotalGrimaceScore'].sum()
                        First_Ten_Min_GrimaceSum = AU_first_ten_min['NewTotalGrimaceScore'].sum()
                        Sampled_First_Ten_Min_GrimaceSum = str('na')
                    if useableframes_first_ten_min == 0:
                        scores = [0,1,2,3,4,5,6,7,8,9,10]
                        storage = []
                        ten_min_grimace_score = str("na")
                        grimace_score_threehundred_frames = str('na')
                        TotalGrimaceSum = str('na')
                        First_Ten_Min_GrimaceSum = str('na')
                        Sampled_First_Ten_Min_GrimaceSum = str('na')
                        per0s = str('na')
                        per1s = str('na')
                        per2s = str('na')
                        per3s = str('na')
                        per4s = str('na')
                        per5s = str('na')
                        per6s = str('na')
                        per7s = str('na')
                        per8s = str('na')
                        per9s = str('na')
                        per10s = str('na')
                    count += 1
                    end_time = datetime.datetime.now()
                    file_process_time = (end_time- begin_time)
                    with open('data_log.csv', 'a') as file:
                        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                        writer.writerow([f'{FileName}',f'{UseableFrames}',f'{useableframes_first_ten_min}', f'{total_grimace_score}',f'{ten_min_grimace_score}',f'{grimace_score_threehundred_frames}',f'{per0s}', f'{per1s}',f'{per2s}',f'{per3s}', f'{per4s}',f'{per5s}',f'{per6s}',f'{per7s}',f'{per8s}',f'{per9s}',f'{per10s}', f'{whole_video_skew}',f'{Sampled_video_skew}',f'{thres}',f'{timeframe}',f'{file_process_time}'])
                print (str(count)+"/"+str(len(to_process))+" files converted.")

        print ("Finished")
        print ("Check the working directory for the newly generated files!")
    else:
        exit()
        
#location=('/Users/rahulpatel/OneDrive - University of North Carolina at Chapel Hill/Zylka/PainFace/Videos/SNI/20200925_Cohort1/Day5/mp4')  
#location = ("/Users/rahulpatel/OneDrive - University of North Carolina at Chapel Hill/Zylka/PainFace/Videos/Optimization/20201027/mp4")
#location = mp4 
#('/Volumes/Zylka Lab/Rahul/PainFace/Optimization/Lighting/20201029/mp4')

#batch_grimace_analysis(300, 0, 600, 4)