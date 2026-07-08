#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Auto CornerPin
# COLOR: #0d6d00
#
#----------------------------------------------------------------------------------------------------------

######################
### created by JNS ###
######################
# Copyright to JNS Creations
### it will auto position the cornerpin to your selected Node's alpha

import nuke


def auto_cornerpin():
    
    layer= "alpha"
    
   

### Remember original set of selected nodes

    original_nodes = nuke.selectedNodes()

### if not selecting a node just create a cornerpin  or colorcorrect  
    
    if not original_nodes:
      nuke.createNode("ColorCorrect")
      return

 ### Creating curve tool

    for i in original_nodes:
        i.knob("selected").setValue(True)
        autocropper = nuke.createNode("CurveTool",
      '''operation 0 ROI {0 0 input.width input.height} Layer %s label "Processing Crop..." selected true''' % (str(layer), ), False)

### Execute the curve tool for the current frame

    nuke.execute(autocropper, int(nuke.frame()), int(nuke.frame()))

### select the curvewriter
    
    autocropper.knob("selected").setValue(True)

### add cornerpin node

    k = nuke.createNode("CornerPin2D",  'name JNS_CornerPin2D gl_color 4278255615.0')

### put the new data from the autocrop into the new cornerpin

    x = autocropper.knob("autocropdata").getValue(0)
    y = autocropper.knob("autocropdata").getValue(1)
    r = autocropper.knob("autocropdata").getValue(2)
    t = autocropper.knob("autocropdata").getValue(3) 
    
### setting keys in "from" and "to" knobs   
    
    k['from1'].setAnimated()
    k['from2'].setAnimated()
    k['from3'].setAnimated()
    k['from4'].setAnimated()
    
    k['to1'].setAnimated()
    k['to2'].setAnimated()
    k['to3'].setAnimated()
    k['to4'].setAnimated()

### setting 'from' knobs 

    k.knob("from1").setValue(x, 0)
    k.knob('from1').setValue(y, 1)

    k.knob('from2').setValue(r, 0)
    k.knob('from2').setValue(y, 1)

    k.knob('from3').setValue(r, 0)
    k.knob('from3').setValue(t, 1)

    k.knob('from4').setValue(x, 0)
    k.knob('from4').setValue(t, 1)

### setting 'to' Knobs

    k.knob('to1').setValue(x, 0)
    k.knob('to1').setValue(y, 1)

    k.knob('to2').setValue(r, 0)
    k.knob('to2').setValue(y, 1)

    k.knob('to3').setValue(r, 0)
    k.knob('to3').setValue(t, 1)

    k.knob('to4').setValue(x, 0)
    k.knob('to4').setValue(t, 1)

# deselect everything
    all_nodes = nuke.allNodes()
    for j in all_nodes:
        j.knob("selected").setValue(False)

# select the curvewriter and delete it
    autocropper.knob("selected").setValue(True)
    nuke.delete(autocropper)

# deselect everything
    all_nodes = nuke.allNodes()
    for j in all_nodes:
        j.knob("selected").setValue(False)

# select the new cornerpin
    k.knob("selected").setValue(True)

# place it in a nice spot
    nuke.autoplace(k)

### the end :)

auto_cornerpin()

