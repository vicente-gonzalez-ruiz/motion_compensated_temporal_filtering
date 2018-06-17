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
log.setLevel('ERROR')
shell.setLogger(log)

# {{{ Logging 

import logging

logging.basicConfig()
log = logging.getLogger("motion_compress")
log.setLevel('ERROR')

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
fields_in_reference = pictures // 4 # First reference is M_2
blocks_in_y = pixels_in_y // block_size
blocks_in_x = pixels_in_x // block_size

# {{{ Decorrelate betweem temporal levels, starting at the bottom level

#if fields_in_reference > 0:
reference_level = 2
while reference_level < TRLs:
    shell.run("trace mkdir R_" + str(reference_level - 1))
    shell.run("mctf interlevel_motion_decorrelate"
              + " --blocks_in_x=" + str(blocks_in_x)
              + " --blocks_in_y=" + str(blocks_in_y)
              + " --fields_in_reference=" + str(fields_in_reference)
              + " --predicted=" + "M_" + str(reference_level - 1)
              + " --reference=" + "M_" + str(reference_level)
              + " --residue=" + "R_" + str(reference_level - 1))
#    else:
#        shell.run("trace cp -r motion_" + str(iter) + " motion_residue_tmp_" + str(iter))

    # Calculate the block size used in this temporal resolution level.
    #block_size = block_size // 2
    #if (block_size < min_block_size):
    #    block_size = min_block_size
    #else:
    #    blocks_in_y = pixels_in_y // block_size
    #    blocks_in_x = pixels_in_x // block_size

    fields_in_reference //= 2
    reference_level += 1

# {{{ Remove bidirectional motion redundancy inside the highest temporal level.
shell.run("trace mkdir R_" + str(TRLs - 1))
shell.run("mctf bidirectional_motion_decorrelate"
          + " --blocks_in_x=" + str(blocks_in_x)
          + " --blocks_in_y=" + str(blocks_in_y)
          + " --fields=" + str(GOPs - 1)
          + " --input=" + "M_" + str(TRLs - 1)
          + " --output=" + "R_"  + str(TRLs - 1))

# }}}

# }}}

# {{{ Compress

level = 1
fields = pictures // 2
while level < TRLs:

    shell.run("mctf subband_motion_compress__" + MCTF_MOTION_CODEC
              + " --blocks_in_x=" + str(blocks_in_x)
              + " --blocks_in_y=" + str(blocks_in_y)
              + " --fields=" + str(fields)
              + " --file=" + "R_" + str(level))

    fields //= 2
    level += 1

# }}}
