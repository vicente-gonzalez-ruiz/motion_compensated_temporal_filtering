#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

#  Decompress the texture. There are a different number of (compressed)
#  texture streams called "low_X", "high_X", "high_X-1", ..., where X
#  is the bumber of temporal resolution levels - 1.

import sys
import os
from GOP import GOP
from subprocess import check_call
from subprocess import CalledProcessError
from arguments_parser import arguments_parser
import logging

logging.basicConfig()
log = logging.getLogger("texture_expand")

MCTF_TEXTURE_CODEC = os.environ["MCTF_TEXTURE_CODEC"]
LOW         = "low"
HIGH        = "high"

parser = arguments_parser(description="Expands the texture.")
parser.GOPs()
parser.pixels_in_x()
parser.pixels_in_y()
parser.SRLs()
parser.TRLs()

args = parser.parse_known_args()[0]
GOPs = int(args.GOPs)
pixels_in_x = str(args.pixels_in_x)
pixels_in_y = str(args.pixels_in_y)
SRLs = int(args.SRLs)
TRLs = int(args.TRLs)

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

        try:
            check_call("mctf subband_texture_expand_" + MCTF_TEXTURE_CODEC
                       + " --file="        + "\"" + HIGH + "_" + str(subband) + "\""
                       + " --pictures="    + str(pictures - 1)
                       + " --pixels_in_x=" + str(pixels_in_x)
                       + " --pixels_in_y=" + str(pixels_in_y)
                       + " --subband="     + str(subband)
                       , shell=True)
        except CalledProcessError:
            sys.exit(-1)

        subband -= 1

# L.
try:
    check_call("mctf subband_texture_expand_" + MCTF_TEXTURE_CODEC
               + " --file="        + "\"" + LOW + "_" + str(TRLs - 1) + "\""
               + " --pictures="    + str(GOPs+1)
               + " --pixels_in_x=" + str(pixels_in_x)
               + " --pixels_in_y=" + str(pixels_in_y)
               + " --subband="     + str(TRLs)
               , shell=True)
except CalledProcessError:
    sys.exit(-1)
