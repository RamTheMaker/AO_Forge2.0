#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Tracker to Roto
# COLOR: #1fff00
# TEXTCOLOR: #000000
#
#----------------------------------------------------------------------------------------------------------

######################
### created by JNS ###
######################
# Copyright to JNS Creations


import nuke

def connectTrackerToRoto():
    sel = None  
    try:
        sel = nuke.selectedNode()
        x = sel.xpos()
        y = sel.ypos()
    except ValueError: 
        pass


    if sel:
            nodeType = sel.Class()    
            if nodeType == 'Tracker4':


                    rt = nuke.createNode('Roto', 'replace true output alpha')
                    rt.setInput(0, None)
                    rt.setXYpos(x, y+100)

                    #bt = nuke.createNode('Blur', 'channels alpha size 3')
                    #bt.hideControlPanel()
                    #bt.setXYpos(x+200,y+50)
                    


                    rt['translate'].fromScript(sel['translate'].toScript())
                    rt['rotate'].fromScript(sel['rotate'].toScript())
                    rt['scale'].fromScript(sel['scale'].toScript())
                    rt['center'].fromScript(sel['center'].toScript())


            else:
                    nuke.message('please select a Tracker node!!!')
    else:
                    nuke.message('please select a Tracker node!!!')        

connectTrackerToRoto()        