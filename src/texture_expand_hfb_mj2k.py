#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-


## @file texture_expand_hfb_mj2k.py
#  Expand the HFB texture data, using Motion JPEG 2000.
#  The two main steps performed are:
#  - Decode components and
#  - Removes the header 'vix' from YUV file.
#
#  If there is no file textures of the current iteration, is created
#  with a neutral texture.
#
#  @authors Jose Carmelo Maturana-Espinosa\n Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package texture_expand_hfb_mj2k
#  Expand the HFB texture data, using Motion JPEG 2000.
#  The two main steps performed are:
#  - Decode components and
#  - Removes the header 'vix' from YUV file.
#
#  If there is no file textures of the current iteration, is created
#  with a neutral texture.

import sys
from subprocess import check_call
from subprocess import CalledProcessError
import arguments_parser

## File that contains the HFB data.
file = ""
## Number of pictures to process.
pictures = 33

## The parser module provides an interface to Python's internal parser
## and byte-code compiler.
parser = arguments_parser(description="Expands the the LFB texture data using JPEG 2000.")
parser.add_argument("--file", help="file that contains the LFB data. Default = {})".format(file))
parser.pictures()

## A script may only parse a few of the command-line arguments,
## passing the remaining arguments on to another script or program.
args = parser.parse_known_args()[0]
if args.file:
    file = args.file
if args.pictures:
    pictures = int(args.pictures)

try:
    ## File that contains the HFB data.
    f = open(file + ".mjc", "rb")
    f.close()

except:
    ##  If there is no file textures of the current iteration, is created
    ##  with a neutral texture.
    byte = 128
    f = open(file, "wb")
    for a in xrange (int(math.floor(pictures * pixels_in_x * pixels_in_y * 1.5))):
        f.write('%c' % byte)
    f.close()
    exit(1)

# Decode.
try:
    check_call("trance kdu_v_expand" +
               " -i " + file + ".mjc" +
               " -o " + file + ".vix",
               shell=True)
except CalledProcessError:
        sys.exit(-1)

# Removes the header 'vix' from YUV file.
try:
    check_call("trace vix2raw < " + file + ".vix > " + file, shell=True)
except CalledProcessError:
        sys.exit(-1)

