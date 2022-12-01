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
data_path = "/Users/audreypohl/Documents/FEA/cs-ap/data/training_data/phase_one_a/radius_file"

file_string = "P"
radius_file = "radius_file"

#number of data points
num = 10

"MAKE AND POPULATE ARRAYS"
#get radius array
radiusArray = get_radius(radius_file)

#get max stress array
maxStressArray = np.zeros(num)

#find max stress for each file
for i in range(num):
    fileName = file_string + str(i) + ".csv"
    maxStressArray[i] = find_max(data_path, fileName)

"ERROR CHECKS"
#checks to see all values were populated
if(np.all(radiusArray) == 0 or np.all(maxStressArray)):
    print("Error: zero element exists in array")

elif(np.size(radiusArray) != num or np.size(maxStressArray) != num):
    print("Error: array size not equal to element number")

"OUTPUT CLEAN DATA"
#put labels
output_dict = {'Radius': radiusArray, 'Max Stress': maxStressArray}
output = pd.DataFrame(output_dict)
print(output)