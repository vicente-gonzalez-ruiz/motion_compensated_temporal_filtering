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

import os
import math
import subprocess as sub
from subprocess   import check_call
from subprocess   import CalledProcessError

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
parser.add_argument("--FPS",
                    help="Number of frames per second",
                    default=30)

args = parser.parse_known_args()[0]
GOPs = int(args.GOPs)
keep_layers = int(args.keep_layers)
TRLs = int(args.TRLs)
layers = int(args.layers)
destination = args.destination
slope = int(args.slope)
FPS = int(args.FPS)

log.info("GOPs={}".format(GOPs))
log.info("keep_layers={}".format(keep_layers))
log.info("TRLs={}".format(TRLs))
log.info("layers={}".format(layers))
log.info("destination={}".format(destination))
log.info("slope={}".format(slope))
log.info("FPS={}".format(FPS))
# }}}

# --------------------------------------------------------------------
def transcode_picture(filename, layers):
    # {{{ 
    log.debug("transcode_picture: {} {}".format(filename, layers))
    if layers > 0 :
        shell.run("trace kdu_transcode"
                  + " -i " + filename
                  + " -jpx_layers sYCC,0,1,2"
                  + " -o " + "transcode_quality/" + filename
                  + " Clayers=" + str(layers))
    # }}}


# --------------------------------------------------------------------
def transcode_images(layersub):
    # {{{ Clean the previus transcode and create directories
    shell.run("rm -rf transcode_quality; mkdir transcode_quality")
    shell.run("mkdir " + destination + "/L_" + str(TRLs - 1))
    for subband in range(TRLs-1, 0, -1):
        shell.run("mkdir " + destination + "/R_" + str(subband))
        shell.run("mkdir " + destination + "/H_" + str(subband))

    # }}}

    # {{{
    log.debug("transcode_images={}".format(layersub))
    for key, value in layersub.items():
        pics_per_subband = (1 << (TRLs-key[1]-1))
        for p in range(pics_per_subband * gop,
                       pics_per_subband * gop + pics_per_subband):
            if key[0] == 'L':
                fname = key[0] + '_' + str(key[1]) + '/' + str('%04d' % (p+1)) + ".jpx"
                transcode_picture(fname, value)
            elif key[0] == 'H':
                fname = key[0] + '_' + str(key[1]) + '/' + str('%04d' % p) + ".jpx"
                transcode_picture(fname, value)
            elif key[0] == 'R':
                if value > 0:
                    fname = "R_" + str(key[1]) + '/' + str('%04d' % p) + ".j2c"
                    shell.run("trace cp " + fname + ' ' + destination + '/' + fname)

    # {{{ Transcode GOP0, using the same number of subband layers than the last GOP
    
    if gop == GOPs-2 :
        wait = input("Gop: " + str(gop) + " de " + str(GOPs)) #############################################################
        transcode_picture("L_" + str(TRLs-1) + "/0000.jpx", layersub[("L", TRLs-1)]) # GOP0
    # }}}
    # }}}
    
# --------------------------------------------------------------------
    
# --------------------------------------------------------------------
# psnr --file_A L_0 --file_B ../L_0 --pixels_in_x=352 --pixels_in_y=288 --GOPs=2 --TRLs=4
''' EJECUCION::::::::::::::::::::::::::::::::::::::::::::::::::
mkdir tanscode_quality
mctf transcode_quality_FSO --GOPs=2 --TRLs=4 --keep_layers=8 --destination=transcode_quality --layers=8 --slope=43000
'''

# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# {{{ Compute GOPs and pictures
gop = GOP()
GOP_size = gop.get_size(TRLs)
log.info("GOP_size={}".format(GOP_size))

pictures = (GOPs - 1) * GOP_size + 1
log.info("pictures={}".format(pictures))
# }}}

# --------------------------------------------------------------------
#wait = input("carpetas. PRESS ENTER TO CONTINUE.") ####################################
#import ipdb; ipdb.set_trace()


# --------------------------------------------------------------------
# ~/tmp			/'tmp'				/transcode_quality        
# ~/compresión	/extracción_total	/extracción_parcial

# {{{ FSO
for gop in range(0, GOPs-1) :
    log.info("GOP={}/{}".format(gop, GOPs))

    # Reset per gop
    layersub = {}
    layersub[('L', TRLs-1)] = 0
    for i in range(TRLs-1,0,-1) :
        layersub[('H', i)] = 0
        layersub[('R', i)] = 0

    # Add one layer
    while layersub[('H',1)] < layers :
        try_layersub = layersub
        biggest_angle = 0
        FSO[0] = 

        for key, value in try_layersub.items() : 
            if try_layersub[key] < layers :
                try_layersub[key] += 1 # Increase one layer in a subband

                '''
                try_layersub[('L', TRLs-1)] = 8
                for i in range(TRLs-1,0,-1) :
                    try_layersub[('H', i)] = 8
                    try_layersub[('R', i)] = 8
                ''' 

                # Get angle                
                transcode_images(try_layersub)

                # kbps
                os.chdir     ("/home/cmaturana/scratch/tmp/tmp/transcode_quality")
                shell.run    ("mctf create_zero_texture --pixels_in_y=" + str(288) + " --pixels_in_x=" + str(352)) # !
                log.debug    ("mctf info --GOPs=" + str(GOPs) + " --TRLs=" + str(TRLs) + " --FPS=" + str(FPS) + " 2> /dev/null | grep \"Average\" | cut -d \" \" -f 5")
                p = sub.Popen("mctf info --GOPs=" + str(GOPs) + " --TRLs=" + str(TRLs) + " --FPS=" + str(FPS) + " 2> /dev/null | grep \"Average\" | cut -d \" \" -f 5", shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
                out, err = p.communicate()
                kbps = float(out)

                # Expand
                shell.run("mctf expand --GOPs=" + str(GOPs) + " --TRLs=" + str(TRLs))
                # Video to Images
                shell.run("../../../raw_pgm.sh")

                # Psnr
                p = sub.Popen("mctf psnr --file_A L_0 --file_B ../L_0 --pixels_in_x=" + str(352) + " --pixels_in_y=" + str(288) + " --GOPs=" + str(GOPs) + " --TRLs=" + str(TRLs), shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
                out, err = p.communicate()
                psnr=float(out)
                log.info("psnr: " + str(psnr))

                # Angle = Tan (difference psnr / difference kbps)
                angle = math.atan ( (psnr - old_psnr) / (kbps - old_kbps) )

                if biggest_angle < angle :
                    biggest_angle = angle
                    best_layersub = try_layersub
                    old_psnr      = psnr
                    old_kbps      = kbps


# Images to Video & play                
shell.run("(ffmpeg -y -s " + str(352) + "x" + str(288) + " -pix_fmt yuv420p -i L_0/%4d.Y /tmp/out.yuv) > /dev/null 2> /dev/null")
shell.run("(mplayer /tmp/out.yuv -demuxer rawvideo -rawvideo w=" + str(352) + ":h=" + str(288) + " -loop 0 -fps " + str(FPS) + ") > /dev/null 2> /dev/null")

sys.exit(0)

#log.info("try_layersub:{}".format(try_layersub)) #     
wait = input("PRESS ENTER TO CONTINUE.")
log.info("key: " + str(key))
log.info("value: " + str(try_layersub[key]))
#shell.run("mctf create_zero_texture --pixels_in_y=288 --pixels_in_x=352")

os.chdir("/home/cmaturana/scratch/tmp")
shell.run("echo $PWD")
shell.run("mctf copy --GOPs=2 --TRLs=4 --destination=tmp/transcode_quality")



#log.info("layersub={}".format(layersub))
#log.info(layersub)
wait = input("fin. PRESS ENTER TO CONTINUE.")
# sys.exit(0)
shell.run("rm -rf *")    
# }}}
# --------------------------------------------------------------------
'''
RADIAN
    if kbps_TM[1] == kbps_antes : # EmptyLayer  # - Improve the quality of the reconstruction without increasing kbps, seems impossible but can occur in this research environment. A codestream is formed by a set of GOPS, besides the GOP0, which is formed by an image of the L subband. # - The GOP0 taken into account in the info.py function for the complete codestream. It may be the case in a sorting algorithm, evaluating quality pillowtop, the codestream: GOP0 grow in, but does not grow in the GOP1, so both have the same codestream kbps, since only look at the GOP1, but have different rmse.
        emptyLayer += 1
        radian      = math.atan ( (rmse1D_antes - rmse1D) / 0.001 ) # A little value.
    else :                        # No EmptyLayer
        emptyLayer  = 0
        radian      = math.atan ( (rmse1D_antes - rmse1D) / (kbps_TM[1] - kbps_antes) )
'''
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------
# --------------------------------------------------------------------
