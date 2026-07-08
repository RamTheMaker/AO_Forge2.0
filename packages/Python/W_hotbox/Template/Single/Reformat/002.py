#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Black Outside
# COLOR: #000000
# TEXTCOLOR: #ffffff
#
#----------------------------------------------------------------------------------------------------------

import nuke

for node in nuke.selectedNodes():
    if node.Class() != "Reformat":
        continue

    try:
        if "black_outside" in node.knobs():
            current = node["black_outside"].value()
            node["black_outside"].setValue(not current)  # toggle
            nuke.tprint(f"[Reformat] {node.name()} → Black Outside: {not current}")
        else:
            nuke.tprint(f"[Reformat] {node.name()} has no 'black_outside' knob")
    except Exception as e:
        nuke.tprint(f"[Reformat] Error on {node.name()}: {e}")
