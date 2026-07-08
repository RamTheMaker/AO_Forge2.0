#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Stencil
# COLOR: #ff0000
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('output').setValue('rgba')
    i.knob('operation').setValue('stencil')