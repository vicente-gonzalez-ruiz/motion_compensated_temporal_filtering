#!/bin/sh
''''exec python3 -O -- "$0" ${1+"$@"} # '''
#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# Peak signal-to-noise ratio.
# Requires: https://github.com/vicente-gonzalez-ruiz/SNR

import sys
import os
from GOP import GOP
from arguments_parser import arguments_parser
import traceback
import logging

log = logging.getLogger("psnr")
log.setLevel('INFO')

parser = arguments_parser(description="PSNR computation between 2 sequences")
parser.add_argument("--file_A",
                    help="First sequence",
                    default="../L_0")
parser.add_argument("--file_B",
                    help="Second sequence",
                    default="L_0")
parser.pixels_in_x()
parser.pixels_in_y()
parser.GOPs()
parser.TRLs()

args = parser.parse_known_args()[0]
file_A = args.file_A
file_B = args.file_B
pixels_in_x = int(args.pixels_in_x)
pixels_in_y = int(args.pixels_in_y)
GOPs = int(args.GOPs)
TRLs = int(args.TRLs)

bytes_per_picture = 3*[None]
bytes_per_picture[0] = pixels_in_x * pixels_in_y
bytes_per_picture[1] = int(pixels_in_x/2 * pixels_in_y/2)
bytes_per_picture[2] = bytes_per_picture[1]

extension = 3*[None]
extension[0] = 'Y'
extension[1] = 'U'
extension[2] = 'V'

gop=GOP()
GOP_size = gop.get_size(TRLs)
pictures = (GOPs - 1) * GOP_size + 1
COMPONENTS = 3

avg = 3*[None]
avg[0] = 0.0
avg[1] = 0.0
avg[2] = 0.0

#import ipdb; ipdb.set_trace()

for p in range(pictures):

    for c in range(COMPONENTS):

        fn_a = file_A + "/" + str('%04d' % (p+1)) + "." + extension[c]
        fn_b = file_B + "/" + str('%04d' % (p+1)) + "." + extension[c]
        
        command = "(snr --type=uchar --peak=255" \
                  + " --file_A=" + fn_a \
                  + " --file_B=" + fn_b \
                  + " --block_size=" + str(bytes_per_picture[c]) + ')'
        if not __debug__:
            command += " 2> /dev/null"
    
        command += " | grep PSNR | grep dB"

        log.info(command)
        out = os.popen(command).read()
        log.debug("output = {}".format(out))
            
        try:
            psnr = float(out.split("\t")[2])
        except:
            log.error("Exception {}".format(traceback.format_exc()))
            sys.exit(-1)
            
        avg[c] += psnr

avg[0] /= pictures
avg[1] /= pictures
avg[2] /= pictures
print((4*avg[0]+avg[1]+avg[2])/6.0)
