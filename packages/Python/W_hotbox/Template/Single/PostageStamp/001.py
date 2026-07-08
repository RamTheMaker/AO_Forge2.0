#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Hide Input
#
#----------------------------------------------------------------------------------------------------------

import nuke

for node in nuke.selectedNodes():
    try:
        if "hide_input" in node.knobs():
            current = node["hide_input"].value()
            node["hide_input"].setValue(not current)  # toggle True/False
            nuke.tprint(f"{node.name()} → hide_input: {not current}")
        else:
            nuke.tprint(f"{node.name()} has no 'hide_input' knob")
    except Exception as e:
        nuke.tprint(f"Error on {node.name()}: {e}")
