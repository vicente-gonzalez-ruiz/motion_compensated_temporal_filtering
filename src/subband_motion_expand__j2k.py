#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# Decompression of the motin vector fields using J2K.

# {{{ Imports

from shell import Shell as shell
from arguments_parser import arguments_parser
from colorlog import log

# }}}

# {{{ Defs

COMPONENTS = 4
BYTES_PER_COMPONENT = 2
BITS_PER_COMPONENT = BYTES_PER_COMPONENT * 8
spatial_dwt_levels = 0 # 1 # SRLs - 1

# }}}

# {{{ Arguments parsing

parser = arguments_parser(description="Expands the motion data using JPEG 2000.")

parser.add_argument("--blocks_in_x",
                    help="number of blocks in the X direction.",
                    default=11)
parser.add_argument("--blocks_in_y",
                    help="number of blocks in the Y direction.",
                    default=9)
parser.add_argument("--fields",
                    help="number of fields in to expand.",
                    default=2)
parser.add_argument("--file",
                    help="name of the file with the motion fields.",
                    default="")

args = parser.parse_known_args()[0]

blocks_in_x = int(args.blocks_in_x)
log.info("blocks_in_x={}".format(blocks_in_x))

blocks_in_y = int(args.blocks_in_y)
log.info("blocks_in_x={}".format(blocks_in_x))

bytes_per_field = blocks_in_x * blocks_in_y * BYTES_PER_COMPONENT

fields = int(args.fields)
log.info("fields={}".format(fields))

file = args.file
log.info("file={}".format(file))

# }}}

field = 0
while field < fields:

    fn = file + "/" + str('%04d' % field)
    shell.run("rm " + fn + ".rawl")
    for c in range(COMPONENTS):
        shell.run("trace kdu_expand"
                  + " -i " + fn + ".j2c"
                  + " -o /tmp/1.rawl"
                  + " -skip_components " + str(c))
        shell.run("cat /tmp/1.rawl >> " + fn + ".rawl")

        field += 1
