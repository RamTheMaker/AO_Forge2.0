#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Play in RV
# COLOR: #ffd455
# TEXTCOLOR: #111111
#
#----------------------------------------------------------------------------------------------------------

import nuke
import os
import subprocess
import platform
import re
import glob


# ------------------------------------------------------------
# Find RV path (studio Rocky Linux install)
# ------------------------------------------------------------
def get_rv_path():
    system = platform.system()

    if system == "Linux":
        paths = [
            "/opt/rv-rocky8-x86-64-2022.3.1/bin/rv",  # your studio build
            "/usr/local/bin/rv",
            "/usr/bin/rv"
        ]
        for p in paths:
            if os.path.exists(p):
                return p
        return None

    if system == "Windows":
        base_paths = [
            r"C:\Program Files\ShotGrid",
            r"C:\Program Files\Shotgun"
        ]
        for root in base_paths:
            if not os.path.exists(root):
                continue
            for folder in os.listdir(root):
                rv_bin = os.path.join(root, folder, "bin", "rv.exe")
                if os.path.exists(rv_bin):
                    return rv_bin
        return None

    if system == "Darwin":
        mac_paths = [
            "/Applications/RV.app/Contents/MacOS/RV",
            "/usr/local/bin/rv"
        ]
        for p in mac_paths:
            if os.path.exists(p):
                return p
        return None

    return None



# ------------------------------------------------------------
# Extract image sequence info (not called for MOV files)
# ------------------------------------------------------------
def extract_sequence_info(path):

    # Movie formats → not sequences
    movie_ext = (".mov", ".mp4", ".avi", ".mxf", ".m4v", ".wmv")
    if path.lower().endswith(movie_ext):
        if os.path.exists(path):
            return path, 1, 1
        return None, None, None

    # Detect %0Xd
    match = re.search(r"%0(\d+)d", path)
    if match:
        padding = int(match.group(1))
        frame_pattern = f"%0{padding}d"

    else:
        # Detect ####
        hash_match = re.search(r"(#+)", path)
        if hash_match:
            padding = len(hash_match.group(1))
            path = path.replace("#" * padding, f"%0{padding}d")
            frame_pattern = f"%0{padding}d"
        else:
            return None, None, None

    # Build glob pattern
    glob_pattern = re.sub(r"%0\d+d", "[0-9]" * padding, path)
    directory = os.path.dirname(path)
    final_pattern = os.path.join(directory, os.path.basename(glob_pattern))

    files = sorted(glob.glob(final_pattern))
    if not files:
        return None, None, None

    base = os.path.basename(path)
    prefix, suffix = base.split(frame_pattern)

    frame_numbers = []
    for f in files:
        name = os.path.basename(f)
        number = name[len(prefix):-len(suffix)] if suffix else name[len(prefix):]
        if number.isdigit():
            frame_numbers.append(int(number))

    if not frame_numbers:
        return None, None, None

    start = min(frame_numbers)
    end = max(frame_numbers)

    first_file = path.replace(frame_pattern, str(start).zfill(padding))

    return first_file, start, end



# ------------------------------------------------------------
# RV Launcher
# ------------------------------------------------------------
def launch_rv():
    selected = nuke.selectedNodes()
    if not selected:
        nuke.message("Select a Read or Write node, bro.")
        return

    rv_path = get_rv_path()
    if not rv_path:
        nuke.message("RV not found on this machine.")
        return

    args = [rv_path]

    for node in selected:
        if node.Class() not in ("Read", "Write"):
            continue

        try:
            raw_path = node['file'].value().replace("\\", "/")
        except:
            continue

        # Explicit MOV / MP4 / MXF handling
        movie_ext = (".mov", ".mp4", ".avi", ".mxf", ".m4v", ".wmv")
        if raw_path.lower().endswith(movie_ext):
            # MOV is NOT a sequence → pass as single clip
            args.append(raw_path)
            args.extend(["-in", "1", "-out", "1"])
            continue

        # IMAGE SEQUENCE HANDLING
        first_file, start, end = extract_sequence_info(raw_path)
        if not first_file:
            nuke.message(f"Can't parse sequence:\n{raw_path}")
            return

        # Detect padding
        num_match = re.search(r"(\d+)(?=\.\w+$)", first_file)
        if not num_match:
            nuke.message("Padding not detected.")
            return

        padding = len(num_match.group(1))
        pattern = f"%0{padding}d"

        # Convert firstfile → pattern:
        # ex: file.000034.exr → file.%06d.exr
        sequence_pattern = re.sub(r"\d+(?=\.\w+$)", pattern, first_file)

        args.append(sequence_pattern)
        args.extend(["-in", str(start), "-out", str(end)])

    if len(args) <= 1:
        nuke.message("Nothing valid to load into RV.")
        return

    try:
        subprocess.Popen(args)
    except Exception as e:
        nuke.message(f"Failed to launch RV:\n{str(e)}")

launch_rv()