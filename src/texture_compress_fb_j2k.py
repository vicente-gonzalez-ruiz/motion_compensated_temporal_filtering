#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

## @file texture_compress_fb_j2k.py
#  Compress textures, using the codec J2K.
#  The two main steps performed are:
#  - Demultiplexing components (Y, U y V) and 
#  - Encode components.
#
#  @authors Jose Carmelo Maturana-Espinosa\n Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package texture_compress_fb_j2k
#  Compress textures, using the codec J2K.
#  The two main steps performed are:
#  - Demultiplexing components (Y, U y V) and 
#  - Encode components.

import shutil
import os
import sys
import display
import math
import struct
import subprocess  as     sub
from   subprocess  import check_call
from   subprocess  import CalledProcessError
from   MCTF_parser import MCTF_parser


## Refers to low frequency subbands.
LOW  = "low"
## Refers to high frequency subbands.
HIGH = "high"
## Number of components.
COMPONENTS    = 3
## Number of bytes per component.
#  - Use 1 byte for unweighted components.
#  - Use 2 bytes for weighted components or that weighted.
BYTES_PER_COMPONENT = 1 # 1 # 2
## File that contains the textures.
file          = ""
## Number of images to process.
pictures      = 33
## Width of the pictures.
pixels_in_x   = 352
## Height of the pictures.
pixels_in_y   = 288
## Controls the quality level and the bit-rate of the code-stream.
quantization  = 45000
## Current temporal iteration.
subband       = 0
## Number of Spatial Resolution Levels.
SRLs          = 5
## Number of layers. Logarithm controls the quality level and the
#  bit-rate of the code-stream.
nLayers       = 5


## The parser module provides an interface to Python's internal parser
## and byte-code compiler.
parser = MCTF_parser(description="Compress the LFB texture data using JPEG 2000.")
parser.add_argument("--file",    help="file that contains the textures data. Default = {})".format(file))
parser.add_argument("--nLayers", help="Number of layers. Logarithm controls the quality level and the bit-rate of the code-stream. (Default = {})".format(nLayers))
parser.pictures(pictures)
parser.pixels_in_x(pixels_in_x)
parser.pixels_in_y(pixels_in_y)
parser.quantization(quantization)
parser.subband(subband)
parser.SRLs(SRLs)

## A script may only parse a few of the command-line arguments,
## passing the remaining arguments on to another script or program.
args = parser.parse_known_args()[0]
if args.file:
    file = args.file
if args.nLayers:
    nLayers = args.nLayers
if args.pictures:
    pictures = int(args.pictures)
if args.pixels_in_x:
    pixels_in_x = int(args.pixels_in_x)
if args.pixels_in_y:
    pixels_in_y = int(args.pixels_in_y)
if args.quantization:
    quantization = str(args.quantization) # 'int' to 'str'
if args.subband:
    subband = int(args.subband)
if args.SRLs:
    SRLs = int(args.SRLs)



#-------------
#- FUNCTIONS -
#-------------


## Weighing the components before compression. It is not necessary
## step, and is not performed by default. The code is useful for
## research tasks. Weighing in some parts of the codestream if it is
## useful, but it becomes a level of quality layers and sub-bands (see
## texture_compress.py)
## @param image_filename Filename textures of the current iteration.

#---------------------------------------------------------------------
def pondComp (image_filename) :

    ## Weighting coefficients for subband. For an example of 5TRLs ([H1, H2, H3, H4, L4]).
    coef = [1, 1.4921569843, 2.7304234608, 5.3339326679, 5.8022196044]
    ## File containing the textures before weighting coefficients.
    f_in = open (image_filename, 'rb')
    ## File containing the textures after weighting coefficients.
    f_out = open (image_filename + "_multCOM", 'wb')

    try :
        ## An unweighted coefficient.
        byte = f_in.read(1)
        while byte != "" :

            # Some examples of weighting coefficients:
            #-----------------------------------------
            #data = ord(byte)                                   # =
            #data = ord(byte) * pow(2, subband-1)               # *2^subband
            #data = ord(byte) * pow(5, subband-1)               # *5^subband
            #data = ord(byte) * pow(math.sqrt(2), subband-1)    # *sqrt(2)^subband
            #data = ord(byte) * coef[subband-1]                 # coef
            #data = ord(byte) * pow(coef[subband-1], subband-1) # coef^subband

            ## A weighted coefficient.
            bin_data = struct.pack('H', int(round(data)))
            f_out.write(bin_data[0]) #0
            f_out.write(bin_data[1]) #1 # Ej: 3 = bin_data[1] bin_data[0] = 00000000 00000011

            byte = f_in.read(1)

    finally :
        f_in.close()
        f_out.close()

    os.rename(image_filename + "_multCOM", image_filename)




## Demultiplexing and encode components. Using Kakadu software.
## @param component Component type, encoded in the current iteration. It can be: Y, U or V.
## @param jump_demux Number of bytes of distance between the same component within the codestream.\n It is useful to locate all occurrences of a particular component and can demux components.
## @param size_component Number of bytes of a given component. It is useful for demultiplexing.
## @param bits_per_component Number of bits per component. It is a constant for the entire duration.
## @param sDimX Number of samples of a particular component, to the width of the image.
## @param sDimY Number of samples of a particular component, to the height of the image.

#---------------------------------------------------------------------
def encode (component, jump_demux, size_component, bits_per_component, sDimX, sDimY) :

    # Demux.
    try :
        check_call("trace demux " + str(YUV_size) + jump_demux
                   + " < " + file + ".tmp | /usr/bin/split --numeric-suffixes --suffix-length=4 --bytes="
                   + str(size_component) + " - " + file + "_" + str(component) + "_"
                   , shell=True)
    except CalledProcessError :
        sys.exit(-1)

    # Encode.
    image_number = 0
    while image_number < pictures :

        image_filename = file + "_" + str(component) + "_" + '%04d' % image_number

        #shutil.copy (image_filename, image_filename + '.SINmult')
        #pondComp (image_filename)


        # kakadu.
        # When compressing images with kdu_compress you have to use the
        # Cuse_sop = yes parameter. This makes the marker SOP (Start of
        # packet) before each packet included codestream.
        os.rename(image_filename, image_filename + ".rawl")

        try :
            if quantization == "automatic_kakadu" :
                # ----- Slopes automaticos del kakadu ----- 
                check_call("trace kdu_compress"
                           + " -i "          + image_filename + ".rawl"
                           + " -o "          + image_filename + ".j2c"
                           + " Creversible=" + "no" # "no" "yes"
                           + " -no_weights"
                           + " Sprecision="  + str(bits_per_component)
                           + " Ssigned="     + "no"
                           + " Sdims='{'"    + str(sDimY) + "," + str(sDimX) + "'}'"
                           + " Clevels="     + str(Clevels)
                           + " Clayers="     + str(nLayers)
                           + " Cuse_sop="    + "yes"
                           , shell=True)
	    else :
                # ----- Slopes segun parametros usuario ----- 
                check_call("trace kdu_compress"
                           + " -i "          + image_filename + ".rawl"
                           + " -o "          + image_filename + ".j2c"
                           + " Creversible=" + "no" # "no" "yes"
                           + " -slope "      + str(quantization)
                           + " -no_weights"
                           + " Sprecision="  + str(bits_per_component)
                           + " Ssigned="     + "no"
                           + " Sdims='{'"    + str(sDimY) + "," + str(sDimX) + "'}'"
                           + " Clevels="     + str(Clevels)
                           + " Clayers="     + str(nLayers)
                           + " Cuse_sop="    + "yes"
                           , shell=True)

        except CalledProcessError :
            sys.exit(-1)

        image_number += 1




#--------
#- MAIN -
#--------

# Displays a log of execution:
check_call("echo file: " + str(file) + " subband: " + str(subband), shell=True)
#raw_input("")


## Number of bits per component.
bits_per_component = BYTES_PER_COMPONENT * 8


## Number of levels to be applied in the DWT, in compressing files by
## Kakadu.
Clevels = SRLs - 1
if Clevels < 0 :
    Clevels = 0

'''
# Clevels = SRLs-1 for L subband. Clevels = 0 for H subband.     
if file[0] == 'h' :
    dwt_levels = 0
'''

## Size of the component 'Y' (measured in pixels).
Y_size     = pixels_in_y * pixels_in_x
## Size of the component 'U' (measured in pixels).
U_size     = Y_size / 4
## Size of the component 'V' (measured in pixels).
V_size     = Y_size / 4
## Size of the components 'YUV' (measured in pixels).
YUV_size   = Y_size + U_size + V_size



# Copy only the required images.
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
## Number of image of the current iteration.
image_number = 0
## Total size of compressed files.
total        = 0

while image_number < pictures:

    ## Name of image of the current iteration.
    str_image_number = '%04d' % image_number

    ## Size of the component 'Y' (measured in bytes, without headers).
    Ysize  = os.path.getsize(file + "_Y_" + str_image_number + ".j2c") - header(file + "_Y_" + str_image_number + ".j2c")
    ## Size of the component 'U' (measured in bytes, without headers).
    Usize  = os.path.getsize(file + "_U_" + str_image_number + ".j2c") - header(file + "_U_" + str_image_number + ".j2c")
    ## Size of the component 'V' (measured in bytes, without headers).
    Vsize  = os.path.getsize(file + "_V_" + str_image_number + ".j2c") - header(file + "_V_" + str_image_number + ".j2c")

    total  = total + Ysize + Usize + Vsize
    file_sizes.write(str(total) + "\n")

    image_number += 1
