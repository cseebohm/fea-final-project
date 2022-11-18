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

def make_model (modelName, partName, pathName, radius, seedSize):
    import displayGroupMdbToolset as dgm
    import mesh
    import displayGroupOdbToolset as dgo

    m = mdb.models[modelName]
    
    #GEOMETRY
    s = m.ConstrainedSketch(name='__profile__', sheetSize=5.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
     
    s.rectangle(point1=(0.0, 0.0), point2=(0.2, 0.2))
    s.CircleByCenterPerimeter(center=(0.1, 0.1), point1=(0.1, radius))
    
    #MAKE PART
    p = m.Part(name=partName, 
        dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
    
    p.BaseShell(sketch=s)
    s.unsetPrimaryObject()

    del m.sketches['__profile__']
    
    #MAKE MATERIAL
    m.Material(name='Steel')
    m.materials['Steel'].Elastic(table=((200000000000.0, 0.32), ))
    m.HomogeneousSolidSection(name='PlateSection', material='Steel', thickness=0.001)

    #SECTION ASSIGNMENT
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region = p.Set(faces=faces, name='Set-1')
    
    p.SectionAssignment(region=region, sectionName='PlateSection', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    
    a = m.rootAssembly
    
    #CREATE INSTANCE
    instanceName = partName+'-1'
    a.DatumCsysByDefault(CARTESIAN)
    a.Instance(name=instanceName, part=p, dependent=ON)
    
    #STEPS, BOUNDARY CONDITIONS, AND LOADS
    m.StaticStep(name='Step-1', previous='Initial')
    
    m.steps['Step-1'].setValues(description='')
    
    e1 = a.instances[instanceName].edges
    edges1 = e1.getSequenceFromMask(mask=('[#10 ]', ), )
    region = a.Set(edges=edges1, name='Set-1')
    
    m.EncastreBC(name='FixedLeftEdge', createStepName='Initial', region=region, localCsys=None)
    
    s1 = a.instances[instanceName].edges
    side1Edges1 = s1.getSequenceFromMask(mask=('[#4 ]', ), )
    
    region = a.Surface(side1Edges=side1Edges1, name='Surf-1')
    
    m.Pressure(name='PressureRightEdge', 
        createStepName='Step-1', region=region, distributionType=UNIFORM, 
        field='', magnitude=-1000000.0, amplitude=UNSET)
    
    #MESH PART    
    elemType1 = mesh.ElemType(elemCode=CPS4R, elemLibrary=STANDARD, 
        secondOrderAccuracy=OFF, hourglassControl=DEFAULT, 
        distortionControl=DEFAULT)
    elemType2 = mesh.ElemType(elemCode=CPS3, elemLibrary=STANDARD)

    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions =(faces, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))

    p.seedPart(size=seedSize, deviationFactor=0.1, minSizeFactor=0.1) # do we need seedSize to be an input here? 
    p.generateMesh()
    a.regenerate()
    
    #SAVE
    mdb.saveAs(pathName)

def submit_job(modelName, jobName, pathName):

    # open mdb object
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
    mdb.jobs[jobName].submit(consistencyChecking=OFF)
    
    # Get ODB
    session.mdbData.summary()

    #odb = session.openOdb(name='C:/temp/Job-1.odb') # this creates an odb object from the file at the dictated path
    # name = '' specifies the name of the repository key (idk what that means)
    # path = '' specifies where the odb is that you want to open
    #o1 = session.openOdb(name='C:/temp/Job-1.odb')
    #odb = session.odbs['C:/temp/Job-1.odb'] # don't know what the "odbs" is here... 
    
    #a = m.rootAssembly # not sure if this line is nessecary either bc we don't use a
    return 

def output_data (fileName, pathName):
    import displayGroupMdbToolset as dgm
    import displayGroupOdbToolset as dgo
    
    o1 = session.openOdb(name='C:/temp/Job-1.odb')
    odb = session.odbs['C:/temp/Job-1.odb'] # don't know what the "odbs" is here... 
    
    # convert ODB to CSV for readable data
    session.fieldReportOptions.setValues(reportFormat=COMMA_SEPARATED_VALUES)
    
    # I don't think o1 is necessary
    session.viewports['Viewport: 1'].setValues(displayedObject=o1)
    session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1)
    
    # double check these to see what's necessary
    session.writeFieldReport(fileName, append=OFF, 
        sortItem='Node Label', odb=odb, step=0, frame=1, outputPosition=NODAL, 
        variable=(('S', INTEGRATION_POINT, ((INVARIANT, 'Mises'), (INVARIANT, 
        'Max. In-Plane Principal'), (INVARIANT, 
        'Max. In-Plane Principal (Abs)'), (INVARIANT, 'Max. Principal'), (
        INVARIANT, 'Max. Principal (Abs)'), )), ), stepFrame=SPECIFY)
    
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
submit_job(modelName, jobName, pathName)

#output data
output_data(fileName, pathName)