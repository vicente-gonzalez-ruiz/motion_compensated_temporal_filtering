#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

#  Compress textures, using the codec J2K.

import shutil
import os
import sys
import display
import math
import struct
import subprocess  as     sub
from   subprocess  import check_call
from   subprocess  import CalledProcessError
from arguments_parser import arguments_parser

LOW         = "low"
HIGH        = "high"
COMPONENTS  = 3

## Number of bytes per component.
#  - Use 1 byte for unweighted components.
#  - Use 2 bytes for weighted components or that weighted.
BYTES_PER_COMPONENT = 1 # 2

parser = arguments_parser(description="Compress the LFB texture data using JPEG 2000.")
parser.add_argument("--file",
                    help="File that contains the texture data.",
                    default="")
parser.texture_layers()
parser.add_argument("--pictures",
                    help="Number of pictures to compress.",
                    default=33)
parser.pixels_in_x()
parser.pixels_in_y()
parser.texture_quantization()
parser.temporal_subband()
parser.SRLs()

args = parser.parse_known_args()[0]

file = args.file
layers = args.texture_layers
pictures = int(args.pictures)
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
quantization = str(args.texture_quantization)
subband = int(args.temporal_subband)
SRLs = int(args.SRLs)

def encode (component,           # Y, U or V.
            jump_demux,          # Number of bytes of distance between the same component within the codestream
            component_size,      # Number of bytes of a given component
            bits_per_component,  # Number of bits per component
            sDimX, sDimY) :      # Dimensions of a component

    # Esto es m�s optimo si se hace a nivel de Python y simplemente
    # vamos recorriendo el archivo y comprimiendolo.
    
    # Split each next image into its components
    try :
        check_call("trace demux "
                   + str(YUV_size)
                   + jump_demux
                   + " < "
                   + file
                   + ".tmp "
                   + "| split --numeric-suffixes --suffix-length=4 "
                   + "--bytes="
                   + str(component_size)
                   + " - "
                   + file
                   + "_"
                   + str(component)
                   + "_"
                   , shell=True)
    except CalledProcessError :
        sys.exit(-1)

    # Encode each component.
    image_number = 0
    while image_number < pictures :

        image_filename = file + "_" + str(component) + "_" + '%04d' % image_number

        os.rename(image_filename, image_filename + ".rawl")

        try :
            check_call("trace kdu_compress"
                       + " -i "          + image_filename + ".rawl"
                       + " -o "          + image_filename + ".j2c"
                       + " Creversible=" + "no" # "no" "yes"
                       + " -slope "      + str(quantization)
                       + " -no_weights"
                       + " Nprecision="  + str(bits_per_component)
                       + " Nsigned="     + "no"
                       + " Sdims='{'"    + str(sDimY) + "," + str(sDimX) + "'}'"
                       + " Clevels="     + str(Clevels)
                       + " Clayers="     + str(layers)
                       + " Cuse_sop="    + "no"
                       , shell=True)

        except CalledProcessError :
            sys.exit(-1)

        image_number += 1

## Number of bits per component.
bits_per_component = BYTES_PER_COMPONENT * 8

## Number of levels to be applied in the DWT, in compressing files by
## Kakadu.
Clevels = SRLs - 1
if Clevels < 0 :
    Clevels = 0

## Size of the component 'Y' (measured in pixels).
Y_size     = pixels_in_y * pixels_in_x
## Size of the component 'U' (measured in pixels).
U_size     = Y_size // 4
## Size of the component 'V' (measured in pixels).
V_size     = Y_size // 4
## Size of the components 'YUV' (measured in pixels).
YUV_size   = Y_size + U_size + V_size

# Copy only the required images.
try :
    check_call("trace dd"
               + " if="    + file
               + " of="    + file + ".tmp"
               + " bs="    + str(YUV_size)
               + " count=" + str(pictures)
               , shell=True)
except CalledProcessError :
    sys.exit(-1)

# Encoding each component accordingly.
encode ('Y', " " + "0"                + " " + str(Y_size), Y_size, bits_per_component, pixels_in_x,   pixels_in_y)
encode ('U', " " + str(Y_size)        + " " + str(U_size), U_size, bits_per_component, pixels_in_x//2, pixels_in_y//2)
encode ('V', " " + str(Y_size+U_size) + " " + str(V_size), V_size, bits_per_component, pixels_in_x//2, pixels_in_y//2)

