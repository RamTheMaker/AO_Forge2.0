import ao_controller
import ao_flux_edit_inpaint
import ao_matte
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


menu_registry.register_ai_tool(

    menu_path="AO Matte",

    callback=ao_matte.create_node,

)


menu_registry.register_ai_tool(

    menu_path="AO Flux Inpaint",

    callback=ao_flux_edit_inpaint.create_node,

)