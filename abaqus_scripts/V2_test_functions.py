"""
this script is a test for the functions, it should run the exact same as V1.py

@version 11-15-2022
@author Clarissa Seebohm and Audrey Pohl
"""

# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

from make_model import make_model
from submit_job import submit_job
from output_data import output_data

#set working directory to cs-ap
workingDir = 'X:/.win_desktop/cs-ap/abaqus_scripts'
#workingDir = 'C:/temp/'

#define paths and filenames
pathName='X:/.win_desktop/cs-ap/data/V2'
fileName='X:/.win_desktop/cs-ap/data/V2.csv'

modelName='Model-1'
partName='Plate-With-Hole'
jobName='Job-1'

#define part 
seedSize = 0.005
radius = 0.1125

#make model
make_model(modelName, partName, pathName, radius, seedSize)

#submit job
odb, o1 = submit_job(modelName, jobName, pathName, workingDir)

#output data
output_data(odb, o1, fileName, pathName)
