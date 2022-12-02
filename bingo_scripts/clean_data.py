"""
this script reads in the .csvs outputted from abaqus and creates numpy arrays that are ready for bingo

inputs are as follows
    - 
    
@version 11-29-2022
@author Clarissa Seebohm and Audrey Pohl
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os as os

from find_max import find_max
from get_radius import get_radius

"DEFINITIONS: CHECK EVERYTIME"
#file name initial
data_path = "/data/training_data_50/"

file_string = "P"
radius_file = "radius_file"

#number of data points
num = 50

"MAKE AND POPULATE ARRAYS"
#get radius array
radiusArray = get_radius(radius_file)

#get max stress array
maxStressArray = np.zeros(num)

#find max stress for each file
for i in range(num):
    fileName = file_string + str(i) + ".csv"
    maxStressArray[i] = find_max(data_path, fileName)

"OUTPUT CLEAN DATA"
# put radius and max stress into a dict to turn it into a df, then csv file
output_dict = {'Radius': radiusArray, 'MaxStress': maxStressArray}
output = pd.DataFrame(output_dict)
output.to_csv('validation_data.csv')