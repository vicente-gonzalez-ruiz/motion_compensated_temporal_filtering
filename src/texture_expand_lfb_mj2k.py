#!/usr/bin/python
# -*- coding: iso-8859-15 -*-


## @file texture_expand_lfb_mj2k.py
#  Expand the LFB texture data, using Motion JPEG 2000.
#  The two main steps performed are:
#  - Decode components and
#  - Removes the header 'vix' from YUV file.
#
#  @authors Jose Carmelo Maturana-Espinosa\n Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package texture_expand_lfb_mj2k
#  Expand the LFB texture data, using Motion JPEG 2000.
#  The two main steps performed are:
#  - Decode components and
#  - Removes the header 'vix' from YUV file.


import sys
from subprocess import check_call
from subprocess import CalledProcessError
import arguments_parser

## File that contains the LFB data.
file = ""
## Number of images to process.
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



# Decode components and removes the header 'vix' from YUV file.
try:
    check_call("trace kdu_v_expand" +
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
