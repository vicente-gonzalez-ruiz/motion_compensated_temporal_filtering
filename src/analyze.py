#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# Performs the temporal analysis of a picture sequence. Generates a
# series of files that will later be encoded.

import os
import sys
from GOP import GOP
from arguments_parser import arguments_parser
from shell import Shell as shell
from colorlog import ColorLog
import logging

log = ColorLog(logging.getLogger("analyze"))
log.setLevel('INFO')
shell.setLogger(log)

MAX_SEARCH_RANGE = 128

parser = arguments_parser(description="Temporal analysis of a picture sequence.")
parser.always_B()
parser.block_overlaping()
parser.block_size()
parser.min_block_size()
parser.border_size()
parser.GOPs()
parser.pixels_in_x()
parser.pixels_in_y()
parser.search_range()
parser.subpixel_accuracy()
parser.TRLs()
parser.update_factor()

args = parser.parse_known_args()[0]
always_B = int(args.always_B)
block_overlaping = int(args.block_overlaping)
block_size = int(args.block_size)
min_block_size = int(args.min_block_size)
border_size = int(args.border_size)
GOPs = int(args.GOPs)
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
search_range = int(args.search_range)
subpixel_accuracy = int(args.subpixel_accuracy)
TRLs = int(args.TRLs)
update_factor = float(args.update_factor)

## Initializes the class GOP (Group Of Pictures).
gop=GOP()

## Extract the value of the size of a GOP, that is, the number of pictures.
GOP_size = gop.get_size(TRLs)

## Calculate the total number of video pictures.
pictures = (GOPs - 1) * GOP_size + 1

#import ipdb; ipdb.set_trace()

## Initializes the value of search factor.
search_factor = 2

## Initializes the variable, temporal subband a '1'. Which refers to
#  the first high-frequency subband. The goal is to apply the
#  algorithm analysis to all high frequency subbands.
temporal_subband = 0

if block_size < min_block_size:
    min_block_size = block_size

while temporal_subband < TRLs:

    shell.run("mctf analyze_step"
              + " --always_B=" + str(always_B)
              + " --block_overlaping=" + str(block_overlaping)
              + " --block_size=" + str(block_size)
              + " --border_size=" + str(border_size)
              + " --pictures="  + str(pictures)
              + " --pixels_in_x=" + str(pixels_in_x)
              + " --pixels_in_y=" + str(pixels_in_y)
              + " --search_range=" + str(search_range)
              + " --subpixel_accuracy=" + str(subpixel_accuracy)
              + " --temporal_subband=" + str(temporal_subband+1)
              + " --update_factor=" + str(update_factor))

    pictures = (pictures + 1) // 2

    search_range = search_range * search_factor
    if search_range > MAX_SEARCH_RANGE:
        log.info("Maximum search range ({}) reached!".format(MAX_SEARCH_RANGE))
        search_range = MAX_SEARCH_RANGE

    block_size = block_size // 2
    if ( block_size < min_block_size ):
        block_size = min_block_size

    temporal_subband += 1
