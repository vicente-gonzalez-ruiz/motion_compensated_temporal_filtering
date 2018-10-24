#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# Texture compression. Kakadu decides the slopes, automatically.

# {{{ Imports

import os
import sys
import display
import math
from GOP import GOP
from arguments_parser import arguments_parser
import io
from shell import Shell as shell
from colorlog import ColorLog
import logging

log = ColorLog(logging.getLogger("texture_compress__automatic"))  # remove __automatic (some day)
log.setLevel('INFO')
shell.setLogger(log)

# }}}

# {{{ Logging

#logging.basicConfig()
#log = logging.getLogger("texture_compress__automatic")
#log.setLevel('INFO')

# }}}

# {{{ Arguments parsing

parser = arguments_parser(description="Compress a texture subband.")
parser.GOPs()
parser.layers()
parser.pixels_in_x()
parser.pixels_in_y()
parser.SRLs()
parser.TRLs()
parser.slope()

args = parser.parse_known_args()[0]
GOPs = int(args.GOPs)
layers = int(args.layers)
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
SRLs = int(args.SRLs)
TRLs = int(args.TRLs)
slope = int(args.slope)

log.info("GOPs={}".format(GOPs))
log.info("layers={}".format(layers))
log.info("pixels_in_x={}".format(pixels_in_x))
log.info("pixels_in_y={}".format(pixels_in_y))
log.info("SRLs={}".format(SRLs))
log.info("TRLs={}".format(TRLs))
log.info("(minimum) slope={}".format(slope))

# }}}

# {{{ Some defs

MCTF_TEXTURE_CODEC = os.environ["MCTF_TEXTURE_CODEC"]
HIGH = "H"
LOW = "L"

# }}}

# {{{ GOP_size

gop = GOP()
GOP_size = gop.get_size(TRLs)
log.info("GOP_size={}".format(GOP_size))

# }}}

# {{{ pictures

pictures = (GOPs - 1) * GOP_size + 1
log.info("pictures={}".format(pictures))

# }}}

# {{{ Compression of HIGH frequency temporal subbands.

subband = 1
while subband < TRLs:
    pictures = (pictures + 1) // 2

    shell.run("mctf subband_texture_compress__" + MCTF_TEXTURE_CODEC
              + " --file=" + HIGH + "_" + str(subband)
              + " --pictures=" + str(pictures - 1)
              + " --pixels_in_x=" + str(pixels_in_x)
              + " --pixels_in_y=" + str(pixels_in_y)
              + " --layers=" + str(layers)
              + " --SRLs=" + str(SRLs)
              + " --slope=" + str(slope))

    subband += 1

# }}}
    
# {{{ Compression of the LOW frequency temporal subband.

shell.run("mctf subband_texture_compress__" + MCTF_TEXTURE_CODEC
          + " --file=" + LOW + "_" + str(TRLs - 1)
          + " --pictures=" + str(pictures)
          + " --pixels_in_x=" + str(pixels_in_x)
          + " --pixels_in_y=" + str(pixels_in_y)
          + " --layers=" + str(layers)
          + " --SRLs=" + str(SRLs)
          + " --slope=" + str(slope))

# }}}
