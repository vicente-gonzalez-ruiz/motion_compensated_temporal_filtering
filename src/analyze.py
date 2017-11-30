#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# The MCTF project has been supported by the Junta de Andalucía through
# the Proyecto Motriz "Codificación de Vídeo Escalable y su Streaming
# sobre Internet" (P10-TIC-6548).

## @file analyze.py
#  Performs the temporal analysis of a picture sequence.
#
#  Apply the temporal transform and generates a series of files that will later be encoded.
#  @author Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package analyze
#  Performs the temporal analysis of a picture sequence.
#
#  Apply the temporal transform and generates a series of files that will later be encoded.


import os
import sys
from GOP import GOP
from subprocess import check_call
from subprocess import CalledProcessError
from MCTF_parser import MCTF_parser

## Maximum search range.
SEARCH_RANGE_MAX  = 128
## Sets a spatial resolution. Here Full-HD.
resolution_FHD    = 1920*1080
## X dimension of a picture.
pixels_in_x       = 352
## Y dimension of a picture.
pixels_in_y       = 288
## Requires that all generated images are of type 'B'.
always_B          = 0
## Number of pixels of overlap between blocks.
block_overlaping  = 0
## Size of a block.
block_size        = 32
## Minimum size of a block.
block_size_min    = 32
## Border size or margin of a block.
border_size       = 0
## Number of Groups Of Pictures of the scene.
GOPs              = 1
## Search range for motion vectors.
search_range      = 4
## Sub-pixel accuracy in motion estimate.
subpixel_accuracy = 0
## Number of Temporal resolution Levels.
TRLs              = 4
## Level update. For example, a value equal to 1/4 means that the high-frequency subband is 4 times less important than the low-frequency subband.
update_factor     = 0 # 1.0/4

## The parser module provides an interface to Python's internal parser and byte-code compiler.
parser = MCTF_parser(description="Performs the temporal analysis of a picture sequence.")
parser.pixels_in_x(pixels_in_x)
parser.pixels_in_y(pixels_in_y)
parser.always_B(always_B)
parser.block_overlaping(block_overlaping)
parser.block_size(block_size)
parser.block_size_min(block_size_min)
parser.border_size(border_size)
parser.GOPs(GOPs)
parser.search_range(search_range)
parser.subpixel_accuracy(subpixel_accuracy)
parser.TRLs(TRLs)
parser.update_factor(update_factor)

## A script may only parse a few of the command-line arguments, passing the remaining arguments on to another script or program.
args = parser.parse_known_args()[0]
if args.always_B:
    always_B = int(args.always_B)
if args.block_overlaping:
    block_overlaping = int(args.block_overlaping)

# Default block_size según pixels_in_xy
if pixels_in_x * pixels_in_y < resolution_FHD:
    block_size = block_size_min = 32
else:
    block_size = block_size_min = 64

if args.block_size:
    block_size = int(args.block_size)
if args.block_size_min:
    block_size_min = int(args.block_size_min)

if args.border_size:
    border_size = int(args.border_size)
if args.GOPs:
    GOPs = int(args.GOPs)
if args.pixels_in_x:
    pixels_in_x = int(args.pixels_in_x)
if args.pixels_in_y:
    pixels_in_y = int(args.pixels_in_y)
if args.search_range:
    search_range = int(args.search_range)
if args.subpixel_accuracy:
    subpixel_accuracy = int(args.subpixel_accuracy)
if args.TRLs:
    TRLs = int(args.TRLs)
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

