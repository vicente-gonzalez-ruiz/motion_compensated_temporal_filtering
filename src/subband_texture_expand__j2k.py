#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# Decodes a subband of texture.

# {{{ Imports

import sys
import math
import struct
import os
from arguments_parser import arguments_parser
from shell import Shell as shell
from colorlog import log
import os

# }}}

# {{{ Arguments parsing

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
log.info("file={}".format(file))

pictures = int(args.pictures)
log.info("pictures={}".format(pictures))

pixels_in_x = int(args.pixels_in_x)
log.info("pixels_in_x={}".format(pixels_in_x))

pixels_in_y = int(args.pixels_in_y)
log.info("pixels_in_y={}".format(pixels_in_y))

# }}}

IMG_EXT = os.environ["MCTF_IMG_EXT"]

p = 0
while p < pictures:

    pic_number = str('%04d' % p)
    
    shell.run("trace kdu_expand"
              + " -i " + file + "/" + pic_number + "." + IMG_EXT
              + " -o "
              + file + "/" + pic_number + "_0.pgm,"
              + file + "/" + pic_number + "_1.pgm,"
              + file + "/" + pic_number + "_2.pgm")

    p += 1
