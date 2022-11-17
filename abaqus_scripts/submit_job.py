"""
this script defines a function to submit a job from an existing model, it does not loop
??it should output an odb file?? (yes it should ouput an odb to input into output_data.py to get/clean the csv)

inputs are as follows
    - name of the model you want to submit job for as a string 'My-Model'
    - the name you want to call your job output as a string 'My-Job'
    - the path in which you put the model that you submited the job for submit job for 'X:/Desktop'

@version 11-15-2022
@author Clarissa Seebohm and Audrey Pohl
"""

def submit_job(modelName, jobName, pathName):
    
    m = mdb.models[modelName] # not sure if this line is nessecary 
    
    #CREATE JOB
    mdb.Job(name=jobName, model=modelName, description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
        numGPUs=0)
    
    #SUBMIT
    mdb.jobs[jobName].submit(consistencyChecking=OFF)
    
    # Get ODB
    session.mdbData.summary()
    o1 = session.openOdb(path=pathName) # this creates an odb object from the file at the dictated path
    # name = '' specifies the name of the repository key (idk what that means)
    # path = '' specifies where the odb is that you want to open
    
    a = m.rootAssembly # not sure if this line is nessecary either bc we don't use a
    odb = session.odbs['C:/temp/Job-1.odb'] # don't know what the "odbs" is here... 
    
    return o1, odb