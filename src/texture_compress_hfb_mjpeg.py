#!/usr/bin/python
# -*- coding: iso-8859-15 -*-


## @file texture_compress_hfb_mjpeg.py
#  Compress the HFB texture data, using Motion JPEG.
#  The two main steps performed are:
#  - Transforms a raw file to YUV file.
#  - Encode components.
#
#  @authors Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package texture_compress_hfb_mjpeg
#  Compress the HFB texture data, using Motion JPEG.
#  The two main steps performed are:
#  - Transforms a raw file to YUV file.
#  - Encode components.


import sys
import os
import display
import getopt


## Number of components.
COMPONENTS = 3
## Number of bytes per component.
BYTES_PER_COMPONENT = 1
## File that contains the HFB data.
file = ""
## Controls the quality level and the bit-rate of the code-stream.
slopes = "32"
## Number of images to process.
pictures = 33
## Width of the pictures.
pixels_in_x = 352
## Height of the pictures.
pixels_in_y = 288
## Current temporal iteration.
subband = 1
## Number of temporal levels.
temporal_levels = 6


## Documentation of usage.
#  - -[-f]ile = file that contains the HFB data.
#  - -[-p]ictures = number of images to process.
#  - -[-]pixels_in_[x] = size of the X dimension of the pictures.
#  - -[-]pixels_in_[y] = size of the Y dimension of the pictures.
#  - -[-s]lopes = distortion-length slope value for the only quality layer.
#  - -[-]sub[b]and = subband to compress.
#  - -[-t]emporal_levels = number of temporal levels.
def usage():
    sys.stderr.write("+---------------------------------+\n")
    sys.stderr.write("| MCTF texture_compress_hfb_mjpeg |\n")
    sys.stderr.write("+---------------------------------+\n")
    sys.stderr.write("\n")
    sys.stderr.write("  Description:\n")
    sys.stderr.write("   Compress the HFB texture data using Motion JPEG.\n")
    sys.stderr.write("\n")
    sys.stderr.write("  Parameters:\n")
    sys.stderr.write("\n")
    sys.stderr.write("   -[-f]ile = file that contains the HFB data (\"%s\")\n" % file)
    sys.stderr.write("   -[-p]ictures = number of images to process (%d)\n" % pictures)
    sys.stderr.write("   -[-]pixels_in_[x] = size of the X dimension of the pictures (%d)\n" % pixels_in_x)
    sys.stderr.write("   -[-]pixels_in_[y] = size of the Y dimension of the pictures (%d)\n" % pixels_in_y)
    sys.stderr.write("   -[-s]lopes = distortion-length slope value for the only quality layer (%s)\n" % "", slopes)
    sys.stderr.write("   -[-]sub[b]and = subband to compress (%d)\n" % subband)
    sys.stderr.write("   -[-t]emporal_levels = number of temporal levels (%d)\n" % temporal_levels)
    sys.stderr.write("\n")

## Define the variable for options.
opts = ""

display.info(str(sys.argv[0:]) + '\n')

try:
    opts, extraparams = getopt.getopt(sys.argv[1:],"f:p:s:x:y:b:t:h",
                                      ["file=",
                                       "pictures=",
                                       "pixels_in_x=",
                                       "pixels_in_y=",
                                       "subband=",
                                       "slopes=",
                                       "temporal_levels=",
                                       "help"
                                       ])
except getopt.GetoptError, exc:
    sys.stderr.write(sys.argv[0] + ": " + exc.msg + "\n")
    sys.exit(2)

for o, a in opts:
    if o in ("-f", "--file"):
        file = a
        display.info(sys.argv[0] + ": file=" + file + '\n')

    if o in ("-p", "--pictures"):
        pictures = int(a)
        display.info(sys.argv[0] + ": pictures=" + str(pictures) + '\n')

    if o in ("-x", "--pixels_in_x"):
        pixels_in_x = int(a)
        display.info(sys.argv[0] + ": pixels_in_x=" + str(pixels_in_x) + '\n')

    if o in ("-y", "--pixels_in_y"):
        pixels_in_y = int(a)
        display.info(sys.argv[0] + ": pixels_in_y=" + str(pixels_in_y) + '\n')

    if o in ("-s", "--slopes"):
        slopes = a
        display.info(sys.argv[0] + ": slopes=" + slopes + '\n')

    if o in ("-b", "--subband"):
        subband = int(a)
        display.info(sys.argv[0] + ": subband=" + str(subband) + '\n')

    if o in ("-t", "--temporal_levels"):
        temporal_levels = int(a)
        display.info(sys.argv[0] + ": temporal_levels=" + str(temporal_levels) + '\n')

    if o in ("-h", "--help"):
	usage()
	sys.exit()

## In the file "trace" a log of execution is recorded.
trace = open ("trace", 'a')

# Raw file to YUV file.
command = "mv " + file + " " + file + ".yuv"
trace.write(sys.argv[0] + ": " + command + "\n")
os.system(command)

## Encode.
command = "(ffmpeg"\
    + " " + "-y " \
    + " " + "-qscale " + slopes \
    + " " + "-s " + str(pixels_in_x) + "x" + str(pixels_in_y) \
    + " " + "-i " + file + ".yuv" \
    + " " + file + ".mjpeg >&2) 2> /dev/null"

trace.write(sys.argv[0] + ": " + command + "\n")
ifdef({{DEBUG}},
os.system(command)
,
trace.write(sys.argv[0] + ": " + command + " > /dev/null\n")
os.system(command + " > /dev/null")
)

# YUV file to Raw file.
command = "mv " + file + ".yuv " + file
trace.write(sys.argv[0] + ": " + command + "\n")
os.system(command)
