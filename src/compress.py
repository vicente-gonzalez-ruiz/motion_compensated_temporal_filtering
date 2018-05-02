#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# Compression of a sequence of images.

# Examples:
#
#  * Show default parameters:
#
#    mctf compress --help
#
#  * Compress using the default parameters:
#
#    mctf compress
#
#  * Using a GOP_size=4:
#
#    TRLs GOP_size
#    ---- --------
#       1        1
#       2        2
#       3        4
#       4        8
#       5       16
#       6       32
#       7       64
#
#    mctf compress --TRLs=3
#
#  * Controlling quantization:
#
#    mctf compress --quality=50

import sys
import os
from GOP import GOP
from subprocess import check_call
from subprocess import CalledProcessError
from arguments_parser import arguments_parser
import logging

logging.basicConfig()
log = logging.getLogger("compress")

parser = arguments_parser(description="Encodes a sequence of pictures into a MCJ2K stream")
parser.always_B()
parser.block_overlaping()
parser.block_size()
parser.border_size()
parser.GOPs()
parser.min_block_size()
parser.motion_layers()
parser.motion_quantization()
parser.motion_quantization_step()
parser.pixels_in_x()
parser.pixels_in_y()
parser.search_range()
parser.subpixel_accuracy()
#parser.layers()
#parser.quality()
#parser.quantization()
parser.quantization_step()
parser.quantization_max()
parser.quantization_min()
parser.SRLs()
parser.TRLs()
parser.update_factor()

args = parser.parse_known_args()[0]
always_B = int(args.always_B)
block_overlaping = int(args.block_overlaping)
block_size = int(args.block_size)
min_block_size = int(args.min_block_size)
border_size = int(args.border_size)
GOPs = int(args.GOPs)
motion_layers = str(args.motion_layers); log.debug("motion_layers={}".format(motion_layers))
motion_quantization = str(args.motion_quantization); log.debug("motion_quantization={}".format(motion_quantization))
motion_quantization_step = str(args.motion_quantization_step); log.debug("motion_quantization_step={}".format(motion_quantization_step))
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
#layers = str(args.layers)
#quality = float(args.quality)
#quantization = str(args.quantization)
quantization_step = str(args.quantization_step)
quantization_max = int(args.quantization_max)
quantization_min = int(args.quantization_min)
search_range = int(args.search_range)
subpixel_accuracy = int(args.subpixel_accuracy)
TRLs = int(args.TRLs)
SRLs = int(args.SRLs)
update_factor = float(args.update_factor)

MCTF_QUANTIZER       = os.environ["MCTF_QUANTIZER"]

if TRLs > 1:
    try:
        # Temporal analysis of image sequence. Temporal decorrelation.
        check_call("mctf analyze"
                   + " --always_B="          + str(always_B)
                   + " --block_overlaping="  + str(block_overlaping)
                   + " --block_size="        + str(block_size)
                   + " --min_block_size="    + str(min_block_size)
                   + " --border_size="       + str(border_size)
                   + " --GOPs="              + str(GOPs)
                   + " --pixels_in_x="       + str(pixels_in_x)
                   + " --pixels_in_y="       + str(pixels_in_y)
                   + " --search_range="      + str(search_range)
                   + " --subpixel_accuracy=" + str(subpixel_accuracy)
                   + " --TRLs="              + str(TRLs)
                   + " --update_factor="     + str(update_factor)
                   , shell=True)
    except CalledProcessError:
        sys.exit(-1)

    try:
        # Compress motion
        check_call("mctf motion_compress"
                   + " --block_size="               + str(block_size)
                   + " --GOPs="                     + str(GOPs)
                   + " --min_block_size="           + str(min_block_size)
                   + " --pixels_in_x="              + str(pixels_in_x)
                   + " --pixels_in_y="              + str(pixels_in_y)
                   + " --motion_layers="            + str(motion_layers)
                   + " --motion_quantization="      + str(motion_quantization)
                   + " --motion_quantization_step=" + str(motion_quantization_step)
                   + " --SRLs="                     + str(SRLs)
                   + " --TRLs="                     + str(TRLs)
                   , shell=True)
    except CalledProcessError:
        sys.exit(-1)

try:
    # Compress texture
    check_call("mctf texture_compress__"         + MCTF_QUANTIZER
               + " --GOPs="                      + str(GOPs)
               + " --pixels_in_x="               + str(pixels_in_x)
               + " --pixels_in_y="               + str(pixels_in_y)
#               + " --layers="                    + str(layers)
#               + " --quantization="              + str(quantization)
               + " --quantization_step="         + str(quantization_step)
               + " --quantization_max="          + str(quantization_max)
               + " --quantization_min="          + str(quantization_min)
#               + " --quality="                   + str(quality)
               + " --SRLs="                      + str(SRLs)
               + " --TRLs="                      + str(TRLs)
               , shell=True)
except CalledProcessError:
    sys.exit(-1)
