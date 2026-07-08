import nuke
from pathlib import Path

from . import config
from . import tool_executor

def build_menus(packages):
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
    
    menubar = nuke.menu("Nuke")
    
    top_menu = menubar.addMenu(
        config.TOOLKIT_NAME
    )

    top_menu.addCommand(
        "About AO_Forge",
        lambda: nuke.message("AO_Forge v2.0")
    )

    root_menu = toolbar.addMenu(
        config.TOOLKIT_NAME,
        icon=str(icon_path)
    )

    # ------------------------------------------------------
    # Menu Registry
    # ------------------------------------------------------

    menus = {
        "": root_menu
    }

    # ======================================================
    # PASS 1
    # Build ALL folders
    # ======================================================

    for package in packages:

        if not package["category"]:
            continue

        current_path = ""

        for part in package["category"].split("/"):

            next_path = (
                part
                if current_path == ""
                else f"{current_path}/{part}"
            )

            if next_path not in menus:

                menus[next_path] = menus[current_path].addMenu(part)

            current_path = next_path

    # ======================================================
    # PASS 2
    # Add ALL commands
    # ======================================================

    for package in packages:

        category_menu = menus.get(package["category"], root_menu)

        display_name = package["name"].replace("_", " ")

        category_menu.addCommand(
            display_name,
            lambda p=package: tool_executor.execute(p)
        )

        build_top_menu()

# ==========================================================
# Build Top Menu
# ==========================================================

def build_top_menu():

    menubar = nuke.menu("Nuke")

    top_menu = menubar.addMenu(
        config.TOOLKIT_NAME
    )

    # ------------------------------------------------------
    # Package Types
    # ------------------------------------------------------

    top_menu.addMenu("Gizmos")

    top_menu.addMenu("Python")

    top_menu.addMenu("Toolsets")

    top_menu.addSeparator()

    top_menu.addCommand(
        "About AO_Forge",
        lambda: nuke.message(f"{config.TOOLKIT_NAME} v{config.VERSION}")
    )
    