#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# Peak signal-to-noise ratio. Requires: https://github.com/vicente-gonzalez-ruiz/SNR

import sys
import os
from arguments_parser import arguments_parser
import logging

logging.basicConfig()
log = logging.getLogger("compress")

parser = arguments_parser(description="PSNR computation")
parser.add_argument("--original",
                    help="Original video.",
                    default='container_352x288x30x420x300.yuv')
parser.pixels_in_x()
parser.pixels_in_y()

args = parser.parse_known_args()[0]
original = args.original
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)

bytes_per_picture = pixels_in_x * pixels_in_y + (pixels_in_x/2 * pixels_in_y/2) * 2

command = "snr --type=uchar --peak=255 --file_A=" + original + \
          " --file_B=low_0 --block_size=" + str(bytes_per_picture) + \
          " | grep PSNR | grep dB "
sys.stderr.write(command + "\n")
out = os.popen(command).read()
sys.stderr.write(out + "\n")
psnr = float(out.split("\t")[2])
print(psnr)
