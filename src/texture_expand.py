#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

## @file texture_expand.py
#  Decompress the texture. There are a different number of (compressed)
#  texture streams called "low_X", "high_X", "high_X-1", ..., where X
#  is the bumber of temporal resolution levels - 1.
#
#  @authors Jose Carmelo Maturana-Espinosa\n Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package texture_expand
#  Decompress the texture. There are a different number of (compressed)
#  texture streams called "low_X", "high_X", "high_X-1", ..., where X
#  is the bumber of temporal resolution levels - 1.

import sys
import os
from GOP import GOP
from subprocess import check_call
from subprocess import CalledProcessError
from MCTF_parser import MCTF_parser

## Refers to the codec to be used for compression of texture
## information.
MCTF_TEXTURE_CODEC = os.environ["MCTF_TEXTURE_CODEC"]
## Refers to low frequency subbands.
LOW         = "low"
## Refers to high frequency subbands.
HIGH        = "high"
## Number of Group Of Pictures to process.
GOPs        = 1
## Number of Temporal Resolution Levels.
TRLs        = 4
## Number of Spatia Resolution Levels.
SRLs        = 5
## Optional and developing parameter indicates whether to extract the
#  codestream to a given bit-rate. The bit-rate control is performed
#  in transcode.py, a detailed manner, and therefore its use is
#  recommended for this purpose.
rates       = "0.0,0.0,0.0,0.0,0.0"
## Width of the pictures.
pixels_in_x = "352,352,352,352,352"
## Height of the pictures.
pixels_in_y = "288,288,288,288,288"

## The parser module provides an interface to Python's internal parser
## and byte-code compiler.
parser = MCTF_parser(description="Expands the texture.")
parser.GOPs(GOPs)
parser.SRLs(SRLs)
parser.TRLs(TRLs)
parser.rates(rates)
parser.pixels_in_x(pixels_in_x)
parser.pixels_in_y(pixels_in_y)

## A script may only parse a few of the command-line arguments,
## passing the remaining arguments on to another script or program.
args = parser.parse_known_args()[0]
if args.GOPs:
    GOPs = int(args.GOPs)
if args.SRLs:
    SRLs = int(args.SRLs)
if args.TRLs:
    TRLs = int(args.TRLs)
if args.rates:
    rates = str(args.rates)
if args.pixels_in_x:
    pixels_in_x = str(args.pixels_in_x)
if args.pixels_in_y:
    pixels_in_y = str(args.pixels_in_y)


## Initializes the class GOP (Group Of Pictures).
gop=GOP()
## Extract the value of the size of a GOP, that is, the number of
## images.
GOP_size = gop.get_size(TRLs)
## Number of images to process.
_pictures = pictures = GOPs * GOP_size + 1



# Decompression HIGH frequency subbands.
#---------------------------------------
if TRLs > 1 :

    ## Number of temporal subbands.
    subband = TRLs - 1
    while subband > 0 :

        ## Current picture iteration.
        pictures = _pictures
        ## Current temporal iteration.
        j = 0
        while j < subband :
            pictures = ( pictures + 1 ) / 2
            j += 1

        try:
            check_call("mctf texture_expand_fb_" + MCTF_TEXTURE_CODEC
#           check_call("mctf texture_expand_hfb_" + MCTF_TEXTURE_CODEC
                       + " --file="        + "\"" + HIGH + "_" + str(subband) + "\""
                       + " --rate="        + str(rates.split(',')[TRLs-subband])
                       + " --pictures="    + str(pictures - 1)
                       + " --pixels_in_x=" + str(pixels_in_x.split(',')[TRLs-subband])
                       + " --pixels_in_y=" + str(pixels_in_y.split(',')[TRLs-subband])
                       + " --subband="     + str(subband)
                       + " --SRLs="        + str(SRLs)
                       , shell=True)
        except CalledProcessError:
            sys.exit(-1)

        subband -= 1



# Decompression LOW frequency subbands.
#--------------------------------------
try:
    check_call("mctf texture_expand_fb_" + MCTF_TEXTURE_CODEC
               + " --file="        + "\"" + LOW + "_" + str(TRLs - 1) + "\""
               + " --rate="        + str(rates.split(',')[0])
               + " --pictures="    + str(GOPs+1)
               + " --pixels_in_x=" + str(pixels_in_x.split(',')[0])
               + " --pixels_in_y=" + str(pixels_in_y.split(',')[0])
               + " --subband="     + str(TRLs)
               + " --SRLs="        + str(SRLs)
               , shell=True)
except CalledProcessError:
    sys.exit(-1)
