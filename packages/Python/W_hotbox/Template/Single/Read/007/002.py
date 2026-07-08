#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: StartAt 1001
#
#----------------------------------------------------------------------------------------------------------

# Set selected Read nodes to "Start at 1001"
import nuke

for n in nuke.selectedNodes():
    if n.Class() != "Read":
        continue

    try:
        # Set frame mode dropdown
        if "frame_mode" in n.knobs():
            n["frame_mode"].setValue("start at")

        # Set the start frame as a string to avoid type issues
        if "frame2" in n.knobs():  # 'frame2' used by Start At mode
            n["frame2"].setValue("1001")
        elif "frame" in n.knobs():
            n["frame"].setValue("1001")

        # Double-check deferred — ensures UI update is complete
        def _deferred_set(node=n):
            try:
                if "frame2" in node.knobs():
                    node["frame2"].setValue("1001")
                elif "frame" in node.knobs():
                    node["frame"].setValue("1001")
            except Exception as e:
                nuke.tprint(f"Deferred set failed for {node.name()}: {e}")

        nuke.executeDeferred(_deferred_set)

        nuke.tprint(f"[OK] {n.name()} → Frame Mode: Start at 1001")

    except Exception as e:
        nuke.tprint(f"[ERROR] {n.name()}: {e}")
