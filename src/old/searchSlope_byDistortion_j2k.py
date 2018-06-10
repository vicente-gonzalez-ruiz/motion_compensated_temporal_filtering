#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

## @file searchSlope_byDistortion.py
#  Search for the proper quantification to produce a compression of an
#  picture with a distortion indicated by the user. Such distortion is
#  indicated for each frame of video and is given by a file.
#
#  @authors Jose Carmelo Maturana-Espinosa\n Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package texture_compress
#  Search for the proper quantification to produce a compression of an
#  picture with a distortion indicated by the user. Such distortion is
#  indicated for each frame of video and is given by a file.


import os
import sys
import display
import math
import subprocess  as sub
from   GOP         import GOP
from   subprocess  import check_call
from   subprocess  import CalledProcessError
import arguments_parser

## Refers to the codec to be used for compression of texture
## information.
MCTF_TEXTURE_CODEC   = os.environ["MCTF_TEXTURE_CODEC"]
## Number of bytes per component.
#  - Use 1 byte for unweighted components.
#  - Use 2 bytes for weighted components or that weighted.
BYTES_PER_COMPONENT = 1 # 1 # 2
## Refers to high frequency subbands.
HIGH                 = "high"
## Refers to low frequency subbands.
LOW                  = "low"
## Useful range of quantification (typical).
range_quantization   = int((46000.0 - 42000.0) / 2)
## Distance in the quantization step, between quality layers in the
#  same subband. (kakadu used by default 256).
quantization_step    = 0
## Number of Group Of Pictures to process.
GOPs                 = 1
## Number of layers. Logarithm controls the quality level and the
## bit-rate of the code-stream.
nLayers              = 5
## Width of the pictures.
pixels_in_x          = 352
## Height of the pictures.
pixels_in_y          = 288
## Controls the quality level and the bit-rate of the code-stream.
quantization         = str((46000 + 42000) / 2) # "44000"
## Number of Temporal Resolution Levels.
TRLs                 = 4
## Number of Spatia Resolution Levels.
SRLs                 = 5
## File containing a distortion value per line. Each line corresponds
## to a frame of the sequence.
distortions           = ""

## The parser module provides an interface to Python's internal parser
## and byte-code compiler.
parser = arguments_parser(description="Compress the texture.")
parser.GOPs()
parser.nLayers()
parser.pixels_in_x()
parser.pixels_in_y()
parser.quantization()
parser.quantization_step()
parser.TRLs()
parser.SRLs()
parser.distortions()

## A script may only parse a few of the command-line arguments,
## passing the remaining arguments on to another script or program.
args = parser.parse_known_args()[0]
if args.GOPs:
    GOPs = int(args.GOPs)
if args.nLayers:
    nLayers = int(args.nLayers)
if args.pixels_in_x:
    pixels_in_x = int(args.pixels_in_x)
if args.pixels_in_y:
    pixels_in_y = int(args.pixels_in_y)
if args.quantization:
    quantization = args.quantization
if args.quantization_step:
    quantization_step = int(args.quantization_step)
if args.TRLs:
    TRLs = int(args.TRLs)
if args.SRLs:
    SRLs = int(args.SRLs)
if args.distortions:
    distortions = args.distortions



############################################################
# FUNCTIONS                                                #
############################################################


#------------------------------------------------
## Demux
def demux (pic, picture_number, component, jump_demux, size_component) :

    try :
        check_call("trace demux " + str(YUV_size) + jump_demux
                   + " < " + pic + ".tmp | split --numeric-suffixes --suffix-length=4 --bytes="
                   + str(size_component) + " - " + pic + "_" + str(component) + "_"
                   , shell=True)
    except CalledProcessError :
        sys.exit(-1)

    picture_filename = pic + "_" + str(component) + "_"
    os.rename(picture_filename + '%04d' % 0, picture_filename + '%04d' % picture_number + ".rawl")
    picture_filename = pic + "_" + str(component) + "_" + '%04d' % picture_number
    
    return picture_filename


#------------------------------------------------
## Encode j2k codec.
def encode (quantization, picture_filename, bits_per_component, sDimX, sDimY) :

    try :
        check_call("trace kdu_compress"
                   + " -i "          + picture_filename + ".rawl"
                   + " -o "          + picture_filename + ".j2c"
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


#------------------------------------------------
## Decode j2k codec.
def decode (picture_filename) :

    check_call("trace kdu_expand"
               + " -i "              + picture_filename + ".j2c"
               + " -o " + "extract/" + picture_filename + ".rawl"
               , shell=True)

    ## Mux
    try:
        check_call("trace cat extract/" + picture_filename + ".rawl >> extract/decoded_pic", shell=True)
    except CalledProcessError:
        sys.exit(-1)


#------------------------------------------------
## Determines the size of the header of a codestream.
#  @param file_name Name of the textures file.
#  @return Header size (bytes).
def header (file_name) :
    p = sub.Popen("header_size " + str(file_name) + " 2> /dev/null | grep OUT", shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
    out, err = p.communicate()
    return long(out[4:])


#------------------------------------------------
## Determines the codestream size.
#  @param file_name Name of the textures file.
#  @return Codestream size (bytes).
def size (file_name) :
    ## Size of the component 'Y' (measured in bytes, without headers).
    Ysize  = os.path.getsize(file_name + "_Y_" + '%04d' % picture_number + ".j2c") - header(file_name + "_Y_" + '%04d' % picture_number + ".j2c")
    ## Size of the component 'U' (measured in bytes, without headers).
    Usize  = os.path.getsize(file_name + "_U_" + '%04d' % picture_number + ".j2c") - header(file_name + "_U_" + '%04d' % picture_number + ".j2c")
    ## Size of the component 'V' (measured in bytes, without headers).
    Vsize  = os.path.getsize(file_name + "_V_" + '%04d' % picture_number + ".j2c") - header(file_name + "_V_" + '%04d' % picture_number + ".j2c")

    return Ysize, Usize, Vsize





#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
#- MAIN ---------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------


# Path
#--------------------

## Current path.
p = sub.Popen("echo $PWD", shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
out, err     = p.communicate()
## Codestream path.
path_base    = out[:-1]
## Truncated codestream path.
path_extract = path_base + "/extract"
## Reconstruction path.
path_tmp     = path_base + "/tmp"


# Inicialization
#--------------------

## Initializes the class GOP (Group Of Pictures).
gop      = GOP()
## Extract the value of the size of a GOP, that is, the number of pictures.
GOP_size = gop.get_size(TRLs)
## Number of pictures to process.
pictures = GOPs * GOP_size + 1
## Number of bits per component.
bits_per_component = BYTES_PER_COMPONENT * 8
## Search quantization-distortion accuracy. 10 = One decimal accuracy,
## 100 = Two decimal, 1000 = Three decimal ...
accuracy = 100

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


# Read distortion frame per frame.
try:
    ## Descriptor file.
    f_distortions = open(distortions, 'rb')
except CalledProcessError:
    print "Error openning distiontions file."
    sys.exit(0)

## File that lists the sizes of the compressed files. It is useful for
## calculating Kbps (see info.py).
f_info = open ("info_mj2k", 'w')

## Truncated codestream path.
p = sub.Popen("mkdir extract", shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
out, err = p.communicate()


# Binary search
#----------------------------
picture_number = 0
while picture_number < pictures :

    #######################
    # Take required picture #
    #######################
    try :
        pic = "picture"
        check_call("trace dd"
                   + " if="    + "low_0"
                   + " of="    + pic + ".tmp"
                   + " ibs="   + str(YUV_size)
                   + " skip="  + str(picture_number)
                   + " count=" + str(1) # Frame per frame.
                   , shell=True)
    except CalledProcessError :
        sys.exit(-1)

    #########
    # Demux # in component.
    #########
    pic_Y = demux (pic, picture_number, 'Y', " " + "0"                + " " + str(Y_size), Y_size)
    pic_U = demux (pic, picture_number, 'U', " " + str(Y_size)        + " " + str(U_size), U_size)
    pic_V = demux (pic, picture_number, 'V', " " + str(Y_size+U_size) + " " + str(V_size), V_size)


    #################
    # Binary search # of slope by distortion
    #################
    # A PSNR (Peak Signal-to-Noise Ratio) value of a reconstrucction in
    # MCJ2K or any other codec.
    distortion = float(f_distortions.readline())
    ## Maximum number of iterations of the binary search, to reach a
    ## granularity of slope equal to 1 is 10 iterations.
    count = 0
    ## Initial value of distortion.
    psnr  = 0
    ## Initial value of quantization.
    slope = int(quantization)
    ## Initial value of binary search.
    stepQ = range_quantization

    while (int(distortion * accuracy) != int(psnr * accuracy)) and (round(stepQ) > 0) : # One decimal accuracy

        # ENCODE #
        encode (slope, pic_Y, bits_per_component, pixels_in_x,   pixels_in_y)
        encode (slope, pic_U, bits_per_component, pixels_in_x/2, pixels_in_y/2)
        encode (slope, pic_V, bits_per_component, pixels_in_x/2, pixels_in_y/2)

        # DECODE #
        check_call("rm -f extract/decoded_pic", shell=True)
        decode (pic_Y)
        decode (pic_U)
        decode (pic_V)

        # PSNR #
        p = sub.Popen("echo \"" + "##    file_A=" + str(pic) + ".tmp   file_B=extract/decoded_pic" + " --block_size=" + str(YUV_size) + "\" >> info_snrFiles", shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
        out, err = p.communicate() # errcode = p.returncode
        p = sub.Popen(            "snr --file_A=" + str(pic) + ".tmp --file_B=extract/decoded_pic" + " --block_size=" + str(YUV_size) + "  2>> info_snrFiles", shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
        out, err = p.communicate() # errcode = p.returncode
        p = sub.Popen(            "snr --file_A=" + str(pic) + ".tmp --file_B=extract/decoded_pic" + " --block_size=" + str(YUV_size) + "  2> /dev/null | grep PSNR | grep dB | cut -f 3", shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
        out, err = p.communicate() # errcode = p.returncode
        psnr = float(out)

        # SIZE #
        Ysize, Usize, Vsize = size (pic)

        # INFO # Slope unfinded.
        info_out = str('%04d' % picture_number) + "\tslope " + str(slope) + "\tbytes " + str(Ysize + Usize + Vsize) + "\tpsnr " + str(psnr) + "\t(psnr wanted " + str(distortion) + ")\t(iteration " + str(count) + "\tstepQ " + str(stepQ) + ")\n"
        f_info.write("# " + info_out)

        # STEP JUMP
        stepQ /= 2.0
        if psnr < distortion :
            slope = int(round(slope-stepQ))
        else :
            slope = int(round(slope+stepQ))

        count += 1

    # INFO # Slope finded.
    f_info.write(info_out)

    picture_number += 1
