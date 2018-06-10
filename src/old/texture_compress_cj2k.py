#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

#  Compress a sequence of texture pictures, using the codec J2K (color
#  pictures).

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

parser = arguments_parser(description="Compress a YUV picture using JPEG 2000.")
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

## Demultiplexing and encode components. Using Kakadu software.
## @param component Component type, encoded in the current iteration. It can be: Y, U or V.
## @param jump_demux Number of bytes of distance between the same component within the codestream.\n It is useful to locate all occurrences of a particular component and can demux components.
## @param size_component Number of bytes of a given component. It is useful for demultiplexing.
## @param bits_per_component Number of bits per component. It is a constant for the entire duration.
## @param sDimX Number of samples of a particular component, to the width of the picture.
## @param sDimY Number of samples of a particular component, to the height of the picture.

#---------------------------------------------------------------------
def encode (component, jump_demux, size_component, bits_per_component, sDimX, sDimY) :

    # Demux.
    try :
        check_call("trace demux "
                   + str(YUV_size)
                   + jump_demux
                   + " < " + file + ".tmp | split --numeric-suffixes --suffix-length=4 --bytes="
                   + str(size_component) + " - " + file + "_" + str(component) + "_"
                   , shell=True)
    except CalledProcessError :
        sys.exit(-1)
        
    picture_number = 0
    while picture_number < pictures :

        picture_filename = file + "_" + '%04d' % picture_number

        os.rename(picture_filename, picture_filename + ".rawl")

        try :
            check_call("trace kdu_compress"
                       + " -i "          + picture_filename + "_Y.rawl,"
                       + picture_filename + "_U.rawl,"
                       + picture_filename + "_V.raw,"
                       + " -o "          + picture_filename + ".j2c"
                       + " Creversible=" + "no" # "no" "yes"
                       + " -slope "      + str(quantization)
                       + " -no_weights"
                       + " Nprecision="  + str(bits_per_component)
                       + " Nsigned="     + "no"
                       + " Sdims="
                       + "'{'" + str(sDimY) + "," + str(sDimX) + "'},'" +
                       + "'{'" + str(sDimY/2) + "," + str(sDimX/2) + "'},'" +
                       + "'{'" + str(sDimY/2) + "," + str(sDimX/2) + "'}'" +
                       + " Clevels="     + str(Clevels)
                       + " Clayers="     + str(layers)
                       + " Cuse_sop="    + "yes"
                       , shell=True)

        except CalledProcessError :
            sys.exit(-1)

        picture_number += 1

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
U_size     = Y_size / 4
## Size of the component 'V' (measured in pixels).
V_size     = Y_size / 4
## Size of the components 'YUV' (measured in pixels).
YUV_size   = Y_size + U_size + V_size

# Copy only the required pictures.
#-------------------------------
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
#-------------------------------------
encode ('Y', " " + "0"                + " " + str(Y_size), Y_size, bits_per_component, pixels_in_x,   pixels_in_y)
encode ('U', " " + str(Y_size)        + " " + str(U_size), U_size, bits_per_component, pixels_in_x/2, pixels_in_y/2)
encode ('V', " " + str(Y_size+U_size) + " " + str(V_size), V_size, bits_per_component, pixels_in_x/2, pixels_in_y/2)
## Number of bytes used for the header of a file.

#------------------------------------------------
## Determines the size of the header of a codestream.
#  @param file_name Name of the file with the motion fields.
#  @return Bytes of the header of a codestream.
def header (file_name) :
    p = sub.Popen("mcj2k header_size " + str(file_name) + " 2> /dev/null | grep OUT", shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
    out, err = p.communicate()
    return long(out[4:])

# Compute file sizes.
#--------------------

## File that lists the sizes of the compressed files. It is useful for
## calculating Kbps (see info.py).
file_sizes   = open (file + ".j2c", 'w')
## Number of picture of the current iteration.
picture_number = 0
## Total size of compressed files.
total        = 0

while picture_number < pictures:

    ## Name of picture of the current iteration.
    str_picture_number = '%04d' % picture_number

    ## Size of the component 'Y' (measured in bytes, without headers).
    Ysize  = os.path.getsize(file + "_Y_" + str_picture_number + ".j2c") - header(file + "_Y_" + str_picture_number + ".j2c")
    ## Size of the component 'U' (measured in bytes, without headers).
    Usize  = os.path.getsize(file + "_U_" + str_picture_number + ".j2c") - header(file + "_U_" + str_picture_number + ".j2c")
    ## Size of the component 'V' (measured in bytes, without headers).
    Vsize  = os.path.getsize(file + "_V_" + str_picture_number + ".j2c") - header(file + "_V_" + str_picture_number + ".j2c")

    total  = total + Ysize + Usize + Vsize
    file_sizes.write(str(total) + "\n")

    picture_number += 1
