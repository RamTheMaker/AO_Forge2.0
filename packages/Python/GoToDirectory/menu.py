import GoToDirectory

from framework import menu_registry

menu_registry.python_menu.addCommand(
    "Utility/Open Explorer",
    GoToDirectory.main,
    "Shift+Q"
)