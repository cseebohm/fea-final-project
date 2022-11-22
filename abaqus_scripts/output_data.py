"""
this script defines a function to output data as a csv from an odb, it does not loop

inputs are as follows 
    - modelName is what you want the model to be called as a string 'My-Model'
    - jobName is what you want your jobs to be called as a string 'My-Job'
    - fileName is the path and file name of your .csv file as a string 'X:/Desktop/My-csv.csv'
    - pathName is where you want your .csv files to be saved 'X:/Desktop'

@version 11-15-2022
@author Clarissa Seebohm and Audrey Pohl
"""

# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

def output_data (modelName, jobName, fileName, pathName):
    import displayGroupMdbToolset as dgm
    import displayGroupOdbToolset as dgo
    
    # OPEN MDB PROJECT
    mdb = openMdb(pathName)
    m = mdb.models[modelName]
    
    #CREATE JOB
    mdb.Job(name=jobName, model=modelName, description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
        numGPUs=0)
    
    #SUBMIT
    mdb.jobs[jobName].submit(consistencyChecking=ON)
    
    #WAIT FOR COMPLETION
    mdb.jobs[jobName].waitForCompletion()
    
    #GET ODB
    session.mdbData.summary() 
    o1 = session.openOdb(name='C:/temp/' + jobName + '.odb')
    odb = session.odbs['C:/temp/' + jobName + '.odb'] 
    
    #CONVERT ODB TO CSV
    session.fieldReportOptions.setValues(reportFormat=COMMA_SEPARATED_VALUES)
    
    session.viewports['Viewport: 1'].setValues(displayedObject=o1)
    session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1)
    
    session.writeFieldReport(fileName, append=OFF, 
        sortItem='Node Label', odb=odb, step=0, frame=1, outputPosition=NODAL, 
        variable=(('S', INTEGRATION_POINT, ((INVARIANT, 'Mises'), (INVARIANT, 
        'Max. In-Plane Principal (Abs)'), (INVARIANT, 'Max. Principal (Abs)'), )), ), 
        stepFrame=SPECIFY)

    odb.close()