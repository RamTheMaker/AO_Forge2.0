# ==========================================================
# Package Executor
# ==========================================================

import nuke


def execute(package):
    """
    Execute a discovered package.
    """

    package_type = package["type"]

    if package_type == "GIZMO":
        execute_gizmo(package)


# ==========================================================
# GIZMO
# ==========================================================

def execute_gizmo(package):
    """
    Create a gizmo node.
    """

    gizmo_folder = str(package["entry_path"].parent)

    if gizmo_folder not in nuke.pluginPath():
        nuke.pluginAddPath(gizmo_folder)

    nuke.createNode(package["entry_path"].stem)