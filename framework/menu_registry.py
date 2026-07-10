"""
AO_Forge Menu Registry
"""

python_menu = None
gizmos_menu = None
toolsets_menu = None
ai_menu = None

nodes_menu = None



# --------------------------------------------------
# Python
# --------------------------------------------------

def register_python_tool(
    menu_path,
    callback,
    shortcut=None,
):

    python_menu.addCommand(
        menu_path,
        callback,
        shortcut,
    )

    nodes_menu.addCommand(
        f"AO_Forge/Python/{menu_path}",
        callback,
    )


# --------------------------------------------------
# AI
# --------------------------------------------------

def register_ai_tool(
    menu_path,
    callback,
    shortcut=None,
):

    ai_menu.addCommand(
        menu_path,
        callback,
        shortcut,
    )

    nodes_menu.addCommand(
        f"AO_Forge/AI/{menu_path}",
        callback,
    )