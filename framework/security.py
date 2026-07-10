import hashlib
from pathlib import Path
#import nuke
import sys
import platform
import subprocess


FRAMEWORK_DIR = Path(__file__).parent

LICENSE_FILE = FRAMEWORK_DIR / "license.dat"


# --------------------------------------------------
# Machine Hash
# --------------------------------------------------

def get_machine_hash():

    # ----------------------------------------
    # Linux
    # ----------------------------------------

    if platform.system() == "Linux":

        machine_id = Path(
            "/etc/machine-id"
        ).read_text().strip()

    # ----------------------------------------
    # Windows
    # ----------------------------------------

    elif platform.system() == "Windows":

        machine_id = subprocess.check_output(
            [
                "powershell",
                "-Command",
                "(Get-CimInstance Win32_ComputerSystemProduct).UUID"
            ],
            text=True
        ).strip()

    else:

        raise RuntimeError(
            "Unsupported Operating System."
        )

    return hashlib.sha256(
        machine_id.encode()
    ).hexdigest()


# --------------------------------------------------
# Check License
# --------------------------------------------------

def is_authorized():

    if not LICENSE_FILE.exists():
        return False

    current_hash = get_machine_hash()

    with open(LICENSE_FILE, "r") as f:

        for line in f:

            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            if line == current_hash:
                return True

    return False


# --------------------------------------------------
# Validate
# --------------------------------------------------


def validate():

    import nuke

    if is_authorized():
        return True

    nuke.message(
        "<center>"
        "<b><font size='5'>Not Authorized</font></b>"
        "</center>"
    )

    return False


if __name__ == "__main__":

    print(get_machine_hash())
