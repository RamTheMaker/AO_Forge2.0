#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Mask
# COLOR: #475100
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('output').setValue('rgba')
    i.knob('operation').setValue('mask')