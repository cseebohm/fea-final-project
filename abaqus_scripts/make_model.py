"""
this script defines a function to make a model, it does not loop

inputs are as follows
    - what you want the model to be called as a string 'My-Model' 
    - name of your part relative to the model each model will generate a new part 'My-Part'
    # not sure about this ^^ I believe the part name will stay constant and just the model will get renamed? 
    # since the part names are relative to and within the model
    - path name of where you want your model to be saved as a string 'C:/Desktop'
    - radius of the circle as a float type 4.2
    - seed size as a float type 0.005
    
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