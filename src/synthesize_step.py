#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

## @file synthesize_step.py
#  Iterates temporal inverse transform.
#
#  @authors Jose Carmelo Maturana-Espinosa\n Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package synthesize_step
#  Iterates temporal inverse transform.


import os
import sys
from GOP import GOP
from subprocess import check_call
from subprocess import CalledProcessError
import arguments_parser

## Number of overlaped pixels between the blocks in the motion
## compensation process.
block_overlaping  = 0
## Size of the blocks in the motion estimation process.
block_size        = 16
## Number of images to process.
pictures          = 33
## Width of the pictures.
pixels_in_x       = 352
## Height of the pictures.
pixels_in_y       = 288
## Size of the search areas in the motion estimation process.
search_range      = 4
## Subpixel motion estimation order.
subpixel_accuracy = 0
## Number of subband. Refers to the interaction of the temporal
## transform.
temporal_subband  = 0
## Weight of the update step.
update_factor     = 1.0/4

## The parser module provides an interface to Python's internal parser
## and byte-code compiler.
parser = arguments_parser(description="Performs a step of the temporal synthesis.")
parser.block_overlaping()
parser.block_size()
parser.pictures()
parser.pixels_in_x()
parser.pixels_in_y()
parser.search_range()
parser.subpixel_accuracy()
parser.add_argument("--temporal_subband", help="iteration of the temporal transform. Default = {}".format(temporal_subband))
parser.update_factor()

## A script may only parse a few of the command-line arguments,
## passing the remaining arguments on to another script or program.
args = parser.parse_known_args()[0]
if args.block_overlaping:
    block_overlaping = int(args.block_overlaping)
if args.block_size:
    block_size = int(args.block_size)
if args.pictures:
    pictures = int(args.pictures)
if args.pixels_in_x:
    pixels_in_x = int(args.pixels_in_x)
if args.pixels_in_y:
    pixels_in_y = int(args.pixels_in_y)
if args.search_range:
    search_range = int(args.search_range)
if args.subpixel_accuracy:
    subpixel_accuracy = int(args.subpixel_accuracy)
if args.temporal_subband:
    temporal_subband = int(args.temporal_subband)
if args.update_factor:
    update_factor = float(args.update_factor)



# To monitor the execution:
# check_call("echo SYNTHETIZE_STEP:: Subband: " + str(temporal_subband), shell=True)
# check_call("echo UN_UPDATE:: Subband: "       + str(temporal_subband), shell=True)
# raw_input("")

try:
    check_call("mctf un_update"
               + " --block_size="        + str(block_size)
               + " --even_fn="           + "even_"        + str(temporal_subband)
               + " --frame_types_fn="    + "frame_types_" + str(temporal_subband)
               + " --high_fn="           + "high_"        + str(temporal_subband)
               + " --low_fn="            + "low_"         + str(temporal_subband)
               + " --motion_fn="         + "motion_"      + str(temporal_subband)
               + " --pictures="          + str(pictures)
               + " --pixels_in_x="       + str(pixels_in_x)
               + " --pixels_in_y="       + str(pixels_in_y)
               + " --subpixel_accuracy=" + str(subpixel_accuracy)
               + " --update_factor="     + str(update_factor)
               , shell=True)
except CalledProcessError:
            sys.exit(-1)



# To monitor the execution:
# check_call("echo end UN_UPDATE:: Subband: " + str(temporal_subband), shell=True)
# check_call("echo CORRELATE:: Subband: "     + str(temporal_subband), shell=True)
# raw_input("")

try:
    check_call("mctf correlate"
               + " --block_overlaping="  + str(block_overlaping)
               + " --block_size="        + str(block_size)
               + " --even_fn="           + "even_"        + str(temporal_subband)
               + " --frame_types_fn="    + "frame_types_" + str(temporal_subband)
               + " --high_fn="           + "high_"        + str(temporal_subband)
               + " --motion_in_fn="      + "motion_"      + str(temporal_subband)
               + " --odd_fn="            + "odd_"         + str(temporal_subband)
               + " --pictures="          + str(pictures)
               + " --pixels_in_x="       + str(pixels_in_x)
               + " --pixels_in_y="       + str(pixels_in_y)
               + " --search_range="      + str(search_range)
               + " --subpixel_accuracy=" + str(subpixel_accuracy)
               , shell=True)
except CalledProcessError:
            sys.exit(-1)



# To monitor the execution:
# check_call("echo end CORRELATE:: Subband: " + str(temporal_subband), shell=True)
# check_call("echo MERGE:: Subband: "         + str(temporal_subband), shell=True)
# raw_input("")

try:
    check_call("mctf merge"
               + " --even="        + "even_" + str(temporal_subband)
               + " --low="         + "low_"  + str(temporal_subband-1)
               + " --odd="         + "odd_"  + str(temporal_subband)
               + " --pictures="    + str(pictures)
               + " --pixels_in_x=" + str(pixels_in_x)
               + " --pixels_in_y=" + str(pixels_in_y)
               , shell=True)
except CalledProcessError:
            sys.exit(-1)
