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

import logging
import sys
from   GOP              import GOP
from   subprocess       import check_call
from   subprocess       import CalledProcessError
from   arguments_parser import arguments_parser
import io
import operator
import math

# }}}

# {{{ Logging

logging.basicConfig()
log = logging.getLogger("transcode_quality_subband")
log.setLevel('INFO')

# }}}

# {{{ Arguments parsing

parser = arguments_parser(description="Transcodes in quality a subband.")
parser.add_argument("--subband",
                    help="Subband prefix (for example, \"low_3\")",
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

# }}}

def transcode_picture(filename, layers):
# {{{

    print(filename, layers)
    try:
        check_call("trace kdu_transcode"
                   + " -i " + filename
                   + " -o " + "transcode_quality/" + filename
                   + " Clayers=" + str(layers), 
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

# }}}

picture_number = 0
while picture_number < pictures:

    str_picture_number = '%04d' % picture_number

    filename = subband + "_" + str_picture_number + "_Y" 
    transcode_picture(filename + ".j2c", layers)

    filename = subband + "_" + str_picture_number + "_U" 
    transcode_picture(filename + ".j2c", layers)

    filename = subband + "_" + str_picture_number + "_V" 
    transcode_picture(filename + ".j2c", layers)

    picture_number += 1
