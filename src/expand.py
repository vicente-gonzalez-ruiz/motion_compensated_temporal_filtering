#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

## Decodes a sequence of pictures.
#  Decoding consists of two major steps:
#  - Decompression textures and movement data.
#  - Synthesizes the video.
#
#  Examples:
#  - Show default parameters.
#  mcj2k expand --help
#
#  - Expands using the default parameters.\n
#  mcj2k expand
#
#  - Example of use.
#  expand --update_factor=0 --GOPs=1 --TRLs=5 --SRLs=5 --block_size=32
#    --min_block_size=32 --search_range=4 --pixels_in_x=352
#    --pixels_in_y=288 --subpixel_accuracy=0

import sys
import display
from GOP import GOP
from subprocess import check_call
from subprocess import CalledProcessError
from arguments_parser import arguments_parser

parser = arguments_parser(description="Decodes a sequence of pictures.")

parser.block_size()
parser.block_overlaping()
parser.border_size()
parser.GOPs()
parser.TRLs()
parser.pixels_in_x()
parser.pixels_in_y()
parser.min_block_size()
parser.SRLs()
parser.subpixel_accuracy()
parser.search_range()
parser.update_factor()

args = parser.parse_known_args()[0]
block_size = str(args.block_size)
block_overlaping = int(args.block_overlaping)
border_size = int(args.border_size)
GOPs = int(args.GOPs)
min_block_size = int(args.min_block_size)
pixels_in_x = str(args.pixels_in_x)
pixels_in_y = str(args.pixels_in_y)
SRLs = int(args.SRLs)
TRLs = int(args.TRLs)
subpixel_accuracy = str(args.subpixel_accuracy)
search_range = int(args.search_range)
update_factor = float(args.update_factor)

# Time
# /usr/bin/time -f "# Real-User-System\n%e\t%U\t%S" -a -o "info_time" date
# /usr/bin/time -f "%e\t%U\t%S" -a -o "info_time_" date

# Decompress texture.
try:
    check_call("mctf texture_expand"
               + " --GOPs="        + str(GOPs)
               + " --pixels_in_x=" + str(pixels_in_x)
               + " --pixels_in_y=" + str(pixels_in_y)
               + " --SRLs="        + str(SRLs)
               + " --TRLs="        + str(TRLs)
               , shell=True)
except CalledProcessError:
    sys.exit(-1)

## Decompress motion data.
if TRLs > 1 :
    try:
        check_call("mctf motion_expand"
                   + " --block_size="  + str(block_size)
                   + " --GOPs="        + str(GOPs)
                   + " --pixels_in_x=" + str(pixels_in_x)
                   + " --pixels_in_y=" + str(pixels_in_y)
                   + " --TRLs="        + str(TRLs)
                   , shell=True)
    except CalledProcessError:
        sys.exit(-1)

    # Synthesizes the video.
    try:
        check_call("mctf synthesize"
                   + " --GOPs="              + str(GOPs)
                   + " --TRLs="              + str(TRLs)
                   + " --block_size="        + str(block_size)
                   + " --pixels_in_x="       + str(pixels_in_x)
                   + " --pixels_in_y="       + str(pixels_in_y)
                   + " --subpixel_accuracy=" + str(subpixel_accuracy)
                   + " --search_range="      + str(search_range)
                   + " --block_overlaping="  + str(block_overlaping)
                   + " --update_factor="     + str(update_factor)
                   , shell=True)
    except CalledProcessError:
        sys.exit(-1)
