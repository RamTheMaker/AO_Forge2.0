#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Cut
# COLOR: #1fff00
# TEXTCOLOR: #111111
#
#----------------------------------------------------------------------------------------------------------

import nuke, os

def load_rotocut():
    toolset_path = "/Shares/Y/SHOTGUNPRO/system_backup/paint_render/_daily_renders/Ramamurthy/RamServer_Own/ToolSets/RotoCut.nk"

    if not os.path.exists(toolset_path):
        nuke.message(f"❌ Toolset not found:\n{toolset_path}")
        return

    # Get selected FrameHold
    framehold = nuke.selectedNode()

    fx = framehold.xpos()
    fy = framehold.ypos()

    # Save current viewer connection
    viewer = nuke.activeViewer()
    viewer_node = viewer.node() if viewer else None
    viewer_input = viewer_node.input(0) if viewer_node else None

    # Paste toolset
    nuke.nodePaste(toolset_path)
    pasted = nuke.selectedNodes()
    if not pasted:
        return

    # Calculate group center
    top_node = min(pasted, key=lambda n: n.ypos())
    left = min(n.xpos() for n in pasted)
    right = max(n.xpos() + n.screenWidth() for n in pasted)
    center_x = (left + right) / 2
    top_y = top_node.ypos()

    # Position under FrameHold
    offset_x = (fx + framehold.screenWidth() - 128) - center_x
    offset_y = (fy + framehold.screenHeight() + 0) - top_y

    for n in pasted:
        n.setXpos(int(n.xpos() + offset_x))
        n.setYpos(int(n.ypos() + offset_y))

    # Find Roto node + disconnect
    roto_node = None
    for n in pasted:
        if n.Class() in ["Roto", "RotoPaint"]:
            n.setInput(0, None)
            roto_node = n

    # Clear selection
    for n in nuke.allNodes():
        n['selected'].setValue(False)

    # Select Roto + show panel
    if roto_node:
        roto_node['selected'].setValue(True)
        nuke.show(roto_node)

    # Restore original viewer input (keep FrameHold visible)
    if viewer_node:
        viewer_node.setInput(0, viewer_input)

    nuke.tprint("✅ RotoCut loaded — Roto selected, FrameHold stays in viewer.")

load_rotocut()
