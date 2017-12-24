#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

#  Traces a RD (Rate-Distortion) curve.

import sys
import os
from GOP import GOP
from subprocess import check_call
from subprocess import CalledProcessError
from arguments_parser import arguments_parser
import logging

logging.basicConfig()
log = logging.getLogger("compress")

parser = arguments_parser(description="Encodes a sequence of pictures.")
parser.always_B()
parser.block_overlaping()
parser.block_size()
parser.border_size()
parser.GOPs()
parser.min_block_size()
parser.motion_layers()
parser.motion_quantization()
parser.motion_quantization_step()
parser.pixels_in_x()
parser.pixels_in_y()
parser.search_range()
parser.subpixel_accuracy()
parser.quantization_max()
parser.quantization_min()
parser.SRLs()
parser.TRLs()
parser.update_factor()

args = parser.parse_known_args()[0]
always_B = int(args.always_B)
block_overlaping = int(args.block_overlaping)
block_size = int(args.block_size)
min_block_size = int(args.min_block_size)
border_size = int(args.border_size)
GOPs = int(args.GOPs)
motion_layers = str(args.motion_layers); log.debug("motion_layers={}".format(motion_layers))
motion_quantization = str(args.motion_quantization); log.debug("motion_quantization={}".format(motion_quantization))
motion_quantization_step = str(args.motion_quantization_step); log.debug("motion_quantization_step={}".format(motion_quantization_step))
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
quantization_max = int(args.quantization_max)
quantization_min = int(args.quantization_min)
search_range = int(args.search_range)
subpixel_accuracy = int(args.subpixel_accuracy)
TRLs = int(args.TRLs)
SRLs = int(args.SRLs)
update_factor = float(args.update_factor)

output = open("psnr_vs_br.txt", "w")

slope = 
while slopes < 65535:

    ## Creates a copy of the original video.
    command = "cp " + original + " low_0"
    os.system(command)

    command = "mctf compress" + \
              " --block_overlaping=" + str(block_overlaping) + \
              " --block_size=" + str(block_size) + \
              " --border_size=" + str(border_size) + \
              " --min_block_size=" + str(min_block_size) + \
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
              " --min_block_size=" + str(min_block_size) + \
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
