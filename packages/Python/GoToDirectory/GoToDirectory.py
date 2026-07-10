import os
import sys
import subprocess

import nuke


# --------------------------------------------------
# Open Folder
# --------------------------------------------------

def open_folder(path):

    if os.path.isfile(path):
        path = os.path.dirname(path)

    if not os.path.isdir(path):
        nuke.message(f"Folder not found:\n\n{path}")
        return

    if sys.platform.startswith("win"):
        os.startfile(path)

    elif sys.platform == "darwin":
        subprocess.Popen(["open", path])

    else:
        subprocess.Popen(["xdg-open", path])


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    # --------------------------------------------------
    # No node selected → Open current script directory
    # --------------------------------------------------

    if len(nuke.selectedNodes()) == 0:

        script_path = nuke.root().name()

        if script_path == "Root":
            nuke.message("Please save the Nuke script first.")
            return

        open_folder(script_path)
        return

    # --------------------------------------------------
    # Node selected
    # --------------------------------------------------

    node = nuke.selectedNode()

    # Prefer "file" knob
    if "file" in node.knobs():

        path = node["file"].evaluate()

        if path:
            open_folder(path)
            return

    # Any File_Knob
    for knob in node.allKnobs():

        if isinstance(knob, nuke.File_Knob):

            path = knob.evaluate()

            if path:
                open_folder(path)
                return

    nuke.message("No File Knob found on the selected node.")