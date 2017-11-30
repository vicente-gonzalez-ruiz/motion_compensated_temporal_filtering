#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

## @file texture_expand_fb_j2k.py
#  Decompress textures, using the codec J2K. 
#  The two main steps performed are:
#  - Decode components and
#  - Multiplexing components (Y, U y V).
#
#  If there is no file textures of the current iteration, is created
#  with a neutral texture.
#
#  @authors Jose Carmelo Maturana-Espinosa\n Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package texture_expand_fb_j2k
#  Decompress textures, using the codec J2K. 
#  The two main steps performed are:
#  - Decode components and
#  - Multiplexing components (Y, U y V).
#
#  If there is no file textures of the current iteration, is created
#  with a neutral texture.


import shutil
import subprocess as sub
import sys
import math
import struct
import os
from subprocess import check_call
from subprocess import CalledProcessError
from MCTF_parser import MCTF_parser

## File that contains the textures.
file        = ""
## Optional and developing parameter indicates whether to extract the
#  codestream to a given bit-rate. The bit-rate control is performed
#  in transcode.py, a detailed manner, and therefore its use is
#  recommended for this purpose.
rate        = 0.0
## Number of images to process.
pictures    = 33
## Width of the pictures.
pixels_in_x = 352
## Height of the pictures.
pixels_in_y = 288
## Current temporal iteration.
subband     = 0

## The parser module provides an interface to Python's internal parser
## and byte-code compiler.
parser = MCTF_parser(description="Expands the the LFB y HFB texture data using JPEG 2000.")
parser.add_argument("--file", help="file that contains the LFB or HFB data. Default = {})".format(file))
parser.add_argument("--rate", help="read only the initial portion of the code-stream, corresponding to an overall bit-rate of \"rate\" bits/sample. Default = {})".format(rate))
parser.pictures(pictures)
parser.pixels_in_x(pixels_in_x)
parser.pixels_in_y(pixels_in_y)
parser.subband(subband)

## A script may only parse a few of the command-line arguments,
## passing the remaining arguments on to another script or program.
args = parser.parse_known_args()[0]
if args.file:
    file = args.file
if args.rate:
    rate = float(args.rate)
if args.pictures:
    pictures = int(args.pictures)
if args.pixels_in_x:
    pixels_in_x = int(args.pixels_in_x)
if args.pixels_in_y:
    pixels_in_y = int(args.pixels_in_y)
if args.subband:
    subband = int(args.subband)




#-------------
#- FUNCTIONS -
#-------------



## Reverses the weighting of components before compression. It is not necessary
## step, and is not performed by default. The code is useful for
## research tasks. Weighing in some parts of the codestream if it is
## useful, but it becomes a level of quality layers and sub-bands (see
## texture_compress.py)
## @param image_filename Filename textures of the current iteration.

#---------------------------------------------------------------------
def pondComp (image_filename) :

    ## Weighting coefficients for subband. For an example of 5TRLs ([H1, H2, H3, H4, L4]).
    coef = [1, 1.4921569843, 2.7304234608, 5.3339326679, 5.8022196044]
    ## File containing the textures before investing weighting coefficients.
    f_in  = open (image_filename + ".rawl", 'rb')
    ## File containing the textures after investing weighting coefficients.
    f_out = open (image_filename + ".rawl_desmultCOM", 'wb')

    try :
        ## A weighted coefficient. (Big endian)
        data = f_in.read(2)
        while data != "" :
            ## A weighted coefficient. (Little endian)
            data_comp = ord(data[1])*256 + ord(data[0]) # [1] + [0]

            # Some examples of weighting coefficients:
            #-----------------------------------------
            
            ## A unweighted coefficient.
            desmult_comp = data_comp                                    # =
            #desmult_comp = data_comp / pow(2, subband-1)               # *2^subband
            #desmult_comp = data_comp / pow(5, subband-1)               # *4^subband
            #desmult_comp = data_comp / pow(math.sqrt(2), subband-1)    # *sqrt(2)^subband
            #desmult_comp = data_comp / coef[subband-1]                 # coef
            #desmult_comp = data_comp / pow(coef[subband-1], subband-1) # coef^subband

            if desmult_comp > 255 :
                desmult_comp = 255

            f_out.write(chr(int(round(desmult_comp))))

            data = f_in.read(2)

    finally:
        f_in.close()
        f_out.close()

    os.rename(image_filename + ".rawl_desmultCOM", image_filename + ".rawl")



## Decode and multiplexing components. Using Kakadu software.
## @param component Component type, encoded in the current iteration. It can be: Y, U or V.
## @param image_number Filenumber textures of the current iteration.

#---------------------------------------------------------------------
def decode (component, image_number) :

    try:
        image_filename = file + "_" + str(component) + "_" + str('%04d' % image_number)

        f = open(image_filename + ".j2c", "rb")
        f.close()

        # Decode.
        try:
            if rate <= 0.0 :
                check_call("trace kdu_expand"
                           + " -i " + image_filename + ".j2c"
                           + " -o " + image_filename + ".rawl"
                           , shell=True)
            else :
                check_call("trace kdu_expand"
                           + " -i " + image_filename + ".j2c"
                           + " -o " + image_filename + ".rawl"
                           + " -rate " + rate
                           , shell=True)

            #shutil.copy (image_filename + '.rawl', image_filename + '.SINdiv')    # Backs weighted components.
            #pondComp (image_filename)

        except CalledProcessError :
            sys.exit(-1)

    except:
        # If there is no file textures of the current iteration, is
        # created with a neutral texture.

        f = open(image_filename + ".rawl", "wb")
        for a in xrange(pixels_in_x * pixels_in_y) :
            f.write('%c' % 128)  # BYTES_PER_COMPONENT = 1   # 1 byte for components used unweighted.
            #f.write('%c' % 128) # BYTES_PER_COMPONENT = 2   # 2 bytes for weighted or components that are used weighted.
        f.close()

    # MUX
    try:
        check_call("trace cat " + image_filename + ".rawl >> " + file, shell=True)
    except CalledProcessError:
        sys.exit(-1)




#--------
#- MAIN -
#--------

# Displays a log of execution:
# check_call("echo file: " + str(file) + " subband: " + str(subband), shell=True)
# raw_input("")

## Current image iteration.
image_number = 0
while image_number < pictures :

    # Decode components Y, U y V.
    decode ('Y', image_number)
    decode ('U', image_number)
    decode ('V', image_number)

    image_number += 1
