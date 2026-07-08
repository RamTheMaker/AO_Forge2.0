#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Fill_Border
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('appearance'). value() == 'Fill':
        i.knob('appearance'). setValue('Border')
    else:
        i.knob('appearance').setValue('Fill')
        