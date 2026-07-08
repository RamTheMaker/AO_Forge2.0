import nuke
import readWrite

nuke.menu("Nuke").addCommand(
    "AO_Forge/Python/Utility/Read From Write",
    "readWrite.readWrite()",
    "Shift+r"
)