#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Unpremult Alpha
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('unpremult').setValue('rgba.alpha')