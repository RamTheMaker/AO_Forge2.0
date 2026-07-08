#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Min
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('output').setValue('rgba')
    i.knob('operation').setValue('min')