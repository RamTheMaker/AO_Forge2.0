import nuke

import ao_controller
import ao_write
import ao_matte


TOOLS = [

    (
        "AO Controller",
        ao_controller.create_controller,
        "Ctrl+Shift+O",
    ),

    (
        "AO Write",
        ao_write.create_ao_write,
        "Ctrl+Shift+W",
    ),

    (
        "AO Matte",
        ao_matte.create_node,
        "Ctrl+Shift+M",
    ),



]


def register():

    menu = nuke.menu("Nuke").findItem("AO_Forge")

    if not menu:
        menu = nuke.menu("Nuke").addMenu("AO_Forge")

    for label, callback, shortcut in TOOLS:

        menu.addCommand(
            label,
            callback,
            shortcut,
        )