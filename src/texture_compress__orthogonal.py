#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

#  Compress textures (temporal subbands) generated in the analysis
#  phase. The number of bits allocated depends on the "quality"
#  parameter, begin 0.0 the minumun quality.

# To determine the slopes whith must be applied to each temporal
# subband (the slope for each subband-layer), it must be known that
# typically, the quality of a image/temporal-subband is reduced with
# an increment in the slope, linearly:
#
#  PSNR[dB]
#     ^
#   50| \
#     | :\
#     | : \
#     | :  \
#   20| :   \
#     | :    :
#     +-+----+-> Slope
#       40K 50K
#
# So, supposing that all temporal subbands have been compressed using
# the same slopes, and that this holds for each quality layer,
# decreasinging the slope in a constant amount (using for example the
# slope 50000 for the first quality layer of each temporal subband, slope
# 50000-X for the second quality layer of each temporal subband, slope
# 50000-2X ...), we can apply the subband gains considering that a given
# number of subband-layers of a low-frequency temporal subband should
# be "transmitted" before the first subband-layer of a
# higher-frecuency temporal subband.
#
# To determine such number, we can use the fact that a linear
# decrement in the slope produces a linear increment in the
# quality. Thus,for example, if we have Q subband-layers and a total
# increment (decoding all the subband-layers) in quality of x dB
# (inside the subband), each subband-layer constributes with an
# increment of x/Q dB, and this is true for all the subband-layers of
# each temporal subband because the total range of quality of all
# subbands is the same.
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
# In terms of slopes, if MAX_SLOPE (50K) generates the minimum
# quality, we should use a slope "quantization_step" for subband H1
# and the slope:
#
# MAX_SLOPE - quality*Q/GAIN[1][0]
#
# for L1, where Q is the number of quality layers and GAIN[1][0] is
# the energy gain of subband L1 compared to H1.
#
# In general, for temporal subband "t", we have:
#
# MAX_SLOPE - GAIN[TRLs][t]*quantization_step*Q
#
# The quality of the recontruction is controlled by the
# quantization_step parameter. If quantization_step=1 we get the
# minimum quality. The higher the quantization step, the higher the
# quality (in the range of slopes [40K, 50K] approximately.
#
# Examples:
#
#   mctf transcode_quality --qstep=50

#to each subband depends on
#  the "slopes" parameter, which controls the quality of each quality
#  layer (such as a quantization factor) in each image of each
#  subband. Therefore, the number of quality layers equals the
#  number of slopes. The optimal bit-rate control should be performed
#  in decompression time using the "extract" program (See
#  transcode.py).

import os
import sys
import math
from GOP import GOP
from subprocess import check_call
from subprocess import CalledProcessError
from arguments_parser import arguments_parser
import logging

logging.basicConfig()
log = logging.getLogger("texture_compress__orthogonal")

parser = arguments_parser(description="Compress the texture.")
parser.GOPs()
parser.layers()
parser.pixels_in_x()
parser.pixels_in_y()
#parser.quantization()
#parser.quantization_step()
parser.add_argument("--quality",
                    help="Quality.",
                    default=0.25)
parser.TRLs()
parser.SRLs()

args = parser.parse_known_args()[0]
GOPs = int(args.GOPs)
layers = int(args.layers)
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
#quantization = int(args.quantization)
#quantization_step = int(args.quantization_step)
quality = float(args.quality)
TRLs = int(args.TRLs)
SRLs = int(args.SRLs)

MCTF_TEXTURE_CODEC   = os.environ["MCTF_TEXTURE_CODEC"]
HIGH                 = "high"            # High frequency subbands.
LOW                  = "low"             # Low frequency subbands.

def kdu_transcode(filename, slope):
    try:
        check_call("trace kdu_transcode"
                   + "slope=" + str(slops)
                   + " -i " + filename
                   + " -o " + "transcode_quality/" + filename,
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

# Slope computation
if   TRLs == 1 :
    pass
elif TRLs == 2 :
    GAINS = [1.0, 1.2460784922] # [L1/L1, L1/H1]
elif TRLs == 3 :
    GAINS = [1.0, 1.2500103877, 1.8652117304] # [L2/L2, /L2/H2, L2/H1]
elif TRLs == 4 :
    GAINS = [1.0, 1.1598810146, 2.1224082769, 3.1669663339]
elif TRLs == 5 :
    GAINS = [1.0, 1.0877939347, 2.1250255455, 3.8884779989, 5.8022196044]
elif TRLs == 6 :
    GAINS = [1.0, 1.0456562538, 2.0788785438, 4.0611276369, 7.4312544148, 11.0885981772]
elif TRLs == 7 :
    GAINS = [1.0, 1.0232370223, 2.0434169985, 4.0625355976, 7.9362383342, 14.5221257323, 21.6692913386]
elif TRLs == 8 :
    GAINS = [1.0, 1.0117165706, 2.0226778348, 4.0393126714, 8.0305936232, 15.6879129862, 28.7065276104, 42.8346456693]
else :
    sys.stderr.write("Gains are not available for " + str(TRLs) + " TRLs. Enter them in texture_compress.py")
    exit (0)

MAX_SLOPE = 50000
MIN_SLOPE = 40000
RANGE_SLOPES = MAX_SLOPE - MIN_SLOPE
slope = [None]*TRLs
log.debug("Subband / Slope::")
for s in range(TRLs):
    slope[TRLs-s-1] = int(round(MAX_SLOPE - RANGE_SLOPES*quality/GAINS[s]))
    if slopes[TRLs-s-1] < 0:
        slopes[TRLs-s-1] = 0
    log.debug("{} / {}".format(s, slope[TRLs-s-1]))

gop      = GOP()
GOP_size = gop.get_size(TRLs)
log.debug("GOP_size = {}".format(GOP_size))

# Number of pictures
pictures = (GOPs - 1) * GOP_size + 1
log.debug("pictures = {}".format(pictures))

#######

#import ipdb; ipdb.set_trace()
# Compression of HIGH frequency temporal subbands.
subband = 1
while subband < TRLs:
    pictures = (pictures + 1) // 2
    log.debug("subband={}".format(subband))
    command = "mctf subband_texture_compress__" + MCTF_TEXTURE_CODEC \
            + " --file="              + HIGH + "_" + str(subband) \
            + " --layers="            + str(layers) \
            + " --pictures="          + str(pictures - 1) \
            + " --pixels_in_x="       + str(pixels_in_x) \
            + " --pixels_in_y="       + str(pixels_in_y) \
            + " --slope=\""           + str(slope[subband-1]) + "\"" \
            + " --SRLs="              + str(SRLs)
    log.debug("command={}".format(command))
    try:
        check_call(command, shell=True)
    except CalledProcessError:
        sys.exit(-1)

    subband += 1

#import ipdb; ipdb.set_trace()
    
# Compression of LOW frequency temporal subband.
command = "mctf subband_texture_compress__" + MCTF_TEXTURE_CODEC \
  + " --file="              + LOW + "_" + str(TRLs - 1) \
  + " --layers="            + str(layers) \
  + " --pictures="          + str(pictures) \
  + " --pixels_in_x="       + str(pixels_in_x) \
  + " --pixels_in_y="       + str(pixels_in_y) \
  + " --slope=\""           + str(slope[TRLs-1]) + "\""\
  + " --SRLs="              + str(SRLs)
log.debug(command)
try:
    check_call(command, shell=True)
except:
    sys.exit(-1)
