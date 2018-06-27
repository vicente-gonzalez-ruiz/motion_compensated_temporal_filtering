#!/bin/sh
''''exec python3 -O -- "$0" ${1+"$@"} # '''
#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# {{{ Imports

from shell import Shell as shell
from arguments_parser import arguments_parser
# from defaults import Defaults
import os
from colorlog import ColorLog
import logging

log = ColorLog(logging.getLogger("subband_texture_compress__j2k"))
log.setLevel('ERROR')
shell.setLogger(log)

# }}}

# {{{ Arguments parsing

parser = arguments_parser(description="Compress texture data using JPEG 2000.")
parser.add_argument("--file",
                    help="File that contains the texture data.",
                    default="")
parser.add_argument("--pictures",
                    help="Number of pictures to compress.",
                    default=3)
parser.pixels_in_x()
parser.pixels_in_y()
parser.layers()
parser.SRLs()
parser.slope()

args = parser.parse_known_args()[0]
file = args.file
layers = int(args.layers)
number_of_pictures = int(args.pictures)
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
SRLs = int(args.SRLs)
slope = int(args.slope)

log.info("file={}".format(file))
log.info("layers={}".format(layers))
log.info("pictures={}".format(number_of_pictures))
log.info("pixels_in_x={}".format(pixels_in_x))
log.info("pixels_in_y={}".format(pixels_in_y))
log.info("SRLs={}".format(SRLs))
log.info("slope={}".format(slope))

# }}}

BYTES_PER_COMPONENT = 1 # 2

IMG_EXT = os.environ["MCTF_IMG_EXT"]

Clevels = SRLs - 1
if Clevels < 0:
   Clevels = 0

picture = 0
while picture < number_of_pictures:

    fn = file + "/" + str('%04d' % picture)

    shell.run("trace convert -endian LSB " + fn + "_0.pgm tmp_0.pgm")
    #shell.run("trace mv /tmp/1 " + fn + "_0.pgm")
    shell.run("trace convert -endian LSB " + fn + "_1.pgm tmp_1.pgm")
    #shell.run("trace mv /tmp/1 " + fn + "_1.pgm")
    shell.run("trace convert -endian LSB " + fn + "_2.pgm tmp_2.pgm")
    #shell.run("trace mv /tmp/1 " + fn + "_2.pgm")
    command = "trace kdu_compress" \
              + " -i " \
              + "tmp_0.pgm," \
              + "tmp_1.pgm," \
              + "tmp_2.pgm" \
              + " -o " + fn + "." + IMG_EXT \
              + " -jpx_space sYCC CRGoffset=\{0,0\},\{0.25,0.25\},\{0.25,0.25\}" \
              + " -no_weights" \
              + " -slope " + str(slope) \
              + " Creversible=" + "no" \
              + " Clayers=" + str(layers) \
              + " Clevels=" + str(Clevels) \
              + " Cuse_sop=" + "no"

    # OJO, que con 16 bpp Creversible podría estar a yes

    if __debug__:
        command += " | tee /dev/tty | awk '/thresholds/{getline; print}' > "
    else:
        command += " | awk '/thresholds/{getline; print}' > "

    command += (fn + ".txt")

    shell.run(command)
    shell.run("trace rm tmp_0.pgm tmp_1.pgm tmp_2.pgm")

    picture += 1
