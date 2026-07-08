import nuke
import os

print("[AO_AutoSave] Loaded")

def get_current_script_path():
    """
    Returns current Nuke script path.
    """

    script_path = nuke.root().name()

    if script_path == "Root":
        return None

    if not script_path.endswith(".nk"):
        return None

    return script_path


def get_script_name():
    """
    Returns script name without extension.
    """

    script_path = get_current_script_path()

    if not script_path:
        return None

    return os.path.splitext(
        os.path.basename(script_path)
    )[0]


def create_backup_folders():
    """
    Creates backup folder structure.
    """

    script_path = get_current_script_path()

    if not script_path:
        nuke.message(
            "Please save the Nuke script first."
        )
        return

    script_dir = os.path.dirname(
        script_path
    )

    script_name = get_script_name()

    backup_root = os.path.join(
        script_dir,
        "backup"
    )

    version_folder = os.path.join(
        backup_root,
        script_name
    )

    autosaves_folder = os.path.join(
        version_folder,
        "autosaves"
    )

    milestones_folder = os.path.join(
        version_folder,
        "milestones"
    )

    os.makedirs(
        autosaves_folder,
        exist_ok=True
    )

    os.makedirs(
        milestones_folder,
        exist_ok=True
    )

    print(
        "[AO_AutoSave] Backup folders created."
    )


def create_autosave():
    """
    Temporary test entry point.
    """

    create_backup_folders()
