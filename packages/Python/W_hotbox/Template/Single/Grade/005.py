#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: reverse
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.allNodes('Grade'):
    if value == None:
        value = i.knob('reverse').value()
    i.knob('reverse').setValue(1-value)