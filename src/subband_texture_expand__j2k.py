#!/bin/sh
''''exec python3 -O -- "$0" ${1+"$@"} # '''
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
from colorlog import ColorLog
import logging

log = ColorLog(logging.getLogger("subband_texture_expand__j2k"))
log.setLevel('ERROR')
shell.setLogger(log)

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

    fn = file + "/" + str('%04d' % p)

    command = "trace kdu_expand" \
              + " -i " + fn + '.' + IMG_EXT \
              + " -o " \
              + "/tmp/0.pgm," \
              + "/tmp/1.pgm," \
              + "/tmp/2.pgm"

    if not __debug__:
        command += " > /dev/null 2> /dev/null"

    try:
        shell.run(command)
        shell.run("trace convert -endian LSB /tmp/0.pgm " + fn + "_0.pgm")
        #shell.run("trace mv /tmp/1 " + fn + "_0.pgm")
        shell.run("trace convert -endian LSB /tmp/1.pgm " + fn + "_1.pgm")
        #shell.run("trace mv /tmp/1 " + fn + "_1.pgm")
        shell.run("trace convert -endian LSB /tmp/2.pgm " + fn + "_2.pgm")
        #shell.run("trace mv /tmp/1 " + fn + "_2.pgm")
    except:
        log.warning("{} is missing".format(fn + '.' + IMG_EXT))

#        shell.run(command)
#        shell.run("trace convert -endian LSB /tmp/0.pgm " + fn + "_0.pgm")
#        #shell.run("trace mv /tmp/1 " + fn + "_0.pgm")
#        shell.run("trace convert -endian LSB /tmp/1.pgm " + fn + "_1.pgm")
#        #shell.run("trace mv /tmp/1 " + fn + "_1.pgm")
#        shell.run("trace convert -endian LSB /tmp/2.pgm " + fn + "_2.pgm")
#        #shell.run("trace mv /tmp/1 " + fn + "_2.pgm")

    p += 1
