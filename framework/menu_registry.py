"""
AO_Forge Menu Registry
"""

python_menu = None
gizmos_menu = None
toolsets_menu = None

nodes_menu = None


def register_python_tool(

    menu_path,
    callback,
    shortcut=None,

):

    # ------------------------------------------
    # AO_Forge → Python Menu
    # ------------------------------------------

    python_menu.addCommand(
        menu_path,
        callback,
        shortcut,
    )

    # ------------------------------------------
    # Nodes Tab Search
    # ------------------------------------------

    tab_path = f"AO_Forge/Python/{menu_path}"

    nodes_menu.addCommand(
        tab_path,
        callback,
    )

    # -----------------------------
    # AO_Forge → Python Menu
    # -----------------------------

    python_menu.addCommand(
        menu_path,
        callback,
        shortcut,
    )

    # -----------------------------
    # Tab Search
    # -----------------------------

    nodes_menu.addCommand(
        tab_path,
        callback,
    )