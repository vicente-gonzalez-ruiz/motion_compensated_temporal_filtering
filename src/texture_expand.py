#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# Decompress a temporal subband of texture.

# {{{ Imports
import sys
import os
from GOP import GOP
from shell import Shell as shell
from arguments_parser import arguments_parser
from colorlog import log
# }}}

MCTF_TEXTURE_CODEC = os.environ["MCTF_TEXTURE_CODEC"]
LOW = "low"
HIGH = "high"

# {{{ Arguments parsing
parser = arguments_parser(description="Expands the texture.")
parser.GOPs()
parser.pixels_in_x()
parser.pixels_in_y()
parser.SRLs()
parser.TRLs()

args = parser.parse_known_args()[0]

GOPs = int(args.GOPs)
log.info("GOPs={}".format(GOPs))

pixels_in_x = str(args.pixels_in_x)
log.info("pixels_in_x={}".format(pixels_in_x))

pixels_in_y = str(args.pixels_in_y)
log.info("pixels_in_y={}".format(pixels_in_y))

SRLs = int(args.SRLs)
log.info("SRLs={}".format(SRLs))

TRLs = int(args.TRLs)
log.info("TRLs={}".format(TRLs))

# }}}

gop=GOP()
GOP_size = gop.get_size(TRLs)
_pictures = pictures = (GOPs - 1) * GOP_size + 1

if TRLs > 1 :
    # Decompression HIGH frequency subbands.
    subband = TRLs - 1
    while subband > 0 :

        ## Current picture iteration.
        pictures = _pictures
        ## Current temporal iteration.
        j = 0
        while j < subband :
            pictures = ( pictures + 1 ) // 2
            j += 1

        shell.run("mctf subband_texture_expand__" + MCTF_TEXTURE_CODEC
                  + " --file=" + "\"" + HIGH + "_" + str(subband) + "\""
                  + " --pictures=" + str(pictures - 1)
                  + " --pixels_in_x=" + str(pixels_in_x)
                  + " --pixels_in_y=" + str(pixels_in_y)
                  + " --subband=" + str(subband))

        subband -= 1

# L.
shell.run("mctf subband_texture_expand__" + MCTF_TEXTURE_CODEC
          + " --file=" + "\"" + LOW + "_" + str(TRLs - 1) + "\""
          + " --pictures=" + str(GOPs)
          + " --pixels_in_x=" + str(pixels_in_x)
          + " --pixels_in_y=" + str(pixels_in_y)
          + " --subband=" + str(TRLs))
