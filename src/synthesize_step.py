#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# Iterates temporal inverse transform.

from shell import Shell as shell
from arguments_parser import arguments_parser
from colorlog import ColorLog
import logging

log = ColorLog(logging.getLogger("synthesize_step"))
log.setLevel('INFO')
shell.setLogger(log)

parser = arguments_parser(description="Performs a step of the temporal synthesis.")
parser.block_overlaping()
parser.block_size()
parser.add_argument("--pictures",
                    help="Number of pictures to synthesize.",
                    default=1)
parser.pixels_in_x()
parser.pixels_in_y()
parser.search_range()
parser.subpixel_accuracy()
parser.add_argument("--temporal_subband",
                    help="Iteration of the temporal transform.",
                    default=0)
parser.update_factor()

args = parser.parse_known_args()[0]
block_overlaping = int(args.block_overlaping)
block_size = int(args.block_size)
pictures = int(args.pictures)
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
search_range = int(args.search_range)
subpixel_accuracy = int(args.subpixel_accuracy)
subband = int(args.temporal_subband)
update_factor = float(args.update_factor)

shell.run("mctf un_update"
          + " --block_size="        + str(block_size)
          + " --even_fn="           + "even_"        + str(subband)
          + " --frame_types_fn="    + "frame_types_" + str(subband)
          + " --H_fn="           + "H_"        + str(subband)
          + " --L_fn="            + "L_"         + str(subband)
          + " --motion_fn="         + "motion_"      + str(subband)
          + " --pictures="          + str(pictures)
          + " --pixels_in_x="       + str(pixels_in_x)
          + " --pixels_in_y="       + str(pixels_in_y)
          + " --subpixel_accuracy=" + str(subpixel_accuracy)
          + " --update_factor="     + str(update_factor))

shell.run("mctf correlate"
          + " --block_overlaping="  + str(block_overlaping)
          + " --block_size="        + str(block_size)
          + " --even_fn="           + "even_"        + str(subband)
          + " --frame_types_fn="    + "frame_types_" + str(subband)
          + " --H_fn="           + "H_"        + str(subband)
          + " --motion_in_fn="      + "motion_"      + str(subband)
          + " --odd_fn="            + "odd_"         + str(subband)
          + " --pictures="          + str(pictures)
          + " --pixels_in_x="       + str(pixels_in_x)
          + " --pixels_in_y="       + str(pixels_in_y)
          + " --search_range="      + str(search_range)
          + " --subpixel_accuracy=" + str(subpixel_accuracy))

shell.run("mctf merge"
          + " -e " + "even_" + str(subband)
          + " -l " + "L_"  + str(subband-1)
          + " -o " + "odd_"  + str(subband)
          + " -p " + str(pictures)
          + " -x " + str(pixels_in_x)
          + " -y " + str(pixels_in_y))
