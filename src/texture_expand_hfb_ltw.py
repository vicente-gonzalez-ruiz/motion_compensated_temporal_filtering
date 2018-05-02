#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-


## @file texture_expand_hfb_ltw.py
#  Expand the HFB texture data, using LTW.
#  The two main steps performed are:
#  - Decode components and
#  - Multiplexing components (Y, U y V).
#
#  @authors Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package texture_expand_hfb_ltw
#  Expand the HFB texture data, using LTW.
#  The two main steps performed are:
#  - Decode components and
#  - Multiplexing components (Y, U y V).

import sys
import os
from subprocess import check_call
from subprocess import CalledProcessError
import arguments_parser

## File that contains the HFB data.
file = ""
## Number of images to process.
pictures = 33

## The parser module provides an interface to Python's internal parser
## and byte-code compiler.
parser = arguments_parser(description="Expands the the HFB texture data using LTW.")
parser.add_argument("--file", help="file that contains the LFB data. Default = {})".format(file))
parser.pictures()

## A script may only parse a few of the command-line arguments,
## passing the remaining arguments on to another script or program.
args = parser.parse_known_args()[0]
if args.file:
    file = args.file
if args.pictures:
    pictures = int(args.pictures)



# Decode and multiplexing all components (YUV).
#----------------------------------------------
## Current image number iteration.
image_number = 0
while image_number < pictures:

    ## Current image number iteration.
    str_image_number = '%04d' % image_number

    # Y
    #---
    ## Current image name iteration.
    image_filename = file + "_Y_" + str_image_number

    # Decode a component.
    try:
        check_call("trace ltw -D "
                   + " -i " + image_filename + ".ltw"
                   + " -o " + image_filename + ".raw"
                   + " -c " + os.environ["MCTF"] + "/bin/config-hfb.txt"
                   + " -a 0"
                   + " -s 0",
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

    try:
        check_call("trace cat " + image_filename + ".raw >> " + file, shell=True)
    except CalledProcessError:
        sys.exit(-1)


    # U
    #---
    image_filename = file + "_U_" + str_image_number

    # Decode a component.
    try:
        check_call("trace ltw -D "
                   + " -i " + image_filename + ".ltw"
                   + " -o " + image_filename + ".raw"
                   + " -c " + os.environ["MCTF"] + "/bin/config-hfb.txt"
                   + " -a 0"
                   + " -s 0",
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

    try:
        check_call("trace cat " + image_filename + ".raw >> " + file, shell=True)
    except CalledProcessError:
        sys.exit(-1)

    # V
    #---
    image_filename = file + "_V_" + str_image_number

    # Decode a component.
    try:
        check_call("trace ltw -D "
                   + " -i " + image_filename + ".ltw"
                   + " -o " + image_filename + ".raw"
                   + " -c " + os.environ["MCTF"] + "/bin/config-hfb.txt"
                   + " -a 0"
                   + " -s 0",
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

    try:
        check_call("trace cat " + image_filename + ".raw >> " + file, shell=True)
    except CalledProcessError:
        sys.exit(-1)

    image_number += 1
