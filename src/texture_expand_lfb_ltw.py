#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-


## @file texture_expand_lfb_ltw.py
#  Expand the LFB texture data, using LTW.
#  The two main steps performed are:
#  - Decode components and
#  - Multiplexing components (Y, U y V).
#
#  @authors Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package texture_expand_lfb_ltw
#  Expand the LFB texture data, using LTW.
#  The two main steps performed are:
#  - Decode components and
#  - Multiplexing components (Y, U y V).

import sys
import os
from subprocess import check_call
from subprocess import CalledProcessError
import arguments_parser

## File that contains the LFB data.
file = ""
## Number of textures to process.
textures = 33

## The parser module provides an interface to Python's internal parser
## and byte-code compiler.
parser = arguments_parser(description="Expands the the LFB texture data using LTW.")
parser.add_argument("--file", help="file that contains the LFB data. Default = {})".format(file))
parser.textures()

## A script may only parse a few of the command-line arguments,
## passing the remaining arguments on to another script or program.
args = parser.parse_known_args()[0]
if args.file:
    file = args.file
if args.textures:
    textures = int(args.textures)



# Decode and multiplexing all components (YUV).
#----------------------------------------------
## Current texture number iteration.
texture_number = 0
while texture_number < textures:

    ## Current texture number iteration.
    str_texture_number = '%04d' % texture_number

    # Y
    #---
    ## Current texture name iteration.
    texture_filename = file + "_Y_" + str_texture_number

    try:
        # Decode a component.
        check_call("trace ltw -D "
                   + " -i " + texture_filename + ".ltw"
                   + " -o " + texture_filename + ".raw"
                   + " -c " + os.environ["MCTF"] + "/bin/config-lfb.txt"
                   + " -a 0"
                   + " -s 0",
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)


    try:
        check_call("trace cat " + texture_filename + ".raw >> " + file, shell=True)
    except CalledProcessError:
        sys.exit(-1)


    # U
    #---
    texture_filename = file + "_U_" + str_texture_number

    try:
        check_call("trace ltw -D "
                   + " -i " + texture_filename + ".ltw"
                   + " -o " + texture_filename + ".raw"
                   + " -c " + os.environ["MCTF"] + "/bin/config-lfb.txt"
                   + " -a 0"
                   + " -s 0",
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

    try:
        check_call("trace cat " + texture_filename + ".raw >> " + file, shell=True)
    except CalledProcessError:
        sys.exit(-1)

    # V
    #---
    texture_filename = file + "_V_" + str_texture_number

    try:
        check_call("trace ltw -D "
                   + " -i " + texture_filename + ".ltw"
                   + " -o " + texture_filename + ".raw"
                   + " -c " + os.environ["MCTF"] + "/bin/config-lfb.txt"
                   + " -a 0"
                   + " -s 0",
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

    try:
        check_call("trace cat " + texture_filename + ".raw >> " + file, shell=True)
    except CalledProcessError:
        sys.exit(-1)

    texture_number += 1
