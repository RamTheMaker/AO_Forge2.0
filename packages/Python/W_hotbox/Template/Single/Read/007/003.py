#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: StartAt Frame
#
#----------------------------------------------------------------------------------------------------------

import nuke

current_frame = nuke.frame()  # grab timeline frame

for n in nuke.selectedNodes():
    if n.Class() != "Read":
        continue

    try:
        # Switch mode → Start at
        if "frame_mode" in n.knobs():
            n["frame_mode"].setValue("start at")

        # Set the start frame to current frame
        if "frame2" in n.knobs():
            n["frame2"].setValue(str(current_frame))
        elif "frame" in n.knobs():
            n["frame"].setValue(str(current_frame))

        # Fix Nuke’s delayed knob update
        def _deferred(node=n):
            try:
                if "frame2" in node.knobs():
                    node["frame2"].setValue(str(current_frame))
                elif "frame" in node.knobs():
                    node["frame"].setValue(str(current_frame))
            except:
                pass

        nuke.executeDeferred(_deferred)

        nuke.tprint(f"[OK] {n.name()} → Start at {current_frame}")

    except Exception as e:
        nuke.tprint(f"[ERROR] {n.name()}: {e}")