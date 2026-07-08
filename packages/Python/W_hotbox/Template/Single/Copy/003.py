#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: BBox
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('bbox'). value() == 'union':
        i.knob('bbox'). setValue('A side')
    else:
        i.knob('bbox').setValue('union')
        