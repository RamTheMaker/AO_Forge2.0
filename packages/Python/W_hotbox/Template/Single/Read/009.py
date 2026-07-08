#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Open in File Browser
#
#----------------------------------------------------------------------------------------------------------

import os
import platform
import subprocess
import nuke

operatingSystem = platform.system()

for i in nuke.selectedNodes():
    path = os.path.dirname(i.knob('file').value())

    if os.path.exists(path):

        if operatingSystem == "Windows":
            os.startfile(path)

        elif operatingSystem == "Darwin":
            subprocess.Popen(["open", path])

        else:
            subprocess.Popen(["flatpak", "run", "org.kde.dolphin", path])