#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

## @file psnr_vs_br.py
#  Traces a RD (Rate-Distortion) curve.
#  @authors Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package psnr_vs_br
#  Traces a RD (Rate-Distortion) curve.

import sys
import getopt
import os
import array
import display
import string

## Number of overlaped pixels between the blocks in the motion compensation process.
block_overlaping = 0
## Size of the blocks in the motion estimation process.
block_size = 16
## Minimal block size allowed in the motion estimation process.
block_size_min = 16
## Size of the border of the blocks in the motion estimation process.
border_size = 0
## Original signal.
original = "../videos/mobile_352x288x30x420x300.yuv"
## Number of images to process.
pictures = 33
## Width of the pictures.
pixels_in_x = 352
## Height of the pictures.
pixels_in_y = 288
## Size of the search areas in the motion estimation process.
search_range = 4
## Controls the quality level and the bit-rate of the code-stream of textures.
slopes = "52000"
## Subpixel motion estimation order.
subpixel_accuracy = 0
## Temporal Resolution Levels.
temporal_levels = 6

## Documentation of usage.
#  - -[-]block_o[v]erlaping = number of overlaped pixels between the blocks in the motion estimation.\n
#  - -[-]block_si[z]e_min = minimal block size allowed in the motion estimation.\n
#  - -[-]block_si[z]e_min = minimal block size allowed in the motion estimation.\n
#  - -[-]bor[d]der_size = size of the border of the blocks in the motion estimation process.\n
#  - -[-o]riginal = original video to compare.\n
#  - -[-p]ictures = number of images to process.\n
#  - -[-]pixels_in_[x] = size of the X dimension of the pictures.\n
#  - -[-]pixels_in_[y] = size of the Y dimension of the pictures.\n
#  - -[-s]earch_range = size of the searching area of the motion estimation.\n
#  - -[-]s[l]opes = distortion-length slope for each quality layer.\n
#  - -[-]subpixel_[a]ccuracy = sub-pixel accuracy of the motion estimation.\n
#  - -[-t]emporal_levels = number of iterations of the temporal transform + 1.
def usage():
    sys.stderr.write("+--------------------------+\n")
    sys.stderr.write("| MCTF psnr_vs_br compress |\n")
    sys.stderr.write("+--------------------------+\n")
    sys.stderr.write("\n")
    sys.stderr.write("  Description:\n")
    sys.stderr.write("\n")
    sys.stderr.write("   Traces a RD (Rate-Distortion) curve.\n")
    sys.stderr.write("\n")
    sys.stderr.write("  Parameters:\n")
    sys.stderr.write("\n")
    sys.stderr.write("   -[-]block_o[v]erlaping=number of overlaped pixels between the blocks in the motion estimation (%d)\n" % block_overlaping)
    sys.stderr.write("   -[-b]lock_size=size of the blocks in the motion estimation process (%d)\n" % block_size)
    sys.stderr.write("   -[-]block_si[z]e_min=minimal block size allowed in the motion estimation (%d)\n" % block_size_min)
    sys.stderr.write("   -[-]bor[d]der_size=size of the border of the blocks in the motion estimation process (%d)\n" % border_size)
    sys.stderr.write("   -[-o]riginal=original video to compare (%s)\n" % original)
    sys.stderr.write("   -[-p]ictures=number of images to process (%d)\n" % pictures)
    sys.stderr.write("   -[-]pixels_in_[x]=size of the X dimension of the pictures (%d)\n" %  pixels_in_x)
    sys.stderr.write("   -[-]pixels_in_[y]=size of the Y dimension of the pictures (%d)\n" %  pixels_in_y)
    sys.stderr.write("   -[-s]earch_range=size of the searching area of the motion estimation (%d)\n" % search_range)
    sys.stderr.write("   -[-]s[l]opes=distortion-length slope for each quality layer (\"%s\")\n" % slopes)
    sys.stderr.write("   -[-]subpixel_[a]ccuracy=sub-pixel accuracy of the motion estimation (%d)\n" % subpixel_accuracy)
    sys.stderr.write("   -[-t]emporal_levels=number of iterations of the temporal transform + 1 (%d)\n" % temporal_levels)
    sys.stderr.write("\n")

## Define the variable for options.
opts = ""

ifdef({{DEBUG}},
display.info(str(sys.argv[0:]) + '\n')
)

try:
    opts, extraparams = getopt.getopt(sys.argv[1:],"v:b:z:d:p:x:y:l:p:a:t:h",
                                      ["block_overlaping=",
                                       "block_size=",
                                       "block_size_min=",
                                       "border_size=",
                                       "original=",
                                       "pictures=",
                                       "pixels_in_x=",
                                       "pixels_in_y=",
                                       "search_range=",
                                       "slopes=",
                                       "subpixel_accuracy=",
                                       "temporal_levels=",
                                       "help"
                                       ])
except getopt.GetoptError, exc:
    sys.stderr.write(sys.argv[0] + ": " + exc.msg + "\n")
    sys.exit(2)

for o, a in opts:
    if o in ("-v", "--block_overlaping"):
        block_overlaping = int(a)
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": block_overlaping=" + str(block_overlaping) + '\n')
        )
    if o in ("-b", "--block_size"):
        block_size = int(a)
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": block_size=" + str(block_size) + '\n')
        )
    if o in ("-z", "--block_size_min"):
        block_size_min = int(a)
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": block_size_min=" + str(block_size_min) + '\n')
        )
    if o in ("-d", "--border_size"):
        border_size = int(a)
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": border_size=" + str(border_size) + '\n')
        )
    if o in ("-o", "--original"):
        original = a
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": original=" + original + '\n')
        )
    if o in ("-p", "--pictures"):
        pictures = int(a)
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": pictures=" + str(pictures) + '\n')
        )
    if o in ("-x", "--pixels_in_x"):
        pixels_in_x = int(a)
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": pixels_in_x=" + str(pixels_in_x) + '\n')
        )
    if o in ("-y", "--pixels_in_y"):
        pixels_in_y = int(a)
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": pixels_in_y=" + str(pixels_in_y) + '\n')
        )
    if o in ("-s", "--search_range"):
        search_range = int(a)
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": search_range=" + str(search_range) + '\n')
        )
    if o in ("-l", "--slopes"):
        slopes = a
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": slopes=" + slopes + '\n')
        )
#        slopes += ",65535"
    if o in ("-a", "--subpixel_accuracy"):
        subpixel_accuracy = int(a)
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": subpixel_accuracy=" + str(subpixel_accuracy) + '\n')
        )
    if o in ("-t", "--temporal_levels"):
        temporal_levels = int(a)
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": temporal_levels=" + str(temporal_levels) + '\n')
        )
    if o in ("-h", "--help"):
	usage()
	sys.exit()

## Output file descriptor.
output = open("psnr_vs_br.txt", "w")

slopes = 52000
while slopes < 65535:

    ## Creates a copy of the original video.
    command = "cp " + original + " low_0"
    os.system(command)

    command = "mctf compress" + \
              " --block_overlaping=" + str(block_overlaping) + \
              " --block_size=" + str(block_size) + \
              " --block_size_min=" + str(block_size_min) + \
              " --border_size=" + str(border_size) + \
              " --pictures=" + str(pictures) + \
              " --pixels_in_x=" + str(pixels_in_x) + \
              " --pixels_in_y=" + str(pixels_in_y) + \
              " --search_range=" + str(search_range) + \
              " --slopes=\"" + str(slopes) + "\"" + \
              " --subpixel_accuracy=" + str(subpixel_accuracy) + \
              " --temporal_levels=" + str(temporal_levels)
    os.system(command)

    command = "mctf expand" + \
              " --block_overlaping=" + str(block_overlaping) + \
              " --block_size=" + str(block_size) + \
              " --block_size_min=" + str(block_size_min) + \
              " --pictures=" + str(pictures) + \
              " --pixels_in_x=" + str(pixels_in_x) + \
              " --pixels_in_y=" + str(pixels_in_y) + \
              " --search_range=" + str(search_range) + \
              " --subpixel_accuracy=" + str(subpixel_accuracy) + \
              " --temporal_levels=" + str(temporal_levels)
    os.system(command)

#    command = "mctf info" + \
#              " --pictures=" + str(pictures) + \
#              " --temporal_levels=" + str(temporal_levels) + \
#              " | grep \"Total Kbps average\""
    command = "mctf info" + \
              " --pictures=" + str(pictures) + \
              " --temporal_levels=" + str(temporal_levels)

    ## System call for the calculation of Rate.
    out = os.popen(command).read()
    print "......"
    print out
    ## Initializes bit-rate.
    br = float(out.split(" ")[3])

    command = "mctf psnr" + \
              " --original=" + original + \
              " --pixels_in_x=" + str(pixels_in_x) + \
              " --pixels_in_y=" + str(pixels_in_y)

    ## System call for the calculation of Distortion.
    out = os.popen(command).read()
    ## Initializes distortion.
    psnr = float(out)

    output.write("%f\t" % br)
    output.write("%f\t" % psnr)
    output.write("#%d\n" % slopes)
    output.flush()
    sys.stdout.write("%f\t" % br)
    sys.stdout.write("%f\t" % psnr)
    sys.stdout.write("#%d\n" % slopes)

    slopes += 100
