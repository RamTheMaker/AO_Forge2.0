import nuke
import marquee_backdrop

from framework import menu_registry

menu_registry.python_menu.addCommand(
    "Utilities/Backdrop (Marquee)",
    marquee_backdrop.create_backdrop_around_selected,
    "Shift+B"
)