# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

def PlateWHole():
    import section # importing all the libraries needed to run the ABAQUS program
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import step
    import interaction
    import load
    import mesh
    import optimization
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    
    # step 1 delete all session.viewports
    # step 2 rename simple stuff to be a single variable or letter
    # remove repeats of p. things or s. things??? not sure how we can just get rid of stuff
    # is there a way to generate a new abaqusMacros.py file instead of appending onto the existing one? 
    # I generated a .csv file to possibly filter through and input into BINGO
    # how does it know to import from ABAQUS? 
    # I got this python script... now what? Do I have to have ABAQUS open and VS code open at the same time for this to work? 
    # what parameters do we use to run the BINGO script
    
    m = mdb.models['Model-1']
    
    s = m.ConstrainedSketch(name='__profile__', sheetSize=5.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.rectangle(point1=(0.0, 0.0), point2=(0.2, 0.2))
    p = m.Part(name='Plate-With-Hole', dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
    p = m.parts['Plate-With-Hole']
    p.BaseShell(sketch=s)
    s.unsetPrimaryObject()
    p = m.parts['Plate-With-Hole']
    del m.sketches['__profile__']
    del m.parts['Plate-With-Hole']
    s1 = m.ConstrainedSketch(name='__profile__', sheetSize=5.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s1.rectangle(point1=(0.0, 0.0), point2=(0.2, 0.2))
    s1.CircleByCenterPerimeter(center=(0.1, 0.1), point1=(0.1, 0.1125))
    s1.resetView()
    p = m.Part(name='Plate-W-Hole', dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
    p = m.parts['Plate-W-Hole']
    p.BaseShell(sketch=s1)
    s1.unsetPrimaryObject()
    p = m.parts['Plate-W-Hole']
    del m.sketches['__profile__']
    mdb.saveAs(pathName='X:/Desktop/PlateWHoleV1')
    m.Material(name='AISI-1025-Carbon-Steel')
    m.materials['AISI-1025-Carbon-Steel'].Elastic(table=((200000000000.0, 0.32), ))
    m.materials['AISI-1025-Carbon-Steel'].Density(table=((0.0,), ))
    m.HomogeneousSolidSection(name='PlateSection', material='AISI-1025-Carbon-Steel', thickness=0.001)
    p = m.parts['Plate-W-Hole']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), ) # mentioned not needing this. Why? 
    region = p.Set(faces=faces, name='Set-1')
    p = m.parts['Plate-W-Hole']
    p.SectionAssignment(region=region, sectionName='PlateSection', offset=0.0, 
        offsetType=MIDDLE_SURFACE, offsetField='', 
        thicknessAssignment=FROM_SECTION)
    a = m.rootAssembly
    a = m.rootAssembly
    a.DatumCsysByDefault(CARTESIAN)
    p = m.parts['Plate-W-Hole']
    a.Instance(name='Plate-W-Hole-1', part=p, dependent=ON)
    m.StaticStep(name='RightEdgePressure', previous='Initial', 
        description='pressure added to right edge of 1MPa')
    a = m.rootAssembly
    e1 = a.instances['Plate-W-Hole-1'].edges
    edges1 = e1.getSequenceFromMask(mask=('[#10 ]', ), )
    region = a.Set(edges=edges1, name='Set-1')
    m.EncastreBC(name='LeftEdgeFixed', 
        createStepName='Initial', region=region, localCsys=None)
    a = m.rootAssembly
    s1 = a.instances['Plate-W-Hole-1'].edges
    side1Edges1 = s1.getSequenceFromMask(mask=('[#4 ]', ), )
    region = a.Surface(side1Edges=side1Edges1, name='Surf-1')
    m.Pressure(name='PlateLoad', createStepName='RightEdgePressure', region=region, 
        distributionType=UNIFORM, field='', magnitude=-1000000.0, amplitude=UNSET)
    mdb.save()
    
    p1 = m.parts['Plate-W-Hole']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    
    elemType1 = mesh.ElemType(elemCode=CPS4R, elemLibrary=STANDARD, 
        secondOrderAccuracy=OFF, hourglassControl=DEFAULT, 
        distortionControl=DEFAULT)
    elemType2 = mesh.ElemType(elemCode=CPS3, elemLibrary=STANDARD)
    p = m.parts['Plate-W-Hole']
    f = p.faces
    faces = f.getSequenceFromMask(mask=('[#1 ]', ), )
    pickedRegions =(faces, )
    p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))
    p = m.parts['Plate-W-Hole']
    p.seedPart(size=0.005, deviationFactor=0.1, minSizeFactor=0.1)
    p = m.parts['Plate-W-Hole']
    p.generateMesh()
    a = m.rootAssembly
    a.regenerate()
    mdb.Job(name='Approx005V1', model='Model-1', 
        description='Plate with hole with macros. Approx global seed size 0.005. Nothing else changed from the Lab 1 tutorial. ', 
        type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, 
        memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
        explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
        modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
        scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
        numGPUs=0)
    mdb.jobs['Approx005V1'].submit(consistencyChecking=OFF)
    session.mdbData.summary()
    o3 = session.openOdb(name='C:/temp/Approx005V1.odb')
    a = m.rootAssembly
    a = m.rootAssembly
    o3 = session.openOdb(name='C:/temp/Approx005V1.odb')
    session.mdbData.summary()
    odb = session.odbs['C:/temp/Approx005V1.odb']
    
    
    session.fieldReportOptions.setValues(reportFormat=COMMA_SEPARATED_VALUES)
    session.writeFieldReport(fileName='X:/Desktop/DataPlateWHoleV1.csv', append=ON, 
        sortItem='Node Label', odb=odb, step=0, frame=1, outputPosition=NODAL, 
        variable=(('S', INTEGRATION_POINT, ((INVARIANT, 'Mises'), (INVARIANT, 
        'Max. In-Plane Principal'), (INVARIANT, 
        'Max. In-Plane Principal (Abs)'), (INVARIANT, 'Max. Principal'), (
        INVARIANT, 'Max. Principal (Abs)'), )), ), stepFrame=SPECIFY)
