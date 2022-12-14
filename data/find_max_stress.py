"""
this script defines the function to find a max stress in the .csv files from output_data 

    also plots convergence study for PA4

inputs are as follows
    - .csv filename in the format "V2_p0.csv"
    
@version 11-22-2022
@author Clarissa Seebohm and Audrey Pohl
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os as os

def find_max(file):

    #set directory to current working directory
    dir = os.getcwd()

    #read csv using pandas
        #data has type DataFrame
    data = pd.read_csv(dir + "/data/convergData/" + file)

    #find max stress of specified column
    maxStress = data['S-Max. In-Plane Principal (Abs)'].max()

    return maxStress

""" Main """
seedSizeArrayInitial = np.linspace(.0005, .01, 10)

#only jobs 1-9 completed, removing jobs 0 and 8,9

seedSizeArray = seedSizeArrayInitial[1:10]
print(seedSizeArray)
maxStressArray = np.zeros(9)

#find max for each file
for i in range(9):
    file = "C2a_p" + str(i+1) + ".csv"
    maxStressArray[i] = find_max(file)

#plot
plt.plot(seedSizeArray, maxStressArray, marker = 'o', label = 'Quad-dominated')

plt.xlabel("Element Seed Size")
plt.ylabel("Max Stress [Pa]")
plt.legend()
plt.title("Approximate Global Seed Size vs Max Stress")

plt.show()
