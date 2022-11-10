# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

def Macro1():
    import displayGroupMdbToolset as dgm
    import mesh
    import displayGroupOdbToolset as dgo

   
    #GEOMETRY
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=5.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
     
    s.rectangle(point1=(0.0, 0.0), point2=(0.2, 0.2))
    s.CircleByCenterPerimeter(center=(0.1, 0.1), point1=(0.1, 0.1125))
    
    #MAKE PART
    p = mdb.models['Model-1'].Part(name='PlateWithHole', 
        dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
    
    p.BaseShell(sketch=s)
    s.unsetPrimaryObject()

    del mdb.models['Model-1'].sketches['__profile__']

    #SAVE
    mdb.saveAs(pathName='X:/PlateWithHole')
    
    #MAKE MATERIAL
    mdb.models['Model-1'].Material(name='Steel')
    mdb.models['Model-1'].materials['Steel'].Elastic(table=((200000000000.0, 0.32), 
        ))
    mdb.models['Model-1'].HomogeneousSolidSection(name='PlateSection', 
        material='Steel', thickness=0.001)

    #SECTION ASSIGNMENT
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    region = p.Set(faces=faces, name='Set-1')
    
    p.SectionAssignment(region=region, sectionName='PlateSection', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    
    a = mdb.models['Model-1'].rootAssembly
    
    #CREATE INSTANCE
    a.DatumCsysByDefault(CARTESIAN)
    a.Instance(name='PlateWithHole-1', part=p, dependent=ON)
    
    #STEPS
    mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')
    
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
    
    mdb.models['Model-1'].steps['Step-1'].setValues(description='')
    
    e1 = a.instances['PlateWithHole-1'].edges
    edges1 = e1.getSequenceFromMask(mask=('[#10 ]', ), )
    region = a.Set(edges=edges1, name='Set-1')
    
    mdb.models['Model-1'].EncastreBC(name='FixedLeftEdge', 
        createStepName='Initial', region=region, localCsys=None)
    
    session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
    s1 = a.instances['PlateWithHole-1'].edges
    side1Edges1 = s1.getSequenceFromMask(mask=('[#4 ]', ), )
    
    region = a.Surface(side1Edges=side1Edges1, name='Surf-1')
    
    mdb.models['Model-1'].Pressure(name='PressureRightEdge', 
        createStepName='Step-1', region=region, distributionType=UNIFORM, 
        field='', magnitude=-1000000.0, amplitude=UNSET)
    
    #MESH PART    
    p1 = mdb.models['Model-1'].parts['PlateWithHole']
    
    elemType1 = mesh.ElemType(elemCode=CPS4R, elemLibrary=STANDARD, 
        secondOrderAccuracy=OFF, hourglassControl=DEFAULT, 
        distortionControl=DEFAULT)
    elemType2 = mesh.ElemType(elemCode=CPS3, elemLibrary=STANDARD)

    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions =(faces, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))

    p.seedPart(size=0.005, deviationFactor=0.1, minSizeFactor=0.1)
    p.generateMesh()
    a.regenerate()
    
    #CREATE JOB
    mdb.Job(name='Job-1', model='Model-1', description='', type=ANALYSIS, 
        atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
        memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
        numGPUs=0)
    
    #SUBMIT
    mdb.jobs['Job-1'].submit(consistencyChecking=OFF)