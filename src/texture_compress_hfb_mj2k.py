#!/usr/bin/python
# -*- coding: iso-8859-15 -*-


## @file texture_compress_hfb_mj2k.py
#  Compress the HFB texture data, using Motion JPEG 2000.
#  The two main steps performed are:
#  - Create a header 'vix' for YUV file and concatenates both.
#  - Encode components.
#
#  @authors Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package texture_compress_hfb_mj2k
#  Compress the HFB texture data, using Motion JPEG 2000.
#  The two main steps performed are:
#  - Create a header 'vix' for YUV file and concatenates both.
#  - Encode components.

import sys
import os
from subprocess import check_call
from subprocess import CalledProcessError
import arguments_parser

## Number of components.
COMPONENTS = 3
## Number of bytes per component.
BYTES_PER_COMPONENT = 1
## File that contains the HFB data.
file = ""
## Controls the quality level and the bit-rate of the code-stream.
slopes = os.environ["SLOPES"]
## Number of images to process.
pictures = 33
## Width of the pictures.
pixels_in_x = 352
## Height of the pictures.
pixels_in_y = 288
## Controls the quality level and the bit-rate of the code-stream.
quantizations = 45000
## Current temporal iteration.
subband = 1
## Number of Spatial Resolution Levels.
SRLs = 5

## The parser module provides an interface to Python's internal parser
## and byte-code compiler.
parser = arguments_parser(description="Compress the HFB texture data using JPEG 2000.")
parser.add_argument("--file", help="file that contains the HFB data. Default = {})".format(file))
parser.pictures()
parser.pixels_in_x()
parser.pixels_in_y()
parser.quantizations()
parser.add_argument("--subband", help="subband to compress. Default = {})".format(file))
parser.SRLs()

## A script may only parse a few of the command-line arguments,
## passing the remaining arguments on to another script or program.
args = parser.parse_known_args()[0]
if args.file:
    file = args.file
if args.pictures:
    pictures = int(args.pictures)
if args.pixels_in_x:
    pixels_in_x = int(args.pixels_in_x)
if args.pixels_in_y:
    pixels_in_y = int(args.pixels_in_y)
if args.quantizations:
    quantizations = args.quantizations
if args.subband:
    subband = int(args.subband)
if args.SRLs:
    SRLs = int(args.SRLs)

## Number of levels of the DWT.
dwt_levels = SRLs - 1

## Create a header 'vix' for YUV file.
fd = open( file + ".vix", 'w' )
fd.write("vix\n")
fd.write(">VIDEO<\n")
fd.write("1.0 0\n")
fd.write(">COLOUR<\n")
fd.write("YCbCr\n")
fd.write(">IMAGE<\n")
#fd.write("signed word 16 little-endian\n")
#fd.write("signed word 10 little-endian\n")
fd.write("unsigned char 8 little-endian\n")
fd.write("%d " % pixels_in_x)
fd.write("%d " % pixels_in_y)
fd.write("%d\n" % COMPONENTS)
fd.write("1 1\n")
fd.write("2 2\n")
fd.write("2 2\n")
fd.close()

## Concatenates both a header 'vix' and YUV file. Then encode.
#os.system("cat " + file + ".yuv16 >> " + file + ".vix" )
try:
    check_call("trace cat " + file + " >> " + file + ".vix", shell=True)
except CalledProcessError:
    sys.exit(-1)

# Haar irreversible
#compressor_params += " "
#compressor_params += "Catk=2 Kextension:I2=CON Kreversible:I2=no Ksteps:I2=\{1,0,0,0\},\{1,0,0,0\} Kcoeffs:I2=-1.0,0.5"

# 5/3 irreversible
#compressor_params += " "
#compressor_params += "Catk=2 Kextension:I2=SYM Kreversible:I2=no Ksteps:I2=\{2,0,0,0\},\{2,-1,0,0\} Kcoeffs:I2=-0.5,-0.5,0.25,0.25"

# Encode.
try:
    check_call("trace kdu_v_compress" +
               " -i " + file + ".vix" +
               " -o " + file + ".mjc" +
               " -slope " + quantizations +
               " -no_weights"  +
               " Clevels=" + str(dwt_levels),
               shell=True)
except CalledProcessError:
    sys.exit(-1)
