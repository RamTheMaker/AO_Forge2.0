#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Read
#
#----------------------------------------------------------------------------------------------------------

# -*- coding: utf-8 -*-
"""
From selected Write and DeepWrite nodes creates Read nodes.
Path and colorspace is taken from Write node, in case of image sequence it will get frame range from rendered images.
So it doesn't matter if only part of project frame range is rendered.
Multi-selection with multi-format is supported.
Created by Marek Bires
"""

import os.path
import glob
import nuke

def evaluated_sequence_path(writeNode):
    import re

    evaluated = writeNode['file'].evaluate()
    raw = writeNode['file'].value()

    m = re.search(r'(%\d+d)', raw)
    if not m:
        return evaluated

    padding = m.group(1)
    return re.sub(r'\d+(?=\.\w+$)', padding, evaluated)



def framerange_from_path(path):
    # get directory path and filename
    filepath = os.path.split(path)

    # get filename without extension
    filename = filepath[1].split('.')[0]

    # get file extension
    fileExt = os.path.splitext(path)

    # filter same sequence files from the folder
    fullPathSequence = glob.glob('{0}/{1}.*{2}'.format(filepath[0], filename, fileExt[1]))

    # if fullPathSequence (this should be one frame render) set first and last frame
    if not fullPathSequence:
        firstFrame = 1
        lastFrame = 1
    else:
        # list only file names for sequence files
        sequence = [os.path.basename(filepath) for filepath in fullPathSequence]

        # get first frame
        firstFile = sorted(sequence)[0]
        firstFrame = int(firstFile.split('.')[-2])

        # get last frame
        lastFile = sorted(sequence)[-1]
        lastFrame = int(lastFile.split('.')[-2])

    # return nuke frame range object
    return nuke.FrameRange(firstFrame, lastFrame, 1)


def readFromWrite():
    # set default group of nodes
    nodes_write = nuke.selectedNodes('Write')
    nodes_deep = nuke.selectedNodes('DeepWrite')

    nodes = nodes_write + nodes_deep

    # break if empty selection
    if len(nodes) < 1:
        print('read_from_write: No Write node selected')
        return

    for writeNode in nodes:

        # check if write file type is mov
        isMov = writeNode.knob('file_type').value()

        if isMov == "mov" or isMov == "mxf":
            file = writeNode.knob('file').evaluate()
            FFrame = nuke.knob('root.first_frame')

            # create Read for mov
            read_node = nuke.nodes.Read()
            read_node['file'].fromUserText(file)
            read_node['frame_mode'].setValue('1.0')
            read_node['frame'].setValue(FFrame)

            read_node.setXpos(writeNode.xpos())
            read_node.setYpos(writeNode.ypos() + 150)

            # label
            read_node['autolabel'].setValue("")
            read_node['label'].setValue(
                '<div align="center">'
                '<font color="Yellow" size="4">'
                '[string range [file root [file tail [value file]]] 0 end-5]'
                '</font><br>'
                '<font color="White" style="bold" size="4">'
                '[value first]-[value last]'
                '</font><br>'
                '<font color="Yellow" style="bold" size="3">'
                '[value colorspace]'
                '</font>'
                '</div>'
            )

        else:
            # gather values from Write node
            #file = writeNode['file'].getValue()
            

            # set frame range variables
            if writeNode['use_limit'].value():
                first = int(writeNode['first'].value())
                last = int(writeNode['last'].value())
            else:
                frange = framerange_from_path(writeNode['file'].evaluate())
                first = frange.first()
                last = frange.last()

            # create Read nodes
            if "DeepWrite" in writeNode.Class():
                read_node = nuke.nodes.DeepRead()
            else:
                read_node = nuke.nodes.Read()

            # set up Read nodes
            #read_node['file'].setValue(file)
            seq_path = evaluated_sequence_path(writeNode)
            read_node['file'].fromUserText(seq_path)
            read_node['first'].setValue(first)
            read_node['last'].setValue(last)
            read_node['origfirst'].setValue(first)
            read_node['origlast'].setValue(last)

            if "DeepWrite" not in writeNode.Class():
                colorspace = writeNode['colorspace'].value()
                if 'default' in colorspace:
                    colorspace = colorspace[9:-1]
                read_node['colorspace'].setValue(colorspace)

            read_node.setXpos(writeNode.xpos())
            read_node.setYpos(writeNode.ypos() + 150)

            # label
            read_node['autolabel'].setValue("")
            read_node['label'].setValue(
                '<div align="center">'
                '<font color="Yellow" size="4">'
                '[string range [file root [file tail [value file]]] 0 end-5]'
                '</font><br>'
                '<font color="White" style="bold" size="4">'
                '[value first]-[value last]'
                '</font><br>'
                '<font color="Yellow" style="bold" size="3">'
                '[value colorspace]'
                '</font>'
                '</div>'
            )

            if "DeepWrite" not in writeNode.Class():
                # gather colorspace value
                colorspace = writeNode['colorspace'].value()
                if 'default' in colorspace:
                    colorspace = colorspace[9:-1]

                read_node['colorspace'].setValue(colorspace)

            # set Read nodes position
            read_node.setXpos(writeNode.xpos())
            read_node.setYpos(writeNode.ypos() + 150)

readFromWrite()
