import nuke
import os
import re
import time
import json
import urllib.request
import random
import shutil
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

WORKFLOW_JSON = (
    THIS_DIR
    / "workflows"
    / "Flux2Klein_Edit_Inpaint.json"
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

    cache_dir = os.path.join(
        project_root,
        "comp",
        "AO_Cache",
        "ImageEdit",
        "Flux2Klein"
    )

    output_dir = os.path.join(
        project_root,
        "ai",
        "ImageEdit",
        "Flux2Klein"
    )

    os.makedirs(
        cache_dir,
        exist_ok=True
    )

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    return {

        "cache_dir": cache_dir,

        "output_dir": output_dir,

        "input_png": os.path.join(
            cache_dir,
            "input.png"
        ),

        "cache_png": os.path.join(
            cache_dir,
            "cache.png"
        )
    }



def get_next_output_path():

    paths = get_paths()

    if not paths:
        return None

    output_dir = paths["output_dir"]

    pattern = re.compile(
        r"output_v(\d{4})\.png$"
    )

    highest = 0

    for filename in os.listdir(output_dir):

        match = pattern.match(
            filename
        )

        if match:

            highest = max(
                highest,
                int(
                    match.group(1)
                )
            )

    next_version = highest + 1

    return os.path.join(
        output_dir,
        f"output_v{next_version:04d}.png"
    )


def hide_expression_arrows():

    try:

        prefs = nuke.toNode(
            "preferences"
        )

        if prefs[
            "expression_arrows"
        ].value():

            nuke.menu(
                "Nuke"
            ).findItem(
                "Edit/Expression Arrows"
            ).invoke()

    except:
        pass

def render_input_png(node):

    if node.input(0) is None:
    
            nuke.message(
                "Connect an image to AO_Flux_Inpaint."
            )
    
            return False

    paths = get_paths()

    if not paths:
        return False

    input_png = paths["input_png"]

    print("=" * 60)
    print("INPUT PNG :", input_png)
    print("EXISTS    :", os.path.exists(os.path.dirname(input_png)))
    print("=" * 60)

    node.begin()

    try:

        write_node = nuke.toNode(
            "WRITE_INPUT"
        )

        if not write_node:

            nuke.message(
                "WRITE_INPUT not found."
            )

            return False

        frame = int(
            nuke.frame()
        )
        
        nuke.execute(
            write_node,
            frame,
            frame
        )

    finally:

        node.end()

    start = time.time()

    while True:

        if (
            os.path.exists(input_png)
            and
            os.path.getsize(input_png) > 1000
        ):
            return True

        if time.time() - start > 10:

            nuke.message(
                "input.png not created."
            )

            return False

        time.sleep(0.2)

def get_generation_data(node):

    
    paths = get_paths()
    
    if not paths:
        return None

    return {

        "prompt":
            node["prompt"].value(),

        "seed":
            int(
                node["seed"].value()
            ),

        "steps":
            int(
                node["steps"].value()
            ),

        "consistency":
            float(
                node[
                    "consistency_strength"
                ].value()
            ),

        "input_png":
            paths["input_png"],

        "cache_png":
            paths["cache_png"]
    }

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

def update_workflow_json(data):

    with open(
        WORKFLOW_JSON,
        "r"
    ) as f:

        workflow = json.load(f)

    # -----------------------
    # Prompt
    # -----------------------

    workflow["386"]["inputs"]["text"] = (
        data["prompt"]
    )

    # -----------------------
    # Seed
    # -----------------------

    workflow["375"]["inputs"]["seed"] = (
        data["seed"]
    )

    # -----------------------
    # Steps
    # -----------------------

    workflow["375"]["inputs"]["steps"] = (
        data["steps"]
    )

    # -----------------------
    # Consistency Strength
    # -----------------------

    workflow["424"]["inputs"][
        "strength_model"
    ] = data["consistency"]

    workflow["424"]["inputs"][
        "strength_clip"
    ] = data["consistency"]

    # -----------------------
    # Input PNG
    # -----------------------

    workflow["412"]["inputs"][
        "value"
    ] = data["input_png"]

    # -----------------------
    # Cache PNG
    # -----------------------

    workflow["422"]["inputs"][
        "value"
    ] = data["cache_png"]

    debug_json = os.path.join(
        data["input_png"].rsplit("/", 1)[0],
        "workflow_debug.json"
    )
    
    with open(
            debug_json,
            "w"
    ) as f:
    
        json.dump(
            workflow,
            f,
            indent=4
        )
    
    print(
        "Saved:",
    )
      

    return workflow


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
            f"Server:\n"
            f"{comfy_url}\n\n"
            f"Please check:\n"
            f"• ComfyUI is running\n"
            f"• Host is correct\n"
            f"• Port is correct"
        )
    
        return None
    
    result = json.loads(
        response.read()
    )
    
    prompt_id = result[
        "prompt_id"
    ]
    
    print(
        "Submitted:",
        prompt_id
    )
    
    return prompt_id

def wait_for_cache(
        node,
        prompt_id,
        cache_png
):

    comfy_url = get_comfy_url(
        node
    )

    # Wait for Comfy

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

    # Wait for cache.png

    start = time.time()

    while True:

        if (
            os.path.exists(cache_png)
            and
            os.path.getsize(cache_png) > 1000
        ):
            return True

        if time.time() - start > 20:

            nuke.message(
                "cache.png not generated."
            )

            return False

        time.sleep(0.5)

def random_seed():

    import random

    n = nuke.thisNode()

    n["seed"].setValue(
            get_random_seed()
    )

def increment_seed():

    n = nuke.thisNode()

    seed = int(
        n["seed"].value()
    )

    n["seed"].setValue(
        str(seed + 1)
    )

def decrement_seed():

    n = nuke.thisNode()

    seed = int(
        n["seed"].value()
    )

    n["seed"].setValue(
        str(
            max(
                1,
                seed - 1
            )
        )
    )



def generate():

    node = nuke.thisNode()

    prompt = node[
            "prompt"
        ].value().strip()
    
    if not prompt:
    
            nuke.message(
                "Please enter a prompt before generating."
            )
    
            return

    success = render_input_png(
        node
    )

    if not success:
        return

    data = get_generation_data(
        node
    )


    if not node[
        "fixed_seed"
    ].value():
    
        new_seed = random.randint(
            1,
            2**63 - 1
        )
    
        node["seed"].setValue(
            str(new_seed)
        )
    
        data["seed"] = new_seed

    workflow = update_workflow_json(
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
        data["cache_png"]
    )
    
    if not success:
        return
    

    node.begin()
    
    try:
    
        read_node = nuke.toNode(
            "READ_CACHE"
        )
    
        output_node = None
    
        for n in nuke.allNodes():
    
            if n.Class() == "Output":
    
                output_node = n
                break
    
        if (
            read_node
            and
            output_node
        ):
    
            read_node["reload"].execute()
    
            if (
                output_node.input(0)
                != read_node
            ):
    
                output_node.setInput(
                    0,
                    read_node
                )
    
    finally:
    
        node.end()
    

    reload_cache(node)

    print(
        "Flux2 Klein "
        "generation finished."
    )
    
    viewer = nuke.activeViewer()
    
    if viewer:
    
        viewer_node = viewer.node()
    
        if (
            viewer_node.input(1)
            != node
        ):
            viewer_node.setInput(
                1,
                node
            )
           
    


def get_random_seed():

    import random

    return str(
        random.randint(
            1,
            2**63 - 1
        )
    )

def reload_cache(node=None):

    if node is None:
        node = nuke.thisNode()

    print("AUTO RELOAD RUNNING")

    node.begin()

    try:

        read_node = nuke.toNode(
            "READ_CACHE"
        )

        if not read_node:
            return

        force_reload_read(
            read_node,
            passes=10
        )

    finally:

        node.end()

    viewer = nuke.activeViewer()

    if viewer:

        viewer.node().connectInput(
            0,
            node
        )

    print(
        "Cache reloaded."
    )

def force_reload_read(
        read_node,
        passes=3
):

    for i in range(passes):

        if hasattr(
            nuke,
            "clearRAMCache"
        ):
            nuke.clearRAMCache()

        read_node["reload"].execute()

        time.sleep(0.1)

def save():

    node = nuke.thisNode()

    paths = get_paths()

    if not paths:
        return

    cache_png = paths["cache_png"]

    if (
        not os.path.exists(
            cache_png
        )
        or
        os.path.getsize(
            cache_png
        ) < 1000
    ):

        nuke.message(
            "Nothing generated yet."
        )

        return

    output_path = (
        get_next_output_path()
    )

    if not output_path:
        return

    shutil.copy2(
        cache_png,
        output_path
    )

    # --------------------------
    # CREATE SAVED READ NODE
    # --------------------------
    
    try:
        nuke.root().begin()
    except:
        pass
    
    read = nuke.nodes.Read()
    
    read["file"].setValue(
        output_path
    )
    
    read["reload"].execute()
    
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
    
    print(
        "Saved:",
        output_path
    )
    

def update_server_preset(node):

    preset = node[
        "server_preset"
    ].value()

    host, port = (
        COMFY_SERVERS[
            preset
        ]
    )

    node[
        "comfy_host"
    ].setValue(
        host
    )

    node[
        "comfy_port"
    ].setValue(
        port
    )

def knob_changed():

    node = nuke.thisNode()

    knob = nuke.thisKnob()

    if (
        knob.name()
        ==
        "server_preset"
    ):

        update_server_preset(
            node
        )


def create_node():

    selected = nuke.selectedNodes()
    
    parent = None
    
    if selected:
        parent = selected[-1]
        

    hide_expression_arrows()

    try:
            nuke.root().begin()
    except:
            pass

    node = nuke.nodes.Group()

    if parent:
    
        x = (
            parent.xpos()
            + parent.screenWidth() // 2
            - node.screenWidth() // 2
        )
    
        y = (
            parent.ypos()
            + 100
        )
    
        node.setXpos(x)
        node.setYpos(y)
    
        node.setInput(
            0,
            parent
        )

    node.setSelected(True)

    node.setName(
        "AO_Flux_Inpaint"
    )

    node["tile_color"].setValue(0x4A4A4AFF)

    node["note_font"].setValue(
        "Verdana Bold"
    )

    node["note_font_size"].setValue(10)

    # --------------------------------------------------
    # TAB
    # --------------------------------------------------

    tab = nuke.Tab_Knob(
        "ao_tab",
        "AO ImageEdit"
    )

    node.addKnob(tab)


    # --------------------------------------------------
    # TITLE
    # --------------------------------------------------

    title = nuke.Text_Knob(
        "title",
        "",
        "<b>AO_Flux_Inpaint</b>"
    )

    node.addKnob(title)

    divider1 = nuke.Text_Knob(
        "divider1",
        "",
        ""
    )

    node.addKnob(divider1)

    # --------------------------------------------------
    # PROMPT
    # --------------------------------------------------

    prompt = nuke.Multiline_Eval_String_Knob(
        "prompt",
        "Prompt"
    )

    node.addKnob(prompt)

    # --------------------------------------------------
    # CONSISTENCY
    # --------------------------------------------------

    consistency = nuke.Double_Knob(
        "consistency_strength",
        "Consistency Strength"
    )

    consistency.setValue(0.2)

    node.addKnob(consistency)

    # --------------------------------------------------
    # STEPS
    # --------------------------------------------------

    steps = nuke.Int_Knob(
        "steps",
        "Steps"
    )

    steps.setValue(4)

    node.addKnob(steps)

    # --------------------------------------------------
    # SEED
    # --------------------------------------------------

    seed = nuke.String_Knob(
        "seed",
        "Seed"
    )
    
    seed.setValue(
        get_random_seed()
    )

    seed.setTooltip(
        "ComfyUI seed value"
    )


    node.addKnob(seed)

    # --------------------------------------------------
    # FIXED
    # --------------------------------------------------

    fixed = nuke.Boolean_Knob(
        "fixed_seed",
        "Fixed"
    )

    fixed.setValue(False)

    node.addKnob(fixed)

    line_break = nuke.Text_Knob(
        "line_break",
        "",
        ""
    )
    
    node.addKnob(
        line_break
    )

    # --------------------------------------------------
    # RANDOM
    # --------------------------------------------------

    random_btn = nuke.PyScript_Knob(
        "random_seed",
        "Random"
    )


    node.addKnob(random_btn)
    

    random_btn.setCommand(
        "import ao_flux_edit_inpaint as ai\n"
        "import importlib\n"
        "importlib.reload(ai)\n"
        "ai.random_seed()"
    )

    # --------------------------------------------------
    # +
    # --------------------------------------------------

    plus_btn = nuke.PyScript_Knob(
        "seed_plus",
        "+"
    )

    plus_btn.clearFlag(
        nuke.STARTLINE
    )


    plus_btn.setCommand(
        "import ao_flux_edit_inpaint as ai\n"
        "import importlib\n"
        "importlib.reload(ai)\n"
        "ai.increment_seed()"
    )

    node.addKnob(plus_btn)

    # --------------------------------------------------
    # -
    # --------------------------------------------------

    minus_btn = nuke.PyScript_Knob(
        "seed_minus",
        "-"
    )

    minus_btn.setCommand(
        "import ao_flux_edit_inpaint as ai\n"
        "import importlib\n"
        "importlib.reload(ai)\n"
        "ai.decrement_seed()"
    )

    node.addKnob(minus_btn)

    divider2 = nuke.Text_Knob(
        "divider2",
        "",
        ""
    )

    node.addKnob(divider2)

    # --------------------------------------------------
    # GENERATE
    # --------------------------------------------------

    generate_btn = nuke.PyScript_Knob(
        "generate",
        "Generate"
    )

    
    generate_btn.setCommand(
        "import ao_flux_edit_inpaint as ai\n"
        "import importlib\n"
        "importlib.reload(ai)\n"
        "ai.generate()"
    )

    node.addKnob(generate_btn)

    # --------------------------------------------------
    # RELOAD CACHE
    # --------------------------------------------------
    
    reload_btn = nuke.PyScript_Knob(
        "reload_cache",
        "Reload"
    )
    
    reload_btn.clearFlag(
        nuke.STARTLINE
    )
    
    reload_btn.setCommand(
        "import ao_flux_edit_inpaint as ai\n"
        "import importlib\n"
        "importlib.reload(ai)\n"
        "ai.reload_cache()"
    )
    
    node.addKnob(
        reload_btn
    )

    # --------------------------------------------------
    # SAVE
    # --------------------------------------------------

    save_btn = nuke.PyScript_Knob(
        "save",
        "Save"
    )

    save_btn.clearFlag(
        nuke.STARTLINE
    )

    save_btn.setCommand(
        "import ao_flux_edit_inpaint as ai\n"
        "import importlib\n"
        "importlib.reload(ai)\n"
        "ai.save()"
    )
   

    node.addKnob(save_btn)



    divider3 = nuke.Text_Knob(
        "divider3",
        "",
        ""
    )
    
    node.addKnob(
        divider3
    )

    # --------------------------------------------------
    # COMFYUI SETTINGS
    # --------------------------------------------------
    
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

    node["server_preset"].setValue(
        "127.0.0.1:8188"
    )
    
    update_server_preset(
        node
    )
    
    comfy_end = nuke.Tab_Knob(
        "comfy_end",
        "",
        nuke.TABENDGROUP
    )
    
    node.addKnob(
        comfy_end
    )

    node["knobChanged"].setValue(
        "import ao_flux_edit_inpaint as ai\n"
        "import importlib\n"
        "importlib.reload(ai)\n"
        "ai.knob_changed()"
    )



    # --------------------------------------------------
    # INTERNAL GROUP NODES
    # --------------------------------------------------

    node.begin()
    
    try:
    
            # ---------------------------
            # INPUT
            # ---------------------------
    
            input_node = nuke.nodes.Input(
                name="Input"
            )
    
            input_node.setXpos(0)
            input_node.setYpos(0)

            # OUTPUT
            output_node = nuke.nodes.Output(
                name="Output"
            )
            
            output_node.setXpos(200)
            output_node.setYpos(100)
            
            output_node.setInput(
                0,
                input_node
            )
    
            # ---------------------------
            # WRITE INPUT
            # ---------------------------
    
            write_node = nuke.nodes.Write(
                name="WRITE_INPUT"
            )
    
            write_node.setInput(
                0,
                input_node
            )
    
            write_node["channels"].setValue(
                "rgba"
            )
    
            write_node["file_type"].setValue(
                "png"
            )
    
            write_node["create_directories"].setValue(
                True
            )

            paths = get_paths()
            
            if paths:
                write_node["file"].setValue(
                    paths["input_png"]
                )

            # ---------------------------
            # READ CACHE
            # ---------------------------
            
            read_cache = nuke.nodes.Read(
                name="READ_CACHE"
            )
            
            if paths:
            
                read_cache["file"].setValue(
                    paths["cache_png"]
                )
            
            read_cache.setXpos(250)
            read_cache.setYpos(0)    
    
            write_node.setXpos(0)
            write_node.setYpos(100)
    
            
            if output_node:
            
                output_node.setInput(
                    0,
                    input_node
                )
            
                output_node.setXpos(200)
                output_node.setYpos(100)
    
    finally:
    
            node.end()

    try:
        prefs = nuke.toNode("preferences")
        prefs["show_input_arrows"].setValue(False)
    except:
        pass

    node.showControlPanel()

    nuke.executeInMainThread(
        lambda: node.setSelected(False)
    )   
    
    return node
