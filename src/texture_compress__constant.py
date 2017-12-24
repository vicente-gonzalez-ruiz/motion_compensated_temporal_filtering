#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Texture compression. Constant quantization of temporal subbands.

import os
import sys
import display
import math
from GOP import GOP
from subprocess import check_call
from subprocess import CalledProcessError
from arguments_parser import arguments_parser
import logging

logging.basicConfig()
log = logging.getLogger("texture_compress__constant")

MCTF_TEXTURE_CODEC   = os.environ["MCTF_TEXTURE_CODEC"]
HIGH                 = "high"
LOW                  = "low"

parser = arguments_parser(description="Compress the texture.")
parser.GOPs()
parser.pixels_in_x()
parser.pixels_in_y()
parser.quantization_max()
parser.quantization_min()
parser.TRLs()
parser.SRLs()

args = parser.parse_known_args()[0]
GOPs = int(args.GOPs); log.debug("GOPs={}".format(GOPs))
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
quantization_max = int(args.quantization_max)
quantization_min = int(args.quantization_min)
TRLs = int(args.TRLs)
SRLs = int(args.SRLs)

gop      = GOP()
GOP_size = gop.get_size(TRLs)

## Number of images to process.
pictures = (GOPs - 1) * GOP_size + 1

#slopes = []
#for i in range(layers):
#    slopes.append(quantization + i * quantization_step)

#if len(slopes) == 1:
#    str_slopes = str(slopes[0])
#else:
#    str_slopes = ','.join(str(i) for i in slopes)
    
# Compression of HIGH frequency temporal subbands.
subband = 1
while subband < TRLs:
    pictures = (pictures + 1) // 2
    try:
        check_call("mctf subband_texture_compress__" + MCTF_TEXTURE_CODEC
                   + " --file="              + HIGH + "_" + str(subband)
                   + " --pictures="          + str(pictures - 1)
                   + " --pixels_in_x="       + str(pixels_in_x)
                   + " --pixels_in_y="       + str(pixels_in_y)
                   + " --slopes="            + str(quantization_max)
                   + " --SRLs="              + str(SRLs)
                   , shell=True)
    except CalledProcessError:
        sys.exit(-1)

    subband += 1

# Compression of LOW frequency temporal subband.
try:
    check_call("mctf subband_texture_compress__" + MCTF_TEXTURE_CODEC
               + " --file="              + LOW + "_" + str(TRLs - 1)
               + " --pictures="          + str(pictures)
               + " --pixels_in_x="       + str(pixels_in_x)
               + " --pixels_in_y="       + str(pixels_in_y)
               + " --slopes="            + str(quantization_max)
               + " --SRLs="              + str(SRLs)
               , shell=True)
except:
    sys.exit(-1)
