#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# The MCTF project has been supported by the Junta de Andalucía through
# the Proyecto Motriz "Codificación de Vídeo Escalable y su Streaming
# sobre Internet" (P10-TIC-6548).

# Performs the temporal analysis of a picture sequence. Generates a series of files that will later be encoded.

import os
import sys
from GOP import GOP
from subprocess import check_call
from subprocess import CalledProcessError
import arguments_parser

parser = arguments_parser(description="Temporal analysis of a picture sequence.")
args = parser.parse_known_args()[0]

parser.always_B()
if args.always_B:
    always_B = int(args.always_B)

parser.block_overlaping()
if args.block_overlaping:
    block_overlaping = int(args.block_overlaping)

resolution_FHD = 1920 * 1080
parser.block_size()
parser.block_size_min(
if pixels_in_x * pixels_in_y < resolution_FHD:
    block_size = block_size_min = 32
else:
    block_size = block_size_min = 64
if args.block_size:
    block_size = int(args.block_size)
if args.block_size_min:
    block_size_min = int(args.block_size_min)

parser.border_size(
if args.border_size:
    border_size = int(args.border_size)

parser.GOPs(GOPs)
if args.GOPs:
    GOPs = int(args.GOPs)

parser.pixels_in_x()
if args.pixels_in_x:
    pixels_in_x = int(args.pixels_in_x)

parser.pixels_in_y()
if args.pixels_in_y:
    pixels_in_y = int(args.pixels_in_y)

parser.search_range()
if args.search_range:
    search_range = int(args.search_range)

parser.subpixel_accuracy()
if args.subpixel_accuracy:
    subpixel_accuracy = int(args.subpixel_accuracy)

parser.TRLs()
if args.TRLs:
    TRLs = int(args.TRLs)

parser.update_factor()
if args.update_factor:
    update_factor = float(args.update_factor)

## Initializes the class GOP (Group Of Pictures).
gop=GOP()
## Extract the value of the size of a GOP, that is, the number of images.
GOP_size = gop.get_size(TRLs)
## Calculate the total number of video images.
pictures = GOPs * GOP_size + 1
## Initializes the value of search factor.
search_factor = 2
## Initializes the variable, temporal subband a '1'. Which refers to the first high-frequency subband. The goal is to apply the algorithm analysis to all high frequency subbands.
temporal_subband = 1

if block_size < block_size_min:
    block_size_min = block_size

while temporal_subband < TRLs:

    try:
        check_call("mctf analyze_step"
                   + " --GOPs="              + str(GOPs)
                   + " --TRLs="              + str(TRLs)
                   + " --always_B="          + str(always_B)
                   + " --block_overlaping="  + str(block_overlaping)
                   + " --block_size="        + str(block_size)
                   + " --border_size="       + str(border_size)
                   + " --pictures="          + str(pictures)
                   + " --pixels_in_x="       + str(pixels_in_x)
                   + " --pixels_in_y="       + str(pixels_in_y)
                   + " --search_range="      + str(search_range)
                   + " --subpixel_accuracy=" + str(subpixel_accuracy)
                   + " --temporal_subband="  + str(temporal_subband)
                   + " --update_factor="     + str(update_factor)
                   , shell=True)
    except CalledProcessError:
        sys.exit(-1)

    pictures = (pictures + 1) / 2

    search_range = search_range * search_factor
    if ( search_range > SEARCH_RANGE_MAX ):
        sys.stdout.write(sys.argv[0] + ": " + str(SEARCH_RANGE_MAX) + " reached!\n")
        search_range = SEARCH_RANGE_MAX

    block_size = block_size / 2
    if ( block_size < block_size_min ):
        block_size = block_size_min

    temporal_subband += 1

