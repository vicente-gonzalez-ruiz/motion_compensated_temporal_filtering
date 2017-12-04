çççç#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

#  Compresses data movement.
#
#  Motion fields are compressed without loss, generating a separate
#  file for each level of temporal resolution and a different stream
#  for each GOP. Compression is done thinking about how the
#  decompressor will perform decompression.
#
#  Removed: the temporal redundancy between bands and bidirectional
#  redundancy.\n
#  - The first states that, if the sub-band "i+1" one component of a
#  vector vale "2x" in the sub-band "i" that component of the vector
#  should be worth "x".  
#  - The second is that, if a component back better "-x", the 
#  corresponding component forward should be worth "x".
#
#  Finally a reversible entropy coder that compresses the wastes used.

import os
import sys
from GOP import GOP
from subprocess import check_call
from subprocess import CalledProcessError
from MCTF_parser import MCTF_parser

#MOTION_CODER_NAME = "gzip"
#MOTION_CODER_NAME = "kdu_v_compress"
MCTF_MOTION_CODEC  = os.environ["MCTF_MOTION_CODEC"]

## Size of the blocks in the motion estimation process.
block_size     = 32
## Minimal block size allowed in the motion estimation process.
block_size_min = 32
## Number of Group Of Pictures to process.
GOPs           = 1
## Number of Temporal Resolution Levels.
TRLs           = 4
## Controls the quality level and the bit-rate of the code-stream.
quantization   = 45000 # Jse
## Number of layers. Logarithm controls the quality level and the bit-rate of the code-stream.
clayers        = "1"

## The parser module provides an interface to Python's internal parser
## and byte-code compiler.
parser = MCTF_parser(description="Compress the motion data.")
parser.TRLs(TRLs)
parser.quantization(quantization)

args = parser.parse_known_args()[0]

parser.pixels_in_x()
if args.pixels_in_x:
    pixels_in_x = int(args.pixels_in_x)

parser.pixels_in_y()
if args.pixels_in_y:
    pixels_in_y = int(args.pixels_in_y)

parser.block_size()
parser.block_size_min()
if pixels_in_x * pixels_in_y < resolution_FHD:
    block_size = block_size_min = 32
else:
    block_size = block_size_min = 64

if args.block_size:
    block_size = int(args.block_size)
if args.block_size_min:
    block_size_min = int(args.block_size_min)

parser.GOPs()
if args.GOPs:
    GOPs = int(args.GOPs)

parser.clayers(clayers)
if args.clayers:
    clayers = str(args.clayers) # 'int' to 'str'
if args.quantization:
    quantization = str(args.quantization) # 'int' to 'str'
if args.TRLs:
    TRLs = int(args.TRLs)


if block_size < block_size_min:
    block_size_min = block_size


## Initializes the class GOP (Group Of Pictures).
gop=GOP()
## Extract the value of the size of a GOP, that is, the number of images.
GOP_size = gop.get_size(TRLs)
## Number of images to process.
pictures = GOPs * GOP_size + 1
## Total number of temporary iterations.
iterations  = TRLs - 1
## Current temporal iteration.
iteration   = 1
## Number of pictures of a temporal resolution.
fields      = pictures / 2
## Number of blocks in the Y direction.
blocks_in_y = pixels_in_y / block_size
## Number of blocks in the X direction.
blocks_in_x = pixels_in_x / block_size




while iteration < iterations:

    # Unmapped fields of movement between levels of resolution.
    #----------------------------------------------------------
    try:
        check_call("mctf interlevel_motion_decorrelate"
                   + " --blocks_in_x="         + str(blocks_in_x)
                   + " --blocks_in_y="         + str(blocks_in_y)
                   + " --fields_in_predicted=" + str(fields)
                   + " --predicted="           + "motion_filtered_" + str(iteration)
                   + " --reference="           + "motion_filtered_" + str(iteration + 1)
                   + " --residue="             + "motion_residue_"  + str(iteration)
                   , shell=True)
    except CalledProcessError:
        sys.exit(-1)

    # Calculate the block size used in this temporal iteration.
    #----------------------------------------------------------
    block_size = block_size / 2
    if (block_size < block_size_min):
        block_size = block_size_min

        fields /= 2
        iteration += 1
        blocks_in_y = pixels_in_y / block_size
        blocks_in_x = pixels_in_x / block_size


# Bidirectionally unmapped level lower temporal resolution. The last
# number of blocks in X and Y calculated in the previous loop is
# used. The same applies to the variable "iteration".
#-------------------------------------------------------------------
try:
    check_call("mctf bidirectional_motion_decorrelate"
               + " --blocks_in_x=" + str(blocks_in_x)
               + " --blocks_in_y=" + str(blocks_in_y)
               + " --fields="      + str(fields)
               + " --input="       + "motion_filtered_" + str(iteration)
               + " --output="      + "motion_residue_"  + str(iteration)
               , shell=True)
except CalledProcessError:
    sys.exit(-1)


# Deleted from the motion flow fields, fields that are no longer used,
# because they refer to images I.


# Compress.
#----------
iteration = 1
fields = pictures / 2
while iteration <= iterations:

    try:
        check_call("mctf motion_compress_" + MCTF_MOTION_CODEC
                   + " --blocks_in_x="     + str(blocks_in_x)
                   + " --blocks_in_y="     + str(blocks_in_y)
                   + " --iteration="       + str(iteration)
                   + " --fields="          + str(fields)
                   + " --quantization=\""  + str(quantization) + "\""
                   + " --clayers=\""       + str(clayers)      + "\""
                   + " --file="            + "motion_residue_" + str(iteration)
                   , shell=True)
    except CalledProcessError:
        sys.exit(-1)

    fields /= 2

    iteration += 1
