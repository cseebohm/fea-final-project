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

#define paths and filenames
pathName='X:/.win_desktop/PlateWithHole'
fileName='X:/.win_desktop/PlateWithHole.csv'

modelName='Model-1'
partName='PlateWithHole'
jobName="Job-1"

#define part 
seedSize = 0.005
radius = 0.1125

#make model
make_model(modelName, partName, pathName, radius, seedSize)

#submit job
o1, odb = submit_job(modelName, jobName, pathName)

#output data
output_data(o1, odb, fileName)
