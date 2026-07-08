#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Alpha
#
#----------------------------------------------------------------------------------------------------------

import nuke

for node in nuke.selectedNodes():
    if node.Class() != "Shuffle2":
        continue

    try:
        node["in1"].setValue("rgba")
        #node["in2"].setValue("rgba")
        node["out1"].setValue("rgba")

        mappings = [
            (0, "rgba.alpha", "rgba.red"),
            (0, "rgba.alpha", "rgba.green"),
            (0, "rgba.alpha", "rgba.blue"),
            (0, "rgba.alpha", "rgba.alpha")
        ]

        node["mappings"].setValue(mappings)

        if "tile_color" in node.knobs():
            node["tile_color"].setValue(int("0xDDDDDDFF", 16))  # grayish tint for alpha

        nuke.tprint(f"[OK] {node.name()} → Shuffle2 all outputs set to Alpha")

    except Exception as e:
        nuke.tprint(f"[ERROR] {node.name()}: {e}")
