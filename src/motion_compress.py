#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

#
#  Compresses motion data.
#

import os
import sys
from GOP import GOP
from shell import Shell as shell
from colorlog import ColorLog
import logging

log = ColorLog(logging.getLogger("motion_compress"))
log.setLevel('INFO')
shell.setLogger(log)

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
pictures = (GOPs - 1) * GOP_size + 1
fields = pictures // 2
blocks_in_y = pixels_in_y // block_size
blocks_in_x = pixels_in_x // block_size

# {{{ Decorrelate

iter = 1
while iter < TRLs:

    if fields > 1:
        # Remove motion redundancy between temporal levels (iter) and (iter+1).
        shell.run("mctf interlevel_motion_decorrelate"
                  + " --blocks_in_x=" + str(blocks_in_x)
                  + " --blocks_in_y="  + str(blocks_in_y)
                  + " --fields_in_predicted=" + str(fields)
                  + " --predicted=" + "motion_filtered_" + str(iter)
                  + " --reference=" + "motion_filtered_" + str(iter + 1)
                  + " --residue=" + "motion_residue_tmp_"  + str(iter))
    else:
        shell.run("trace cp -r motion_filtered_" + str(iter) + " motion_residue_tmp_" + str(iter))

    # Remove motion redundancy inside the temporal level (iter).
    shell.run("mctf bidirectional_motion_decorrelate"
              + " --blocks_in_x=" + str(blocks_in_x)
              + " --blocks_in_y=" + str(blocks_in_y)
              + " --fields=" + str(fields)
              + " --input=" + "motion_residue_tmp_" + str(iter)
              + " --output=" + "motion_residue_"  + str(iter))

    # Calculate the block size used in this temporal resolution level.
    block_size = block_size // 2
    if (block_size < min_block_size):
        block_size = min_block_size
    else:
        blocks_in_y = pixels_in_y // block_size
        blocks_in_x = pixels_in_x // block_size

    fields //= 2
    iter += 1

# }}}

# {{{ Compress

#slopes = []
#for i in range(layers):
#    slopes.append(quantization + i * quantization_step)

#if len(slopes) == 1:
#    str_slopes = str(slopes[0])
#else:
#    str_slopes = ', '.join(str(i) for i in slopes)
    
#import ipdb; ipdb.set_trace()

if TRLs==2:
    shell.run("ln -s motion_filtered_1 motion_residue_1")

iter = 1
fields = pictures // 2
while iter < TRLs:

    shell.run("mctf subband_motion_compress__" + MCTF_MOTION_CODEC
              + " --blocks_in_x=" + str(blocks_in_x)
              + " --blocks_in_y=" + str(blocks_in_y)
              + " --iteration=" + str(iter)
              + " --fields=" + str(fields)
              + " --file="  + "motion_residue_" + str(iter))

    fields //= 2
    iter += 1

# }}}
