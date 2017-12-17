#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-


## @file texture_compress_hfb_ltw.py
#  Compress the HFB texture data, using LTW.
#  The two main steps performed are:
#  - Demultiplexing components (Y, U y V) and 
#  - Encode components.
#
#  @authors Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package texture_compress_hfb_ltw
#  Compress the HFB texture data, using LTW.
#  The two main steps performed are:
#  - Demultiplexing components (Y, U y V) and 
#  - Encode components.

import sys
import os
from subprocess import check_call
from subprocess import CalledProcessError
import arguments_parser

## Number of components.
COMPONENTS = 3
## Number of bytes per component.
BYTES_PER_COMPONENT = 1
## File that contains the HFB data.
file = ""
## Number of images to process.
pictures = 33
## Width of the pictures.
pixels_in_x = 352
## Height of the pictures.
pixels_in_y = 288
## Controls the quality level and the bit-rate of the code-stream.
quantizations = "45000"
## Number of Spatial Resolution Levels.
SRLs = 5

## The parser module provides an interface to Python's internal parser
## and byte-code compiler.
parser = arguments_parser(description="Compress the LFB texture data using LTW")
parser.add_argument("--file", help="file that contains the HFB data. Default = {})".format(file))
parser.pictures()
parser.pixels_in_x()
parser.pixels_in_y()
parser.quantizations()
parser.SRLs()

## A script may only parse a few of the command-line arguments,
## passing the remaining arguments on to another script or program.
args = parser.parse_known_args()[0]
if args.file:
    file = args.file
if args.pictures:
    pictures = int(args.pictures)
if args.pixels_in_x:
    pixels_in_x = int(args.pixels_in_x)
if args.pixels_in_y:
    pixels_in_y = int(args.pixels_in_y)
if args.quantizations:
    quantizations = args.quantizations
if args.SRLs:
    SRLs = int(args.SRLs)

## Size of the component 'Y' (measured in pixels).
Y_size = pixels_in_y * pixels_in_x
## Size of the components 'U' and 'V' (measured in pixels).
U_size = V_size = Y_size / 4
## Size of the components 'YUV' (measured in pixels).
YUV_size = Y_size + U_size + V_size

## Copy only the required images.
try:
    check_call("trace dd" +
               " if=" + file + 
               " of=" + file + ".tmp"
               " bs=" + str(YUV_size) +
               " count=" + str(pictures),
               shell=True)
except CalledProcessError:
    sys.exit(-1)



# Demultiplexing and encoding the 'Y' component.
#-----------------------------------------------
try:
    check_call("trace demux " + str(YUV_size) + " 0 " + str(Y_size)
               + " < " + file
               + ".tmp | /usr/bin/split --numeric-suffixes --suffix-length=4 --bytes="
               + str(Y_size) + " - " + file + "_Y_",
               shell=True)
except CalledProcessError:
    sys.exit(-1)

## Current image number iteration.
image_number = 0
while image_number < pictures:

    ## Current image number iteration.
    str_image_number = '%04d' % image_number
    ## Current image name iteration.
    image_filename = file + "_Y_" + str_image_number

    try:
        check_call("trace mv " + image_filename + " " + image_filename + ".raw",
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

    try:
        check_call("trace ltw -C"
                   + " -i " + image_filename + ".raw"
                   + " -o " + image_filename + ".ltw"
                   + " -c " + os.environ["MCTF"] + "/bin/config-hfb.txt"
                   + " -h " + str(pixels_in_y)
                   + " -w " + str(pixels_in_x) 
                   + " -r 2 "
                   + " -q " + str(quantizations)
                   + " -a 0"
                   + " -l " + str(SRLs),
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

    image_number += 1



# Demultiplexing and encoding the 'U' component.
#-----------------------------------------------
try:
    check_call("trace demux "
               + str(YUV_size) + " " + str(Y_size) + " " + str(U_size)
               + " < " + file
               + ".tmp | /usr/bin/split --numeric-suffixes --suffix-length=4 --bytes="
               + str(U_size) + " - " + file + "_U_",
               shell=True)
except CalledProcessError:
    sys.exit(-1)

image_number = 0
while image_number < pictures:

    str_image_number = '%04d' % image_number
    image_filename = file + "_U_" + str_image_number

    try:
        check_call("trace mv " + image_filename + " " + image_filename + ".raw",
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

    try:
        check_call("trace ltw -C"
                   + " -i " + image_filename + ".raw"
                   + " -o " + image_filename + ".ltw"
                   + " -c " + os.environ["MCTF"] + "/bin/config-hfb.txt"
                   + " -h " + str(pixels_in_y/2)
                   + " -w " + str(pixels_in_x/2) 
                   + " -r 2 "
                   + " -q " + str(quantizations)
                   + " -a 0"
                   + " -l " + str(SRLs),
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

    image_number += 1




# Demultiplexing and encoding the 'V' component.
#-----------------------------------------------
try:
    check_call("trace demux "
               + str(YUV_size) + " " + str(U_size+Y_size) + " " + str(V_size)
               + " < " + file
               + ".tmp | /usr/bin/split --numeric-suffixes --suffix-length=4 --bytes="
               + str(V_size) + " - " + file + "_V_",
               shell=True)
except CalledProcessError:
    sys.exit(-1)

image_number = 0
while image_number < pictures:

    str_image_number = '%04d' % image_number
    image_filename = file + "_V_" + str_image_number

    try:
        check_call("trace mv " + image_filename + " " + image_filename + ".raw",
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

    try:
        check_call("trace ltw -C"
                   + " -i " + image_filename + ".raw"
                   + " -o " + image_filename + ".ltw"
                   + " -c " + os.environ["MCTF"] + "/bin/config-hfb.txt"
                   + " -h " + str(pixels_in_y/2)
                   + " -w " + str(pixels_in_x/2) 
                   + " -r 2 "
                   + " -q " + str(quantizations)
                   + " -a 0"
                   + " -l " + str(SRLs),
                   shell=True)
    except CalledProcessError:
        sys.exit(-1)

    image_number += 1






# Compute file sizes.
#---------------------

## File that lists the sizes of the compressed files. It is useful for
## calculating Kbps (see info.py).
file_sizes = open (file + ".ltw", 'w')
## Number of image of the current iteration.
image_number = 0
## Total size of compressed files.
total = 0

while image_number < pictures:

    str_image_number = '%04d' % image_number
    ## Size of the component 'Y' (measured in bytes).
    Ysize = os.path.getsize(file + "_Y_" + str_image_number + ".ltw")
    ## Size of the component 'U' (measured in bytes).
    Usize = os.path.getsize(file + "_U_" + str_image_number + ".ltw")
    ## Size of the component 'V' (measured in bytes).
    Vsize = os.path.getsize(file + "_V_" + str_image_number + ".ltw")

    ## Total size of compressed files of the current iteration.
    size = Ysize + Usize + Vsize
    total += size
    file_sizes.write(str(total) + "\n")

    image_number += 1
