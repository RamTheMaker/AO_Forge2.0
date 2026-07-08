"""
AO_Forge Python Loader
"""
import sys
import nuke
import importlib.util

from pathlib import Path




def load(python_packages):
    """
    Load all Python packages.
    """

    print("[AO_Forge] Loading Python Packages...")

    for package in python_packages:
    
        package_path = str(package["package_path"])
    
        if package_path not in sys.path:
            sys.path.insert(0, package_path)
    
        nuke.pluginAddPath(package_path)
    
        module_name = f"AO_Forge_{package['name']}_menu"
    
        spec = importlib.util.spec_from_file_location(
            module_name,
            package["entry_path"]
        )
    
        if spec and spec.loader:
    
            module = importlib.util.module_from_spec(spec)
    
            spec.loader.exec_module(module)
    
        print(f"[AO_Forge] Loaded: {package['name']}")