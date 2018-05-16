#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# Compressing of the motion vector fields using the codec J2K.

import os
import sys
import subprocess  as     sub
from   subprocess  import check_call
from   subprocess  import CalledProcessError
from arguments_parser import arguments_parser
from defaults import Defaults
import logging

logging.basicConfig()
log = logging.getLogger("subband_motion_compress__j2k")
log.setLevel('INFO')

COMPONENTS          = 4
BYTES_PER_COMPONENT = 2
BITS_PER_COMPONENT  = BYTES_PER_COMPONENT * 8

parser = arguments_parser(description="Compress the motion data using JPEG 2000.")
parser.add_argument("--blocks_in_x",
                    help="number of blocks in the X direction.",
                    default=11)
parser.add_argument("--blocks_in_y",
                    help="number of blocks in the Y direction.",
                    default=9)
parser.add_argument("--fields",
                    help="number of fields in to compress.",
                    default=2)
parser.add_argument("--file",
                    help="name of the file with the motion fields.",
                    default="")
#parser.add_argument("--slopes",
#                    help="Slopes used for compression",
#                    default=Defaults.motion_slopes)

args = parser.parse_known_args()[0]
blocks_in_x = int(args.blocks_in_x)
blocks_in_y = int(args.blocks_in_y)
number_of_fields = int(args.fields)
file = args.file
#slopes = args.slopes; log.info("slopes={}".format(slopes))

spatial_dwt_levels = 0 # 1 # SRLs - 1

field = 0
while field < number_of_fields:

    fn = file + "/" + str('%04d' % field)
    log.info("Compressing {}".format(fn))
    try:
        # Compress.
        check_call("trace kdu_compress"
                   + " -i "          + fn + ".rawl"
                   + " -o "          + fn + ".j2c"
                   + " -no_weights"
                   + " -slope 0"
                   + " Nprecision="  + str(BITS_PER_COMPONENT)
                   + " Nsigned="     + "yes"
                   + " Sdims='{'"    + str(blocks_in_y) + "," + str(blocks_in_x) + "'}'"
                   + " Creversible=yes"
                   + " Clevels="     + str(spatial_dwt_levels)
                   + " Cuse_sop="    + "no"
                   , shell=True)
        # + " Catk=2 Kextension:I2=CON Kreversible:I2=yes Ksteps:I2=\{1,0,0,0\},\{1,0,1,1\} Kcoeffs:I2=-1.0,0.5"
        # An alternative to compress the motion vectors:
        # kdu_compress -i mini_motion_4.rawl -o mini_motion_4.j2c
        # -no_weights Sprecision=16 Ssigned=yes Sdims='{'4,4'}'
        # Clevels=1 Catk=2 Kextension:I2=CON Kreversible:I2=yes
        # Ksteps:I2=\{1,0,0,0\},\{1,0,1,1\} Kcoeffs:I2=-1.0,0.5
        
    except CalledProcessError:
        sys.exit(-1)

    field += 1
