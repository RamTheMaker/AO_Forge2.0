# AO_Forge/framework/startup.py

from . import knob_defaults
from . import package_manager
from . import menu_builder
from . import config
from . import security
from . import python_loader





def initialize():

    print("-" * 60)
    print(f"{config.TOOLKIT_NAME} v{config.VERSION}")
    print("Initializing...")
    print("-" * 60)

    # ------------------------------------------------------
    # License Validation
    # ------------------------------------------------------

    if not security.validate():
        return

    knob_defaults.initialize()

    discovered = package_manager.load_packages()

    menu_builder.build_menus(
        discovered["gizmos"]
    )

    python_loader.load(
        discovered["python"]
    )

    print(f"{config.TOOLKIT_NAME} Loaded Successfully.")
    print("-" * 60)