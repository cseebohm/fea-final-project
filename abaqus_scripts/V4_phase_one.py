"""
this script is to generate training data for phase one: varying the radius of a hole located in the center of the plate

@version 11-17-2022
@author Clarissa Seebohm and Audrey Pohl
"""

import numpy as np

# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

def make_model(modelName, partName, pathName, radius):
    import displayGroupMdbToolset as dgm
    import mesh
    import displayGroupOdbToolset as dgo

    mdb.Model(name=modelName, modelType=STANDARD_EXPLICIT)
    m = mdb.models[modelName]
    
    #GEOMETRY
    s = m.ConstrainedSketch(name='__profile__', sheetSize=5.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
     
    s.rectangle(point1=(0.0, 0.0), point2=(0.2, 0.2))
    s.CircleByCenterPerimeter(center=(0.1, 0.1), point1=(0.1, radius))
    
    #MAKE PART
    p = m.Part(name=partName, dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
    
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
        offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)
    
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
    
    m.Pressure(name='PressureRightEdge', createStepName='Step-1', region=region, 
        distributionType=UNIFORM, field='', magnitude=-1000000.0, amplitude=UNSET)
    
    #MESH PART    
    p1 = m.parts[partName]
    
    elemType1 = mesh.ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
        hourglassControl=DEFAULT, distortionControl=DEFAULT)
    
    elemType2 = mesh.ElemType(elemCode=CPS3, elemLibrary=STANDARD)

    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions = (faces, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))

    p.seedPart(size= XX, deviationFactor=0.1, minSizeFactor=0.1) # do we need seedSize to be an input here? 
    p.generateMesh()
    a.regenerate()
    
    #SAVE
    mdb.saveAs(pathName)

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
    mdb.jobs[jobName].submit(consistencyChecking=OFF)
    
    # Get ODB
    session.mdbData.summary()
    
    o1 = session.openOdb(name='C:/temp/' + jobName + '.odb')
    odb = session.odbs['C:/temp/' + jobName + '.odb'] 
    
    # CONVERT ODB TO CSV
    session.fieldReportOptions.setValues(reportFormat=COMMA_SEPARATED_VALUES)
    
    session.viewports['Viewport: 1'].setValues(displayedObject=o1)
    session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1)
    
    session.writeFieldReport(fileName, append=OFF, sortItem='Node Label', 
        odb=odb, step=0, frame=1, outputPosition=NODAL, variable=(('S', INTEGRATION_POINT, 
        ((INVARIANT, 'Mises'), (INVARIANT, 'Max. In-Plane Principal (Abs)'), (INVARIANT, 
        'Max. Principal (Abs)'), )), ), stepFrame=SPECIFY)

    odb.close()

radiusArray = np.linspace(0, 0.199, 10) # 10 as a placeholder

# GENERATE 10 MODELS WITH VARYING RADII
for i in range(10):
    pathName='X:/.win_desktop/deleteme/V2_p'+ str(i)
    partName='P-'+ str(i)
    modelName='Model-'+str(i)

    radius = radiusArray[i]

    make_model(modelName, partName, pathName, radius)

# CONVERT FROM ODB TO CSV AND OUTPUT CSV
for i in range(10):
    pathName='X:/.win_desktop/deleteme/V2_p'+ str(i)
    fileName='X:/.win_desktop/cs-ap/data/V2_p'+ str(i)+'.csv'
    jobName = 'Job-'+str(i)
    modelName='Model-'+str(i)

    output_data(modelName, jobName, fileName, pathName)
    