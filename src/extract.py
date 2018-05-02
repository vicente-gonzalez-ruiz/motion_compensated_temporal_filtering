#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# Extracts a MCJ2K codestream from a bigger one, with the aim of
# reducing quality, temporal or spatial resolution. At this moment,
# only a quality reduction has been implemented.

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
#   mctf extract --QSLs=5

import sys
from GOP              import GOP
from subprocess       import check_call
from subprocess       import CalledProcessError
from arguments_parser import arguments_parser

parser = arguments_parser(description="Extracts a number of subband-layers.")
parser.GOPs()
parser.motion_layers()
parser.pixels_in_x()
parser.pixels_in_y()
parser.add_argument("--QSLs",
                    help="Number of Quality Subband-Layers.",
                    default=1)
parser.layers()
parser.TRLs()

args = parser.parse_known_args()[0]
GOPs = int(args.GOPs)
motion_layers = int(args.motion_layers)
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
QSLs = int(args.QSLs)
texture_layers = int(args.layers)
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

print("TRLs = {}".format(TRLs))
print("Texture layers = {}".format(texture_layers))
print("Motion layers = {}".format(motion_layers))

all_subband_layers = generate_list_of_subband_layers(T=TRLs,
                                                     Qt=texture_layers,
                                                     Qm=motion_layers
                                                     )

print("Subband layers = {}".format(all_subband_layers))
print("QSLs = {}".format(QSLs))
print("Number of subband-layers = {}".format(len(all_subband_layers)))

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
    print("transcoding {} to {} layers".format(filename, layers))
    if layers>0:
        try:
            check_call("trace kdu_transcode Clayers=" + str(layers)
                       + " -i " + filename
                       + " -o " + "/tmp/" + filename,
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
pictures -= 1 # First GOP is out
while subband < TRLs:

    pictures = (pictures + 1) // 2
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


# Transcoding of L subband
image_number = 0
while image_number < pictures + 1:

    str_image_number = '%04d' % image_number

    filename = LOW + "_" + str(TRLs-1) + "_" + str_image_number + "_Y"
    kdu_transcode(filename + ".j2c", number_of_quality_layers_in_L)

    filename = LOW + "_" + str(TRLs-1) + "_" + str_image_number + "_U"
    kdu_transcode(filename + ".j2c", number_of_quality_layers_in_L)

    filename = LOW + "_" + str(TRLs-1) + "_" + str_image_number + "_V"
    kdu_transcode(filename + ".j2c", number_of_quality_layers_in_L)

    image_number += 1

# Transcoding of M "subbands"
subband = 1
pictures = (GOPs - 1) * GOP_size + 1
fields = pictures // 2
while subband < TRLs:

    field = 0
    
    while field < fields:

        str_field = '%04d' % field

        for component in range(4):
            
            filename = MOTION + "_" + str(subband) + "_" + str_field + "_" + str(component) + ".j2c"
            kdu_transcode(filename, number_of_quality_layers_in_M[subband])

        field += 1

    fields /= 2

    subband += 1

# Posiblemente quitar
subband = 1
while subband < TRLs:

    try:
        check_call("cp frame_types_" + str(subband) + " /tmp/",
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

    subband += 1
