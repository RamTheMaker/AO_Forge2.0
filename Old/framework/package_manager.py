from pathlib import Path

from . import config


# ==========================================================
# Public API
# ==========================================================

def load_packages():
    """
    Discover all AO_Forge packages.
    """

    print("[AO_Forge] Discovering Packages...")

    packages = []

    packages.extend(scan_gizmos())
    packages.extend(scan_python())
    packages.extend(scan_toolsets())

    print(f"[AO_Forge] {len(packages)} package(s) discovered.")

    return packages


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
    
        print(f"[AO_Forge] Gizmo: {relative_path}")

    return packages

# ==========================================================
# Scan Python
# ==========================================================

def scan_python():
    """
    Discover all Python packages.

    (Implementation coming later.)
    """

    return []


# ==========================================================
# Scan Toolsets
# ==========================================================

def scan_toolsets():
    """
    Discover all Toolsets.

    (Implementation coming later.)
    """

    return []