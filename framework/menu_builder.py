import nuke
from pathlib import Path

from . import config
from . import tool_executor
from . import menu_registry



# ==========================================================
# Build Menu Tree
# ==========================================================

def get_or_create_menu(root_menu, menus, category):
    """
    Create nested menus if they don't already exist.
    """

    if not category:
        return root_menu

    current_menu = root_menu
    current_path = ""

    for part in category.split("/"):

        current_path = (
            part
            if current_path == ""
            else f"{current_path}/{part}"
        )

        if current_path not in menus:
            menus[current_path] = current_menu.addMenu(part)

        current_menu = menus[current_path]

    return current_menu

def build_menus(gizmos):
    """
    Build the AO_Forge menu hierarchy.
    """

    print("[AO_Forge] Building Menus...")

    # ------------------------------------------------------
    # Root Menu
    # ------------------------------------------------------

    toolbar = nuke.menu("Nodes")

    framework_root = Path(__file__).resolve().parent.parent

    icon_path = framework_root / "assets" / "icons" / "pipeline_icon.png"

    # ------------------------------------------------------
    # Top Menu
    # ------------------------------------------------------
    
    root_menu = toolbar.addMenu(
        config.TOOLKIT_NAME,
        icon=str(icon_path)
    )

    # ------------------------------------------------------
    # Menu Registry
    # ------------------------------------------------------

    menus = {}
    
    for package in gizmos:
    
        category_menu = get_or_create_menu(
            root_menu,
            menus,
            package["category"]
        )
    
        display_name = package["name"].replace("_", " ")
    
        category_menu.addCommand(
            display_name,
            lambda p=package: tool_executor.execute(p)
        )

    # ------------------------------------------------------
    # Build Top Menu
    # ------------------------------------------------------
    
    build_top_menu(gizmos)




# ==========================================================
# Build Top Menu
# ==========================================================

def build_top_menu(gizmos):

    menubar = nuke.menu("Nuke")

    top_menu = menubar.addMenu(
        config.TOOLKIT_NAME
    )

    # ------------------------------------------------------
    # Package Types
    # ------------------------------------------------------

    ai_menu = top_menu.addMenu("AI")
    
    gizmos_menu = top_menu.addMenu("Gizmos")
    
    python_menu = top_menu.addMenu("Python")
    
    toolsets_menu = top_menu.addMenu("Toolsets")

    
    menu_registry.ai_menu = ai_menu
    menu_registry.gizmos_menu = gizmos_menu
    menu_registry.python_menu = python_menu
    menu_registry.toolsets_menu = toolsets_menu
    menu_registry.nodes_menu = nuke.menu("Nodes")

    
    # ------------------------------------------------------
    # Temporary Gizmo List
    # ------------------------------------------------------
    
    menus = {}
    
    for package in gizmos:
    
        if package["type"] != "GIZMO":
            continue
    
        category_menu = get_or_create_menu(
            gizmos_menu,
            menus,
            package["category"]
        )
    
        display_name = package["name"].replace("_", " ")
    
        category_menu.addCommand(
            display_name,
            lambda p=package: tool_executor.execute(p)
        )

    top_menu.addSeparator()
    
    top_menu.addCommand(
        f"About {config.TOOLKIT_NAME}",
        lambda: nuke.message(
            f"{config.TOOLKIT_NAME}\n"
            f"Version {config.VERSION}\n\n"
            "Forged with Fire."
        )
    )
    