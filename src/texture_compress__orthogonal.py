#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Texture compression. Variable quantization of temporal subbands for
# approximating MCTF to an orthogonal transform.

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
log = logging.getLogger("texture_compress__orthogonal")

MCTF_TEXTURE_CODEC   = os.environ["MCTF_TEXTURE_CODEC"]
HIGH                 = "high"            # High frequency subbands.
LOW                  = "low"             # Low frequency subbands.

parser = arguments_parser(description="Compress the texture.")
parser.GOPs()
parser.texture_layers()
parser.pixels_in_x()
parser.pixels_in_y()
parser.texture_layers()
parser.texture_quantization()
parser.texture_quantization_step()
parser.TRLs()
parser.SRLs()

args = parser.parse_known_args()[0]
GOPs = int(args.GOPs)
layers = int(args.texture_layers); log.debug("layers={}".format(layers))
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
quantization = int(args.texture_quantization); log.debug("quantization={}".format(quantization))
quantization_step = int(args.texture_quantization_step); log.debug("quantization_step={}".format(quantization_step))
TRLs = int(args.TRLs)
SRLs = int(args.SRLs)

gop      = GOP()
GOP_size = gop.get_size(TRLs)

## Number of images to process.
pictures = (GOPs - 1) * GOP_size + 1

if   TRLs == 1 :
    pass
elif TRLs == 2 :
    GAINS = [1.2460784922] # [L1/H1]
elif TRLs == 3 :
    GAINS = [1.2500103877, 1.8652117304] # [L2/H2, L2/H1]
elif TRLs == 4 :
    GAINS = [1.1598810146, 2.1224082769, 3.1669663339]
elif TRLs == 5 :
    GAINS = [1.0877939347, 2.1250255455, 3.8884779989, 5.8022196044]
elif TRLs == 6 :
    GAINS = [1.0456562538, 2.0788785438, 4.0611276369, 7.4312544148, 11.0885981772]
elif TRLs == 7 :
    GAINS = [1.0232370223, 2.0434169985, 4.0625355976, 7.9362383342, 14.5221257323, 21.6692913386]
elif TRLs == 8 :
    GAINS = [1.0117165706, 2.0226778348, 4.0393126714, 8.0305936232, 15.6879129862, 28.7065276104, 42.8346456693]
else :
    sys.stderr.write("Gains are not available for " + str(TRLs) + " TRLs. Enter them in texture_compress.py")
    exit (0)

# To determine the slopes whith must be applied to each temporal
# subband, it must be known that typically, the quality of a
# image/temporal-subband is reduced with an increment in the slope,
# linearly:
#
#  PSNR[dB]
#     ^
#     |
#     |  \
#     |   \
#     |    \
#     |     \
#     +-----------> Slope
#
# So, supposing that all temporal subbands have been compressed using
# the same slopes, and that this holds for each quality layer,
# incrementing the slope in a constant amount (using for example the
# slope S for the first quality layer of each temporal subband, slope
# S+X for the second quality layer of each temporal subband, slope
# S+2X ...), we can apply the subband gains considering that a given
# number of subband-layers of a low-frequency temporal subband should
# be "transmitted" before the first subband-layer of a
# higher-frecuency temporal subband.
#
# To determine such number, we can use the fact that a linear
# decrement in the slope produces a linear increment in the
# quality. Thus,for example, if we have Q subband-layers and a total
# increment (decoding all the subband-layers) in quality of x dB, each
# subband-layer constributes with an increment of x/Q dB, and this is
# true for all the temporal subbands because the total range of
# quality of all subbands is the same.
#
# For example, if TRLs=2, temporal subband L1 should contribute to the
# reconstruction of the GOP (to the output code-stream) approximately
# 1.25 times more than temporal subband H1. If Q=8, each subband-layer
# of L1 and H1 contributes with x/8 = 0.125*x dB. Therefore, it is
# easy to see that the optimal order for the subband-layers of these
# temporal subbands should be:
#
# L1.l7 (= Subband-layer 7 of temporal subband L1) which increases x/8
# dB the quality of each GOP.
#
# L1.l6 which produces a total increase of x/8 + x/8 = x/4 = 0.25*x dB
# in the quality of each GOP.
#
# At this point, we can "transmit" the next subband-layer of L1 or the
# first subband-layer of H1 (after having "transmitted" the
# corresponding subband-layer of M1). Experimentally we have
# determined that is better (in general) to "transmit" the next
# subband-layer of L1: L1.l5.
#
# M1.
#
# H1.l7, L1.l4, H1.l6, L1.l3, H1.l5, ...
#
# In terms of slopes, if MAX_SLOPE determines the minimum usable
# quality for a subband-layer, we should use the slope "quantization"
# for temporal subband L1 and the slope:
#
# quantization + (MAX_SLOPE - quantization) / GAIN[1][0]
#
# should be used for H1.
#
# In general, for subband-layer "l" of temporal subband "s", we have:
#
# quantization + (MAX_SLOPE - quantization) / GAIN[s][l]
#

MAX_SLOPE = 50000
log.debug("Subband / Slope::")
slopes = [] # Among temporal subbands (subband / slope):
for s in range(TRLs):
    slope = int(round(quantization + (MAX_SLOPE - quantization) / GAINS[s]))
    log.debug("{} / {}".format(s, slope))
    slopes.append(slope)

# Compression of HIGH frequency temporal subbands.
subband = 1
while subband < TRLs:
    pictures = (pictures + 1) // 2
    try:
        check_call("mctf texture_compress_" + MCTF_TEXTURE_CODEC
                   + " --file="             + HIGH + "_" + str(subband)
                   + " --texture_layers="   + str(layers)
                   + " --pictures="         + str(pictures - 1)
                   + " --pixels_in_x="      + str(pixels_in_x)
                   + " --pixels_in_y="      + str(pixels_in_y)
                   + " --quantization=\""   + str(slope[subband])
                   + " --subband="          + str(subband)
                   + " --SRLs="             + str(SRLs)
                   , shell=True)
    except CalledProcessError:
        sys.exit(-1)

    subband += 1

# Compression of LOW frequency temporal subband.
try:
    check_call("mctf texture_compress_" + MCTF_TEXTURE_CODEC
               + " --file="             + LOW + "_" + str(TRLs - 1)
               + " --texture_layers="   + str(layers)
               + " --pictures="         + str(pictures)
               + " --pixels_in_x="      + str(pixels_in_x)
               + " --pixels_in_y="      + str(pixels_in_y)
               + " --quantization=\""   + quantization
               + " --subband="          + str(subband)
               + " --SRLs="             + str(SRLs)
               , shell=True)
except:
    sys.exit(-1)
