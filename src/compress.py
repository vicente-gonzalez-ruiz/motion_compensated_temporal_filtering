#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# Compression of a sequence of images.

# {{{ Importing

import sys
import os
from GOP import GOP
from shell import Shell as shell

# }}}

# {{{ Logging

import logging

logging.basicConfig()
log = logging.getLogger("compress")
log.setLevel('INFO')

# }}}

# {{{ Arguments parsing

from arguments_parser import arguments_parser

parser = arguments_parser(description="Encodes a sequence of imagesy into a MCJ2K stream")
parser.always_B()
parser.block_overlaping()
parser.block_size()
parser.border_size()
parser.GOPs()
parser.min_block_size()
#parser.motion_layers()
#parser.motion_quantization()
#parser.motion_quantization_step()
parser.pixels_in_x()
parser.pixels_in_y()
parser.search_range()
parser.subpixel_accuracy()
parser.layers()
parser.SRLs()
parser.TRLs()
parser.update_factor()

args = parser.parse_known_args()[0]
always_B = int(args.always_B)
block_overlaping = int(args.block_overlaping)
block_size = int(args.block_size)
min_block_size = int(args.min_block_size)
border_size = int(args.border_size)
GOPs = int(args.GOPs)
#motion_layers = str(args.motion_layers); log.debug("motion_layers={}".format(motion_layers))
#motion_quantization = str(args.motion_quantization); log.debug("motion_quantization={}".format(motion_quantization))
#motion_quantization_step = str(args.motion_quantization_step); log.debug("motion_quantization_step={}".format(motion_quantization_step))
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
layers = str(args.layers)
search_range = int(args.search_range)
subpixel_accuracy = int(args.subpixel_accuracy)
TRLs = int(args.TRLs)
SRLs = int(args.SRLs)
update_factor = float(args.update_factor)

# }}}

MCTF_QUANTIZER       = os.environ["MCTF_QUANTIZER"]

if TRLs > 1:
    # {{{ Temporal analysis of image sequence. Temporal decorrelation.
    shell.run("mctf analyze"
              + " --always_B="          + str(always_B)
              + " --block_overlaping="  + str(block_overlaping)
              + " --block_size="        + str(block_size)
              + " --min_block_size="    + str(min_block_size)
              + " --border_size="       + str(border_size)
              + " --GOPs="              + str(GOPs)
              + " --pixels_in_x="       + str(pixels_in_x)
              + " --pixels_in_y="       + str(pixels_in_y)
              + " --search_range="      + str(search_range)
              + " --subpixel_accuracy=" + str(subpixel_accuracy)
              + " --TRLs="              + str(TRLs)
              + " --update_factor="     + str(update_factor))
    # }}}
    # {{{ Motion data compression.
    shell.run("mctf motion_compress"
              + " --block_size="               + str(block_size)
              + " --GOPs="                     + str(GOPs)
              + " --min_block_size="           + str(min_block_size)
              + " --pixels_in_x="              + str(pixels_in_x)
              + " --pixels_in_y="              + str(pixels_in_y)
              #                   + " --motion_layers="            + str(motion_layers)
              #                   + " --motion_quantization="      + str(motion_quantization)
              #                   + " --motion_quantization_step=" + str(motion_quantization_step)
              + " --SRLs="                     + str(SRLs)
              + " --TRLs="                     + str(TRLs)
    # }}}
    
# {{{ Texture compression.
shell.run("mctf texture_compress__"         + MCTF_QUANTIZER
          + " --GOPs="                      + str(GOPs)
          + " --pixels_in_x="               + str(pixels_in_x)
          + " --pixels_in_y="               + str(pixels_in_y)
          + " --SRLs="                      + str(SRLs)
          + " --layers="                    + str(layers)
          + " --TRLs="                      + str(TRLs))
# }}}
