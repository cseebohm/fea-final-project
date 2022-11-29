"""
this script finds the radius from a .csv file outputted from V4_phase_one

inputs are as follows
    - .csv filename
    
@version 11-29-2022
@author Clarissa Seebohm and Audrey Pohl
"""
import pandas as pd
import os

def get_radius(file):

    #set directory to current working directory
    dir = os.getcwd()

    #read csv using pandas
        #data has type DataFrame
    radius_df = pd.read_csv(dir + "/data/training_data/phase_one_a/" + file)
    radiusArray = radius_df.to_numpy

    return radiusArray