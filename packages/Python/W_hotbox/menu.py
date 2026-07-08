import nuke
import os
import W_hotbox, W_hotboxManager

nuke.menu('Nuke').findItem('Edit').addCommand('HotBox', 'channel_hotbox.start()', 'alt+q')
