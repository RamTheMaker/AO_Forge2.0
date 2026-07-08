#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Localise
#
#----------------------------------------------------------------------------------------------------------

# Toggle "Localization Policy" dropdown on selected Read nodes
import nuke

for n in nuke.selectedNodes():
    if n.Class() != "Read":
        continue

    try:
        if "localizationPolicy" in n.knobs():
            current_value = n["localizationPolicy"].value()
            
            # Switch between "on" and "off"
            if current_value == "on":
                n["localizationPolicy"].setValue("off")
                nuke.tprint(f"[OFF] Localization disabled for {n.name()}")
            else:
                n["localizationPolicy"].setValue("on")
                nuke.tprint(f"[ON] Localization enabled for {n.name()}")

            # Ensure UI refresh after dropdown change
            def _deferred_update(node=n):
                try:
                    node["localizationPolicy"].setValue(
                        "on" if current_value == "off" else "off"
                    )
                except Exception as e:
                    nuke.tprint(f"Deferred update failed for {node.name()}: {e}")

            nuke.executeDeferred(_deferred_update)

        else:
            nuke.tprint(f"[SKIP] {n.name()} has no localizationPolicy knob.")

    except Exception as e:
        nuke.tprint(f"[ERROR] {n.name()}: {e}")
