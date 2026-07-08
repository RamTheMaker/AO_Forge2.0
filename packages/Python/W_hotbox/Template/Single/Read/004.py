#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: RawData
# COLOR: #adff9b
# TEXTCOLOR: #000000
#
#----------------------------------------------------------------------------------------------------------

import nuke

for n in nuke.selectedNodes():
    if n.Class() != "Read":
        continue

    try:
        if "raw" in n.knobs():
            current = n["raw"].value()
            new_value = not current
            n["raw"].setValue(new_value)

            state = "ON ✅" if new_value else "OFF ⛔"
            nuke.tprint(f"[{state}] Raw data for {n.name()}")

        else:
            nuke.tprint(f"[SKIP] {n.name()} has no 'raw' knob.")

    except Exception as e:
        nuke.tprint(f"[ERROR] {n.name()}: {e}")
