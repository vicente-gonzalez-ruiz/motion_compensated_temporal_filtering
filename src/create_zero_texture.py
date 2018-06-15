#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# Create a file with texture where each pixel is 128.

import sys
from arguments_parser import arguments_parser
from colorlog import ColorLog
import logging
#import colorlog
import struct

log = ColorLog(logging.getLogger("create_zero_texture"))
log.setLevel('ERROR')

parser = arguments_parser(description="Creates a \"empty\" (unsigned char = 128) texture image file.")
parser.add_argument("--file",
                    help="File that contains the texture.",
                    default="empty.pgm")
parser.pixels_in_x()
parser.pixels_in_y()

args = parser.parse_known_args()[0]

file = args.file

pixels_in_x = int(args.pixels_in_x)
log.info("pixels_in_x={}".format(pixels_in_x))

pixels_in_y = int(args.pixels_in_y)
log.info("pixels_in_y={}".format(pixels_in_y))

f = open(file, "wb")
f.write(b"P5\n")
f.write(bytes(str.encode("{} {}\n".format(pixels_in_x, pixels_in_y))))
f.write(b"255\n")
for a in range(pixels_in_x * pixels_in_y) :
    f.write(struct.pack('B', 128))
f.close()
