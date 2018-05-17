#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# Decodes a subband of texture.

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

parser = arguments_parser(description="Decodes a subband of texture.")
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

    fn = file + "_" + str('%04d' % picture_number) + "_" + str(component)

    shell.run("trace kdu_expand"
              + " -i " + fn + ".jp2"
              + " -o " + fn + ".rawl")

p = 0
while p < pictures:

    decode ('0', picture_number)
    decode ('1', picture_number)
    decode ('2', picture_number)

    p += 1
