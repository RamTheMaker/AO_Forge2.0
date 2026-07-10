# ==========================================================
# Framework Identity
# ==========================================================

# Display name shown in Nuke
TOOLKIT_NAME = "AO_Forge"

# Prefix added to Categories and Node Names
#
# Examples:
#
#   AI          -> AO_AI
#   Pipeline    -> AO_Pipeline
#   Matte       -> AO_Matte
#   Cache       -> AO_Cache
#
PREFIX = "AO"

# Framework Version
VERSION = "2.0"

# ==========================================================
# Debug
# ==========================================================

DEBUG = False

from pathlib import Path

# ==========================================================
# AO_Forge Root
# ==========================================================

FRAMEWORK_DIR = Path(__file__).resolve().parent

AO_FORGE_ROOT = FRAMEWORK_DIR.parent
