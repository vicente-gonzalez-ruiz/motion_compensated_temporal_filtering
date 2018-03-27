#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Quality transcoding. Extracts a codestream from a bigger one.

import sys
from GOP              import GOP
from subprocess       import check_call
from subprocess       import CalledProcessError
from arguments_parser import arguments_parser
import logging

logging.basicConfig()
log = logging.getLogger("transcode_quality")

parser = arguments_parser(description="Transcodes in quality a MCJ2K sequence.")
parser.GOPs()
parser.pixels_in_x()
parser.pixels_in_y()
parser.add_argument("--quality",
                    help="Quality.",
                    default=0.25)
parser.texture_layers()
parser.TRLs()

args = parser.parse_known_args()[0]
GOPs = int(args.GOPs)
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
quality = float(args.qstep)
texture_layers = int(args.texture_layers)
TRLs = int(args.TRLs)

LOW = "low"
HIGH = "high"
MOTION = "motion_residue"

def kdu_transcode(filename, slope):
    try:
        check_call("trace kdu_transcode"
                   + "slope=" + str(slops)
                   + " -i " + filename
                   + " -o " + "transcode_quality/" + filename,
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

gop=GOP()
GOP_size = gop.get_size(TRLs)
log.debug("GOP_size = {}".format(GOP_size))

pictures = (GOPs - 1) * GOP_size + 1
log.debug("pictures = {}".format(pictures))

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
    sys.stderr.write("Gains are not available for " + str(TRLs) + " TRLs. Enter them in texture_compress.py")
    exit (0)

MAX_SLOPE = 50000
MIN_SLOPE = 40000
RANGE_SLOPES = MAX_SLOPE - MIN_SLOPE
    
slope = [None]*TRLs # Among temporal subbands (subband / slope):
log.debug("Subband / Slope::")
for s in range(TRLs):
    slope[s] = int(round(MAX_SLOPE - RANGE_SLOPES*quality/GAINS[s]))
    if slopes[s] < 0:
        slopes[s] = 0
    log.debug("{} / {}".format(s, slope[s]))

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
