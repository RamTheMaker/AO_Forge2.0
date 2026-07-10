import nuke
import os
import re
import shutil

LINK_ARROWS_HIDDEN = False



def _update_mov_codec(node):

    codec = node[
        "mov_codec"
    ].value()

    node[
        "mov_h264_profile"
    ].setVisible(False)

    node[
        "mov_prores_profile"
    ].setVisible(False)

    node[
        "mov_dnxhd_profile"
    ].setVisible(False)

    node[
        "mov_dnxhr_profile"
    ].setVisible(False)

    if codec == "H.264":

        node[
            "mov_h264_profile"
        ].setVisible(True)

    elif codec == "Apple ProRes":

        node[
            "mov_prores_profile"
        ].setVisible(True)

    elif codec == "Avid DNxHD":

        node[
            "mov_dnxhd_profile"
        ].setVisible(True)

    elif codec == "Avid DNxHR":

        node[
            "mov_dnxhr_profile"
        ].setVisible(True)




def _knob_changed():

    try:
    
            node = nuke.thisNode()
            knob = nuke.thisKnob()
    
    except:
    
            return
    

    node = nuke.thisNode()

    knob = nuke.thisKnob()

    _update_node_label(node)


    if knob.name() in [
        "task",
        "task_name",
        "mov_type",
        "overwrite"
    ]:
        
    
        _update_task_ui(node)
        _update_mov_ui(node)
    
    elif knob.name() == "compression":
    
        _update_compression(node)
    
    elif knob.name() == "channels":
    
        _update_channels(node)

    elif knob.name() == "raw_data":
    
        _update_raw_data(node)
    
    elif knob.name() == "output_transform":
    
        _update_output_transform(
            node
        )

    
    elif knob.name() == "mov_codec":
    
        _update_mov_codec(
            node
        )
    
        _update_mov_settings(
            node
        )

    
    elif knob.name() in [
    
        "mov_h264_profile",
        "mov_prores_profile",
        "mov_dnxhd_profile",
        "mov_dnxhr_profile",
        "mov_fps"
    
    ]:
    
        _update_mov_settings(
            node
        )
  


def _connect_controller(node):

    controller = nuke.toNode("AO_Controller")

    if not controller:
        return

    node["shot_name_info"].setValue(
        controller["shot_name"].value()
    )

    node["project_root_info"].setValue(
        controller["project_root"].value()
    )

def _update_node_label(node):

    try:
    
            render_file = node[
                "render_file"
            ].value()
    
    except:
    
            return

    render_file = node["render_file"].value()

    display_name = render_file.replace(
        ".%04d.exr",
        ""
    )

    try:

        node.begin()

        write_node = nuke.toNode(
            "Internal_Write"
        )

        colorspace = write_node[
            "colorspace"
        ].value()

        node.end()

    except:

        try:
            node.end()
        except:
            pass

        colorspace = ""

    channels = node[
        "channels"
    ].value()
    
    node["label"].setValue(
        "\n" +
        display_name +
        "\n" +
        colorspace
    )

def _update_mov_ui(node):

    task = node["task"].value()

    node[
        "render_range_btn"
    ].setVisible(
        task != "MOV"
    )

    show_mov = (
        task == "MOV"
    )

    show_exr = (
        task != "MOV"
    )

    node["compression"].setVisible(show_exr)

    node["compression"].setVisible(
        show_exr
    )
    
    node[
        "render_range_btn"
    ].setVisible(
        show_exr
    )

    node["mov_type"].setVisible(show_mov)
    node["mov_info_divider"].setVisible(show_mov)
    node["mov_info"].setVisible(show_mov)
    node["mov_codec"].setVisible(show_mov)
    node["mov_fps"].setVisible(show_mov)

    node["mov_h264_profile"].setVisible(False)
    node["mov_prores_profile"].setVisible(False)
    node["mov_dnxhd_profile"].setVisible(False)
    node["mov_dnxhr_profile"].setVisible(False)

    if show_mov:

        _update_mov_codec(node)


        

def _update_task_ui(node):

    task = node["task"].value()
    mov_type = node["mov_type"].value()  
    project_root = node["project_root_info"].value()

    if task == "Denoise":
    
        path = (
            project_root +
            "/comp/denoise_input"
        )
    
    elif task == "QC":
    
        path = (
            project_root +
            "/comp/qc"
        )
    
    elif task == "Precomp":
    
        path = (
            project_root +
            "/comp/precomp"
        )
    
    elif task == "MattePaint":
    
        path = (
            project_root +
            "/mattepaint/output"
        )
    
    elif task == "Others":
    
        path = (
            project_root +
            "/comp/others"
        )
    
    elif task == "SmartVectors":
    
        path = (
            project_root +
            "/comp/smartvectors"
        )
    
    elif task == "MOV":
    
        if node["mov_type"].value() == "Review":
    
            path = (
                project_root +
                "/comp/Review_mov"
            )
    
        else:
    
            path = (
                project_root +
                "/delivery/mov"
            )


    name = node["task_name"].value().strip()
    shot_name = node["shot_name_info"].value()



    path = ""
    render_file = ""

    # ----------------------------------------
    # Resolve Path First
    # ----------------------------------------

    if task == "Denoise":

        path = project_root + "/comp/denoise_input"

    elif task == "Precomp":

        if name:
            path = project_root + "/comp/precomp/" + name
        else:
            path = project_root + "/comp/precomp"

    elif task == "QC":

        path = project_root + "/comp/qc"

    elif task == "MattePaint":

        if name:
            path = (
                project_root +
                "/mattepaint/output/" +
                name
            )
        else:
            path = (
                project_root +
                "/mattepaint/output"
            )

    elif task == "Others":

        if name:
            path = (
                project_root +
                "/comp/others/" +
                name
            )
        else:
            path = (
                project_root +
                "/comp/others"
            )
    elif task == "SmartVectors":
    
        if name:
    
            path = (
                project_root +
                "/comp/smartvectors/" +
                name
            )
    
        else:
    
            path = (
                project_root +
                "/comp/smartvectors"
            )   



    # ----------------------------------------
    # Get Version
    # ----------------------------------------
    
    version_scan_path = path

    if task == "Denoise":
    
        version_scan_path = (
            project_root +
            "/comp/denoise_input"
        )
    
    elif task == "Precomp":
    
        version_scan_path = (
            project_root +
            "/comp/precomp"
        )
    
    elif task == "MattePaint":
    
        version_scan_path = (
            project_root +
            "/mattepaint/output"
        )
    
    elif task == "Others":
    
        version_scan_path = (
            project_root +
            "/comp/others"
        )
    
    elif task == "QC":
    
        version_scan_path = (
            project_root +
            "/comp/qc"
        )
    
    elif task == "SmartVectors":
    
        version_scan_path = (
            project_root +
            "/comp/smartvectors"
        )

    
    elif task == "MOV":
    
        if mov_type == "Review":
    
            version_scan_path = (
                project_root +
                "/comp/Review_mov"
            )
    
        else:
    
            version_scan_path = (
                project_root +
                "/delivery/mov"
            )
    
    if task == "Denoise":
    
        version_prefix = (
            shot_name +
            "_Denoise"
        )
    
    elif task == "QC":
    
        version_prefix = (
            shot_name +
            "_QC"
        )
    
    elif task == "SmartVectors":
    
        version_prefix = (
            shot_name +
            "_SmartVectors"
        )

    elif task == "MOV":
    
        version_prefix = (
            shot_name +
            "_Comp"
        )
    
    elif task == "Precomp":
    
        version_prefix = (
            shot_name +
            "_Precomp_" +
            name
        )
    
    elif task == "MattePaint":
    
        version_prefix = (
            shot_name +
            "_MattePaint_" +
            name
        )
    
    elif task == "Others":
    
        version_prefix = (
            shot_name +
            "_" +
            name
        )
    
    next_version = _get_next_version(
        version_scan_path,
        version_prefix
    )
    
    overwrite = node[
        "overwrite"
    ].value()
    
    if overwrite:
    
        version_number = (
            next_version - 1
        )
    
        if version_number < 1:
    
            version_number = 1
    
    else:
    
        version_number = (
            next_version
        )
    
    version_string = (
        "v{:03d}".format(
            version_number
        )
    )

    if task == "Denoise":
    
        path = (
            project_root +
            "/comp/denoise_input/" +
            shot_name +
            "_Denoise_" +
            version_string
        )
    
    elif task == "QC":
    
        path = (
            project_root +
            "/comp/qc/" +
            shot_name +
            "_QC_" +
            version_string
        )

    elif task == "SmartVectors":
    
        path = (
            project_root +
            "/comp/smartvectors/" +
            shot_name +
            "_SmartVectors_" +
            version_string
        )

    elif task == "MOV":
    
        if mov_type == "Review":
    
            path = (
                project_root +
                "/comp/Review_mov"
            )
    
        else:
    
            path = (
                project_root +
                "/delivery/mov"
            )

    if task == "Precomp" and name:
    
        path = (
            project_root +
            "/comp/precomp/" +
            shot_name +
            "_Precomp_" +
            name +
            "_" +
            version_string
        )
    
    elif task == "MattePaint" and name:
    
        path = (
            project_root +
            "/mattepaint/output/" +
            shot_name +
            "_MattePaint_" +
            name +
            "_" +
            version_string
        )
    
    elif task == "Others" and name:
    
        path = (
            project_root +
            "/comp/others/" +
            shot_name +
            "_" +
            name +
            "_" +
            version_string
        )

    # ----------------------------------------
    # Build Render Filename
    # ----------------------------------------

    if task == "Denoise":

        render_file = (
            shot_name +
            "_Denoise_" +
            version_string +
            ".%04d.exr"
        )

    elif task == "Precomp":

        if name:

            render_file = (
                shot_name +
                "_Precomp_" +
                name +
                "_" +
                version_string +
                ".%04d.exr"
            )

        else:

            render_file = (
                shot_name +
                "_Precomp_" +
                version_string +
                ".%04d.exr"
            )

    elif task == "QC":

        render_file = (
            shot_name +
            "_QC_" +
            version_string +
            ".%04d.exr"
        )

    elif task == "MattePaint":

        if name:

            render_file = (
                shot_name +
                "_MattePaint_" +
                name +
                "_" +
                version_string +
                ".%04d.exr"
            )

        else:

            render_file = (
                shot_name +
                "_MattePaint_" +
                version_string +
                ".%04d.exr"
            )

    elif task == "Others":

        if name:

            render_file = (
                shot_name +
                "_" +
                name +
                "_" +
                version_string +
                ".%04d.exr"
            )

        else:

            render_file = (
                shot_name +
                "_" +
                version_string +
                ".%04d.exr"
            )


    elif task == "SmartVectors":
    
        if name:
    
            render_file = (
                shot_name +
                "_SmartVectors_" +
                name +
                "_" +
                version_string +
                ".%04d.exr"
            )
    
        else:
    
            render_file = (
                shot_name +
                "_SmartVectors_" +
                version_string +
                ".%04d.exr"
            )     

    elif task == "MOV":
    
        render_file = (
            shot_name +
            "_Comp_" +
            version_string +
            ".mov"
        )  


    # ----------------------------------------
    # UI
    # ----------------------------------------

    show_name = task in [
        "Precomp",
        "MattePaint",
        "Others"
    ]

    if not show_name:
    
        node["task_name"].setValue("")

    if task == "Precomp":
    
        node["task_name"].setLabel(
            "Precomp Name"
        )
    
    elif task == "MattePaint":
    
        node["task_name"].setLabel(
            "MattePaint Name"
        )
    
    elif task == "Others":
    
        node["task_name"].setLabel(
            "Others Name"
        )
    
    else:
    
        node["task_name"].setLabel(
            "Name"
        )
    
    show_move_to_final = (
        task == "QC"
        and
        version_number > 1
    )
    
    node["task_name"].setVisible(
        show_name
    )
    
    node[
        "move_to_final_btn"
    ].setVisible(
        show_move_to_final
    )

    node["real_path"].setValue(path)

    display_path = path
    
    if project_root and path.startswith(project_root):
    
        display_path = path.replace(
            project_root + "/",
            ""
        )
    
        project_name = os.path.basename(
            project_root
        )
    
        display_path = (
            project_name +
            "/" +
            display_path
        )
    
    node["resolved_path"].setValue(
        display_path
    )

    node["task_name"].setVisible(show_name)
    node["render_file"].setValue(render_file)
    node["latest_version"].setValue(version_string)  
    _update_node_label(node)
    _update_internal_write(node)  


def _get_next_version(
    path,
    version_prefix
):

    if not os.path.exists(path):
        return 1

    highest = 0

    version_pattern = re.compile(
        re.escape(version_prefix) +
        r"_v(\d{3})"
    )

    for filename in os.listdir(path):

        match = version_pattern.search(
            filename
        )

        if match:

            version = int(
                match.group(1)
            )

            highest = max(
                highest,
                version
            )

    return highest + 1

def _update_internal_write(node):

    try:

        node.begin()

        write_node = nuke.toNode(
            "Internal_Write"
        )

        if not write_node:
            node.end()
            return

        path = node["real_path"].value()

        filename = node["render_file"].value()

        full_path = (
            path +
            "/" +
            filename
        )
        
        task = node[
            "task"
        ].value()
        
        if task == "MOV":
        
            write_node[
                "file_type"
            ].setValue(
                "mov\t\t\tffmpeg"
            )

            node["mov_codec"].setValue(
                "Apple ProRes"
            )
            
            node["mov_prores_profile"].setValue(
                "ProRes 4:4:4:4 12-bit"
            )
            
            node["mov_fps"].setValue(
                24
            )

            _update_mov_codec(
                node
            )
            
            _update_mov_settings(
                node
            )
        
        else:
        
            write_node[
                "file_type"
            ].setValue(
                "exr"
            )
        
        write_node["file"].setValue(
            full_path
        )

        node.end()

    except Exception as e:

        try:
            node.end()
        except:
            pass

        nuke.warning(
            str(e)
        )

def _validate_qc_metadata(node):

    task = node["task"].value()

    input_node = node.input(0)
    
    if input_node is None:
    
        nuke.message(
            "Nothing Connected\n\n"
            "Connect your output pipe\n"
            "to AO_Write before rendering."
        )
    
        return

    if task != "QC":
        return True

    try:

        upstream_nodes = node.dependencies(
            nuke.INPUTS
        )

        visited = set()

        while upstream_nodes:

            current = upstream_nodes.pop()

            if current in visited:
                continue

            visited.add(current)

            if current.Class() == "CopyMetaData":
                return True

            upstream_nodes.extend(
                current.dependencies(
                    nuke.INPUTS
                )
            )

    except:
        pass

    return False

def _open_task_folder(node):

    try:

        project_root = node[
            "project_root_info"
        ].value()

        task = node[
            "task"
        ].value()

        if task == "Denoise":

            path = (
                project_root +
                "/comp/denoise_input"
            )

        elif task == "QC":

            path = (
                project_root +
                "/comp/qc"
            )

        elif task == "Precomp":

            path = (
                project_root +
                "/comp/precomp"
            )

        elif task == "MattePaint":

            path = (
                project_root +
                "/mattepaint/output"
            )

        elif task == "Others":

            path = (
                project_root +
                "/comp/others"
            )

        elif task == "SmartVectors":

            path = (
                project_root +
                "/comp/smartvectors"
            )

        elif task == "MOV":

            if node["mov_type"].value() == "Review":

                path = (
                    project_root +
                    "/comp/Review_mov"
                )

            else:

                path = (
                    project_root +
                    "/delivery/mov"
                )

        else:

            return

        import platform
        import subprocess

        operating_system = platform.system()

        if operating_system == "Windows":

            os.startfile(path)

        elif operating_system == "Darwin":

            subprocess.Popen(
                ["open", path]
            )

        else:

            subprocess.Popen(
                ["xdg-open", path]
            )

    except Exception as e:

        nuke.message(
            str(e)
        )


def _render_range(node):

    controller = nuke.toNode(
        "AO_Controller"
    )

    first_frame = int(
        controller[
            "frame_in"
        ].value()
    )

    last_frame = int(
        controller[
            "frame_out"
        ].value()
    )

    frame_range = nuke.getInput(
        "Frame Range",
        "{}-{}".format(
            first_frame,
            last_frame
        )
    )

    if not frame_range:

        return

    try:

        frame_range_obj = nuke.FrameRange(
            frame_range
        )

    except:

        nuke.message(
            "Invalid Frame Range"
        )

        return

    _render(
        node,
        frame_range_obj.first(),
        frame_range_obj.last()
    )

def _render(
    node,
    first_frame=None,
    last_frame=None
):

    try:

        path = node["real_path"].value()

        filename = node[
            "render_file"
        ].value()

        task = node["task"].value()

        full_path = (
            path +
            "/" +
            filename
        )

        if (
            first_frame is None
            or
            last_frame is None
        ):
        
            controller = nuke.toNode(
                "AO_Controller"
            )
        
            first_frame = int(
                controller[
                    "frame_in"
                ].value()
            )
        
            last_frame = int(
                controller[
                    "frame_out"
                ].value()
            )

        

        input_node = node.input(0)

        if input_node is None:
        
            nuke.message(
                "Output Not Connected\n\n"
                "Connect your output pipe\n"
                "to AO_Write before rendering."
            )
        
            return
        

        name = node["task_name"].value().strip()
        
        if task in [
            "Precomp",
            "MattePaint",
            "Others"
        ]:
        
            if not name:
        
                nuke.message(
                    task +
                    " Name Required\n\n"
                    "Please enter a name.\n\n"
                    "Render cancelled."
                )
        
                return
        
        if not _validate_qc_metadata(node):
        
            nuke.message(
                "QC Validation Failed\n\n"
                "CopyMetaData node is required\n"
                "for QC renders.\n\n"
                "Render cancelled."
            )
        
            return
        
        display_name = filename.replace(
             ".%04d.exr",
             ""
        )  

        # validations here...

        message = (
            "Render\n\n"
            +
            "Task: "
            +
            task
            +
            "\n\nOutput: "
            +
            display_name
            +
            "\n\nFrames: "
            +
            str(first_frame)
            +
            " - "
            +
            str(last_frame)
            +
            "\n\nProceed?"
        )


        if node["overwrite"].value():
        
            message += (
                "\n\nWARNING:\n"
                "Existing version will be overwritten."
            )

        #if not nuke.ask(
        #    message
        #):
            
        
        #    return
        
        os.makedirs(
            path,
            exist_ok=True
        )

        node.begin()

        write_node = nuke.toNode(
            "Internal_Write"
        )

        node.end()

        nuke.execute(
            write_node,
            first_frame,
            last_frame
        )

        
        read_node = nuke.nodes.Read()

               
        read_node["file"].fromUserText(
            full_path
        )

        read_node["tile_color"].setValue(
            0x2b2b2bff
        )

        read_node["label"].setValue(
            '<div align="center">'
            'FrameRange'
            '<br><font color="White" style="bold" size="4">'
            '[value first]-[value last]'
            '</font>'
            '<br><font color="Yellow" style="bold" size="3">'
            '[value colorspace]'
            '</font>'
            '</div>'
        )
        
        if task != "MOV":
        
            read_node["first"].setValue(
                first_frame
            )
        
            read_node["last"].setValue(
                last_frame
            )
        
            read_node["origfirst"].setValue(
                first_frame
            )
        
            read_node["origlast"].setValue(
                last_frame
            )
        
        read_node.setXpos(
            node.xpos()
        )
        
        read_node.setYpos(
            node.ypos() + 150
        )
        
        _update_task_ui(node)
        
        print(
            "[AO_Write] Render Complete : {}".format(
                display_name
            )
        )
        

    except Exception as e:

        nuke.message(
            str(e)
        )

def _move_to_final(node):

    try:

        controller = nuke.toNode(
            "AO_Controller"
        )

        shot_name = controller[
            "shot_name"
        ].value()

        project_root = controller[
            "project_root"
        ].value()

        qc_path = (
            project_root +
            "/comp/qc"
        )

        if not os.path.exists(
            qc_path
        ):

            nuke.message(
                "No QC versions found."
            )

            return

        qc_versions = []

        for item in sorted(
            os.listdir(qc_path),
            reverse=True
        ):

            full_path = os.path.join(
                qc_path,
                item
            )

            if (
                os.path.isdir(
                    full_path
                )
                and
                item.startswith(
                    shot_name +
                    "_QC_"
                )
            ):

                qc_versions.append(
                    item
                )

        if not qc_versions:

            nuke.message(
                "No QC versions found."
            )

            return

        panel = nuke.Panel(
            "Move To Final"
        )

        panel.addEnumerationPulldown(
            "QC Version",
            " ".join(
                qc_versions
            )
        )

        if not panel.show():

            return

        selected_qc = panel.value(
            "QC Version"
        )

        selected_qc = panel.value(
            "QC Version"
        )
        
        delivery_path = (
            project_root +
            "/delivery/exr"
        )
        
        os.makedirs(
            delivery_path,
            exist_ok=True
        )
        
        final_version = _get_next_version(
            delivery_path,
            shot_name + "_Comp"
        )
        
        final_version_string = (
            "v{:03d}".format(
                final_version
            )
        )
        
        final_folder = (
            shot_name +
            "_Comp_" +
            final_version_string
        )
        
        final_path = os.path.join(
            delivery_path,
            final_folder
        )
        
        source_path = os.path.join(
            qc_path,
            selected_qc
        )

        if not os.path.exists(
            source_path
        ):
        
            nuke.message(
                "Selected QC folder does not exist."
            )
        
            return
        
        files = [
            f
            for f in os.listdir(
                source_path
            )
            if os.path.isfile(
                os.path.join(
                    source_path,
                    f
                )
            )
        ]
        
        if not files:
        
            nuke.message(
                "Selected QC folder is empty."
            )
        
            return
        

        publish_message = (
            "Publish Final\n\n"
            "QC Version:\n"
            +
            selected_qc
            +
            "\n\nFinal Version:\n"
            +
            final_folder
            +
            "\n\nProceed?"
        )
        
        if not nuke.ask(
            publish_message
        ):
        
            return
        
        os.makedirs(
            final_path,
            exist_ok=True
        )
        
        for filename in os.listdir(
            source_path
        ):
        
            source_file = os.path.join(
                source_path,
                filename
            )
        
            if not os.path.isfile(
                source_file
            ):
                continue
        
            new_filename = filename.replace(
                selected_qc,
                final_folder
            )
        
            destination_file = os.path.join(
                final_path,
                new_filename
            )
        
            shutil.copy2(
                source_file,
                destination_file
            )

        from datetime import datetime
        
        controller = nuke.toNode(
            "AO_Controller"
        )
        
        if controller:
        
            controller[
                "last_approved_qc"
            ].setValue(
                selected_qc
            )
        
            timestamp = datetime.now().strftime(
                "%Y-%m-%d %I:%M %p"
            )
        
            history_entry = (
                timestamp +
                "\n" +
                selected_qc +
                " -> " +
                final_folder +
                "\n\n"
            )
        
            existing_history = controller[
                "promotion_history"
            ].value()
        
            controller[
                "promotion_history"
            ].setValue(
                history_entry +
                existing_history
            )
        
        nuke.message(
            "Published Final\n\n"
            "QC Version:\n"
            +
            selected_qc
            +
            "\n\nFinal Version:\n"
            +
            final_folder
        )


    except Exception as e:

        nuke.message(
            str(e)
        )

def _update_channels(node):

    try:

        node.begin()

        write_node = nuke.toNode(
            "Internal_Write"
        )

        if not write_node:

            node.end()

            return

        channels = node[
            "channels"
        ].value()

        if channels == "RGB":

            write_node[
                "channels"
            ].setValue(
                "rgb"
            )

        elif channels == "RGBA":

            write_node[
                "channels"
            ].setValue(
                "rgba"
            )

        elif channels == "ALL":

            write_node[
                "channels"
            ].setValue(
                "all"
            )

        node.end()

    except Exception as e:

        try:
            node.end()
        except:
            pass

        nuke.warning(
            str(e)
        )

def _update_raw_data(node):

    try:

        node.begin()

        write_node = nuke.toNode(
            "Internal_Write"
        )

        if not write_node:

            node.end()
            return

        write_node[
            "raw"
        ].setValue(
            node[
                "raw_data"
            ].value()
        )

        node.end()

    except Exception as e:

        try:
            node.end()
        except:
            pass

        nuke.warning(
            str(e)
        )


def _refresh_output_transforms(node):

    try:

        node.begin()

        write_node = nuke.toNode(
            "Internal_Write"
        )

        if not write_node:

            node.end()

            return

        colorspace_knob = write_node["colorspace"]

        raw_values = list(
            colorspace_knob.values()
        )

        current_internal = colorspace_knob.value()

        node.end()

        display_values = []

        current_display = None

        
        for item in raw_values:
        
            display_values.append(item)
        
        current_display = current_internal

        node["output_transform"].setValues(
            display_values
        )

        if current_display:

            node["output_transform"].setValue(
                current_display
            )

    except Exception as e:

        try:
            node.end()
        except:
            pass

        nuke.warning(str(e))


def _update_output_transform(node):

    try:

        node.begin()

        write_node = nuke.toNode(
            "Internal_Write"
        )

        if not write_node:

            node.end()

            return

        colorspace = node[
            "output_transform"
        ].value()
        
        write_node[
            "colorspace"
        ].setValue(
            colorspace
        )

        node.end()

        _update_node_label(node)

    except Exception as e:

        try:
            node.end()
        except:
            pass

        nuke.warning(str(e))

def _update_mov_settings(node):

    try:

        node.begin()

        write_node = nuke.toNode(
            "Internal_Write"
        )

        if not write_node:
            node.end()
            return

        codec = node[
            "mov_codec"
        ].value()

        if codec == "H.264":

            write_node[
                "mov64_codec"
            ].setValue(
                "h264"
            )

            write_node[
                "mov_h264_codec_profile"
            ].setValue(
                node[
                    "mov_h264_profile"
                ].value()
            )

        elif codec == "Apple ProRes":

            write_node[
                "mov64_codec"
            ].setValue(
                "appr"
            )

            write_node[
                "mov_prores_codec_profile"
            ].setValue(
                node[
                    "mov_prores_profile"
                ].value()
            )

        elif codec == "Avid DNxHD":

            write_node[
                "mov64_codec"
            ].setValue(
                "AVdn"
            )

            write_node[
                "mov64_dnxhd_codec_profile"
            ].setValue(
                node[
                    "mov_dnxhd_profile"
                ].value()
            )

        elif codec == "Avid DNxHR":

            write_node[
                "mov64_codec"
            ].setValue(
                "AVdh"
            )

            write_node[
                "mov64_dnxhr_codec_profile"
            ].setValue(
                node[
                    "mov_dnxhr_profile"
                ].value()
            )

        write_node[
            "mov64_fps"
        ].setValue(
            node[
                "mov_fps"
            ].value()
        )

        node.end()

    except Exception as e:

        try:
            node.end()
        except:
            pass

        nuke.warning(
            str(e)
        )


def _update_compression(node):

    try:

        node.begin()

        write_node = nuke.toNode(
            "Internal_Write"
        )

        if not write_node:
            node.end()
            return

        compression = node[
            "compression"
        ].value()

        if compression == "ZIP (1 Scanline)":
        
            write_node[
                "compression"
            ].setValue(
                "Zip (1 scanline)"
            )
        
        elif compression == "ZIP (16 Scanlines)":
        
            write_node[
                "compression"
            ].setValue(
                "Zip (16 scanlines)"
            )
        
        elif compression == "PIZ Wavelet (32 Scanlines)":
        
            write_node[
                "compression"
            ].setValue(
                "PIZ Wavelet"
            )

        elif compression == "DWAA":
        
            write_node[
                "compression"
            ].setValue(
                "DWAA"
            )
        
            write_node[
                "dw_compression_level"
            ].setValue(
                150
            )
        
        node.end()

    except Exception as e:

        try:
            node.end()
        except:
            pass

        nuke.warning(str(e))

def create_ao_write():

    group = nuke.createNode("Group")
    group.setName("AO_Write")
    group["tile_color"].setValue(
        0x2b2b2bff
    )
    
    group["note_font_color"].setValue(
        0xffffffff
    )

    # --------------------------------------------------
    # Internal Group Structure
    # --------------------------------------------------

    group.begin()

    input_node = nuke.nodes.Input(
        name="Output"
    )

    write_node = nuke.nodes.Write(
        name="Internal_Write"
    )

    write_node.setInput(
        0,
        input_node
    )

    output_node = nuke.nodes.Output(
        name="Output1"
    )

    output_node.setInput(
        0,
        input_node
    )

    group.end()

    # --------------------------------------------------
    # AO Write UI
    # --------------------------------------------------

    tab = nuke.Tab_Knob(
        "ao_write_tab",
        "AO Write"
    )
    group.addKnob(tab)

    render_info = nuke.Text_Knob(
        "render_info",
        "",
        "<b>Render Info</b>"
    )
    
    group.addKnob(render_info)


    # --------------------------------------------------
    # Shot Name
    # --------------------------------------------------
    
    shot_name_info = nuke.String_Knob(
        "shot_name_info",
        "Shot Name"
    )
    
    shot_name_info.setEnabled(False)
    shot_name_info.setValue("")
    
    group.addKnob(shot_name_info)

    # --------------------------------------------------
    # Task
    # --------------------------------------------------

    task = nuke.Enumeration_Knob(
        "task",
        "Task",
        [
            "Denoise",
            "Precomp",
            "QC",
            "MattePaint",
            "Others",
            "SmartVectors",
            "MOV"
        ]
    )

    group.addKnob(task)   


    mov_type = nuke.Enumeration_Knob(
        "mov_type",
        "",
        [
            "Review",
            "Final"
        ]
    )
    
    mov_type.clearFlag(
        nuke.STARTLINE
    )
    
    mov_type.setVisible(False)
    
    group.addKnob(
        mov_type
    )

    open_folder_btn = nuke.PyScript_Knob(
        "open_folder_btn",
        "Open Folder"
    )
    
    open_folder_btn.setCommand(
        "import ao_write\n"
        "ao_write._open_task_folder(nuke.thisNode())"
    )
    
    open_folder_btn.clearFlag(
        nuke.STARTLINE
    )
    
    group.addKnob(
        open_folder_btn
    )

    mov_info_divider = nuke.Text_Knob(
        "mov_info_divider",
        "",
        ""
    )
    
    mov_info_divider.setVisible(
        False
    )
    
    group.addKnob(
        mov_info_divider
    )
    
    mov_info = nuke.Text_Knob(
        "mov_info",
        "",
        "<b>MOV Info</b>"
    )
    
    mov_info.setVisible(
        False
    )
    
    group.addKnob(
        mov_info
    )


    # --------------------------------------------------
    # MOV Settings
    # --------------------------------------------------

    mov_codec = nuke.Enumeration_Knob(
        "mov_codec",
        "Codec",
        [
            "H.264",
            "Apple ProRes",
            "Avid DNxHD",
            "Avid DNxHR"
        ]
    )
    
    mov_codec.setVisible(False)
    
    group.addKnob(
        mov_codec
    )
    
    
    mov_h264_profile = nuke.Enumeration_Knob(
        "mov_h264_profile",
        "Codec Profile",
        [
            "Main 4:2:0 8-bit",
            "High 4:2:0 8-bit"
        ]
    )
    
    mov_h264_profile.setValue(
        "High 4:2:0 8-bit"
    )
    
    mov_h264_profile.setVisible(False)
    
    group.addKnob(
        mov_h264_profile
    )

    mov_prores_profile = nuke.Enumeration_Knob(
        "mov_prores_profile",
        "Codec Profile",
        [
            "ProRes 4:4:4:4 XQ 12-bit",
            "ProRes 4:4:4:4 12-bit",
            "ProRes 4:2:2 HQ 10-bit",
            "ProRes 4:2:2 10-bit",
            "ProRes 4:2:2 LT 10-bit",
            "ProRes 4:2:2 Proxy 10-bit"
        ]
    )
    
    mov_prores_profile.setValue(
        "ProRes 4:2:2 HQ 10-bit"
    )
    
    mov_prores_profile.setVisible(False)
    
    group.addKnob(
        mov_prores_profile
    )


    mov_dnxhd_profile = nuke.Enumeration_Knob(
        "mov_dnxhd_profile",
        "Codec Profile",
        [
            "DNxHD 444 10-bit 440Mbit",
            "DNxHD 422 10-bit 220Mbit",
            "DNxHD 422 8-bit 220Mbit",
            "DNxHD 422 8-bit 145Mbit",
            "DNxHD 422 8-bit 36Mbit"
        ]
    )
    
    mov_dnxhd_profile.setValue(
        "DNxHD 422 10-bit 220Mbit"
    )
    
    mov_dnxhd_profile.setVisible(False)
    
    group.addKnob(
        mov_dnxhd_profile
    )



    mov_dnxhr_profile = nuke.Enumeration_Knob(
        "mov_dnxhr_profile",
        "Codec Profile",
        [
            "4:4:4 12-bit",
            "HQX 4:2:2 12-bit",
            "HQ 4:2:2 8-bit",
            "SQ 4:2:2 8-bit",
            "LB 4:2:2 8-bit"
        ]
    )
    
    mov_dnxhr_profile.setValue(
        "HQX 4:2:2 12-bit"
    )
    
    mov_dnxhr_profile.setVisible(False)
    
    group.addKnob(
        mov_dnxhr_profile
    )





    
    mov_fps = nuke.Int_Knob(
        "mov_fps",
        "FPS"
    )
    
    mov_fps.setValue(24)
    
    mov_fps.setVisible(False)
    
    group.addKnob(
        mov_fps
    )

    group.addKnob(
        nuke.Text_Knob(
            "additional_info_top",
            "",
            ""
        )
    )
    
    group.addKnob(
        nuke.Text_Knob(
            "additional_info",
            "",
            "<b>Additional Info</b>"
        )
    )
    
    

    # --------------------------------------------------
    # Compression
    # --------------------------------------------------

    compression = nuke.Enumeration_Knob(
        "compression",
        "Compression",
        [
            "ZIP (1 Scanline)",
            "ZIP (16 Scanlines)",
            "PIZ Wavelet (32 Scanlines)",
            "DWAA"
        ]
    )

    group.addKnob(compression)

    channels = nuke.Enumeration_Knob(
        "channels",
        "Channels",
        [
            "RGB",
            "RGBA",
            "ALL"
        ]
    )
    
    channels.setValue(
        "RGB"
    )
    
    group.addKnob(channels)

    raw_data = nuke.Boolean_Knob(
        "raw_data",
        "Raw Data"
    )
    
    group.addKnob(raw_data)

    raw_data.clearFlag(
        nuke.STARTLINE
    )

    output_transform = nuke.Enumeration_Knob(
        "output_transform",
        "Output Transform",
        []
    )
    
    group.addKnob(
        output_transform
    )

    separator = nuke.Text_Knob(
        "separator",
        "",
        ""
    )
    
    group.addKnob(separator)

 
    
    path_info = nuke.Text_Knob(
        "path_info",
        "",
        "<b>Path Info</b>"
    )
    
    group.addKnob(path_info)


    # --------------------------------------------------
    # Project Root
    # --------------------------------------------------
    
    project_root_info = nuke.String_Knob(
        "project_root_info",
        "Project Root"
    )
    
    project_root_info.setEnabled(False)
    project_root_info.setValue("Not Connected")
    project_root_info.setVisible(False)

    group.addKnob(project_root_info)

    # --------------------------------------------------
    # Name
    # --------------------------------------------------

    task_name = nuke.String_Knob(
        "task_name",
        "Name"
    )

    group.addKnob(task_name)

    # --------------------------------------------------
    # Resolved Path
    # --------------------------------------------------

    resolved_path = nuke.String_Knob(
        "resolved_path",
        "Resolved Path"
    )

    real_path = nuke.String_Knob(
        "real_path",
        "Real Path"
    )
    
    real_path.setVisible(False)
    
    group.addKnob(real_path)

    resolved_path.setEnabled(False)

    group.addKnob(resolved_path)

    # --------------------------------------------------
    # Resolved Path
    # --------------------------------------------------

    render_file = nuke.String_Knob(
        "render_file",
        "Render File"
    )
    
    render_file.setEnabled(False)
    
    group.addKnob(render_file)

    # --------------------------------------------------
    # Latest Version
    # --------------------------------------------------

    latest_version = nuke.String_Knob(
        "latest_version",
        "Next Version"
    )

    latest_version.setEnabled(False)

    group.addKnob(latest_version)

    overwrite = nuke.Boolean_Knob(
        "overwrite",
        "Overwrite Existing Version"
    )
    
    group.addKnob(
        overwrite
    )

    # --------------------------------------------------
    # Render Buttons
    # --------------------------------------------------
    
    button_row = nuke.Text_Knob(
        "button_row",
        "",
        ""
    )
    
    group.addKnob(button_row)
    
    
    render_btn = nuke.PyScript_Knob(
        "render_btn",
        "Render"
    )

    render_btn.setCommand(
        "import ao_write\n"
        "ao_write._render(nuke.thisNode())"
    )
    
    move_to_final_btn = nuke.PyScript_Knob(
        "move_to_final_btn",
        "Move To Final"
    )

    move_to_final_btn.setCommand(
        "import ao_write\n"
        "ao_write._move_to_final(nuke.thisNode())"
    )


    
    move_to_final_btn.setVisible(False)
    
    render_range_btn = nuke.PyScript_Knob(
        "render_range_btn",
        "Render Range"
    )
    
    render_range_btn.setCommand(
        "import ao_write\n"
        "ao_write._render_range(nuke.thisNode())"
    )
    
    group.addKnob(
        render_btn
    )
    
    render_range_btn.clearFlag(
        nuke.STARTLINE
    )
    
    group.addKnob(
        render_range_btn
    )
    
    move_to_final_btn.clearFlag(
        nuke.STARTLINE
    )
    
    group.addKnob(
        move_to_final_btn
    )


       
    _connect_controller(group)
    
    _update_task_ui(group)
    
    _update_mov_ui(group)
    
    _update_channels(group)
    
    _update_raw_data(group)
    
    _update_compression(group)
    
    _refresh_output_transforms(group)
    
    _update_output_transform(group)
    
    _update_mov_settings(group)


    group["knobChanged"].setValue(
        "import ao_write\n"
        "ao_write._knob_changed()"
    )

    return group