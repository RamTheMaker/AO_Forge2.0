#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Green
#
#----------------------------------------------------------------------------------------------------------

import nuke

for node in nuke.selectedNodes():
    if node.Class() != "Shuffle2":
        continue

    try:
        # Make sure we're reading from input 1 ("rgba")
        node["in1"].setValue("rgba")
       # node["in2"].setValue("rgba")
        node["out1"].setValue("rgba")

        # Mappings: (inputIndex, inputChannel, outputChannel)
        # inputIndex = 0 → first input
        # So: take rgba.red → into rgba.red/green/blue/alpha
        mappings = [
            (0, "rgba.green", "rgba.red"),
            (0, "rgba.green", "rgba.green"),
            (0, "rgba.green", "rgba.blue"),
            (0, "rgba.green", "rgba.alpha")
        ]

        # Apply mappings
        node["mappings"].setValue(mappings)

        # Optional: tile color visual feedback (a mild red tone)
        if "tile_color" in node.knobs():
            node["tile_color"].setValue(int("0x44CC44FF", 16))

        nuke.tprint(f"[OK] {node.name()} → Shuffle2 all outputs set to Red")

    except Exception as e:
        nuke.tprint(f"[ERROR] {node.name()}: {e}")
