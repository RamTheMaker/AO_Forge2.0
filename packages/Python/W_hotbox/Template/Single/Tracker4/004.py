#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Track Updater
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
    if node.Class() != "Tracker4":  # ensure it's a Tracker node
        continue

    # transform indices: 6 = translate, 7 = rotate, 8 = scale
    for transformMode in [6, 7, 8]:
        # count tracks
        tracks = 0
        while node.knob('tracks').isAnimated(31 * tracks + 2):
            tracks += 1

        # set each track's transform to ON (1)
        for track in range(tracks):
            node.knob('tracks').setValue(1, 31 * track + transformMode)
