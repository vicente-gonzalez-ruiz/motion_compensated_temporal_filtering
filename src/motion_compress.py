#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

#
#  Compresses motion data.
#

import os
import sys
from GOP import GOP
from subprocess import check_call
from subprocess import CalledProcessError

# {{{ Logging 

import logging

logging.basicConfig()
log = logging.getLogger("motion_compress")
log.setLevel('INFO')

# }}}

MCTF_MOTION_CODEC  = os.environ["MCTF_MOTION_CODEC"]

# {{{ Arguments parsing

from arguments_parser import arguments_parser

parser = arguments_parser(description="Compress the motion data.")
parser.pixels_in_x()
parser.pixels_in_y()
parser.block_size()
parser.min_block_size()
parser.GOPs()
#parser.motion_layers()
#parser.motion_quantization()
#parser.motion_quantization_step()
parser.TRLs()

args = parser.parse_known_args()[0]
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
block_size = int(args.block_size)
min_block_size = int(args.min_block_size)
GOPs = int(args.GOPs)
#layers = int(args.motion_layers); log.debug("layers={}".format(layers))
#quantization = int(args.motion_quantization); log.debug("quantization={}".format(quantization))
#quantization_step = int(args.motion_quantization_step); log.debug("quantization_step={}".format(quantization_step))
TRLs = int(args.TRLs)

# }}}

gop=GOP()
GOP_size = gop.get_size(TRLs)
images = (GOPs - 1) * GOP_size + 1
fields = images // 2
blocks_in_y = pixels_in_y // block_size
blocks_in_x = pixels_in_x // block_size

iter = 1
while iter < TRLs - 1:

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

    # Calculate the block size used in this temporal resolution level.
    block_size = block_size // 2
    if (block_size < min_block_size):
        
        block_size = min_block_size
        fields //= 2
        iter += 1
        blocks_in_y = pixels_in_y // block_size
        blocks_in_x = pixels_in_x // block_size

## Bidirectionally unmapped level lower temporal resolution. The last
#  number of blocks in X and Y calculated in the previous loop is
#  used. The same applies to the variable "iter".
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

#slopes = []
#for i in range(layers):
#    slopes.append(quantization + i * quantization_step)

#if len(slopes) == 1:
#    str_slopes = str(slopes[0])
#else:
#    str_slopes = ', '.join(str(i) for i in slopes)
    
#import ipdb; ipdb.set_trace()

iter = 1
fields = images // 2
while iter <= TRLs - 1:

    try:
        check_call("mctf subband_motion_compress__" + MCTF_MOTION_CODEC
                   + " --blocks_in_x="      + str(blocks_in_x)
                   + " --blocks_in_y="      + str(blocks_in_y)
                   + " --iteration="        + str(iter)
                   + " --fields="           + str(fields)
                   + " --file="             + "motion_residue_" + str(iter)
                   + " --slopes=\""         + str_slopes + "\""
                   , shell=True)
    except CalledProcessError:
        sys.exit(-1)

    fields //= 2

    iter += 1
