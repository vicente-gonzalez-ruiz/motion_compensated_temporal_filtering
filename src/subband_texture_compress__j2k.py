#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# {{{ Imports

from shell import Shell as shell
from arguments_parser import arguments_parser
# from defaults import Defaults
from colorlog import log
import os

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

args = parser.parse_known_args()[0]
file = args.file
layers = int(args.layers)
number_of_pictures = int(args.pictures)
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
SRLs = int(args.SRLs)

log.info("file={}".format(file))
log.info("layers={}".format(layers))
log.info("pictures={}".format(number_of_pictures))
log.info("pixels_in_x={}".format(pixels_in_x))
log.info("pixels_in_y={}".format(pixels_in_y))
log.info("SRLs={}".format(SRLs))

# }}}

BYTES_PER_COMPONENT = 1 # 2

IMG_EXT = os.environ["MCTF_IMG_EXT"]

Clevels = SRLs - 1
if Clevels < 0:
    Clevels = 0

picture = 0
while picture < number_of_pictures:

    fn = file + "/" + str('%04d' % picture)
    shell.run("trace kdu_compress"
              + " -i "
              + fn + "_0.pgm,"
              + fn + "_1.pgm,"
              + fn + "_2.pgm"
              + " -o " + fn + "." + IMG_EXT
              + " -jpx_space sYCC CRGoffset=\{0,0\},\{0.25,0.25\},\{0.25,0.25\}"
              + " -no_weights"
              + " -slope 42000"
              + " Creversible=" + "no"
              + " Clayers=" + str(layers)
              + " Clevels=" + str(Clevels)
              + " Cuse_sop=" + "no"
              + " | tee /dev/tty | awk '/thresholds/{getline; print}' > " + fn + ".txt")

    picture += 1
