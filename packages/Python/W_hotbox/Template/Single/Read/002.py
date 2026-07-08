#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: AutoAplha
#
#----------------------------------------------------------------------------------------------------------

import nuke

def toggle_auto_alpha():
    # Prefer selected Read nodes
    nodes = nuke.selectedNodes("Read")
    if not nodes:
        try:
            tn = nuke.thisNode()
            if tn and tn.Class() == "Read":
                nodes = [tn]
        except Exception:
            nodes = []

    if not nodes:
        nuke.message("Select (or hover) a Read node and try again.")
        return

    for node in nodes:
        if "auto_alpha" not in node.knobs():
            nuke.tprint(f"{node.name()}: no 'auto_alpha' knob.")
            continue

        k = node.knob("auto_alpha")
        cur = k.value()

        # Normalize value to boolean
        if isinstance(cur, str):
            cur_bool = cur == "1"
        else:
            cur_bool = bool(cur)

        # Invert
        new_bool = not cur_bool

        # Set value properly
        try:
            k.setValue(int(new_bool))  # Nuke checkboxes prefer int 0/1
        except Exception as e:
            nuke.tprint(f"{node.name()}: failed to set auto_alpha -> {e}")

        nuke.tprint(f"{node.name()}: auto_alpha -> {'ON' if new_bool else 'OFF'}")

# Run the function
toggle_auto_alpha()
