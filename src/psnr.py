#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

## @file psnr.py
#  Peak signal-to-noise ratio.
#  @authors Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package psnr
#  Peak signal-to-noise ratio.

import sys
import getopt
import os
import display

## Size of the X dimension of the pictures.
pixels_in_x = 352
## Size of the Y dimension of the pictures.
pixels_in_y = 288

## Documentation of usage.
#  - -[-]pixels_in_[x]=size of the X dimension of the pictures.
#  - -[-]pixels_in_[Y]=size of the Y dimension of the pictures.
def usage():
    sys.stderr.write("\n")
    sys.stderr.write("  Description:\n")
    sys.stderr.write("\n")
    sys.stderr.write("    Compute the Kbps/GOP.\n")
    sys.stderr.write("\n")
    sys.stderr.write("  Parameters:\n")
    sys.stderr.write("\n")
    sys.stderr.write("   -[-]pixels_in_[x]=size of the X dimension of the pictures (%d)\n" %  pixels_in_y)
    sys.stderr.write("   -[-]pixels_in_[y]=size of the Y dimension of the pictures (%d)\n" %  pixels_in_x)
    sys.stderr.write("\n")

ifdef({{DEBUG}},
display.info(str(sys.argv[0:]) + '\n')
)

try:
    opts, extraparams = getopt.getopt(sys.argv[1:],"o:x:y::h",
                                      ["original=",
                                       "pixels_in_x=",
                                       "pixels_in_y=",
                                       "help"
                                       ])
except getopt.GetoptError, exc:
    sys.stderr.write(sys.argv[0] + ": " + exc.msg + "\n")
    sys.exit(2)

for o, a in opts:
    if o in ("-o", "--original"):
        ## Original signal.
        original = a
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": original=" + original + '\n')
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

    if o in ("-h", "--help"):
	usage()
	sys.exit()

## Calculate the number of bytes per image
bytes_per_picture = pixels_in_x * pixels_in_y + (pixels_in_x/2 * pixels_in_y/2) * 2

display.info(sys.argv[0] + ": bytes_per_picture=" + str(bytes_per_picture) + "\n")

## Is an engineering term for the ratio between the maximum possible power of a signal and the power of corrupting noise that affects the fidelity of its representation.
command = "mctf snr --type=uchar --peak=255 --file_A=" + original + \
          " --file_B=low_0 --block_size=" + str(bytes_per_picture) + \
          " | grep PSNR | grep dB "

display.info(sys.argv[0] + ": " + command + "\n")
## Displays information about the instruction which calls your system.
out = os.popen(command).read()
## Return of execution.
psnr = float(out.split(" ")[2])

print psnr
