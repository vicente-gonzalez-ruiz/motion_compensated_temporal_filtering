#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# Quality transcoding. Extracts a codestream from a longest one,
# preserving the FPS and spatial resolution. A number of quality
# layers of each image of each temporal subband (that is, a number of
# subband-layers) will be copied to the output.

# Example of use:
#
#  mctf transcode_quality --layers=1 # <- Will output L^{T-1}_{Q-1}
#                                    # where T=number of TRLs,
#                                    # Q=number of quality layers.
#
#  mctf transcode_quality --layers=2 # <- Will output L^{T-1}_{Q-1}
#                                    # and depending on Q, will output
#                                    # L^{T-1}_{Q-2} or M^{T-1}.

# Procedure.
#
# Each temporal subband has been compressed using the same slopes. The
# slopes has been selected equidistant, and threfore, each
# subband-layer will contribute with the same quality Q to the
# corresponding temporal subband. This value depends on the distance
# between the slopes.
#
# On the other hand, each temporal subband contributes with a
# different of energy (~quality) to the reconstruction of the GOP. For
# example, if L1 is 1.25 times more energetic than H1, each
# subband-layer of L1 also will contribute 1.25 times more than any
# other layer of H1. In fact, any subband-layer of L1 contributes
# 1.25*Q where any subband-layer of H1 contributes Q.
#
# The size of each subband-layer in each subband has a different
# length. If R is the length of L1.l3 and H1.l3 (supposing 4
# subband-layers), \sqrt(2)*R will be the length (on average) of L1.l2
# and H1.l2. To find an optimal ordering of subband layers in this
# example, the lengths of the subband-layers of L1 can be considered
# 1.25 times smaller than the lengths of the subband-layers of H1. So,
# the slopes generated by the subband-layers of L1 will have 1.25
# times the slopes of the subband-layers of H1.
#
# If the slope (when reconstructing the GOP) of L1.l3 is X, the slope
# of L1.l2 is X/sqrt(2), the slope of L1.l1 is X/(sqrt(2)^2) and so
# on. The slope (when reconstructing the GOP) of H1.l3 is X/1.25, the
# slope of H1.l2 is (X/1.25)/sqrt(2), the slope of H1.l1 is
# (X/1.25)/(sqrt(2)^2), etc. Therefore, depending on X, each
# subband-layer of each temporal subband will generate a slope. The
# optimal subband-layers ordering can be determined by sorting the
# slopes. For example, is X=5dB, slope(L1.l3)=5,
# slope(L1.l2)=5/sqrt(2)=3.53. slope(L1.l1)=5/(sqrt(2)^2)=2.5,
# slope(L1.l0)=5/(sqrt(2)^3)=1.77, slope(H1.l3)=5/1.25=4,
# slope(H1.l2)=5/1.25/sqrt(2)=2.83, slope(H1.l1)=5/1.25/(sqrt(2)^2)=2
# and slope(H1.l0)=5/1.25/(sqrt(2)^3)=1.41 The optimal ordering is:
# L1.l3 (5), H1.l3 (4), L1.l2 (3.53), H1.l2 (2.83), L1.l1 (2.5), H1.l1
# (2), L1.l0 (1.77), H1.l0 (1.41).
#
# If X=1dB, slope(L1.l3)=1 (5 times smaller than in the previous
# example), slope(H1.l3)=1/1.25=0.8, slope(L1.l2)=1/sqrt(2)=0.71,
# slope(H1.l2)=1/1.25/sqrt(2)=0.56, slope(L1.l1)=1/sqrt(2)^2=0.5,
# slope(H1.l1)=1/1.25/sqrt(2)^2=0.4, slope(L1.l0)=1/sqrt(2)^3=0.35,
# slope(H1.l0)=1/1.25/sqrt(2)^3=0.28. Logically, the ordering does not
# varie as a function of Q.
#
# If we use for example 8 quality layers, slope(L1.l7)=1,
# slope(L1.l6)=1/sqrt(2), slope(L1.l5)=1/sqrt(2)=^2 ... and
# slope(H1.l7)=1/1.25, slope(H1.l6)=1/1.25/sqrt(2) ..., so the
# ordering is the same than in the previous example.
#
# If TRLs=3, we have the following subband attenuations: 1.0,
# 1.2500103877, 1.8652117304. For 4 quality-layers, we have:
# 
# slope(L2.l3)=1,
# slope(L2.l2)=1/sqrt(2)=0.71,
# slope(L2.l1)=1/sqrt(2)^2=0.5,
# slope(L2.l0)=1/sqrt(2)^3=0.35,
# slope(H2.l3)=1/1.25=0.8,
# slope(H2.l2)=1/1.25/sqrt(2)=0.56,
# slope(H2.l1)=1/1.25/sqrt(2)^2=0.4,
# slope(H2.l0)=1/1.25/sqrt(2)^3=0.28,
# slope(H1.l3)=1/1.86=0.54,
# slope(H1.l2)=1/1.86/sqrt(2)=0.38,
# slope(H1.l1)=1/1.86/sqrt(2)^2=0.26,
# slope(H1.l0)=1/1.86/sqrt(2)^3=0.19.
# 
# So the ordering is:
#
#  1. L2.l3 (1),
#  2. H2.l3 (0.8),
#  3. L2.l2 (0.71),
#  4. H2.l2 (0.56),
#  5. H1.l3 (0.54),
#  6. L2.l1 (0.5),
#  7. H2.l1 (0.4),
#  8. H1.l2 (0.38),
#  9. L2.l0 (0.35),
# 10. H2.l0 (0.28),
# 11. H1.l1 (0.26),
# 12. H1.l0 (0.19)

import logging
import sys
from   GOP              import GOP
from   subprocess       import check_call
from   subprocess       import CalledProcessError
from   arguments_parser import arguments_parser
import io
import operator

# {{{ Logging

logging.basicConfig()
log = logging.getLogger("transcode_quality")

# }}}

# {{{ Arguments parsing

parser = arguments_parser(description="Transcodes in quality a MCJ2K sequence.")
parser.GOPs()
parser.add_argument("--layers",
                    help="Number of quality layers to output",
                    default=8)
#parser.layers()       # Number of layers to copy
#parser.quantization_max()
#parser.quantization_min()
#parser.quantization_step()
parser.TRLs()

args = parser.parse_known_args()[0]
GOPs = int(args.GOPs)
layers = int(args.layers)
#quality = float(args.quality)
#quantization_step = int(args.quantization_step)
TRLs = int(args.TRLs)

# }}} Arguments parsing

# {{{ Set attenuations among temporal subbands

if   TRLs == 1 :
    pass
elif TRLs == 2 :
    gain = [1.0, 1.2460784922] # [L1/H1]
elif TRLs == 3 :
    gain = [1.0, 1.2500103877, 1.8652117304] # [L2/H2, L2/H1]
elif TRLs == 4 :
    gain = [1.0, 1.1598810146, 2.1224082769, 3.1669663339]
elif TRLs == 5 :
    gain = [1.0, 1.0877939347, 2.1250255455, 3.8884779989, 5.8022196044]
elif TRLs == 6 :
    gain = [1.0, 1.0456562538, 2.0788785438, 4.0611276369, 7.4312544148, 11.0885981772]
elif TRLs == 7 :
    gain = [1.0, 1.0232370223, 2.0434169985, 4.0625355976, 7.9362383342, 14.5221257323, 21.6692913386]
elif TRLs == 8 :
    gain = [1.0, 1.0117165706, 2.0226778348, 4.0393126714, 8.0305936232, 15.6879129862, 28.7065276104, 42.8346456693]
else :
    sys.stderr.write("Gains are not available for " + str(TRLs) + " TRLs. Enter them in transcode_quality.py")
    exit (0)

# }}} Set attenuations among temporal subbands

# {{{ subband_layers: a list of tuples ('L'|'H', subband, layer, relative slope)

# Read the number of quality layers used for texture compression
quality_layers = sum(1 for line in open('slopes.txt'))
    
subband_layers = []
    
# L
for q in range(quality_layers):
    subband_layers.append(('L', TRLs, q, 1/math.sqrt(2.0)^q))

# H's
for s in range(TRLs,1):
    for q in range(quality_layers):
        subband_layers.append(('H', s, q, 1/gains[s]/math.sqrt(2.0)^q))

# }}} subband_layers: a list of tuples ('L'|'H', subband, layer, relative slope)

# Sort the subband-layers by their relative slope
sorted = subband_layers.sort(key=operator.itemgetter(3))

# Truncate the list
truncated = del sorted[layers:]

# {{{ Count the number of subband-layers per subband
layers = {}
layers[('L', TRLs)] = 0
for i in range(TRLs):
    layers[('H', i)] = 0
for i in truncated:
    layers[(i[0], i[1]] += 1
# }}}

def transcode_image(filename, layers):
    try:
        check_call("trace kdu_transcode"
                   + " -i " + filename
                   + " -o " + "transcode_quality/" + filename,
                   + " Clayers=" + str(layers), 
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

# {{{ GOPs and pictures

gop=GOP()
GOP_size = gop.get_size(TRLs)
log.debug("GOP_size = {}".format(GOP_size))

pictures = (GOPs - 1) * GOP_size + 1
log.debug("pictures = {}".format(pictures))

# }}}

# Transcoding of H subbands
subband = 1
while subband < TRLs:

    pictures = (pictures + 1) // 2 - 1
    log.debug("Transcoding subband H[{}] of {} pictures".format(subband, pictures))
    
    image_number = 0
    while image_number < pictures:

        str_image_number = '%04d' % image_number

        filename = HIGH + "_" + str(subband) + "_" + str_image_number + "_Y" 
        transcode_image(filename + ".j2c", slope[subband])

        filename = HIGH + "_" + str(subband) + "_" + str_image_number + "_U" 
        transcode_image(filename + ".j2c", slope[subband])

        filename = HIGH + "_" + str(subband) + "_" + str_image_number + "_V" 
        transcode_image(filename + ".j2c", slope[subband])

        image_number += 1

    subband += 1

# Transcoding of L subband
pictures - 1:

    str_image_number = '%04d' % image_number

    filename = LOW + "_" + str(TRLs-1) + "_" + str_image_number + "_Y"
    kdu_transcode(filename + ".j2c", number_of_quality_layers_in_L)

    filename = LOW + "_" + str(TRLs-1) + "_" + str_image_number + "_U"
    kdu_transcode(filename + ".j2c", number_of_quality_layers_in_L)

    filename = LOW + "_" + str(TRLs-1) + "_" + str_image_number + "_V"
    kdu_transcode(filename + ".j2c", number_of_quality_layers_in_L)

    image_number += 1


sys.quit()
# -------


        
# {{{ Slope computation of each subband-layer of each temporal subband

if   TRLs == 1 :
    pass
elif TRLs == 2 :
    gain = [1.0, 1.2460784922] # [L1/H1]
elif TRLs == 3 :
    gain = [1.0, 1.2500103877, 1.8652117304] # [L2/H2, L2/H1]
elif TRLs == 4 :
    gain = [1.0, 1.1598810146, 2.1224082769, 3.1669663339]
elif TRLs == 5 :
    gain = [1.0, 1.0877939347, 2.1250255455, 3.8884779989, 5.8022196044]
elif TRLs == 6 :
    gain = [1.0, 1.0456562538, 2.0788785438, 4.0611276369, 7.4312544148, 11.0885981772]
elif TRLs == 7 :
    gain = [1.0, 1.0232370223, 2.0434169985, 4.0625355976, 7.9362383342, 14.5221257323, 21.6692913386]
elif TRLs == 8 :
    gain = [1.0, 1.0117165706, 2.0226778348, 4.0393126714, 8.0305936232, 15.6879129862, 28.7065276104, 42.8346456693]
else :
    sys.stderr.write("Gains are not available for " + str(TRLs) + " TRLs. Enter them in transcode_quality.py")
    exit (0)

# {{{ Typical range of useful slopes in Kakadu
MAX_SLOPE = 50000 # Min quality
MIN_SLOPE = 40000 # Max quality
RANGE_SLOPES = MAX_SLOPE - MIN_SLOPE
# }}}

Q_STEP = 256 # In Kakadu, this should avoid the generation of empty layers

#slope = [[0 for l in range(layers)] for t in range(TRLs)]
slope = []
slope.append([])
#layer = 0
with io.open('slopes.txt', 'r') as file:
    for line in file:
        slope[0].append(int(line))
        #slope[0][layer] = int(line)
        #layer += 1

# TRLs = 1
#  L^0
# TRLs = 2
#  L^1, H^1
# TRLs = 3
#  L^2, H^2, H^1
# :

for s in range(1,TRLs):
    slope.append([])
    for l in range(layers):
        slope[s].append(int(slope[0][l]*gain[s]))

for l in range(layers):
    for s in range(TRLs):
        print('{} '.format(slope[s][l]), end="")
    print()

# {{{ Compute slopes
#for s in range(TRLs):
#    log.debug("Temporal subband {}".format(s))
#    for q in range(layers):
#        log.debug("Subband-layer {}".format(q))
#        _slope_ = int(round(MAX_SLOPE - quality - Q_STEP*q) / GAINS[s])
#        if _slope_ < 0:
#            slope[s][q] = (0, s, q)
#        else:
#            slope[s][q] = (_slope_, s, q)
#        log.debug("Slope {}".format(slope[s][q]))
# }}}

# }}}

#print("{}".format(slope))
        
# {{{ GOPs and pictures

gop=GOP()
GOP_size = gop.get_size(TRLs)
log.debug("GOP_size = {}".format(GOP_size))

pictures = (GOPs - 1) * GOP_size + 1
log.debug("pictures = {}".format(pictures))

# }}}

# {{{ Transcode the (texture) subbands

LOW = "low"
HIGH = "high"
MOTION = "motion_residue"

def kdu_transcode(filename, layers):
    try:
        check_call("trace kdu_transcode"
                   + " -i " + filename
                   + " -o " + "transcode_quality/" + filename,
                   + " Clayers=" + str(layers), 
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

# Transcoding of H subbands
subband = 1
while subband < TRLs:

    pictures = (pictures + 1) // 2 - 1
    log.debug("Transcoding subband H[{}] of {} pictures".format(subband, pictures))
    
    image_number = 0
    while image_number < pictures:

        str_image_number = '%04d' % image_number

        filename = HIGH + "_" + str(subband) + "_" + str_image_number + "_Y" 
        kdu_transcode(filename + ".j2c", slope[subband])

        filename = HIGH + "_" + str(subband) + "_" + str_image_number + "_U" 
        kdu_transcode(filename + ".j2c", slope[subband])

        filename = HIGH + "_" + str(subband) + "_" + str_image_number + "_V" 
        kdu_transcode(filename + ".j2c", slope[subband])

        image_number += 1

    subband += 1


# We know the number of subband-layers (quality layers of each
# temporal subband): texture_layers and the number of subbands
# (TRLs). If for example, texture_layers (Q)==8, and TRLs (T)==5, the
# order of subband-layers should be: L^4_7 (one quality layer of L^4),
# L^4_6 (two quality levels of L^4), M^4 (the first and only layer of
# M4), L^4_5 (in total, tree quality layers of L^4), 

# Q=4, T=5:

# q=1: L^4_3
# q=2: L^4_2, M^4, H^4_3
# q=3: L^4_1,      H^4_2, M^3, H^3_3
# q=4: L^4_0,      H^4_1,      H^3_2, M^2, H^2_3
# q=5:             H^4_0,      H^3_1,      H^2_2
# q=6:                         H^3_0,      H^2_1, M^1, H^1_3
# q=7:                                     H^2_0,      H^1_2
# q=8:                                                 H^1_1
# q=9:                                                 H^1_0

#### OLD ####

# Transcoding of M "subbands"
'''
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
'''

# Transcoding of L subband image_number = 0 while image_number <
pictures - 1:

    str_image_number = '%04d' % image_number

    filename = LOW + "_" + str(TRLs-1) + "_" + str_image_number + "_Y"
    kdu_transcode(filename + ".j2c", number_of_quality_layers_in_L)

    filename = LOW + "_" + str(TRLs-1) + "_" + str_image_number + "_U"
    kdu_transcode(filename + ".j2c", number_of_quality_layers_in_L)

    filename = LOW + "_" + str(TRLs-1) + "_" + str_image_number + "_V"
    kdu_transcode(filename + ".j2c", number_of_quality_layers_in_L)

    image_number += 1

'''
subband = 1
while subband < TRLs:

    try:
        check_call("cp frame_types_" + str(subband) + " transcode_quality/",
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

    subband += 1
'''
