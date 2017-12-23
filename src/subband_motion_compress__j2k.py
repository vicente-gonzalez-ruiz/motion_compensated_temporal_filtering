#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

## Compressing the motion vectors, using the codec J2K.
#  The compression consists of two major steps:\n
#  - Demultiplexing components.
#  - Encode components (lossless compression).\n
#
#  Additionally is calculated the size in bytes of motion fields belonging 
#  to each component, each image and each temporal subband.\n It records in 
#  a file that can be consulted later. In these calculations do not take 
#  into account the size of the header of a codestream.

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

## Number of components of a motion field.
COMPONENTS          = 4
## Number of bytes for each component.
BYTES_PER_COMPONENT = 2
## Number of bits for each component.
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
parser.add_argument("--slopes",
                    help="Slopes used for compression",
                    default=Defaults.motion_slopes)

args = parser.parse_known_args()[0]
blocks_in_x = int(args.blocks_in_x)
blocks_in_y = int(args.blocks_in_y)
fields = int(args.fields)
file = args.file
slopes = args.slopes; log.debug("slopes={}".format(slopes))

## Number of levels of the DWT to be applied in compression.
spatial_dwt_levels = 0 # 1 # SRLs - 1

## Number of bytes required by the movement information (uncompressed)
#  for each image.
bytes_compF = blocks_in_x * blocks_in_y * BYTES_PER_COMPONENT

for comp_number in range (0, COMPONENTS) :

    # DEMUX components.
    try :
        check_call("demux "
                   + str(COMPONENTS * BYTES_PER_COMPONENT)
                   + " "
                   + str(comp_number * BYTES_PER_COMPONENT)
                   + " "
                   + str(BYTES_PER_COMPONENT)
                   + " < " + file
                   + " | split --numeric-suffixes --suffix-length=4 "
                   + "--bytes="
                   + str(bytes_compF)
                   + " - "
                   + file
                   + "_comp"
                   + str(comp_number)
                   + "_" # .rawl aquí!
                   , shell=True)
    except CalledProcessError:
        sys.exit(-1)

    # ENCODE components.
    campoMov_number = 0
    while campoMov_number < fields :

        ## Name of the file containing the data of movement of a
        #  component of a desired image and a specific subband.
        campoMov_name = file + "_" + str('%04d' % campoMov_number) +  "_comp" + str(comp_number)

        try:
            check_call("mv " + file + "_comp" + str(comp_number) + "_" + str('%04d' % campoMov_number) + " " + campoMov_name + ".rawl"
                       , shell=True)
        except CalledProcessError:
            sys.exit(-1)

        try:
            # Compress.
            check_call("trace kdu_compress"
                       + " -i "          + campoMov_name + ".rawl"
                       + " -o "          + campoMov_name + ".j2c"
                       + " -no_weights"
                       + " -slope "      + slopes
                       + " Creversible=" + "yes" # "no" "yes" # Da igual como esté al usar el kernel descrito
                       + " Nprecision="  + str(BITS_PER_COMPONENT)
                       + " Nsigned="     + "yes"
                       + " Sdims='{'"    + str(blocks_in_y) + "," + str(blocks_in_x) + "'}'"
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

        campoMov_number += 1
