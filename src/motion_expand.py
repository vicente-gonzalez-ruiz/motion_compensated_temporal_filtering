#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# {{{ Importing
import os
from GOP import GOP
from shell import Shell as shell
from arguments_parser import arguments_parser
from colorlog import log
# }}}

# {{{ Arguments parsing
parser = arguments_parser(description="Expands the motion data.")
parser.GOPs()
parser.TRLs()
parser.block_size()
parser.pixels_in_x()
parser.pixels_in_y()

args = parser.parse_known_args()[0]

block_size = int(args.block_size)
log.info("block_size={}".format(block_size))

GOPs = int(args.GOPs)
log.info("GOPs={}".format(GOPs))

pixels_in_x = int(args.pixels_in_x)
log.info("pixels_in_x={}".format(pixels_in_x))

pixels_in_y = int(args.pixels_in_y)
log.info("pixels_in_y={}".format(pixels_in_y))

TRLs = int(args.TRLs)
log.info("TRLs={}".format(TRLs))
# }}}

#MOTION_DECODER_NAME = "gzip"
#MOTION_DECODER_NAME = "kdu_v_expand"
## Refers to the codec to be used for compression of motion information.
MCTF_MOTION_CODEC = os.environ["MCTF_MOTION_CODEC"]

gop = GOP()
GOP_size = gop.get_size(TRLs)
pictures = (GOPs - 1) * GOP_size + 1

blocks_in_x = pixels_in_x // block_size
blocks_in_y = pixels_in_y // block_size

i = 1
fields = pictures // 2
while i < TRLs:

    shell.run("mctf subband_motion_expand__" + MCTF_MOTION_CODEC
              + " --file=" + "\"" + "motion_residue_" + str(i) + "\""
              + " --blocks_in_y=" + str(blocks_in_y)
              + " --blocks_in_x=" + str(blocks_in_x)
              + " --fields=" + str(fields)
              + " --pictures=" + str(pictures))

    fields //= 2
    i += 1
    
# First (decode) temporal level.
shell.run("mctf bidirectional_motion_correlate"
          + " --blocks_in_y=" + str(blocks_in_y)
          + " --blocks_in_x=" + str(blocks_in_x)
          + " --fields=" + str(GOPs)
          + " --input=" + "\"" + "motion_residue_" + str(TRLs - 1) + "\""
          + " --output=" + "\"" + "motion_" + str(TRLs - 1) + "\"")

# Now, the rest of resolutions.
i = TRLs - 1
while i > 1:

    i -= 1
    fields = pictures // (2**i)

    shell.run("mctf interlevel_motion_correlate"
              + " --blocks_in_y=" + str(blocks_in_y)
              + " --blocks_in_x=" + str(blocks_in_x)
              + " --fields_in_predicted=" + str(fields)
              + " --reference=" + "\"" + "motion_" + str(i + 1) + "\""
              + " --predicted=" + "\"" + "motion_" + str(i) + "\""
              + " --residue=" + "\"" + "motion_residue_" + str(i) + "\"")
