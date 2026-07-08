#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Open In Explorer
# COLOR: #ffffff
# TEXTCOLOR: #111111
#
#----------------------------------------------------------------------------------------------------------

import nuke
import os
import platform
import subprocess


def open_folder(path):
    if not path or not os.path.exists(path):
        return

    operatingSystem = platform.system()

    if operatingSystem == "Windows":
        os.startfile(path)

    elif operatingSystem == "Darwin":
        subprocess.Popen(["open", path])

    else:
        # Linux → Flatpak Dolphin
        subprocess.Popen([
            "flatpak",
            "run",
            "org.kde.dolphin",
            path
        ])


def openPathInExplorer():
    selected_nodes = nuke.selectedNodes()

    # No node selected → open current script folder
    if not selected_nodes:
        script_path = nuke.script_directory()
        open_folder(script_path)
        return

    # Open folders from selected nodes
    for node in selected_nodes:
        if node.knob("file"):
            file_path = node.knob("file").value()
            folder_path = os.path.dirname(file_path)
            open_folder(folder_path)


openPathInExplorer()