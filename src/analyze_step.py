#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# The MCTF project has been supported by the Junta de Andalucía through
# the Proyecto Motriz "Codificación de Vídeo Escalable y su Streaming
# sobre Internet" (P10-TIC-6548).

#  Iteration of the temporal transform.

import sys
import os
import traceback
from subprocess import check_call
from subprocess import CalledProcessError
from arguments_parser import arguments_parser

parser = arguments_parser(description="Performs a temporal analysis step.")
parser.add_argument("--pictures",
                    help="number of pictures to analyze",
                    default=33)
parser.search_range()
parser.subpixel_accuracy()
parser.update_factor()
parser.pixels_in_x()
parser.pixels_in_y()
parser.add_argument("--temporal_subband",
                    help="number of the temporal subband.",
                    default=0)
parser.always_B()
parser.block_overlaping()
parser.block_size()
parser.border_size()

args = parser.parse_known_args()[0]
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
subband = int(args.temporal_subband)
always_B = int(args.always_B)
block_overlaping = int(args.block_overlaping)
block_size = int(args.block_size)
border_size = int(args.border_size)
pictures = int(args.pictures)
search_range = int(args.search_range)
subpixel_accuracy = int(args.subpixel_accuracy)
update_factor = float(args.update_factor)

try :
    # Lazzy transform.
    check_call("mctf split"
               + " --even_fn="     + "even_" + str(subband)
               + " --low_fn="      + "low_"  + str(subband-1)
               + " --odd_fn="      + "odd_"  + str(subband)
               + " --pictures="    + str(pictures)
               + " --pixels_in_x=" + str(pixels_in_x)
               + " --pixels_in_y=" + str(pixels_in_y)
               , shell=True)
except CalledProcessError :
    sys.exit(-1)

try :
    # Motion estimation.
    check_call("mctf motion_estimate"
               + " --block_size="        + str(block_size)
               + " --border_size="       + str(border_size)
               + " --even_fn="           + "even_"    + str(subband)
               + " --imotion_fn="        + "imotion_" + str(subband)
               + " --motion_fn="         + "motion_"  + str(subband)
               + " --odd_fn="            + "odd_"     + str(subband)
               + " --pictures="          + str(pictures)
               + " --pixels_in_x="       + str(pixels_in_x)
               + " --pixels_in_y="       + str(pixels_in_y)
               + " --search_range="      + str(search_range)
               + " --subpixel_accuracy=" + str(subpixel_accuracy)
               , shell=True)
except Exception:
    print("Exception {} when calling mctf motion_estimate".format(traceback.format_exc()))
    sys.exit(-1)

try :
    # Motion Compensation.
    check_call("mctf decorrelate"
               + " --block_overlaping="  + str(block_overlaping)
               + " --block_size="        + str(block_size)
               + " --even_fn="           + "even_"            + str(subband)
               + " --frame_types_fn="    + "frame_types_"     + str(subband)
               + " --high_fn="           + "high_"            + str(subband)
               + " --motion_in_fn="      + "motion_"          + str(subband)
               + " --motion_out_fn="     + "motion_filtered_" + str(subband)
               + " --odd_fn="            + "odd_"             + str(subband)
               + " --pictures="          + str(pictures)
               + " --pixels_in_x="       + str(pixels_in_x)
               + " --pixels_in_y="       + str(pixels_in_y)
               + " --search_range="      + str(search_range)
               + " --subpixel_accuracy=" + str(subpixel_accuracy)
               + " --always_B="          + str(always_B)
               , shell=True)
except CalledProcessError :
    sys.exit(-1)

try :
    # Eliminate the temporal aliasing (smoothing).
    check_call("mctf update"
               + " --block_size="        + str(block_size)
               + " --even_fn="           + "even_"            + str(subband)
               + " --frame_types_fn="    + "frame_types_"     + str(subband)
               + " --high_fn="           + "high_"            + str(subband)
               + " --low_fn="            + "low_"             + str(subband)
               + " --motion_fn="         + "motion_filtered_" + str(subband)
               + " --pictures="          + str(pictures)
               + " --pixels_in_x="       + str(pixels_in_x)
               + " --pixels_in_y="       + str(pixels_in_y)
               + " --subpixel_accuracy=" + str(subpixel_accuracy)
               + " --update_factor="     + str(update_factor)
               , shell=True)
except CalledProcessError :
    sys.exit(-1)
