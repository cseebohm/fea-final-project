"""
this script defines a function to output data as a csv from an odb, it does not loop

@version 11-15-2022
@author Clarissa Seebohm and Audrey Pohl
"""

def output_data (o1, odb, fileName):
    import displayGroupMdbToolset as dgm
    import displayGroupOdbToolset as dgo
    
    # convert ODB to CSV for readable data
    session.fieldReportOptions.setValues(reportFormat=COMMA_SEPARATED_VALUES)
    
    session.viewports['Viewport: 1'].setValues(displayedObject=o1)
    session.viewports['Viewport: 1'].odbDisplay.setFrame(step=0, frame=1)
    
    # double check these to see what's necessary
    session.writeFieldReport(fileName, append=OFF, 
        sortItem='Node Label', odb=odb, step=0, frame=1, outputPosition=NODAL, 
        variable=(('S', INTEGRATION_POINT, ((INVARIANT, 'Mises'), (INVARIANT, 
        'Max. In-Plane Principal'), (INVARIANT, 
        'Max. In-Plane Principal (Abs)'), (INVARIANT, 'Max. Principal'), (
        INVARIANT, 'Max. Principal (Abs)'), )), ), stepFrame=SPECIFY)