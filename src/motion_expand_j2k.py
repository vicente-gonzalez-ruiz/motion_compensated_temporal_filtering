#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

## @file motion_expand_j2k.py
#  Decompressing data movement, using the codec J2K.
#  The decompression consists of two major steps:\n
#  - Decode components (lossless compression).
#  - Multiplexing components.
#
#  If there is no vector file, a file is created with linear
#  movement. That is, a file of zeros.
#
#  @authors Jose Carmelo Maturana-Espinosa\n Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package motion_expand_j2k
#  Decompressing data movement, using the codec J2K.
#  The decompression consists of two major steps:\n
#  - Decode components (lossless compression).
#  - Multiplexing components.
#
#  If there is no vector file, a file is created with linear
#  movement. That is, a file of zeros.


import os
import sys
from subprocess import check_call
from subprocess import CalledProcessError
from MCTF_parser import MCTF_parser


## Number of components.
COMPONENTS      = 4
## Number of bytes of each component.
BYTES_COMPONENT = 2
## Number of bits of each component.
BITS_COMPONENT  = BYTES_COMPONENT * 8
## Number of blocks in the X direction.
blocks_in_x = 0
## Number of blocks in the Y direction.
blocks_in_y = 0
## Number of pictures of a temporal resolution.
fields      = 0
## Name of the file with the motion fields.
file        = ""
# Number of discard level.
# discard_levels = 0

## The parser module provides an interface to Python's internal parser
#  and byte-code compiler.
parser = MCTF_parser(description="Expands the motion data using JPEG 2000.")
#parser.add_argument("--discard_levels", help="number of discard level. (Default = {})".format(discard_levels))
parser.add_argument("--blocks_in_x",     help="number of blocks in the X direction. (Default = {})".format(blocks_in_x))
parser.add_argument("--blocks_in_y",     help="number of blocks in the Y direction. (Default = {})".format(blocks_in_y))
parser.add_argument("--fields",          help="number of fields in to compress. (Default = {})".format(fields))
parser.add_argument("--file",            help="name of the file with the motion fields. (Default = {})".format(file))

## A script may only parse a few of the command-line arguments,
#  passing the remaining arguments on to another script or program.
args = parser.parse_known_args()[0]
#if args.discard_levels:
#    discard_levels = int(args.discard_levels)
if args.blocks_in_x:
    blocks_in_x = int(args.blocks_in_x)
if args.blocks_in_y:
    blocks_in_y = int(args.blocks_in_y)
if args.fields:
    fields = int(args.fields)
if args.file:
    file = args.file





# Expand each field.
#-------------------
for comp_number in range (0, COMPONENTS) :

    # Decode components.
    #-------------------
    for campoMov_number in range (0, fields) :

        ## Refers to a particular component from a field of movement.
        campoMov_name = file + "_comp" + str(comp_number) + "_" + str('%04d' % campoMov_number)

        try:
            ## File compressed motion vectors. If there is no vector
            #  file, a file is created with linear movement. That is,
            #  a file of zeros.
            f = open(campoMov_name + ".j2c", "rb")
            f.close()

            try:
                check_call("trace kdu_expand"
                           + " -i " + str(campoMov_name) + ".j2c"
                           + " -o " + str(campoMov_name) + ".rawl"
                           , shell=True)
            except CalledProcessError:
                sys.exit(-1)

        except: 
            # If there is no vector file, a file is created with
            # linear movement. That is, a file of zeros.
            # check_call("echo Motion interpolation..", shell=True)
            # raw_input("")
            
            f = open(campoMov_name + ".rawl", "wb")
            for a in xrange(BYTES_COMPONENT * blocks_in_y * blocks_in_x) :
                f.write('%c' % 0)
            f.close()

# Multiplexing.
#--------------
for campoMov_number in range (0, fields) :

    try:
        ## Component 1.
        f0 = open(file + "_comp0_" + str('%04d' % campoMov_number) + ".rawl", "rb")
        ## Component 2.
        f1 = open(file + "_comp1_" + str('%04d' % campoMov_number) + ".rawl", "rb")
        ## Component 3.
        f2 = open(file + "_comp2_" + str('%04d' % campoMov_number) + ".rawl", "rb")
        ## Component 4.
        f3 = open(file + "_comp3_" + str('%04d' % campoMov_number) + ".rawl", "rb")
        # Component 1, Component 2, Component 3 y Component 4.
        f  = open(file + "_"       + str('%04d' % campoMov_number) + ".join", "wb")

        while 1 : # 792 -> 198 -> 49.5
            ## Multiplexing all components.
            comps = f0.read(BYTES_COMPONENT) + f1.read(BYTES_COMPONENT) + f2.read(BYTES_COMPONENT) + f3.read(BYTES_COMPONENT)
            if len(comps) == (BYTES_COMPONENT * COMPONENTS) :
                f.write(comps)
            else :
                break

        f0.close()
        f1.close()
        f2.close()
        f3.close()
        f.close()

    except CalledProcessError :
        sys.exit(-1)

# cat file_????.join > file
check_call("trace cat " + file + "_????.join > " + file, shell=True)

