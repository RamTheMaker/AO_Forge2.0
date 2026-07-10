import nuke


def FRM():
    frame_hold = nuke.createNode("FrameHold")
    frame_hold["first_frame"].setValue(nuke.frame())