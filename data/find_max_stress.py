"""
this script defines the function to find a max stress in the .csv files from output_data

inputs are as follows
    - .csv filename in the format "V2_p0.csv"
    
@version 11-22-2022
@author Clarissa Seebohm and Audrey Pohl
"""

import pandas as pd
import os as os

def find_max(file):

    #set directory to current working directory
    dir = os.getcwd()

    #read csv using pandas
        #data has type DataFrame
    data = pd.read_csv(dir + "/data/" + file)

    #find max stress of specified column
    maxStress = data['S-Max. Principal (Abs)'].max()

    return maxStress

#TEST
file = "V2_p2.csv"
maxStress = find_max(file)

print(maxStress)