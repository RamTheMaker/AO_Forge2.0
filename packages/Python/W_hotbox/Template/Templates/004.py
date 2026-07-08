#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Transform_Switch
# COLOR: #ffffff
# TEXTCOLOR: #000000
#
#----------------------------------------------------------------------------------------------------------

import nuke

for n in nuke.selectedNodes():
    if n.Class() != "Tracker4":
        continue

    try:
        knob = n["transform"]
        current = knob.value()

        # Full menu list in order (as in Nuke)
        # ['none', 'stabilize', 'stabilize 1pt', 'match-move', 'match-move 1pt', 'remove jitter', 'add jitter']
        if current in ("match-move", "match-move 1pt"):
            knob.setValue("stabilize")
            nuke.tprint(f"[{n.name()}] → Stabilize Mode")
        elif current in ("stabilize", "stabilize 1pt"):
            knob.setValue("match-move")
            nuke.tprint(f"[{n.name()}] → Match-Move Mode")
        else:
            knob.setValue("match-move")
            nuke.tprint(f"[{n.name()}] → Forced to Match-Move (was {current})")

    except Exception as e:
        nuke.tprint(f"[ERROR] {n.name()}: {e}")
