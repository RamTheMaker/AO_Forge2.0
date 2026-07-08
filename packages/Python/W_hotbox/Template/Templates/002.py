#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Set Project Range
# COLOR: #ffffff
# TEXTCOLOR: #000000
#
#----------------------------------------------------------------------------------------------------------

node = nuke.selectedNode()

first = node.knob('first').value()
last = node.knob('last').value()

nuke.Root().knob('first_frame').setValue(first)
nuke.Root().knob('last_frame').setValue(last)

if nuke.frame() not in range(first,last+1):
    nuke.frame(first)