#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Localise
#
#----------------------------------------------------------------------------------------------------------

import nuke

for node in nuke.selectedNodes():
    if node.Class() != "Read":
        continue

    if "localizationPolicy" not in node.knobs():
        nuke.tprint(f"[SKIP] {node.name()} has no localizationPolicy knob.")
        continue

    current = node["localizationPolicy"].value()

    # If OFF → turn ON
    if current == "off":
        node["localizationPolicy"].setValue("on")
        nuke.tprint(f"[ON ] Localization ON for {node.name()}")

    # If ON or ANY OTHER MODE → turn OFF
    else:
        node["localizationPolicy"].setValue("off")
        nuke.tprint(f"[OFF] Localization OFF for {node.name()}")