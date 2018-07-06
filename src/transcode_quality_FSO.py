#!/bin/sh
''''exec python3 -- "$0" ${1+"$@"} # '''
#!/usr/bin/env python3
#!/home/vruiz/.pyenv/shims/python -i
# -*- coding: iso-8859-15 -*-

# {{{ Transcode a MCTF sequence in quality.

# Input:
#
#  MJ2K texture sequence.
#
# Output:
#
#  Transcoded MJ2K texture sequence.
#
# Examples:
#
#  mctf transcode_quality --keep_layers=16
#
# Procedure.
#
#  Each temporal subband has been compressed with a number of quality
#  layers. Each quality layer has a slope. This script, GOP by GOP
#  reads the slopes of each quality layer (computing an average if
#  more than one image per temporal subband is found), scales them
#  using the theoretical subband gains which should convert MCTF into
#  a uniform transform, sorts the subbands-layers by their
#  contribution and finally, truncates the Input using this
#  information, to produce the Output.

# }}}

# {{{ Importing

import sys
from GOP import GOP
from arguments_parser import arguments_parser
import io
import operator
from shell import Shell as shell
from colorlog import ColorLog
import logging

log = ColorLog(logging.getLogger("transcode_quality"))
log.setLevel('DEBUG')
shell.setLogger(log)

# }}}

# {{{ Arguments parsing

parser = arguments_parser(
    description="Transcodes in quality a MCJ2K sequence.")
parser.GOPs()
parser.add_argument("--keep_layers",
                    help="Number of quality layers to output",
                    default=16)
parser.TRLs()
parser.layers()
parser.add_argument("--destination",
                    help="destination directory (must exist)",
                    default="/transcode_quality")
parser.slope()

args = parser.parse_known_args()[0]
GOPs = int(args.GOPs)
keep_layers = int(args.keep_layers)
TRLs = int(args.TRLs)
layers = int(args.layers)
destination = args.destination
slope = int(args.slope)

log.info("GOPs={}".format(GOPs))
log.info("keep_layers={}".format(keep_layers))
log.info("TRLs={}".format(TRLs))
log.info("layers={}".format(layers))
log.info("destination={}".format(destination))
log.info("slope={}".format(slope))

# }}}

# --------------------------------------------------------------------
def transcode_picture(filename, layers):
    # {{{ 
    log.debug("transcode_picture: {} {}".format(filename, layers))
    if layers > 0:
        shell.run("trace kdu_transcode"
                  + " -i " + filename
                  + " -jpx_layers sYCC,0,1,2"
                  + " -o " + "transcode_quality/" + filename
                  + " Clayers=" + str(layers))
    # }}}



# --------------------------------------------------------------------
shell.run("mctf $TRANSCODE_QUALITY --GOPs=$GOPs --TRLs=$TRLs --keep_layers=$keep_layers --destination="transcode_quality" --layers=$layers --slope=$slope
cd transcode_quality
mctf create_zero_texture --pixels_in_y=$y_dim --pixels_in_x=$x_dim
mctf info --GOPs=$GOPs --TRLs=$TRLs --FPS=$FPS
mctf expand --GOPs=$GOPs --TRLs=$TRLs
img=1
while [ $img -le $number_of_images ]; do
    _img=$(printf "%04d" $img)
    let img_1=img-1
    _img_1=$(printf "%04d" $img_1)
    
    input=L_0/${_img_1}_0.pgm
    output=L_0/$_img.Y
    PGMTORAW $input $output
    
    input=L_0/${_img_1}_1.pgm
    output=L_0/$_img.U
    PGMTORAW $input $output
    
    input=L_0/${_img_1}_2.pgm
    output=L_0/$_img.V
    PGMTORAW $input $output

    let img=img+1 
done
mctf psnr --file_A L_0 --file_B ../L_0 --pixels_in_x=$x_dim --pixels_in_y=$y_dim --GOPs=$GOPs --TRLs=$TRLs")

# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------


wait = input("PRESS ENTER TO CONTINUE.")
sys.exit(0)
    
# --------------------------------------------------------------------
# {{{ Compute GOPs and pictures
gop = GOP()
GOP_size = gop.get_size(TRLs)
log.info("GOP_size={}".format(GOP_size))

pictures = (GOPs - 1) * GOP_size + 1
log.info("pictures={}".format(pictures))
# }}}

# --------------------------------------------------------------------
# {{{ Create directories
shell.run("mkdir " + destination + "/L_" + str(TRLs - 1))
for subband in range(TRLs-1, 0, -1):
    shell.run("mkdir " + destination + "/R_" + str(subband))
    shell.run("mkdir " + destination + "/H_" + str(subband))
# }}}

#import ipdb; ipdb.set_trace()


log.debug("FSO")
# --------------------------------------------------------------------
# {{{ FSO
subband_layers = []

for gop in range(0, GOPs-1):
    log.info("GOP={}/{}".format(gop, GOPs))
    subband_layers = [0] * TRLs


    log.info("subband layers={}".format(subband_layers))

    wait = input("PRESS ENTER TO CONTINUE.")
    sys.exit(0)
    

    # }}}



    # {{{ Include motion layers in subband_layers

    for t in range(TRLs-1, 0, -1):
        c = 0
        l = len(subband_layers)
        for s in range(l):
            if subband_layers[s][0] == 'H':
                if subband_layers[s][1] == t:
                    subband_layers.insert(c, ('R', t, 0, 0))
                    break
            c += 1

    log.debug("(after including motion layers) subband_layers={}".
              format(subband_layers))
    
    # }}}

    # {{{ Truncate the list of subband_layers

    del subband_layers[keep_layers:]
    log.info("(after truncating) subband_layers={}".format(subband_layers))

    # }}}

    # {{{ Count the number of subband-layers per subband

    # Reset
    slayers_per_subband = {}
    slayers_per_subband[('L', TRLs-1)] = 0
    for i in range(TRLs-1,0,-1):
        slayers_per_subband[('H', i)] = 0
        slayers_per_subband[('R', i)] = 0
        
    # Count
    for i in subband_layers:
        slayers_per_subband[(i[0], i[1])] += 1

    # Write
    with io.open("layers.txt", 'a') as file:
        log.info("{}:{}".format(('L', TRLs-1),
                                slayers_per_subband[('L', TRLs-1)]))
        file.write("{}:{} ".format(('L', TRLs-1),
                                   slayers_per_subband[('L', TRLs-1)]))
        for i in range(TRLs-1, 0, -1):
            log.info("{}:{}".format(('R', i),
                                    slayers_per_subband[('R', i)]))
            file.write("{}:{} ".format(('R', i),
                                       slayers_per_subband[('R', i)]))
        for i in range(TRLs-1, 0, -1):
            log.info("{}:{}".format(('H', i),
                                    slayers_per_subband[('H', i)]))
            file.write("{}:{} ".format(('H', i),
                                       slayers_per_subband[('H', i)]))
        file.write("\n")

    # }}}

    # {{{ Transcode the images

    log.debug(slayers_per_subband)
    for key, value in slayers_per_subband.items():
        pics_per_subband = (1 << (TRLs-key[1]-1))
        for p in range(pics_per_subband * gop,
                       pics_per_subband * gop + pics_per_subband):
            if key[0] == 'L':
                fname = key[0] + '_' + str(key[1]) + '/' \
                + str('%04d' % (p+1)) + ".jpx"
                transcode_picture(fname, value)
            elif key[0] == 'H':
                fname = key[0] + '_' + str(key[1]) + '/' \
                + str('%04d' % p) + ".jpx"
                transcode_picture(fname, value)
            elif key[0] == 'R':
                if value > 0:
                    fname = "R_" + str(key[1]) + '/' \
                        + str('%04d' % p) + ".j2c"
                    shell.run("trace cp " + fname + ' '
                              + destination + '/' + fname)
    # }}}

# }}}

# {{{ Transcode GOP0, using the same number of subband layers than the last GOP

transcode_picture("L_" + str(TRLs-1) + "/0000.jpx",
                  slayers_per_subband[("L", TRLs-1)]) # GOP0
# }}}

