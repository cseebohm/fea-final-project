"""
this script finds the radius from a .csv file outputted from V4_phase_one

inputs are as follows
    - .csv filename
    
@version 11-29-2022
@author Clarissa Seebohm and Audrey Pohl
"""
import pandas as pd
import os
import csv

def get_radius(file):
    
    #set directory to current working directory
    dir = os.getcwd()

    #read csv using pandas so that data has type DataFrame
    with open((dir + "/data/training_data_50/" + file + ".csv"), 'r') as radius_csv:
        radiusArray = []
        for radius in radius_csv:
            radiusArray.append(radius.replace("\n", ""))
            
    return radiusArray