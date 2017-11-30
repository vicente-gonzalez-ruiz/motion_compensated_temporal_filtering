#!/usr/bin/python
# -*- coding: iso-8859-15 -*-


## @file motion_expand_gzip.py
#  Decompressing the motion vectors, using gzip.
#
#  After decompressing, joint files motion fields are called
#  "*_motion_residue_i_j.*" into one file per temporal subband.
#  Where i = temporal iteration, and j = GOP.\n The exact format of
#  how information is organized in one of these files depends on the
#  implementation of motion.cpp.\n However, appear the same number of
#  bidirectional motion fields that picture there at that level of
#  temporal resolution for the GOP, but multiplying by 2.
#
#  @author Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package motion_expand_gzip
#  Decompressing the motion vectors, using gzip.
#
#  After decompressing, joint files motion fields are called
#  "*_motion_residue_i_j.*" into one file per temporal subband.
#  Where i = temporal iteration, and j = GOP.\n The exact format of
#  how information is organized in one of these files depends on the
#  implementation of motion.cpp.\n However, appear the same number of
#  bidirectional motion fields that picture there at that level of
#  temporal resolution for the GOP, but multiplying by 2.


import sys
import getopt
import os
import display
from GOP import GOP

## Number of blocks in the X direction.
blocks_in_x = 0
## Number of blocks in the Y direction.
blocks_in_y = 0
## Temporal iteration.
iteration = 1
## Name of the file with the motion fields.
file = ""
## Number of images to process.
pictures = 33
## Temporal resolution levels.
temporal_levels = 5


## Documentation of usage.
#  - -[-]blocks_in_[x] = number of blocks in the X direction.
#  - -[-]blocks_in_[y] = number of blocks in the Y direction.
#  - -[-i]iteration = temporal iteration.
#  - -[-f]ile = name of the file with the motion fields.
#  - -[-p]ictures = number of images to process.
#  - -[-t]ermporal_levels = number of temporal levels.
def usage():
    sys.stderr.write("+-------------------------+\n")
    sys.stderr.write("| MCTF motion_expand_gzip |\n")
    sys.stderr.write("+-------------------------+\n")
    sys.stderr.write("   -[-]blocks_in_[x] = number of blocks in the X direction (%d)\n" % blocks_in_x)
    sys.stderr.write("   -[-]blocks_in_[y] = number of blocks in the Y direction (%d)\n" % blocks_in_y)
    sys.stderr.write("   -[-i]iteration = temporal iteration (%d)\n" % iterationi)
    sys.stderr.write("   -[-f]ile = name of the file with the motion fields (\"%s\")\n" % file)
    sys.stderr.write("   -[-p]ictures = number of images to process (%d)\n" % pictures)
    sys.stderr.write("   -[-t]ermporal_levels = number of temporal levels (%d)\n" % temporal_levels)

    
ifdef({{DEBUG}},
display.info(str(sys.argv[0:]) + '\n')
)

## Define the variable for options.
opts = ""

try:
    opts, extraparams = getopt.getopt(sys.argv[1:],
                                      "x:y:i:f:p:t:h",
                                      ["blocks_in_x=",
                                       "blocks_in_y=",
                                       "iteration=",
                                       "file=",
                                       "pictures=",
                                       "temporal_levels=",
                                       "help"
                                       ])

except getopt.GetoptError, exc:
    display.info(sys.argv[0] + ": " + exc.msg + "\n")

for o, a in opts:
    if o in ("-x", "--blocks_in_x"):
        blocks_in_x = int(a)
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": blocks_in_x=" + str(blocks_in_x) + '\n')
        )
    if o in ("-y", "--blocks_in_y"):
        blocks_in_y = int(a)
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": blocks_in_y=" + str(blocks_in_y) + '\n')
        )
    if o in ("-i", "--iteration"):
        iteration = int(a)
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": iteration=" + str(iteration) + '\n')
        )
    if o in ("-i", "--file"):
        file = a
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": file=" + file + '\n')
        )
    if o in ("-p", "--pictures"):
        pictures = int(a)
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": pictures=" + str(pictures) + '\n')
        )
    if o in ("-t", "--temporal_levels"):
        temporal_levels = int(a)
        ifdef({{DEBUG}},
        display.info(sys.argv[0] + ": temporal_levels=" + str(temporal_levels) + '\n')
        )
    if o in ("-h", "--help"):
        usage()
        sys.exit()

## Initializes the class GOP (Group Of Pictures).
gop=GOP()

## Extract the value of the size of a GOP, that is, the number of images.
GOP_size = gop.get_size(temporal_levels)
ifdef({{DEBUG}},
sys.stdout.write(sys.argv[0] + ": GOP_size=" + str(GOP_size) + '\n')
)

## Number of GOPs.
number_of_GOPs = pictures / GOP_size
ifdef({{DEBUG}},
sys.stdout.write(sys.argv[0] + ": number_of_GOPs=" + str(number_of_GOPs) + '\n')
)

## Instruction compression by gzip.
command = "cat " + file + ".gz | gzip -d > " + file

ifdef({{DEBUG}},
sys.stdout.write(sys.argv[0] + ": " + command + "\n")
)
    
os.system(command)
