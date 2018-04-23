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
import io

# {{{ Logging
logging.basicConfig()
log = logging.getLogger("texture_compress__constant") # remove __constant (some day)
# }}}

# {{{ Arguments parsing
parser = arguments_parser(description="Compress a texture subband.")
parser.GOPs()
#parser.layers()
parser.pixels_in_x()
parser.pixels_in_y()
parser.quantization_max()
parser.quantization_min()
parser.quantization_step()
#parser.quality()
parser.SRLs()
parser.TRLs()

args = parser.parse_known_args()[0]
GOPs = int(args.GOPs); log.debug("GOPs={}".format(GOPs))
#layers = int(args.layers)
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
quantization_max = int(args.quantization_max)
quantization_min = int(args.quantization_min)
quantization_step = int(args.quantization_step)
# Min slope in Kakadu
#quality = float(args.quality)
SRLs = int(args.SRLs)
TRLs = int(args.TRLs)
# }}}

MCTF_TEXTURE_CODEC   = os.environ["MCTF_TEXTURE_CODEC"]
HIGH                 = "high"
LOW                  = "low"

# Typical range of useful slopes in Kakadu
#MAX_SLOPE = 50000 # Min quality
#MIN_SLOPE = 40000 # Max quality
#RANGE_SLOPES = MAX_SLOPE - MIN_SLOPE
#Q_STEP = 256 # In Kakadu, this should avoid the generation of empty layers

#slope = [None]*layers

# {{{ Compute slopes
slope = []
_slope_ = quantization_max
while _slope_ > quantization_min:
    #input()
    slope.append(_slope_)
    _slope_ -= quantization_step
# }}}
    
# {{{ Write slopes to disk
with io.open('slopes.txt', 'w') as file:
    for i in slope:
        file.write('{}\n'.format(i))
# }}}

#for q in range(layers):
#    _slope_ = int(round(quantization_max - quality - quantization_step*q))
#    if _slope_ < 0:
#        slope[q] = 0
#    else:
#        slope[q] = _slope_

gop      = GOP()
GOP_size = gop.get_size(TRLs)
log.debug("GOP_size = {}".format(GOP_size))

pictures = (GOPs - 1) * GOP_size + 1
log.debug("pictures = {}".format(pictures))

# Compression of HIGH frequency temporal subbands.
subband = 1
while subband < TRLs:
    pictures = (pictures + 1) // 2
    slopes = ','.join(str(i) for i in slope)
    command = "mctf subband_texture_compress__" + MCTF_TEXTURE_CODEC \
      + " --file="              + HIGH + "_" + str(subband) \
      + " --pictures="          + str(pictures - 1) \
      + " --pixels_in_x="       + str(pixels_in_x) \
      + " --pixels_in_y="       + str(pixels_in_y) \
      + " --slope=\""           + slopes + "\"" \
      + " --SRLs="              + str(SRLs)

    log.debug("command={}".format(command))
    try:
        check_call(command, shell=True)
    except CalledProcessError:
        sys.exit(-1)

    subband += 1

# Compression of the LOW frequency temporal subband.
slopes = ','.join(str(i) for i in slope)
command = "mctf subband_texture_compress__" + MCTF_TEXTURE_CODEC \
  + " --file="              + LOW + "_" + str(TRLs - 1) \
  + " --pictures="          + str(pictures) \
  + " --pixels_in_x="       + str(pixels_in_x) \
  + " --pixels_in_y="       + str(pixels_in_y) \
  + " --slope=\""           + slopes + "\""\
  + " --SRLs="              + str(SRLs)

log.debug(command)
try:
    check_call(command, shell=True)
except:
    sys.exit(-1)
