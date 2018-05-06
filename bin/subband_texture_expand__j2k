#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

#  Decompress textures, using the codec J2K. 
#  The two main steps performed are:
#  - Decode components and
#  - Multiplexing components (Y, U y V).
#
#  If there is no file textures of the current iteration, is created
#  with a neutral texture.

import shutil
import subprocess as sub
import sys
import math
import struct
import os
from subprocess import check_call
from subprocess import CalledProcessError
from arguments_parser import arguments_parser
import logging

logging.basicConfig()
log = logging.getLogger("subband_texture_expand__j2k")

parser = arguments_parser(description="Expands the the LFB y HFB texture data using JPEG 2000.")
parser.add_argument("--file",
                    help="File that contains the LFB or HFB data.",
                    default="")
parser.add_argument("--pictures",
                    help="Number of pictures to expand.",
                    default=1)
parser.pixels_in_x()
parser.pixels_in_y()

args = parser.parse_known_args()[0]
file = args.file
pictures = int(args.pictures)
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)

def decode (component, image_number) :

    try:
        image_filename = file + "_" + str('%04d' % image_number) + "_" + str(component)

        f = open(image_filename + ".j2c", "rb")
        f.close()

        # Decode.
        try:
            check_call("trace kdu_expand"
                       + " -i " + image_filename + ".j2c"
                       + " -o " + image_filename + ".rawl"
                       , shell=True)
        except CalledProcessError :
            sys.exit(-1)

    except:
        # If there is no file textures of the current iteration, is
        # created with a neutral texture.

        f = open(image_filename + ".rawl", "wb")
        for a in range(pixels_in_x * pixels_in_y) :
            f.write(struct.pack('B', 128))  # BYTES_PER_COMPONENT = 1   # 1 byte for components used unweighted.
            #f.write('%c' % 128) # BYTES_PER_COMPONENT = 2   # 2 bytes for weighted or components that are used weighted.
        f.close()

    # MUX
    try:
        check_call("trace cat " + image_filename + ".rawl >> " + file, shell=True)
    except CalledProcessError:
        sys.exit(-1)

image_number = 0
while image_number < pictures :

    decode ('Y', image_number)
    decode ('U', image_number)
    decode ('V', image_number)

    image_number += 1
