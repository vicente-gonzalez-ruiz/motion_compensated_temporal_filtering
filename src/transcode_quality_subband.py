#!/usr/bin/env python3
#!/home/vruiz/.pyenv/shims/python -i
# -*- coding: iso-8859-15 -*-

# Quality transcoding of a subband.
#
# Input: original subband, number of pictures and number of
# quality-layers.
#
# Output: truncated subband.

# {{{ Importing

import sys
from GOP import GOP
from arguments_parser import arguments_parser
import io
import operator
import math
from shell import Shell as shell
from colorlog import ColorLog
import logging
import os

log = ColorLog(logging.getLogger("transcode_quality_subband"))
log.setLevel('INFO')
shell.setLogger(log)

# }}}

# {{{ Arguments parsing

parser = arguments_parser(description="Transcodes in quality a subband.")
parser.add_argument("--subband",
                    help="Subband prefix (for example, \"L_3\")",
                    default="")
parser.add_argument("--layers",
                    help="Number of quality layers to output",
                    default=8)
parser.add_argument("--pictures",
                    help="Number of pictures to transcode",
                    default=1)

args = parser.parse_known_args()[0]
subband = args.subband
layers = int(args.layers)
pictures = int(args.pictures)

log.info("subband={}".format(subband))
log.info("layers={}".format(layers))
log.info("pictures={}".format(pictures))

IMG_EXT = os.environ["MCTF_IMG_EXT"]

# }}}

def transcode_picture(filename, layers):
# {{{

    print(filename, layers)
    shell.run("trace kdu_transcode"
              + " -i " + filename
              + " -jpx_layers sYCC,0,1,2"
              + " -o " + "transcode_quality/" + filename
              + " Clayers=" + str(layers))

# }}}

picture_number = 0
while picture_number < pictures:

    str_picture_number = '%04d' % picture_number

    filename = subband + "/" + str_picture_number
    transcode_picture(filename + "." + IMG_EXT, layers)

    picture_number += 1
