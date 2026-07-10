import os
import re
import nuke
from pathlib import Path
from pathlib import PureWindowsPath, PurePosixPath
from PySide2 import QtWidgets



FOLDER_STRUCTURE = [
    "plates",

    "comp/scripts",
    "comp/denoise_input",
    "comp/smartvectors",
    "comp/precomp",
    "comp/qc",
    "comp/Review_mov",
    "comp/others",

    "paint/output",

    "roto/output",

    "reference",

    "ai/workflows",

    "mattepaint/nuke/scripts",
    "mattepaint/nuke/temp",
    "mattepaint/nuke/nk_output",

    "mattepaint/comfyui/workflows",
    "mattepaint/comfyui/temp_images",

    "mattepaint/output",

    "delivery/mov",
    "delivery/exr",
]

PROJECT_FORMATS = [
    "HD_720",
    "HD_1080",
    "UHD_4K",

    "2K_Super_35(full-ap)",
    "2K_Cinemascope",
    "2K_DCP",

    "4K_Super_35(full-ap)",
    "4K_Cinemascope",
    "4K_DCP",

    "square_2K",
    "square_4k",

    "2K_LatLong",
    "4K_LatLong",
    "6K_LatLong",
    "8K_LatLong",

    "2K_CubeMap",
    "4K_CubeMap",
    "6K_CubeMap"
]


def _knob_changed():

    node = nuke.thisNode()

    knob = nuke.thisKnob()

    if knob.name() == "project_root":

        path = node[
            "project_root"
        ].value().strip()

        if path:

            shot_name = os.path.basename(
                path.rstrip("/\\")
            )

            node[
                "shot_name"
            ].setValue(
                shot_name
            )

    if knob.name() in [
        "frame_in",
        "frame_out"
    ]:
    
        nuke.root()[
            "first_frame"
        ].setValue(
            int(
                node[
                    "frame_in"
                ].value()
            )
        )
    
        nuke.root()[
            "last_frame"
        ].setValue(
            int(
                node[
                    "frame_out"
                ].value()
            )
        )


def _normalize_path(path):
    """
    AO_Forge path normalization.

    - Windows -> G:/Project/Shot
    - Linux   -> /Shares/Project/Shot
    """

    if not path:
        return ""

    path = path.strip()

    if os.name == "nt":
        return PureWindowsPath(path).as_posix().rstrip("/")

    return PurePosixPath(path).as_posix().rstrip("/")


def _next_script_version(script_dir, shot_name):
    pattern = re.compile(
        r"^{}_Comp_v(\d{{3}})\.nk$".format(re.escape(shot_name))
    )

    highest = 0

    if os.path.exists(script_dir):
        for filename in os.listdir(script_dir):
            match = pattern.match(filename)
            if match:
                highest = max(highest, int(match.group(1)))

    next_version = highest + 1

    return os.path.join(
        script_dir,
        "{}_Comp_v{:03d}.nk".format(shot_name, next_version)
    )


def _set_status(node, message):
    if node.knob("status"):
        node["status"].setValue(message)


def _set_script_path(node, path):
    if node.knob("current_script"):
        node["current_script"].setValue(path)


def _browse_project_root():

    node = nuke.thisNode()

    selected = QtWidgets.QFileDialog.getExistingDirectory(
        None,
        "Select Project Root"
    )

    if not selected:
        return

    normalized = _normalize_path(selected)

    node["project_root"].setValue(normalized)

def _create_shot_structure():
    node = nuke.thisNode()

    project_root = _normalize_path(
        node["project_root"].value()
    )

    nuke.root()["first_frame"].setValue(
        int(node["frame_in"].value())
    )
    
    nuke.root()["last_frame"].setValue(
        int(node["frame_out"].value())
    )

    shot_name = node["shot_name"].value().strip()

    if not project_root:
        nuke.message("Please set Project Root.")
        return

    if not shot_name:
    
        shot_name = os.path.basename(
            project_root.rstrip("/\\")
        )
    
        node[
            "shot_name"
        ].setValue(
            shot_name
        )

    if not os.path.exists(project_root):
        nuke.message("Invalid Project Root.")
        return

    
    comp_scripts = (
        Path(project_root)
        / "comp"
        / "scripts"
    )

    structure_exists = os.path.exists(comp_scripts)

    for folder in FOLDER_STRUCTURE:
        full_path = (
            Path(project_root)
            / folder
        )
        full_path.mkdir(
            parents=True,
            exist_ok=True
        )

    save_path = _next_script_version(
        comp_scripts,
        shot_name
    )

    # Apply frame range
    nuke.root()["first_frame"].setValue(
        int(node["frame_in"].value())
    )
    
    nuke.root()["last_frame"].setValue(
        int(node["frame_out"].value())
    )
    
    # Apply format
    nuke.root()["format"].setValue(
        node["project_format"].value()
    )


    if structure_exists:
    
        _set_status(
            node,
            "Structure Exists / New Version Saved"
        )
    
    else:
    
        _set_status(
            node,
            "Structure Created"
        )

    _set_script_path(
        node,
        save_path
    )

    
    
    # --------------------------------------------------
    # AO Forge Initialized
    # --------------------------------------------------
    
    node["tile_color"].setValue(
        0xA64410FF
    )
    
    node["note_font"].setValue(
        "Verdana Bold"
    )
    
    node["note_font_size"].setValue(
        11
    )
    
    backdrop_exists = False
    
    for n in nuke.allNodes():
    
        if (
            n.Class() == "BackdropNode"
            and
            n.name() == "DoNotDelete"
        ):
    
            backdrop_exists = True
            break
    
    if not backdrop_exists:
    
        backdrop = nuke.nodes.BackdropNode()
    
        backdrop["name"].setValue(
            "DoNotDelete"
        )
    
        backdrop["label"].setValue(
            '<div align="center">'
            '<font color="White" style="bold" size="4">'
            'AO FORGE | PROJECT CONTROLLER'
            '</font><br>'
            '<font color="#EC7638" style="bold" size="3">'
            '!! Do not Delete !!'
            '</font>'
            '</div>'
        )
    
        backdrop["tile_color"].setValue(
            0x2b2b2bff
        )
    
        backdrop["note_font"].setValue(
            "Verdana Bold"
        )
    
        backdrop["note_font_size"].setValue(
            15
        )
    
        backdrop.setXpos(
            node.xpos() - 130
        )
    
        backdrop.setYpos(
            node.ypos() - 100
        )
    
        backdrop["bdwidth"].setValue(
            350
        )
    
        backdrop["bdheight"].setValue(
            150
        )

        nuke.scriptSaveAs(save_path)
   

def _match_selected():
    
        selected = nuke.selectedNodes()
    
        if len(selected) != 1:
    
            nuke.message(
                "Select a single Read node."
            )
    
            return
    
        read = selected[0]
    
        if read.Class() != "Read":
    
            nuke.message(
                "Please select a Read node."
            )
    
            return
    
        controller = nuke.toNode(
            "AO_Controller"
        )
    
        if not controller:
    
            nuke.message(
                "AO_Controller not found."
            )
    
            return
        
        controller[
            "frame_in"
        ].setValue(
            int(
                read[
                    "first"
                ].value()
            )
        )

        controller[
            "frame_out"
        ].setValue(
            int(
                read[
                    "last"
                ].value()
            )
        )

        nuke.root()[
            "first_frame"
        ].setValue(
            int(
                read[
                    "first"
                ].value()
            )
        )
        
        nuke.root()[
            "last_frame"
        ].setValue(
            int(
                read[
                    "last"
                ].value()
            )
        )        
        
        fmt = read.format()
        
        format_name = fmt.name()
        
        formats = list(
            controller[
                "project_format"
            ].values()
        )
        
        if format_name not in formats:
        
            custom_name = (
                "AO_{}x{}".format(
                    fmt.width(),
                    fmt.height()
                )
            )
        
            print(
                "Creating Custom Format:",
                custom_name
            )
        
            format_exists = False
        
            for f in nuke.formats():
        
                if f.name() == custom_name:
        
                    format_exists = True
                    break
        
            if not format_exists:
        
                nuke.addFormat(
                    "{} {} {} {}".format(
                        fmt.width(),
                        fmt.height(),
                        fmt.pixelAspect(),
                        custom_name
                    )
                )
        
            formats.append(
                custom_name
            )
        
            controller[
                "project_format"
            ].setValues(
                formats
            )
        
            format_name = custom_name
        
        controller[
            "project_format"
        ].setValue(
            format_name
        )
        
        nuke.root()[
            "format"
        ].setValue(
            format_name
        )
        
        print(
            "Controller Format =",
            controller[
                "project_format"
            ].value()
        )

def create_controller():
    existing = nuke.toNode("AO_Controller")
    if existing:
        existing.showControlPanel()
        return existing

    node = nuke.createNode("NoOp")
    node.setName("AO_Controller")
    
    node["hide_input"].setValue(True)
    node["tile_color"].setValue(0x288ECBff)
    node["note_font_size"].setValue(8)
    node["note_font_color"].setValue(0xffffffff)
    node["note_font"].setValue("Verdana Bold")
    

    tab = nuke.Tab_Knob("ao_tab", "AO Controller")
    node.addKnob(tab)

    shotinfo_title = nuke.Text_Knob(
        "shotinfo_title",
        "",
        "<b>Shot Info</b>"
    )
    node.addKnob(shotinfo_title)

    # -------------------------
    # Project Root
    # -------------------------
    root_knob = nuke.String_Knob(
        "project_root",
        "Project Root"
    )
    node.addKnob(root_knob)

    browse = nuke.PyScript_Knob(
        "browse_root",
        "Browse"
    )

    browse.setCommand(
        "import ao_controller as ao; "
        "ao._browse_project_root()"
    )

    browse.clearFlag(nuke.STARTLINE)
    node.addKnob(browse)

    # -------------------------
    # Shot Name
    # -------------------------
    shot_knob = nuke.String_Knob(
        "shot_name",
        "Shot Name"
    )
    
    shot_knob.setEnabled(
        False
    )
    
    node.addKnob(
        shot_knob
    )

    shotinfo_divider = nuke.Text_Knob(
        "shotinfo_divider",
        "",
        ""
    )
    node.addKnob(shotinfo_divider)

    

    # -------------------------
    # Reformat
    # -------------------------
    
    settings_divider = nuke.Text_Knob(
        "settings_divider",
        "",
        ""
    )

    settings_title = nuke.Text_Knob(
        "settings_title",
        "",
        "<b>Project Settings</b>"
    )
    node.addKnob(settings_title)

    # -------------------------
    # Frame Range
    # -------------------------
    
    frame_in = nuke.Int_Knob(
        "frame_in",
        "Frame Range"
    )
    
    frame_out = nuke.Int_Knob(
        "frame_out",
        ""
    )
    
    frame_out.clearFlag(nuke.STARTLINE)
    
    frame_in.setValue(
        int(nuke.root()["first_frame"].value())
    )
    
    frame_out.setValue(
        int(nuke.root()["last_frame"].value())
    )

    node.addKnob(frame_in)
    node.addKnob(frame_out)
    
    
    project_format = nuke.Enumeration_Knob(
        "project_format",
        "Project Format",
        PROJECT_FORMATS
    )
    
    node.addKnob(project_format)

    match_format_btn = nuke.PyScript_Knob(
        "match_selected",
        "Match Plate"
    )
    
    match_format_btn.setCommand(
        "import ao_controller as ao\n"
        "ao._match_selected()"
    )
    
    match_format_btn.clearFlag(
        nuke.STARTLINE
    )
    
    node.addKnob(
        match_format_btn
    )
     
    
    project_format.setValue(2)  # UHD_4K


    # -------------------------
    # Spacer
    # -------------------------
    spacer = nuke.Text_Knob(
    "create_spacer",
    "",
    ""
    )
    node.addKnob(spacer)

    management_title = nuke.Text_Knob(
        "management_title",
        "",
        "<b>Shot Management</b>"
    )
    
    node.addKnob(
        management_title
    )


    # -------------------------
    # Create Button
    # -------------------------
    create_btn = nuke.PyScript_Knob(
        "create_structure",
        "Create Shot Structure"
    )
    
    create_btn.setLabel("Create Folder Structure")
    
    
    create_btn.setCommand(
        "import ao_controller as ao; "
        "ao._create_shot_structure()"
    )

    create_btn.setFlag(
        nuke.STARTLINE
    )

    node.addKnob(create_btn)


    # -------------------------
    # Current Script
    # -------------------------
    current_script = nuke.String_Knob(
        "current_script",
        "Current Script Path"
    )

    current_script.setEnabled(False)
    node.addKnob(current_script)

    # -------------------------
    # Status
    # -------------------------
    status = nuke.String_Knob(
        "status",
        "Status"
    )

    status.setEnabled(False)
    status.setValue("Ready")

    node.addKnob(status)


    publish_divider = nuke.Text_Knob(
        "publish_divider",
        "",
        ""
    )
    
    node.addKnob(
        publish_divider
    )

    # ==================================================
    # Publishing
    # ==================================================
    
    publish_title = nuke.Text_Knob(
        "publish_title",
        "",
        "<b>Publishing</b>"
    )
    
    node.addKnob(
        publish_title
    )


    # -------------------------
    # Last Approved QC
    # -------------------------
    last_qc = nuke.String_Knob(
        "last_approved_qc",
        "Approved QC"
    )
    last_qc.setEnabled(False)
    node.addKnob(last_qc)
       
    # -------------------------
    # Promotion History
    # -------------------------
    promotion_history = nuke.Multiline_Eval_String_Knob(
        "promotion_history",
        "Promotion History"
    )
    promotion_history.setEnabled(False)
    promotion_history.setValue("\n\n\n")
    node.addKnob(promotion_history)
    
    # -------------------------
    # End Publishing Group
    # -------------------------
    publish_group_end = nuke.Tab_Knob(
        "publish_group_end",
        "",
        nuke.TABENDGROUP
    )
    node.addKnob(publish_group_end)

    node["knobChanged"].setValue(
        "import ao_controller as ao\n"
        "ao._knob_changed()"
    )

    return node

    



