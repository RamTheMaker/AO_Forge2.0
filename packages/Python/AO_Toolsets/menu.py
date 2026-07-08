import ao_controller
import ao_write
import ao_matte

from framework import menu_registry

python_menu = menu_registry.python_menu
gizmo_menu = menu_registry.gizmos_menu

import ao_controller
import ao_write

from framework import menu_registry


menu_registry.register_python_tool(

    menu_path="Core/AO Controller",

    callback=ao_controller.create_controller,

    shortcut="Ctrl+Shift+O",

)

menu_registry.register_python_tool(

    menu_path="Rendering/AO Write",

    callback=ao_write.create_ao_write,

    shortcut="Ctrl+Shift+W",

)

gizmo_menu.addCommand(
    "AI/AO Matte",
    ao_matte.create_node,
)

