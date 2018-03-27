#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Iterates temporal inverse transform.

import os
import sys
from GOP import GOP
from subprocess import check_call
from subprocess import CalledProcessError
from arguments_parser import arguments_parser

parser = arguments_parser(description="Performs a step of the temporal synthesis.")
parser.block_overlaping()
parser.block_size()
parser.add_argument("--pictures",
                    help="Number of pictures to synthesize.",
                    default=1)
parser.pixels_in_x()
parser.pixels_in_y()
parser.search_range()
parser.subpixel_accuracy()
parser.add_argument("--temporal_subband",
                    help="Iteration of the temporal transform.",
                    default=0)
parser.update_factor()

args = parser.parse_known_args()[0]
block_overlaping = int(args.block_overlaping)
block_size = int(args.block_size)
pictures = int(args.pictures)
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
search_range = int(args.search_range)
subpixel_accuracy = int(args.subpixel_accuracy)
subband = int(args.temporal_subband)
update_factor = float(args.update_factor)

try:
    check_call("mctf un_update"
               + " --block_size="        + str(block_size)
               + " --even_fn="           + "even_"        + str(subband)
               + " --frame_types_fn="    + "frame_types_" + str(subband)
               + " --high_fn="           + "high_"        + str(subband)
               + " --low_fn="            + "low_"         + str(subband)
               + " --motion_fn="         + "motion_"      + str(subband)
               + " --pictures="          + str(pictures)
               + " --pixels_in_x="       + str(pixels_in_x)
               + " --pixels_in_y="       + str(pixels_in_y)
               + " --subpixel_accuracy=" + str(subpixel_accuracy)
               + " --update_factor="     + str(update_factor)
               , shell=True)
except CalledProcessError:
            sys.exit(-1)

try:
    check_call("mctf correlate"
               + " --block_overlaping="  + str(block_overlaping)
               + " --block_size="        + str(block_size)
               + " --even_fn="           + "even_"        + str(subband)
               + " --frame_types_fn="    + "frame_types_" + str(subband)
               + " --high_fn="           + "high_"        + str(subband)
               + " --motion_in_fn="      + "motion_"      + str(subband)
               + " --odd_fn="            + "odd_"         + str(subband)
               + " --pictures="          + str(pictures)
               + " --pixels_in_x="       + str(pixels_in_x)
               + " --pixels_in_y="       + str(pixels_in_y)
               + " --search_range="      + str(search_range)
               + " --subpixel_accuracy=" + str(subpixel_accuracy)
               , shell=True)
except CalledProcessError:
            sys.exit(-1)

try:
    check_call("mctf merge"
               + " --even="        + "even_" + str(subband)
               + " --low="         + "low_"  + str(subband-1)
               + " --odd="         + "odd_"  + str(subband)
               + " --pictures="    + str(pictures)
               + " --pixels_in_x=" + str(pixels_in_x)
               + " --pixels_in_y=" + str(pixels_in_y)
               , shell=True)
except CalledProcessError:
            sys.exit(-1)
