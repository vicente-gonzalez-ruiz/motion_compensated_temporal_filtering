#!/usr/bin/python
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
import arguments_parser

#MOTION_CODER_NAME = "gzip"
#MOTION_CODER_NAME = "kdu_v_compress"
MCTF_MOTION_CODEC  = os.environ["MCTF_MOTION_CODEC"]

parser = arguments_parser(description="Compress the motion data.")

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
if block_size < block_size_min:
    block_size_min = block_size
if args.block_size_min:
    block_size_min = int(args.block_size_min)

parser.GOPs()
if args.GOPs:
    GOPs = int(args.GOPs)

parser.motion_layers()
if args.motion_layers:
    layers = str(args.motion_layers)

parser.motion_quantization()
if args.motion_quantization:
    quantization = str(args.motion_quantization)

parser.TRLs()
if args.TRLs:
    TRLs = int(args.TRLs)

gop=GOP()
GOP_size = gop.get_size(TRLs)
pictures = GOPs * GOP_size + 1
## Number of pictures of a temporal resolution.
fields      = pictures / 2
iterations  = TRLs - 1
## Number of blocks in the Y direction.
blocks_in_y = pixels_in_y / block_size
## Number of blocks in the X direction.
blocks_in_x = pixels_in_x / block_size

iter   = 1

while iter < iterations:

    # Unmapped fields of movement between levels of resolution.
    try:
        check_call("mctf interlevel_motion_decorrelate"
                   + " --blocks_in_x="         + str(blocks_in_x)
                   + " --blocks_in_y="         + str(blocks_in_y)
                   + " --fields_in_predicted=" + str(fields)
                   + " --predicted="           + "motion_filtered_" + str(iter)
                   + " --reference="           + "motion_filtered_" + str(iter + 1)
                   + " --residue="             + "motion_residue_"  + str(iter)
                   , shell=True)
    except CalledProcessError:
        sys.exit(-1)

    # Calculate the block size used in this temporal iteration.
    block_size = block_size / 2
    if (block_size < block_size_min):
        block_size = block_size_min

        fields /= 2
        iter += 1
        blocks_in_y = pixels_in_y / block_size
        blocks_in_x = pixels_in_x / block_size


# Bidirectionally unmapped level lower temporal resolution. The last
# number of blocks in X and Y calculated in the previous loop is
# used. The same applies to the variable "iter".
try:
    check_call("mctf bidirectional_motion_decorrelate"
               + " --blocks_in_x=" + str(blocks_in_x)
               + " --blocks_in_y=" + str(blocks_in_y)
               + " --fields="      + str(fields)
               + " --input="       + "motion_filtered_" + str(iter)
               + " --output="      + "motion_residue_"  + str(iter)
               , shell=True)
except CalledProcessError:
    sys.exit(-1)

# Compress.
iter = 1
fields = pictures / 2
while iter <= iterations:

    try:
        check_call("mctf motion_compress_" + MCTF_MOTION_CODEC
                   + " --blocks_in_x="     + str(blocks_in_x)
                   + " --blocks_in_y="     + str(blocks_in_y)
                   + " --iteration="       + str(iter)
                   + " --fields="          + str(fields)
                   + " --quantization=\""  + str(quantization) + "\""
                   + " --layers=\""        + str(layers)       + "\""
                   + " --file="            + "motion_residue_" + str(iter)
                   , shell=True)
    except CalledProcessError:
        sys.exit(-1)

    fields /= 2

    iter += 1
