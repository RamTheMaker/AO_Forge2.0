from pathlib import Path

from . import config


# ==========================================================
# Public API
# ==========================================================


def load_packages():
    """
    Discover all package types.
    """

    gizmos = scan_gizmos()
    python_packages = scan_python()

    toolsets = []

    total = (
        len(gizmos)
        + len(python_packages)
        + len(toolsets)
    )

    print(f"[AO_Forge] {total} package(s) discovered.")

    return {

        "gizmos": gizmos,

        "python": python_packages,

        "toolsets": toolsets,

    }


# ==========================================================
# Scan Gizmos
# ==========================================================

def scan_gizmos():
    """
    Discover all Gizmos.
    """

    framework_root = Path(__file__).resolve().parent.parent

    gizmos_root = framework_root / "packages" / "Gizmos"

    if not gizmos_root.exists():
        return []

    packages = []

    
    for gizmo_file in sorted(gizmos_root.rglob("*.gizmo")):
    
        relative_path = gizmo_file.relative_to(gizmos_root)
    
        category = "/".join(relative_path.parts[:-1])
    
        package = {
    
            "type": "GIZMO",
    
            "category": category,
    
            "name": gizmo_file.stem,
    
            "entry_path": gizmo_file,
    
        }
    
        packages.append(package)
    
        if config.DEBUG:
            print(f"[AO_Forge] Gizmo: {relative_path}")

    return packages

# ==========================================================
# Scan Python
# ==========================================================

def scan_python():
    """
    Discover all Python packages.
    """

    python_root = Path(__file__).resolve().parent.parent / "packages" / "Python"

    if not python_root.exists():
        return []

    packages = []

    for package_folder in sorted(python_root.iterdir()):

        if not package_folder.is_dir():
            continue

        menu_file = package_folder / "menu.py"

        if not menu_file.exists():
            continue

        package = {

            "type": "PYTHON",

            "name": package_folder.name,

            "entry_path": menu_file,

            "package_path": package_folder,

        }

        packages.append(package)

        if config.DEBUG:
            print(f"[AO_Forge] Python: {package_folder.name}")

    return packages


# ==========================================================
# Scan Toolsets
# ==========================================================

def scan_toolsets():
    """
    Discover all Toolsets.

    (Implementation coming later.)
    """

    return []
