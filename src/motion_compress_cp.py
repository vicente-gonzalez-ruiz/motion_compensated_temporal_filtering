#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

## @file motion_compress_cp.py
#  It stores the motion vectors, without using any compression.
#
#  @author Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.

## @package motion_compress_cp
#  It stores the motion vectors, without using any compression.

import sys
import getopt
import os
import display

## Name of the file with the motion fields.
file = ""

## Documentation of usage.
#  -[-f]ile = Name of the file with the motion fields.
def usage():
    sys.stderr.write("+-------------------------+\n")
    sys.stderr.write("| MCTF motion_compress_cp |\n")
    sys.stderr.write("+-------------------------+\n")

## Define the variable for options.
opts = ""

try:
    opts, extraparams = getopt.getopt(sys.argv[1:], "f:h", ["file=", "help"])

except getopt.GetoptError, exc:
    display.info(sys.argv[0] + ": " + exc.msg + "\n")

for o, a in opts:
    if o in ("f", "--file"):
        file = a
        display.info(sys.argv[0] + ": file=" + file + '\n')
    if o in ("h", "--help"):
        usage()
        sys.exit()

os.system("cp " + file + " " + file + ".cp")
