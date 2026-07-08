#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Fill/Border
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
    if node.Class() == "BackdropNode":
        current = node['appearance'].value()
        if current == "fill":
            node['appearance'].setValue("border")
        else:
            node['appearance'].setValue("fill")
            
"""for i in nuke.selectedNodes():
    if i.knob('appearance'). value() == 'Fill':
        i.knob('appearance'). setValue('Border')
    else:
        i.knob('appearance').setValue('Fill')"""
                   