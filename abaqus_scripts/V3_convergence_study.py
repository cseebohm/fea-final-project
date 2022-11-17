"""
this script is for the convergence study for phase one (PA 4)

@version 11-17-2022
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

#define part 
radius = 0.1125

#define paths and filenames
for i in range(5):
    pathName='X:/.win_desktop/P'+i
    fileName='X:/.win_desktop/P'+i+'.csv'

    modelName='Model-'+i
    partName='P'+i

    seedSize = seedSize + .05 

    #make model
    make_model(modelName, partName, pathName,  radius, seedSize)

#submit jobs
o1, odb = submit_job()

#output data
output_data(o1, odb, fileName)