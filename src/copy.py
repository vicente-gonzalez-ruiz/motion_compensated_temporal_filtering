#!/bin/sh
''''exec python3 -- "$0" ${1+"$@"} # '''

#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# Copy MCTF structure to a different place.

import sys
import io
from GOP import GOP
from arguments_parser import arguments_parser
import traceback
from shell import Shell as shell
import os
from colorlog import ColorLog
import logging

log = ColorLog(logging.getLogger("copy"))
log.setLevel('INFO')
shell.setLogger(log)

parser = arguments_parser(description="Copy MCTF structure.")
parser.GOPs()
parser.TRLs()
parser.add_argument("--destination",
                    help="destination directory (must exist)",
                    default="/tmp")

args = parser.parse_known_args()[0]
GOPs = int(args.GOPs)
TRLs = int(args.TRLs)
destination = args.destination

gop = GOP()
GOP_size = gop.get_size(TRLs)
pictures = GOP_size*(GOPs-1)+1

IMG_EXT = os.environ["MCTF_IMG_EXT"]

sys.stdout.write("\n" + sys.argv[0] + ":\n\n")
sys.stdout.write("TRLs           = " + str(TRLs) + " temporal resolution levels\n")
sys.stdout.write("Pictures       = " + str(pictures) + " pictures\n")
sys.stdout.write("GOP size       = " + str(GOP_size) + " pictures\n")
sys.stdout.write("Number of GOPs = " + str(GOPs) + " groups of pictures\n")

# Frame types
shell.run("cp frame_types_* " + destination)

# L_<TRLs-1>
shell.run("mkdir "
          + destination
          + "/L_"
          + str(TRLs - 1))
shell.run("cp L_"
          + str(TRLs - 1)
          + "/"
          + "*."
          + IMG_EXT
          + " "
          + destination
          + "/L_"
          +  str(TRLs - 1))
shell.run("cp L_"
          + str(TRLs - 1)
          + "/"
          + "*.txt "
          + destination
          + "/L_"
          + str(TRLs - 1))

for subband in range(TRLs-1, 0, -1):
    
    # motion_residue_<subband>
    shell.run("mkdir "
              + destination + "/R_" + str(subband))
    shell.run("cp R_" + str(subband) + "/*.j2c "
              + destination + "/R_" + str(subband))

    # H_<subband>
    shell.run("mkdir "
              + destination + "/H_" + str(subband))
    shell.run("cp H_" + str(subband) + "/*." + IMG_EXT + " "
              + destination + "/H_" + str(subband))
    shell.run("cp H_" + str(subband) + "/*.txt "
              + destination + "/H_" + str(subband))
