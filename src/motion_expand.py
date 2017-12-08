#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#  Decompresses data movement.
#
#  The decompressor will find on the first level, a field of
#  bidirectional movement has been solely uncorrelated bidirectionally
#  (bidirectional decorrelation exploits the redundancy that exists in
#  a bidirectional vector, where the vector in a direction generally
#  like the other, although with opposite sign).
#
#  Once the field in the first level has been restored, it can serve
#  as a reference for two fields next level of resolution (interlevel
#  decorrelation). Specifically, divide by two, the motion vectors and
#  we have a prediction.
#
#  In this second level of resolution (and the following) is not
#  necessary decorrelate bidirectionally. Because the interlevel
#  decorrelation, bidirectional starts from correlated fields, and
#  this will cause bidirectional decorrelation automatically.
#

import os
import sys
from GOP import GOP
from subprocess import check_call
from subprocess import CalledProcessError
from arguments_parser import arguments_parser

#MOTION_DECODER_NAME = "gzip"
#MOTION_DECODER_NAME = "kdu_v_expand"
## Refers to the codec to be used for compression of motion information.
MCTF_MOTION_CODEC    = os.environ["MCTF_MOTION_CODEC"]
## Number of Group Of Pictures to process.
GOPs        = 1
## Number of Temporal Resolution Levels.
TRLs        = 4
## Size of the blocks in the motion estimation process.
block_size  = "16,16,16,16"
## Width of the pictures.
pixels_in_x = "352,352,352,352,352"
## Height of the pictures.
pixels_in_y = "288,288,288,288,288"


## The parser module provides an interface to Python's internal parser
## and byte-code compiler.
parser = arguments_parser(description="Expands the motion data.")
parser.GOPs()
parser.TRLs()
parser.block_size()
parser.pixels_in_x()
parser.pixels_in_y()

## A script may only parse a few of the command-line arguments,
## passing the remaining arguments on to another script or program.
args = parser.parse_known_args()[0]
if args.GOPs:
    GOPs = int(args.GOPs)
if args.TRLs:
    TRLs = int(args.TRLs)
if args.block_size:
    block_size = str(args.block_size)
if args.pixels_in_x:
    pixels_in_x = str(args.pixels_in_x)
if args.pixels_in_y:
    pixels_in_y = str(args.pixels_in_y)


## Size of the blocks in the motion estimation process, represented as a list.
_block_size  = map(int, block_size.split(','))
## Width of the pictures, represented as a list.
_pixels_in_x = map(int, pixels_in_x.split(','))
## Height of the pictures, represented as a list.
_pixels_in_y = map(int, pixels_in_y.split(','))
## Number of blocks in the X direction, represented as a list.
_blocks_in_x = []
## Number of blocks in the Y direction, represented as a list.
_blocks_in_y = []

## Initializes the class GOP (Group Of Pictures).
gop=GOP()
## Extract the value of the size of a GOP, that is, the number of images.
GOP_size = gop.get_size(TRLs)
## Number of images to process.
pictures = GOPs * GOP_size + 1



# Calculate the number of blocks.
#--------------------------------
for z in range (0, TRLs - 1) :
    _blocks_in_x.append( _pixels_in_x[z+1] / _block_size[z] )
    _blocks_in_y.append( _pixels_in_y[z+1] / _block_size[z] )



# Decompression motion fields.
#-----------------------------

## Current temporal iteration.
iteration = 1
## Number of pictures of a temporal resolution.
fields = pictures / 2
while iteration <= (TRLs - 1) :

    try:
        check_call("mctf motion_expand_" + MCTF_MOTION_CODEC
                   + " --file=" + "\""   + "motion_residue_" + str(iteration) + "\""
                   + " --blocks_in_y="   + str(_blocks_in_y[(TRLs-1)-iteration])
                   + " --blocks_in_x="   + str(_blocks_in_x[(TRLs-1)-iteration])
                   + " --fields="        + str(fields)
                   + " --pictures="      + str(pictures)
                   ,shell=True)
    except CalledProcessError :
        sys.exit(-1)

    fields /= 2
    iteration += 1
    
# Decorrelation bidirectional level lower temporal resolution.
#-------------------------------------------------------------
try:
    check_call("mctf bidirectional_motion_correlate"
               + " --blocks_in_y=" + str(_blocks_in_y[len(_blocks_in_y)-1])
               + " --blocks_in_x=" + str(_blocks_in_x[len(_blocks_in_x)-1])
               + " --fields="      + str(GOPs)
               + " --input="       + "\"" + "motion_residue_" + str(TRLs - 1) + "\""
               + " --output="      + "\"" + "motion_"         + str(TRLs - 1) + "\""
               , shell=True)
except CalledProcessError :
    sys.exit(-1)

# Decorrelation between levels of resolution.
#--------------------------------------------
iteration = TRLs - 1 # total iterations
while iteration > 1 :
    
    iteration -= 1
    fields = pictures / (2**iteration)

    try:
        check_call("mctf interlevel_motion_correlate"
                   + " --blocks_in_y="         + str(_blocks_in_y[iteration-1])
                   + " --blocks_in_x="         + str(_blocks_in_x[iteration-1])
                   + " --fields_in_predicted=" + str(fields)
                   + " --reference="           + "\"" + "motion_"         + str(iteration + 1) + "\""
                   + " --predicted="           + "\"" + "motion_"         + str(iteration)     + "\""
                   + " --residue="             + "\"" + "motion_residue_" + str(iteration)     + "\""
                   , shell=True)
    except CalledProcessError :
        sys.exit(-1)
