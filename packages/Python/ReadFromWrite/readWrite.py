
'''******************************************************
        Creat Read Noder From Write Node.
    -----------------------------------------

__author__ = anupam-b
__version__= 0.1145324799
__contact__ = nimda@htmldigger.in

*******************************************************'''

import nuke


def readWrite():
    sel = nuke.selectedNode()
       
    if sel.Class() == 'Write':
        read = nuke.createNode('Read')
        read.setXpos(int(sel['xpos'].getValue()))
        read.setYpos(int(sel['ypos'].getValue()+100))
        read['file'].setValue(sel['file'].getValue())
        read['first'].setValue(int(nuke.Root()['first_frame'].getValue()))
        read['last'].setValue(int(nuke.Root()['last_frame'].getValue()))
        read['origfirst'].setValue(int(nuke.Root()['first_frame'].getValue()))
        read['origlast'].setValue(int(nuke.Root()['last_frame'].getValue()))
        read['colorspace'].setValue(int(sel['colorspace'].getValue()))

    else:
        nuke.message("Hey man Please select Nuke <b>Write</b> node")
        snote = nuke.createNode('StickyNote')
        snote['label'].setValue('Please select <b>Write</b> node You selected worng Node')
        snote.setYpos(int(sel['ypos'].getValue()))
        snote.setXpos(int(sel['xpos'].getValue()+100))
