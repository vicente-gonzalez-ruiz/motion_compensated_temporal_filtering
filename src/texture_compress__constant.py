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
log = logging.getLogger("teture_compress")

MCTF_TEXTURE_CODEC   = os.environ["MCTF_TEXTURE_CODEC"]
HIGH                 = "high"            # High frequency subbands.
LOW                  = "low"             # Low frequency subbands.

parser = arguments_parser(description="Compress the texture.")
parser.GOPs()
parser.texture_layers()
parser.pixels_in_x()
parser.pixels_in_y()
parser.texture_quantization()
parser.quantization_step()
parser.TRLs()
parser.SRLs()

args = parser.parse_known_args()[0]
GOPs = int(args.GOPs); log.debug("GOPs={}".format(GOPs))
layers = int(args.texture_layers)
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
quantization = args.texture_quantization
quantization_step = int(args.quantization_step)
TRLs = int(args.TRLs)
SRLs = int(args.SRLs)

# print "texture_compress.py ; Q= " + str(quantization)
# raw_input("\ntexture_compress.py Press ENTER to continue ...")

gop      = GOP()
GOP_size = gop.get_size(TRLs)

## Number of images to process.
pictures = (GOPs - 1) * GOP_size + 1

slopes = [TQ]
for i in range(texture_layers):
    slopes.append(TQ+i*TQS]

# Compression of HIGH frequency temporal subbands.
subband = 1
while subband < TRLs:
    pictures = (pictures + 1) // 2
    try:
        check_call("mctf texture_compress__" + MCTF_TEXTURE_CODEC
                   + " --file="              + HIGH + "_" + str(subband)
                   + " --pictures="          + str(pictures - 1)
                   + " --pixels_in_x="       + str(pixels_in_x)
                   + " --pixels_in_y="       + str(pixels_in_y)
                   + " --slopes="            + ', '.join(str(i) for in in slopes)
                   + " --subband="           + str(subband)
                   + " --SRLs="              + str(SRLs)
                   , shell=True)
    except CalledProcessError:
        sys.exit(-1)

    subband += 1

# Compression of LOW frequency temporal subband.
try:
    check_call("mctf texture_compress__" + MCTF_TEXTURE_CODEC
               + " --file="              + LOW + "_" + str(TRLs - 1)
               + " --pictures="          + str(pictures)
               + " --pixels_in_x="       + str(pixels_in_x)
               + " --pixels_in_y="       + str(pixels_in_y)
               + " --slopes="            + ', '.join(str(i) for in in slopes)
               + " --subband="           + str(subband)
               + " --SRLs="              + str(SRLs)
               , shell=True)
except:
    sys.exit(-1)
