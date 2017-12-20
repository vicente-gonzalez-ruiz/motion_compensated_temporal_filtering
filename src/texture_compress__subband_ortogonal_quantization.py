#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

#  Compress textures (temporal subbands) generated from the analysis
#  phase. The number of bits allocated to each subband depends on
#  the "slopes" parameter, which controls the quality of each quality
#  layer (such as a quantization factor) in each image of each
#  subband. Therefore, the number of quality layers equals the
#  number of slopes. The optimal bit-rate control should be performed
#  in decompression time using the "extract" program (See
#  transcode.py).

import os
import sys
import display
import math
from GOP import GOP
from subprocess import check_call
from subprocess import CalledProcessError
from arguments_parser import arguments_parser

MCTF_TEXTURE_CODEC   = os.environ["MCTF_TEXTURE_CODEC"]
HIGH                 = "high"            # High frequency subbands.
LOW                  = "low"             # Low frequency subbands.
range_quantization   = 46000.0 - 42000.0 # Useful range of quantification

parser = arguments_parser(description="Compress the texture.")
parser.GOPs()
parser.texture_layers()
parser.pixels_in_x()
parser.pixels_in_y()
parser.texture_quantization()
parser.quantization_step()
parser.TRLs()
parser.SRLs()
parser.using_gains()

args = parser.parse_known_args()[0]
GOPs = int(args.GOPs)
layers = int(args.texture_layers)
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
quantization = args.texture_quantization
quantization_step = int(args.quantization_step)
TRLs = int(args.TRLs)
SRLs = int(args.SRLs)
using_gains = str(args.using_gains)

# print "texture_compress.py ; Q= " + str(quantization)
# raw_input("\ntexture_compress.py Press ENTER to continue ...")

gop      = GOP()
GOP_size = gop.get_size(TRLs)

## Number of images to process.
pictures = (GOPs - 1) * GOP_size + 1

if   TRLs == 1 :
    pass
elif TRLs == 2 :
    GAINS = [1.2460784922] # [L1/H1]
elif TRLs == 3 :
    GAINS = [1.8652117304, 1.2500103877] # [L2/H2, L2/H1]
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

## Distance in the quantization step, between different temporal subbands.
quantization_step_subband = 256 / math.sqrt(2)

## Slope distance for each quality layer in the same temporal subband. If a
## quantization_step is specified by parameter, one proportional to
## the number of layers and the useful range of quantification is
## used.
if quantization_step == 0 and layers > 1 :
    quantization_step = int(round( range_quantization / (layers-1) ))

# Slopes for layers
if using_gains == "automatic_kakadu" :
    SLOPES = [["automatic_kakadu"]] * TRLs
else :
    if using_gains == "gains" :
        ## LAST QUALITY LAYER of each temporal subband according to the GAINS of
        ## the number of TLRs the codestream. The order of subbands in the
        ## list is [L4, H4, H3, H2, H1]. After determines a slope for each
        ## quality layer in the same temporal subband.
        SLOPES = [[int(quantization)]]   # Temporal subband L
        for sub in range (0, TRLs-1) :   # Temporal subbands Hs with GAINS
            SLOPES.append( [ int(round( SLOPES[0][0] + (quantization_step_subband * GAINS[sub]) )) ] )
    elif using_gains == "nogains" :
        ## LAST QUALITY LAYER of each temporal subband same to quantization
        ## parameter.
        SLOPES = [[int(quantization)]]   # Temporal subband L
        for sub in range (0, TRLs-1) :   # Temporal subbands Hs with GAINS
            SLOPES.append( [ int(quantization) ] )
    else :
        sys.stderr.write("Available options: kakadu, gains, nogains. Not available: " + str(using_gains) + ". Check texture_compress.py")
        exit (0)

    # OTHERS QUALITY LAYERs in the same temporal subband, determines a
    # different slope accord to first slope layer AND
    # range_quantization
    for sub in range (0, TRLs) :
        for layer in range (0, layers-1) :
            SLOPES[sub].append(int(round( SLOPES[sub][layer] + quantization_step )))
            
## Stored in a file the slopes used for compression.
f_slopes = open ("slopes", 'w')
f_slopes.write ('\n'.join(map(str, SLOPES)))
f_slopes.close ()

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
                   + " --quantization=\""   + ','.join(map(str, SLOPES[TRLs-subband])) + "\""
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
               + " --quantization=\""   + ','.join(map(str, SLOPES[0])) + "\""
               + " --subband="          + str(subband)
               + " --SRLs="             + str(SRLs)
               , shell=True)
except:
    sys.exit(-1)
