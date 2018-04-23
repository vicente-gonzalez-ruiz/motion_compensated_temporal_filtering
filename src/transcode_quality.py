#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Quality transcoding. Extracts a codestream from a bigger one,
# preserving the FPS and spatial resolution. A number of quality
# layers of each image of each temporal subband (that is, a number of
# subband-layers) will be copied to the output.

# Example of use:
#
#  mctf transcode_quality --layers=1 # <- Will output L^{T-1}_{Q-1}
#                                    # where T=number of TRLs,
#                                    # Q=number of quality layers.
#
#  mctf transcode_quality --layers=2 # <- Will output L^{T-1}_{Q-1}
#                                    # and depending on Q, will output
#                                    # L^{T-1}_{Q-2} or M^{T-1}.

import logging
import sys
from   GOP              import GOP
from   subprocess       import check_call
from   subprocess       import CalledProcessError
from   arguments_parser import arguments_parser

# {{{ Logging

logging.basicConfig()
log = logging.getLogger("transcode_quality")

# }}}

# {{{ Arguments parsing

parser = arguments_parser(description="Transcodes in quality a MCJ2K sequence.")
parser.GOPs()
parser.layers()       # Number of layers to copy
parser.quantization() # Min slope used when compressing
parser.quantization_step()
parser.TRLs()

args = parser.parse_known_args()[0]
GOPs = int(args.GOPs)
layers = int(args.layers)
quality = float(args.quality)
quantization_step = int(args.quantization_step)
TRLs = int(args.TRLs)

# }}}

# {{{ Slope computation of each subband-layer of each temporal subband

if   TRLs == 1 :
    pass
elif TRLs == 2 :
    GAINS = [1.0, 1.2460784922] # [L1/H1]
elif TRLs == 3 :
    GAINS = [1.0, 1.2500103877, 1.8652117304] # [L2/H2, L2/H1]
elif TRLs == 4 :
    GAINS = [1.0, 1.1598810146, 2.1224082769, 3.1669663339]
elif TRLs == 5 :
    GAINS = [1.0, 1.0877939347, 2.1250255455, 3.8884779989, 5.8022196044]
elif TRLs == 6 :
    GAINS = [1.0, 1.0456562538, 2.0788785438, 4.0611276369, 7.4312544148, 11.0885981772]
elif TRLs == 7 :
    GAINS = [1.0, 1.0232370223, 2.0434169985, 4.0625355976, 7.9362383342, 14.5221257323, 21.6692913386]
elif TRLs == 8 :
    GAINS = [1.0, 1.0117165706, 2.0226778348, 4.0393126714, 8.0305936232, 15.6879129862, 28.7065276104, 42.8346456693]
else :
    sys.stderr.write("Gains are not available for " + str(TRLs) + " TRLs. Enter them in transcode_quality.py")
    exit (0)

# {{{ Typical range of useful slopes in Kakadu
MAX_SLOPE = 50000 # Min quality
MIN_SLOPE = 40000 # Max quality
RANGE_SLOPES = MAX_SLOPE - MIN_SLOPE
# }}}

Q_STEP = 256 # In Kakadu, this should avoid the generation of empty layers

# {{{ Init matrix of slopes
slope = [[0 for q in range(layers)] for t in range(TRLs)]
# }}}

# {{{ Compute slopes
for s in range(TRLs):
    log.debug("Temporal subband {}".format(s))
    for q in range(layers):
        log.debug("Subband-layer {}".format(q))
        _slope_ = int(round(MAX_SLOPE - quality - Q_STEP*q) / GAINS[s])
        if _slope_ < 0:
            slope[s][q] = (0, s, q)
        else:
            slope[s][q] = (_slope_, s, q)
        log.debug("Slope {}".format(slope[s][q]))
# }}}

# }}}

print("{}".format(slope))
        
# {{{ GOPs and pictures

gop=GOP()
GOP_size = gop.get_size(TRLs)
log.debug("GOP_size = {}".format(GOP_size))

pictures = (GOPs - 1) * GOP_size + 1
log.debug("pictures = {}".format(pictures))

# }}}

# {{{ Transcode the (texture) subbands
        
LOW = "low"
HIGH = "high"
MOTION = "motion_residue"

def kdu_transcode(filename, layers):
    try:
        check_call("trace kdu_transcode"
                   + " -i " + filename
                   + " -o " + "transcode_quality/" + filename,
                   + " Clayers=" + str(layers), 
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

# Transcoding of H subbands
subband = 1
while subband < TRLs:

    pictures = (pictures + 1) // 2 - 1
    log.debug("Transcoding subband H[{}] of {} pictures".format(subband, pictures))
    
    image_number = 0
    while image_number < pictures:

        str_image_number = '%04d' % image_number

        filename = HIGH + "_" + str(subband) + "_" + str_image_number + "_Y" 
        kdu_transcode(filename + ".j2c", slope[subband])

        filename = HIGH + "_" + str(subband) + "_" + str_image_number + "_U" 
        kdu_transcode(filename + ".j2c", slope[subband])

        filename = HIGH + "_" + str(subband) + "_" + str_image_number + "_V" 
        kdu_transcode(filename + ".j2c", slope[subband])

        image_number += 1

    subband += 1


# We know the number of subband-layers (quality layers of each
# temporal subband): texture_layers and the number of subbands
# (TRLs). If for example, texture_layers (Q)==8, and TRLs (T)==5, the
# order of subband-layers should be: L^4_7 (one quality layer of L^4),
# L^4_6 (two quality levels of L^4), M^4 (the first and only layer of
# M4), L^4_5 (in total, tree quality layers of L^4), 

# Q=4, T=5:

# q=1: L^4_3
# q=2: L^4_2, M^4, H^4_3
# q=3: L^4_1,      H^4_2, M^3, H^3_3
# q=4: L^4_0,      H^4_1,      H^3_2, M^2, H^2_3
# q=5:             H^4_0,      H^3_1,      H^2_2
# q=6:                         H^3_0,      H^2_1, M^1, H^1_3
# q=7:                                     H^2_0,      H^1_2
# q=8:                                                 H^1_1
# q=9:                                                 H^1_0

#### OLD ####

# Transcoding of M "subbands"
'''
subband = 1
pictures = GOPs * GOP_size - 1
fields = pictures // 2
while subband < TRLs:

    field = 0
    
    while field < fields:

        str_field = '%04d' % field

        for component in range(4):
            
            filename = MOTION + "_" + str(subband) + "_" + str_field + "_comp" + str(component) + ".j2c"
            kdu_transcode(filename, number_of_quality_layers_in_M[subband])

        field += 1

    fields /= 2

    subband += 1
'''

# Transcoding of L subband
image_number = 0
while image_number < pictures - 1:

    str_image_number = '%04d' % image_number

    filename = LOW + "_" + str(TRLs-1) + "_" + str_image_number + "_Y"
    kdu_transcode(filename + ".j2c", number_of_quality_layers_in_L)

    filename = LOW + "_" + str(TRLs-1) + "_" + str_image_number + "_U"
    kdu_transcode(filename + ".j2c", number_of_quality_layers_in_L)

    filename = LOW + "_" + str(TRLs-1) + "_" + str_image_number + "_V"
    kdu_transcode(filename + ".j2c", number_of_quality_layers_in_L)

    image_number += 1

'''
subband = 1
while subband < TRLs:

    try:
        check_call("cp frame_types_" + str(subband) + " transcode_quality/",
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

    subband += 1
'''
