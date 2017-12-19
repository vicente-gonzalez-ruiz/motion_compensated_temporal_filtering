#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

#  Decompresses data movement.
#
#  The decompressor will find on the first level, a field of
#  bidirectional movement has been solely uncorrelated bidirectionally
#  (bidirectional decorrelation exploits the redundancy that exists in
#  a bidirectional vector, where the vector in a direction generally
#  like the other, although with opposite sign).
#
#  Once the field in the first level has been restored, it can serve
#  as a reference for two fields next level of resolution (interlevel
#  decorrelation). Specifically, divide by two, the motion vectors and
#  we have a prediction.
#
#  In this second level of resolution (and the following) is not
#  necessary decorrelate bidirectionally. Because the interlevel
#  decorrelation, bidirectional starts from correlated fields, and
#  this will cause bidirectional decorrelation automatically.
#

import os
import sys
from GOP import GOP
from subprocess import check_call
from subprocess import CalledProcessError
from arguments_parser import arguments_parser

#MOTION_DECODER_NAME = "gzip"
#MOTION_DECODER_NAME = "kdu_v_expand"
## Refers to the codec to be used for compression of motion information.
MCTF_MOTION_CODEC    = os.environ["MCTF_MOTION_CODEC"]

parser = arguments_parser(description="Expands the motion data.")
parser.GOPs()
parser.TRLs()
parser.block_size()
parser.pixels_in_x()
parser.pixels_in_y()

args = parser.parse_known_args()[0]
GOPs = int(args.GOPs)
TRLs = int(args.TRLs)
block_size = int(args.block_size)
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)

gop=GOP()
GOP_size = gop.get_size(TRLs)
pictures = (GOPs - 1) * GOP_size + 1

blocks_in_x = pixels_in_x // block_size
blocks_in_y = pixels_in_y // block_size

iteration = 1
fields = pictures // 2
while iteration <= (TRLs - 1) :

    try:
        check_call("mctf motion_expand_" + MCTF_MOTION_CODEC
                   + " --file=" + "\""   + "motion_residue_" + str(iteration) + "\""
                   + " --blocks_in_y="   + str(blocks_in_y)
                   + " --blocks_in_x="   + str(blocks_in_x)
                   + " --fields="        + str(fields)
                   + " --pictures="      + str(pictures)
                   ,shell=True)
    except CalledProcessError :
        sys.exit(-1)

    fields //= 2
    iteration += 1
    
# Decorrelation bidirectional level lower temporal resolution.
try:
    check_call("mctf bidirectional_motion_correlate"
               + " --blocks_in_y=" + str(blocks_in_y)
               + " --blocks_in_x=" + str(blocks_in_x)
               + " --fields="      + str(GOPs)
               + " --input="       + "\"" + "motion_residue_" + str(TRLs - 1) + "\""
               + " --output="      + "\"" + "motion_"         + str(TRLs - 1) + "\""
               , shell=True)
except CalledProcessError :
    sys.exit(-1)

# Decorrelation between levels of resolution.
iteration = TRLs - 1 # total iterations
while iteration > 1 :
    
    iteration -= 1
    fields = pictures // (2**iteration)

    try:
        check_call("mctf interlevel_motion_correlate"
                   + " --blocks_in_y="         + str(blocks_in_y)
                   + " --blocks_in_x="         + str(blocks_in_x)
                   + " --fields_in_predicted=" + str(fields)
                   + " --reference="           + "\"" + "motion_"         + str(iteration + 1) + "\""
                   + " --predicted="           + "\"" + "motion_"         + str(iteration)     + "\""
                   + " --residue="             + "\"" + "motion_residue_" + str(iteration)     + "\""
                   , shell=True)
    except CalledProcessError :
        sys.exit(-1)
