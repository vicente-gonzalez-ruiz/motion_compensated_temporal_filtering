#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Quality transcoding.

# Extracts a codestream from a bigger one.

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
# MAX_SLOPE - GAIN[1][0]*quantization_step*Q
#
# for L1, where Q is the number of quality layers and GAIN[1][0] is
# the energy gain of subband L1 compared to H1.
#
# In general, for subband-layer "q" of temporal subband "t", we have:
#
# MAX_SLOPE - GAIN[t][q]*quantization_step*Q
#
# The quality of the recontruction is controlled by the
# quantization_step parameter. If quantization_step=1 we get the
# minimum quality. The higher the quantization step, the higher the
# quality (in the range of slopes [40K, 50K] approximately.
#

#
# For progressive transmission:
#
# Reducing the number of quality subband-layers basically means that
# the list:
#
# [L^{T-1}_{Q-1}, M^{T-1}_{q-1}, H^{T-1}_{Q-1}, M^{T-2}_{q-1}, H^{T-2}_{Q-1}, ..., M^1_{q-1}, H^1_{Q-1},
#  L^{T-1}_{Q-2}, M^{T-1}_{q-2}, H^{T-1}_{Q-2}, M^{T-2}_{q-2}, H^{T-2}_{Q-2}, ..., M^1_{q-2}, H^1_{Q-2},
#  :
#  L^{T-1}_0, -, H^{T-1}_0, H^{T-1}_0, H^{T-2}_0, ..., H^1_0]
#
# is going to be truncated at a subband-layer, starting at
# L^{T-1}_{Q-1}, where T=number of TRLs, Q=number of quality layers
# for texture, and q=number of quality layers for movement. A total
# number of TQ+q subband-layers are available. In the last set
# description, it has been supposed that q<Q.

# Examples:
#
#   mctf transcode_quality --QSLs=5

import sys
from GOP              import GOP
from subprocess       import check_call
from subprocess       import CalledProcessError
from arguments_parser import arguments_parser

parser = arguments_parser(description="Transcodes in quality a MCJ2K sequence.")
parser.GOPs()
parser.pixels_in_x()
parser.pixels_in_y()
parser.add_argument("--qstep",
                    help="Quantization step.",
                    default=256)
parser.texture_layers()
parser.TRLs()

args = parser.parse_known_args()[0]
GOPs = int(args.GOPs)
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
qstep = int(args.qstep)
texture_layers = int(args.texture_layers)
TRLs = int(args.TRLs)

LOW = "low"
HIGH = "high"
MOTION = "motion_residue"

# We need to compute the number of quality layers of each temporal
# subband. For example, if QSLs=1, only the first quality layer of the
# subband L^{T-1} will be output. If QSLs=2, only the first quality
# layer of the subbands L^{T-1} and M^{T-1} will be output, if QSLs=3,
# the first quality layer of H^{T-1} will be output too, and so on.

def generate_list_of_subband_layers(T, Qt, Qm):
    l = []
    for q in range(Qt):
        l.append(('L', T-1, Qt-q-1))
        for t in range(T-1):
            if q < Qm:
                l.append(('M', T-t-1, Qm-q-1))
            l.append(('H', T-t-1, Qt-q-1))
    return l

print("Texture layers = {}".format(texture_layers))
print("Motion layers = {}".format(motion_layers))

all_subband_layers = generate_list_of_subband_layers(T=TRLs,
                                                     Qt=texture_layers,
                                                     Qm=motion_layers
                                                     )

print("Subband layers = {}".format(all_subband_layers))
print("QSLs = {}".format(QSLs))

subband_layers_to_copy = all_subband_layers[:QSLs]
print("Subband layers to copy = {}".format(subband_layers_to_copy))

number_of_quality_layers_in_L = len([x for x in subband_layers_to_copy
                                    if x[0]=='L'])
print("Number of subband layers in L = {}".format(number_of_quality_layers_in_L))

number_of_quality_layers_in_H = [None]*TRLs
for i in range(1, TRLs):
    number_of_quality_layers_in_H[i] = len([x for x in subband_layers_to_copy
                                            if x[0]=='H' and x[1]==i])
    print("Number of quality layers in H_{} = {}".format(i, number_of_quality_layers_in_H[i]))
    
number_of_quality_layers_in_M = [None]*TRLs
for i in range(1, TRLs):
    number_of_quality_layers_in_M[i] = len([x for x in subband_layers_to_copy
                                            if x[0]=='M' and x[1]==i])
    print("Number of quality layers in M_{} = {}".format(i, number_of_quality_layers_in_M[i]))

def kdu_transcode(filename, layers):
    try:
        check_call("trace kdu_transcode Clayers=" + str(layers)
                   + " -i " + filename
                   + " -o " + "transcode_quality/" + filename,
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

gop=GOP()
GOP_size = gop.get_size(TRLs)
print("GOP_size = {}".format(GOP_size))

pictures = (GOPs - 1) * GOP_size + 1
print("pictures = {}".format(pictures))

# Transcoding of H subbands
subband = 1
while subband < TRLs:

    pictures = (pictures + 1) // 2 - 1
    print("Transcoding subband H[{}] of {} pictures".format(subband, pictures))
    
    image_number = 0
    # pictures = 
    while image_number < pictures:

        str_image_number = '%04d' % image_number

        filename = HIGH + "_" + str(subband) + "_" + str_image_number + "_Y" 
        kdu_transcode(filename + ".j2c", number_of_quality_layers_in_H[subband])

        filename = HIGH + "_" + str(subband) + "_" + str_image_number + "_U" 
        kdu_transcode(filename + ".j2c", number_of_quality_layers_in_H[subband])

        filename = HIGH + "_" + str(subband) + "_" + str_image_number + "_V" 
        kdu_transcode(filename + ".j2c", number_of_quality_layers_in_H[subband])

        image_number += 1

    subband += 1

# Transcoding of M "subbands"
subband = 1
pictures = GOPs * GOP_size - 1
fields = pictures // 2
while subband < TRLs:

    field = 0
    
    while field < fields:

        str_field = '%04d' % field

        for component in range(4):
            
            filename = MOTION + "_" + str(subband) + "_" + str_field + "_comp" + str(component) + ".j2c"
            kdu_transcode(filename, number_of_quality_layers_in_M[subband])

        field += 1

    fields /= 2

    subband += 1

# Transcoding of L subband
image_number = 0
while image_number < pictures - 1:

    str_image_number = '%04d' % image_number

    filename = LOW + "_" + str(TRLs-1) + "_" + str_image_number + "_Y"
    kdu_transcode(filename + ".j2c", number_of_quality_layers_in_L)

    filename = LOW + "_" + str(TRLs-1) + "_" + str_image_number + "_U"
    kdu_transcode(filename + ".j2c", number_of_quality_layers_in_L)

    filename = LOW + "_" + str(TRLs-1) + "_" + str_image_number + "_V"
    kdu_transcode(filename + ".j2c", number_of_quality_layers_in_L)

    image_number += 1

subband = 1
while subband < TRLs:

    try:
        check_call("cp frame_types_" + str(subband) + " transcode_quality/",
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

    subband += 1
