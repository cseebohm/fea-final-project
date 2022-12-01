"""
this script finds the max of a single csv file outputted from abaqus using the output_data function

inputs are as follows
    - dataPath is the directory of where you're getting the .csv files from 
    - .csv filename as a string without the incrementing numbers
 
@version 11-29-2022
@author Clarissa Seebohm and Audrey Pohl
"""
import pandas as pd
import os

def find_max(data_path, file_string):
    
    #set directory to current working directory
    dir = os.getcwd()

    #read csv using pandas so that data has type DataFrame
    data = pd.read_csv(dir + data_path + file_string)

    #find max stress of specified column
    maxStress = data['S-Mises'].max()

    return maxStress