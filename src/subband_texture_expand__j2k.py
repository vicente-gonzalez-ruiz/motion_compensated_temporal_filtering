#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

#  Decompress textures, using the codec J2K. 
#  The two main steps performed are:
#  - Decode components and
#  - Multiplexing components (Y, U y V).
#
#  If there is no file textures of the current iteration, is created
#  with a neutral texture.

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

def decode (component, picture_number) :

    picture_filename = file + "_" + str('%04d' % picture_number) + "_" + str(component)

    try:
        check_call("trace kdu_expand"
                   + " -i " + picture_filename + ".j2c"
                   + " -o " + picture_filename + ".rawl"
                   , shell=True)
        check_call("trace cat " + picture_filename + ".rawl >> " + file, shell=True)
    except:
        print("Unable to open {}".format(picture_filename))
        check_call("trace cat /tmp/128 >> "+ file, shell=True)


f = open("/tmp/128", "wb")
for a in range(pixels_in_x * pixels_in_y) :
    f.write(struct.pack('B', 128))  # BYTES_PER_COMPONENT = 1   # 1 byte for components used unweighted.
f.close()
        
p = 0
while p < pictures:

    decode ('Y', picture_number)
    decode ('U', picture_number)
    decode ('V', picture_number)

    p += 1
