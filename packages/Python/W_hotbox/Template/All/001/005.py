#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Paint Color Texture
# COLOR: #1fff00
# TEXTCOLOR: #111111
#
#----------------------------------------------------------------------------------------------------------

"""import nuke
nuke.pluginAddPath("/Shares/Y/SHOTGUNPRO/system_backup/paint_render/_daily_renders/Ramamurthy/RamServer/Gizmos/PaintColorTexture")
nuke.createNode("PaintColorTexture")"""

import nuke

# Add gizmo path if needed
nuke.pluginAddPath("/Shares/Y/SHOTGUNPRO/system_backup/paint_render/_daily_renders/Ramamurthy/RamServer/Gizmos/PaintColorTexture")

# Create the gizmo
node = nuke.createNode("PaintColorTexture", inpanel=False)

# Move node to current cursor position
pos = nuke.center()
node.setXpos(int(pos[0]))
node.setYpos(int(pos[1]))
