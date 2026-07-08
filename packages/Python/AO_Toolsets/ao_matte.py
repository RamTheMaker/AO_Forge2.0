import nuke
import os
import re
import time
import json
import urllib.request
import shutil

MATANYONE_JSON = (
    "/Shares/Y/SHOTGUNPRO/system_backup/"
    "paint_render/_daily_renders/"
    "Ramamurthy/AO/AO_Forge/"
    "Workflows/Matte/"
    "Matanyone.json"
)

VIDEOMAMA_JSON = (
    "/Shares/Y/SHOTGUNPRO/system_backup/"
    "paint_render/_daily_renders/"
    "Ramamurthy/AO/AO_Forge/"
    "Workflows/Matte/"
    "VideoMama.json"
)

COMFY_SERVERS = {

    "127.0.0.1:8188":
        ("127.0.0.1", 8188),

    "172.16.0.157:9876":
        ("172.16.0.157", 9876)
}

def find_controller():

    controller = nuke.toNode(
        "AO_Controller"
    )

    if not controller:

        nuke.message(
            "AO_Controller not found."
        )

        return None

    return controller


def get_project_root():

    controller = find_controller()

    if not controller:
        return None

    project_root = controller[
        "project_root"
    ].value().strip()

    if not project_root:

        nuke.message(
            "Project Root not set in AO_Controller."
        )

        return None

    return project_root
    
def get_paths():

    project_root = get_project_root()

    if not project_root:
        return None

    ao_root = os.path.join(
        project_root,
        "ai",
        "AO_Matte"
    )

    input_dir = os.path.join(
        ao_root,
        "input"
    )

    cache_dir = os.path.join(
        ao_root,
        "cache"
    )

    draft_dir = os.path.join(
        ao_root,
        "output",
        "Draft"
    )

    enhanced_dir = os.path.join(
        ao_root,
        "output",
        "Enhanced"
    )

    temp_dir = os.path.join(
        ao_root,
        "temp"
    )
    
    source_dir = input_dir
    
    reference_dir = os.path.join(
        ao_root,
        "ref"
    )
    
    for path in (
        input_dir,
        reference_dir,
        cache_dir,
        draft_dir,
        enhanced_dir,
        temp_dir
    ):
        
    
        
        os.makedirs(
            path,
            exist_ok=True
        )

    return {



        "ao_root":
            ao_root,

        "input_dir":
            input_dir,

        "cache_dir":
            cache_dir,

        "draft_dir":
            draft_dir,

        "enhanced_dir":
            enhanced_dir,

        
        "source_dir":
            input_dir,
        
        
        "source_pattern":
            os.path.join(
                input_dir,
                "input.%04d.png"
            ),

        

        "cache_pattern":
            os.path.join(
                cache_dir,
                "matte.%04d.png"
            ),

        "temp_dir":
            os.path.join(
                ao_root,
                "temp"
            ),
        
        "temp_matanyone_json":
            os.path.join(
                ao_root,
                "temp",
                "Temp_MatAnyone.json"
            ),
        
        "temp_videomama_json":
            os.path.join(
                ao_root,
                "temp",
                "Temp_VideoMama.json"
            ),
        
        "reference_dir":
            reference_dir,
        
        "reference_png":
            os.path.join(
                reference_dir,
                "ref.png"
            )

        
    }

def clear_render_cache():

    paths = get_paths()

    if not paths:
        return False

    folders = [

        paths["input_dir"],
        paths["cache_dir"]

    ]

    for folder in folders:

        if not os.path.isdir(folder):
            continue

        for file_name in os.listdir(folder):

            path = os.path.join(
                folder,
                file_name
            )

            if os.path.isfile(path):

                try:
                    os.remove(path)

                except:
                    pass

    return True

def export_reference_png(node):

    paths = get_paths()

    if not paths:
        return None

    write_reference = node.node(
        "WRITE_REFERENCE"
    )

    if not write_reference:

        nuke.message(
            "WRITE_REFERENCE not found."
        )

        return None

    reference_path = paths[
        "reference_png"
    ]

    write_reference["file"].setValue(
        reference_path
    )

    frame = int(
        nuke.frame()
    )

    write_reference["disable"].setValue(
        False
    )

    try:

        nuke.execute(
            write_reference,
            frame,
            frame
        )

    finally:

        write_reference["disable"].setValue(
            True
        )

    return reference_path

def export_source_sequence(
        node,
        first_frame=None,
        last_frame=None
):

    paths = get_paths()

    if not paths:
        return None

    controller = find_controller()

    if not controller:
        return None

    write_source = node.node(
        "WRITE_SOURCE"
    )

    if not write_source:
        return None

    write_source["file"].setValue(
        paths[
            "source_pattern"
        ]
    )

    if first_frame is None:
    
        first_frame = int(
            controller[
                "frame_in"
            ].value()
        )
    
    if last_frame is None:
    
        last_frame = int(
            controller[
                "frame_out"
            ].value()
        )

    write_source["disable"].setValue(
        False
    )

    try:

        nuke.execute(
            write_source,
            first_frame,
            last_frame
        )

    finally:

        write_source["disable"].setValue(
            True
        )

    return paths[
        "source_dir"
    ]

def get_generation_data():

    paths = get_paths()

    if not paths:
        return None

    return {
    
        
        "source_dir":
            paths["source_dir"],
        
        "source_pattern":
            paths["source_pattern"],
    
        "reference_png":
            paths["reference_png"],
    
        "cache_pattern":
            paths["cache_pattern"],
    
        "cache_dir":
            paths["cache_dir"],
    
        "temp_matanyone_json":
            paths["temp_matanyone_json"],
    
        "temp_videomama_json":
            paths["temp_videomama_json"]
    }

def update_matanyone_json(
        node,
        data
):

    with open(
        MATANYONE_JSON,
        "r"
    ) as f:

        workflow = json.load(f)

    if not node:

        nuke.message(
            "Select AO_Matte node."
        )

        return None
    

    # -----------------------------------
    # SOURCE DIRECTORY
    # -----------------------------------
    
    workflow["13"]["inputs"][
        "value"
    ] = data[
        "source_dir"
    ]


    # -----------------------------------
    # REFERENCE PNG
    # -----------------------------------

    workflow["5"]["inputs"][
        "value"
    ] = data[
        "reference_png"
    ]

    # -----------------------------------
    # CACHE OUTPUT
    # -----------------------------------

    workflow["9"]["inputs"][
        "value"
    ] = data[
        "cache_pattern"
    ]

    # -----------------------------------
    # ERODE
    # -----------------------------------

    workflow["6"]["inputs"][
        "erode_kernel"
    ] = int(
        node[
            "erode"
        ].value()
    )

    # -----------------------------------
    # DILATE
    # -----------------------------------

    workflow["6"]["inputs"][
        "dilate_kernel"
    ] = int(
        node[
            "dilate"
        ].value()
    )

    temp_json = data[
        "temp_matanyone_json"
    ]
    
    with open(
            temp_json,
            "w"
    ) as f:
    
        json.dump(
            workflow,
            f,
            indent=4
        )
    
    return workflow

def update_videomama_json(
        node,
        data
):

    with open(
        VIDEOMAMA_JSON,
        "r"
    ) as f:

        workflow = json.load(f)

    if not node:

        nuke.message(
            "Select AO_Matte node."
        )

        return None

    # -----------------------------------
    # SOURCE DIRECTORY
    # -----------------------------------

    workflow["13"]["inputs"][
        "value"
    ] = data[
        "source_dir"
    ]

    # -----------------------------------
    # REFERENCE PNG
    # -----------------------------------

    workflow["5"]["inputs"][
        "value"
    ] = data[
        "reference_png"
    ]

    # -----------------------------------
    # CACHE OUTPUT
    # -----------------------------------

    workflow["9"]["inputs"][
        "value"
    ] = data[
        "cache_pattern"
    ]

    # -----------------------------------
    # ERODE
    # -----------------------------------

    workflow["6"]["inputs"][
        "erode_kernel"
    ] = int(
        node[
            "erode"
        ].value()
    )

    # -----------------------------------
    # DILATE
    # -----------------------------------

    workflow["6"]["inputs"][
        "dilate_kernel"
    ] = int(
        node[
            "dilate"
        ].value()
    )

    temp_json = data[
        "temp_videomama_json"
    ]

    with open(
            temp_json,
            "w"
    ) as f:

        json.dump(
            workflow,
            f,
            indent=4
        )

    return workflow

def get_current_node():

    try:
        node = nuke.thisNode()

    except:
        node = None

    if (
        not node
        or
        node.Class() == "Root"
    ):

        try:
            node = nuke.selectedNode()

        except:
            node = None

    return node

def get_comfy_url(node):

    host = (
        node["comfy_host"]
        .value()
        .strip()
    )

    port = int(
        node["comfy_port"]
        .value()
    )

    return (
        f"http://{host}:{port}"
    )

def submit_workflow(
        node,
        workflow
):

    comfy_url = get_comfy_url(
        node
    )

    data = {
        "prompt": workflow
    }

    req = urllib.request.Request(
        f"{comfy_url}/prompt",
        data=json.dumps(data).encode(
            "utf-8"
        ),
        headers={
            "Content-Type":
            "application/json"
        }
    )

    try:

        response = urllib.request.urlopen(
            req
        )

    except urllib.error.URLError:

        nuke.message(
            f"Cannot connect to ComfyUI.\n\n"
            f"{comfy_url}"
        )

        return None

    result = json.loads(
        response.read()
    )

    return result[
        "prompt_id"
    ]

def wait_for_cache(
        node,
        prompt_id,
        cache_pattern
):

    comfy_url = get_comfy_url(
        node
    )

    while True:

        try:

            history_req = (
                urllib.request.urlopen(
                    f"{comfy_url}/history/{prompt_id}"
                )
            )

            history = json.loads(
                history_req.read()
            )

            if prompt_id in history:
                break

        except:
            pass

        time.sleep(1)

    cache_dir = os.path.dirname(
        cache_pattern
    )

    start = time.time()

    while True:

        files = [

            f for f in os.listdir(
                cache_dir
            )

            if f.endswith(".png")
        ]

        if files:
            return True

        if time.time() - start > 60:

            nuke.message(
                "Matte cache not generated."
            )

            return False

        time.sleep(0.5)

def reload_cache(node):

    node.begin()

    try:

        read_node = nuke.toNode(
            "READ_CACHE"
        )

        if not read_node:
            return

        read_node["reload"].execute()

        first = int(
            nuke.root().firstFrame()
        )
        
        last = int(
            nuke.root().lastFrame()
        )
        
        read_node[
            "first"
        ].setValue(
            first
        )
        
        read_node[
            "last"
        ].setValue(
            last
        )
        
        read_node[
            "origfirst"
        ].setValue(
            first
        )
        
        read_node[
            "origlast"
        ].setValue(
            last
        )

        output_node = None

        for n in nuke.allNodes():

            if n.Class() == "Output":

                output_node = n
                break

        if (
            output_node
            and
            output_node.input(0)
            != read_node
        ):

            output_node.setInput(
                0,
                read_node
            )

    finally:

        node.end()


def wait_for_cache(
        node,
        prompt_id,
        cache_pattern
):

    comfy_url = get_comfy_url(
        node
    )

    # -----------------------
    # Wait for Comfy History
    # -----------------------

    while True:

        try:

            history_req = (
                urllib.request.urlopen(
                    f"{comfy_url}/history/{prompt_id}"
                )
            )

            history = json.loads(
                history_req.read()
            )

            if prompt_id in history:
                break

        except:
            pass

        time.sleep(1)

    # -----------------------
    # Wait for first matte
    # -----------------------

    first_frame = int(
        nuke.root().firstFrame()
    )

    first_file = (
        cache_pattern
        %
        first_frame
    )

    start = time.time()

    while True:

        if (
            os.path.exists(
                first_file
            )
            and
            os.path.getsize(
                first_file
            ) > 1000
        ):
        
            print(
                "MATTE CACHE FOUND"
            )
        
            return True

        if time.time() - start > 60:

            nuke.message(
                "Matte cache not generated."
            )

            return False

        time.sleep(0.5)

def draft():

    
    node = get_current_node()
    
    if not node:
    
        nuke.message(
            "Select AO_Matte node."
        )
    
        return

    export_reference_png(
        node
    )

    export_source_sequence(
        node
    )

    data = get_generation_data()

    if not data:
        return

    workflow = update_matanyone_json(
        node,
        data
    )

    prompt_id = submit_workflow(
        node,
        workflow
    )
    
    if not prompt_id:
        return
    
    success = wait_for_cache(
        node,
        prompt_id,
        data["cache_pattern"]
    )
    
    if not success:
        return
    
    print(
        "RELOADING CACHE"
    )
    
    reload_cache(
        node
    )
    
    print(
        "AO_Matte Draft finished."
    )

def save_draft():

    node = get_current_node()
    
    if not node:
    
        nuke.message(
            "Select AO_Matte node."
        )
    
        return
    
    matte_name = nuke.getInput(
            "Matte Name",
            "Head"
        )
    
    if not matte_name:
            return
    
    matte_name = (
            matte_name
            .strip()
            .replace(
                " ",
                "_"
            )
        )
    
    paths = get_paths()
    
    if not paths:
            return
    
    draft_root = paths[
        "draft_dir"
    ]
    
    version = 1
    
    while True:
    
            folder_name = (
                f"{matte_name}"
                f"_Draft_v"
                f"{version:03d}"
            )
    
            save_dir = os.path.join(
                draft_root,
                folder_name
            )
    
            if not os.path.exists(
                save_dir
            ):
                break
    
            version += 1

    os.makedirs(
            save_dir
        )
    
    print(
            save_dir
        )
    
    paths = get_paths()
    
    cache_dir = paths[
        "cache_dir"
    ]
    
    for file_name in os.listdir(
            cache_dir
    ):
    
        if not file_name.endswith(
                ".png"
        ):
            continue
    
        src = os.path.join(
            cache_dir,
            file_name
        )
    
        dst = os.path.join(
            save_dir,
            file_name
        )
    
        shutil.copy2(
            src,
            dst
        )

    # --------------------------
    # CREATE SAVED READ NODE
    # --------------------------
    
    try:
        nuke.root().begin()
    except:
        pass
    
    read = nuke.nodes.Read()

    read.setName(
        folder_name
    )
    
    read["file"].setValue(
        os.path.join(
            save_dir,
            "matte.%04d.png"
        )
    )
    
    read["reload"].execute()

    first = int(
        nuke.root().firstFrame()
    )
    
    last = int(
        nuke.root().lastFrame()
    )
    
    read[
        "first"
    ].setValue(
        first
    )
    
    read[
        "last"
    ].setValue(
        last
    )
    
    read[
        "origfirst"
    ].setValue(
        first
    )
    
    read[
        "origlast"
    ].setValue(
        last
    )
    
    x = (
        node.xpos()
        + node.screenWidth() // 2
        - read.screenWidth() // 2
    )
    
    read.setXpos(x)
    
    read.setYpos(
        node.ypos() + 50
    )
    
    nuke.root().end()
    
    nuke.message(
        f"Draft saved:\n\n{save_dir}"
    )


def reload():

    node = get_current_node()

    if not node:
        return

    reload_cache(
        node
    )

    print(
        "AO_Matte Reload finished."
    )

def save_enhanced():

    
    node = get_current_node()
    
    if not node:
    
        nuke.message(
            "Select AO_Matte node."
        )
    
        return

    matte_name = nuke.getInput(
        "Matte Name",
        "Head"
    )

    if not matte_name:
        return

    matte_name = (
        matte_name
        .strip()
        .replace(
            " ",
            "_"
        )
    )

    paths = get_paths()

    if not paths:
        return

    enhanced_root = paths[
        "enhanced_dir"
    ]

    version = 1

    while True:

        folder_name = (
            f"{matte_name}"
            f"_Enhanced_v"
            f"{version:03d}"
        )

        save_dir = os.path.join(
            enhanced_root,
            folder_name
        )

        if not os.path.exists(
            save_dir
        ):
            break

        version += 1

    os.makedirs(
        save_dir
    )

    cache_dir = paths[
        "cache_dir"
    ]

    for file_name in os.listdir(
            cache_dir
    ):

        if not file_name.endswith(
                ".png"
        ):
            continue

        src = os.path.join(
            cache_dir,
            file_name
        )

        dst = os.path.join(
            save_dir,
            file_name
        )

        shutil.copy2(
            src,
            dst
        )

    # --------------------------
    # CREATE READ NODE
    # --------------------------

    try:
        nuke.root().begin()
    except:
        pass

    read = nuke.nodes.Read()

    read.setName(
        folder_name
    )

    read["file"].setValue(
        os.path.join(
            save_dir,
            "matte.%04d.png"
        )
    )

    read["reload"].execute()

    first = int(
        nuke.root().firstFrame()
    )

    last = int(
        nuke.root().lastFrame()
    )

    read["first"].setValue(
        first
    )

    read["last"].setValue(
        last
    )

    read["origfirst"].setValue(
        first
    )

    read["origlast"].setValue(
        last
    )

    x = (
        node.xpos()
        + node.screenWidth() // 2
        - read.screenWidth() // 2
    )

    read.setXpos(x)

    read.setYpos(
        node.ypos() + 100
    )

    nuke.root().end()

    nuke.message(
        f"Enhanced saved:\n\n{save_dir}"
    )


def refine(
        first_frame=None,
        last_frame=None
):
    
    node = get_current_node()

    
    if not node:
    
        nuke.message(
            "Select AO_Matte node."
        )
    
        return
    
    clear_render_cache()

    success = export_reference_png(
        node
    )

    if not success:
        return

    success = export_source_sequence(
        node,
        first_frame,
        last_frame
    )

    if not success:
        return

    data = get_generation_data()

    if not data:
        return

    workflow = update_videomama_json(
        node,
        data
    )

    prompt_id = submit_workflow(
        node,
        workflow
    )

    if not prompt_id:
        return

    success = wait_for_cache(
        node,
        prompt_id,
        data[
            "cache_pattern"
        ]
    )

    if not success:
        return

    reload_cache(
        node
    )

    print(
        "AO_Matte Refine finished."
    )

def render_range():

    controller = find_controller()

    if not controller:
        return

    default_range = (
        f"{int(controller['frame_in'].value())}"
        f"-"
        f"{int(controller['frame_out'].value())}"
    )

    text = nuke.getInput(
        "Render Range",
        default_range
    )

    if not text:
        return

    try:

        frame_range = nuke.FrameRange(
            text
        )

    except:

        nuke.message(
            "Invalid Frame Range."
        )

        return

    refine(
        frame_range.first(),
        frame_range.last()
    )

def create_node():

    try:
        nuke.root().begin()
    except:
        pass

    node = nuke.nodes.Group()

    node.setName(
        "AO_Matte"
    )

    node["tile_color"].setValue(
        0x4A4A4AFF
    )

    node["note_font"].setValue(
        "Verdana Bold"
    )

    node["note_font_size"].setValue(
        10
    )

    # -------------------------
    # TAB
    # -------------------------
    
    tab = nuke.Tab_Knob(
        "ao_tab",
        "AO Matte"
    )
    
    node.addKnob(tab)
    
    # -------------------------
    # TITLE
    # -------------------------
    
    title = nuke.Text_Knob(
        "title",
        "",
        "<b>AO_Matte</b>"
    )
    
    node.addKnob(title)
    
    divider1 = nuke.Text_Knob(
        "divider1",
        "",
        ""
    )

    node.addKnob(divider1)

    
    erode = nuke.Int_Knob(
        "erode",
        "Erode"
    )
    
    erode.setValue(10)
    
    node.addKnob(erode)
    
    dilate = nuke.Int_Knob(
        "dilate",
        "Dilate"
    )
    
    dilate.setValue(10)
    
    node.addKnob(dilate)
    
    divider2 = nuke.Text_Knob(
        "divider2",
        "",
        ""
    )
    
    node.addKnob(divider2)

    #draft_btn = nuke.PyScript_Knob(
    #    "draft",
    #    "Draft"
    #)
    
    #draft_btn.setCommand(
    #    "import scripts.tools.AO_AI.Matte.ao_matte as ai;"
    #    "import importlib;"
    #    "importlib.reload(ai);"
    #    "ai.draft()"
    #)
    
    #node.addKnob(
    #    draft_btn
    #)
    
    #save_draft = nuke.PyScript_Knob(
    #    "save_draft",
    #    "Save"
    #)
    
    #save_draft.clearFlag(
    #    nuke.STARTLINE
    #)
    
    #save_draft.setCommand(
    #    "import scripts.tools.AO_AI.Matte.ao_matte as ai;"
    #    "import importlib;"
    #    "importlib.reload(ai);"
    #    "ai.save_draft()"
    #)
    
    #node.addKnob(
    #    save_draft
    #)


    #divider_refine = nuke.Text_Knob(
    #    "divider_refine",
    #    "",
    #    ""
    #)
    
    #node.addKnob(
    #    divider_refine
    #)    

    
    #refine_btn = nuke.PyScript_Knob(
    #    "refine",
    #    "Refine"
    #)
    
    #refine_btn.setCommand(
    #    "import scripts.tools.AO_AI.Matte.ao_matte as ai;"
    #    "import importlib;"
    #    "importlib.reload(ai);"
    #    "ai.refine()"
    #)
    
    #node.addKnob(
    #    refine_btn
    #)
    
    #save_enhanced = nuke.PyScript_Knob(
    #    "save_enhanced",
    #    "Save"
    #) 
    
    #save_enhanced.clearFlag(
    #    nuke.STARTLINE
    #)
    
    #save_enhanced.setCommand(
    #    "import scripts.tools.AO_AI.Matte.ao_matte as ai;"
    #    "import importlib;"
    #    "importlib.reload(ai);"
    #    "ai.save_enhanced()"
    #)
    
    #node.addKnob(
    #    save_enhanced
    #)

    get_matte_btn = nuke.PyScript_Knob(
        "get_matte",
        "Get Matte"
    )
    
    get_matte_btn.setCommand(
        "import scripts.tools.AO_AI.Matte.ao_matte as ai;"
        "import importlib;"
        "importlib.reload(ai);"
        "ai.refine()"
    )
    
    node.addKnob(
        get_matte_btn
    )
    
    
    range_btn = nuke.PyScript_Knob(
        "render_range",
        "Range"
    )
    
    range_btn.clearFlag(
        nuke.STARTLINE
    )
    
    range_btn.setCommand(
        "import scripts.tools.AO_AI.Matte.ao_matte as ai;"
        "import importlib;"
        "importlib.reload(ai);"
        "ai.render_range()"
    )
    
    node.addKnob(
        range_btn
    )
    
    reload_btn = nuke.PyScript_Knob(
        "reload",
        "Reload"
    )

    reload_btn.clearFlag(
        nuke.STARTLINE
    )
    
    reload_btn.setCommand(
        "import scripts.tools.AO_AI.Matte.ao_matte as ai;"
        "import importlib;"
        "importlib.reload(ai);"
        "ai.reload()"
    )
    
    node.addKnob(
        reload_btn
    )

    divider3 = nuke.Text_Knob(
        "divider3",
        "",
        ""
    )
    
    node.addKnob(
        divider3
    )

    save_matte_btn = nuke.PyScript_Knob(
        "save_matte",
        "Save Matte"
    )
    
    save_matte_btn.setCommand(
        "import scripts.tools.AO_AI.Matte.ao_matte as ai;"
        "import importlib;"
        "importlib.reload(ai);"
        "ai.save_enhanced()"
    )
    
    node.addKnob(
        save_matte_btn
    )

    divider_settings = nuke.Text_Knob(
        "divider_settings",
        "",
        ""
    )
    
    node.addKnob(
        divider_settings
    )
    
    # -----------------------------------
    # COMFYUI SETTINGS
    # -----------------------------------
    
    comfy_begin = nuke.Tab_Knob(
        "comfy_begin",
        "ComfyUI Settings",
        nuke.TABBEGINCLOSEDGROUP
    )
    
    node.addKnob(
        comfy_begin
    )
    
    server_preset = nuke.Enumeration_Knob(
        "server_preset",
        "Server",
        list(
            COMFY_SERVERS.keys()
        )
    )
    
    node.addKnob(
        server_preset
    )
    
    comfy_host = nuke.String_Knob(
        "comfy_host",
        "Host"
    )
    
    comfy_host.setValue(
        "127.0.0.1"
    )
    
    node.addKnob(
        comfy_host
    )
    
    comfy_port = nuke.Int_Knob(
        "comfy_port",
        "Port"
    )
    
    comfy_port.setValue(
        8188
    )
    
    node.addKnob(
        comfy_port
    )
    
    comfy_end = nuke.Tab_Knob(
        "comfy_end",
        "",
        nuke.TABENDGROUP
    )
    
    node.addKnob(
        comfy_end
    )

    node.begin()
    
    try:
        
        # ---------------------------------------
        # INPUTS
        # ---------------------------------------
        
        input_node = nuke.nodes.Input(
            name="INPUT"
        )
                
        # ---------------------------------------
        # OUTPUT
        # ---------------------------------------
        
        output_node = nuke.nodes.Output(
            name="Output"
        )
        
        output_node.setInput(
            0,
            input_node
        )
    
        read_cache = nuke.nodes.Read(
            name="READ_CACHE"
        )

                
    
        paths = get_paths()
    
        if paths:
    
            read_cache["file"].setValue(
                paths["cache_pattern"]
            )

        
        # ---------------------------------------
        # WRITE SOURCE
        # ---------------------------------------
        
        
        write_source = nuke.nodes.Write(
            name="WRITE_SOURCE"
        )
        
        write_source.setInput(
            0,
            input_node
        )
        
        write_source.setXYpos(
            input_node.xpos(),
            input_node.ypos() + 120
        )
        
        
        write_source["file_type"].setValue(
            "png"
        )
        
        write_source["channels"].setValue(
            "rgb"
        )
        
        write_source["create_directories"].setValue(
            True
        )
        
        write_source["disable"].setValue(
            True
        )
        
        write_source["disable"].setValue(
            True
        )

        # ---------------------------------------
        # ALPHA TO RGB
        # ---------------------------------------
        
        alpha_to_rgb = nuke.nodes.Expression(
            name="ALPHA_TO_RGB"
        )
        
        
        alpha_to_rgb.setInput(
            0,
            input_node
        )
        
        alpha_to_rgb["expr0"].setValue("a")
        alpha_to_rgb["expr1"].setValue("a")
        alpha_to_rgb["expr2"].setValue("a")
        
        alpha_to_rgb.setXYpos(
            input_node.xpos() + 250,
            input_node.ypos() + 120
        )
        
        # ---------------------------------------
        # WRITE REFERENCE
        # ---------------------------------------
        
        write_reference = nuke.nodes.Write(
            name="WRITE_REFERENCE"
        )
        
        write_reference.setInput(
            0,
            alpha_to_rgb
        )
        
        write_reference.setXYpos(
            input_node.xpos() + 250,
            input_node.ypos() + 240
        )
        
        write_reference["file_type"].setValue(
            "png"
        )
        
        write_reference["channels"].setValue(
            "rgb"
        )
        
        write_reference["create_directories"].setValue(
            True
        )
        
        write_reference["disable"].setValue(
            True
        )
    
    finally:
    
        node.end()
    


    

    node.showControlPanel()

    return node



