#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

## @file synthesize.py
#  Undo the temporal transformation (Temporal inverse transform).
#  @authors Jose Carmelo Maturana-Espinosa\n Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package synthesize
#  Undo the temporal transformation (Temporal inverse transform).

import os
import sys
from GOP import GOP
from subprocess import check_call
from subprocess import CalledProcessError
import arguments_parser

## Maximum search range.
SEARCH_RANGE_MAX = 128
## Number of Group Of Pictures to process.
GOPs              = 1
## Number of Temporal Resolution Levels.
TRLs              = 4
## Size of the blocks in the motion estimation process. There the
## possibility of changing the spatial resolution of each level of
## temporal resolution, therefore, a value indicated for each TRL.
block_size        = "16,16,16,16"
## Width of the pictures.
pixels_in_x       = "352,352,352,352,352"
## Height of the pictures.
pixels_in_y       = "288,288,288,288,288"
## Subpixel motion estimation order.
subpixel_accuracy = "0,0,0,0"
## Size of the border of the blocks in the motion estimation process.
border_size       = 0
## Number of overlaped pixels between the blocks in the motion
## compensation process.
block_overlaping  = 0
## Size of the search areas in the motion estimation process.
search_range      = 4
## Weight of the update step.
update_factor     = 1.0/4
## Size of the search areas in the motion estimation process.
search_factor     = 2


## The parser module provides an interface to Python's internal parser
## and byte-code compiler.
parser = arguments_parser(description="Performs the temporal synthesis of a picture sequence.")
parser.GOPs()
parser.TRLs()
parser.block_size()
parser.pixels_in_x()
parser.pixels_in_y()
parser.subpixel_accuracy()
parser.border_size()
parser.block_overlaping()
parser.search_range()
parser.update_factor()

## A script may only parse a few of the command-line arguments,
## passing the remaining arguments on to another script or program.
args = parser.parse_known_args()[0]
if args.TRLs:
    TRLs = int(args.TRLs)
if args.GOPs:
    GOPs = int(args.GOPs)
if args.block_size:
    block_size = str(args.block_size)
if args.pixels_in_x:
    pixels_in_x = str(args.pixels_in_x)
if args.pixels_in_y:
    pixels_in_y = str(args.pixels_in_y)
if args.subpixel_accuracy:
    subpixel_accuracy = str(args.subpixel_accuracy)
if args.border_size:
    border_size = int(args.border_size)
if args.block_overlaping:
    block_overlaping = int(args.block_overlaping)
if args.search_range:
    search_range = int(args.search_range)
if args.update_factor:
    update_factor = float(args.update_factor)


#block_overlaping >>= int(number_of_discarded_spatial_levels)
#max_block_size >>= int(number_of_discarded_spatial_levels)
#min_block_size >>= int(number_of_discarded_spatial_levels)
#pixels_in_x >>= int(number_of_discarded_spatial_levels)
#pixels_in_y >>= int(number_of_discarded_spatial_levels)
#interpolation_factor += int(number_of_discarded_spatial_levels)
#interpolation_factor -= int(number_of_discarded_spatial_levels)

## Initializes the class GOP (Group Of Pictures).
gop = GOP()
## Extract the value of the size of a GOP, that is, the number of
## images.
GOP_size = gop.get_size(TRLs)
## Calculate the total number of video images.
pictures = GOPs * GOP_size + 1
## Initializes a auxiliar value of search factor.
_search_range = search_range
## Initializes a auxiliar value of pictures.
_pictures = pictures


if TRLs > 1 :

    ## Initializes the variable, temporal subband a '1'. Which refers
    ## to the first high-frequency subband. The goal is to apply the
    ## algorithm analysis to all high frequency subbands.
    temporal_subband = 1
    while temporal_subband < (TRLs - 1) :

        search_range = search_range * search_factor
        if search_range > SEARCH_RANGE_MAX :
            search_range = SEARCH_RANGE_MAX

        pictures = (pictures + 1) / 2
        temporal_subband += 1


    while temporal_subband > 0 :
        try :
            check_call("mctf synthesize_step"
                       + " --block_overlaping="  + str(block_overlaping)
                       + " --block_size="        + str(block_size.split(',')[(TRLs-1)-temporal_subband])
                       + " --pictures="          + str(pictures)
                       + " --pixels_in_x="       + str(pixels_in_x.split(',')[TRLs-temporal_subband])
                       + " --pixels_in_y="       + str(pixels_in_y.split(',')[TRLs-temporal_subband])
                       + " --search_range="      + str(search_range)
                       + " --subpixel_accuracy=" + str(subpixel_accuracy.split(',')[TRLs-temporal_subband])
                       + " --temporal_subband="  + str(temporal_subband)
                       + " --update_factor="     + str(update_factor)
                       , shell=True)
        except CalledProcessError :
            sys.exit(-1)

        pictures = _pictures
        search_range = _search_range
        temporal_subband -= 1

        ## Initializes the variable, temporal subband a '1'.
        j = 1
        while j < temporal_subband :

            search_range = search_range * search_factor
            if search_range > SEARCH_RANGE_MAX :
                search_range = SEARCH_RANGE_MAX

            pictures = ( pictures + 1 ) / 2
            j += 1
