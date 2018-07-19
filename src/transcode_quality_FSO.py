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

parser.pixels_in_x()
parser.pixels_in_y()

args = parser.parse_known_args()[0]

GOPs = int(args.GOPs)
keep_layers = int(args.keep_layers)
TRLs = int(args.TRLs)
layers = int(args.layers)
destination = args.destination
slope = int(args.slope)
FPS = int(args.FPS)
x_dim = int(args.pixels_in_x)
y_dim = int(args.pixels_in_y)

log.info("GOPs={}".format(GOPs))
log.info("keep_layers={}".format(keep_layers))
log.info("TRLs={}".format(TRLs))
log.info("layers={}".format(layers))
log.info("destination={}".format(destination))
log.info("slope={}".format(slope))
log.info("FPS={}".format(FPS))
log.info("pixels_in_x={}".format(x_dim))
log.info("pixels_in_y={}".format(y_dim))

# }}}


# --------------------------------------------------------------------
def transcode_picture(filename_in, filename_out, layers):
    # {{{ 
    log.debug("transcode_picture: {} to {} with {} layers".format(filename_in, filename_out, layers))
    if layers > 0 :
        shell.run("trace kdu_transcode"
                  + " -i " + filename_in
                  + " -jpx_layers sYCC,0,1,2"
                  + " -o " + "transcode_quality/" + filename_out
                  + " Clayers=" + str(layers))
    # }}}


# --------------------------------------------------------------------
def transcode_images(layersub):
    
    os.chdir(pwd)
    # {{{ Clean the previus transcode and create directories
    shell.run("rm -rf " + destination + "; mkdir " + destination)
    shell.run("mkdir " + destination + "/L_" + str(TRLs - 1))
    for subband in range(TRLs-1, 0, -1):
        shell.run("mkdir " + destination + "/R_" + str(subband))
        shell.run("mkdir " + destination + "/H_" + str(subband))

    # }}}

    # {{{
    log.debug("transcode_images={}".format(layersub))

    for key, value in layersub.items():
        pics_per_subband = (1 << (TRLs-key[1]-1))
        for p in range(pics_per_subband * gop, pics_per_subband * gop + pics_per_subband):
            if key[0] == 'L':
                fname_in  = "L_" + str(key[1]) + '/' + str('%04d' % (p+1)) + ".jpx"
                fname_out = "L_" + str(key[1]) + '/' + str('%04d' % (p-(pics_per_subband * gop)+1)) + ".jpx"
                transcode_picture(fname_in, fname_out, value)
            elif key[0] == 'H':
                fname_in  = "H_" + str(key[1]) + '/' + str('%04d' % p) + ".jpx"
                fname_out = "H_" + str(key[1]) + '/' + str('%04d' % (p-(pics_per_subband * gop))) + ".jpx"
                transcode_picture(fname_in, fname_out, value)

            elif key[0] == 'R':
                if value > 0:
                    fname_in  = "R_" + str(key[1]) + '/' + str('%04d' % p) + ".j2c"
                    fname_out = "R_" + str(key[1]) + '/' + str('%04d' % (p-(pics_per_subband * gop))) + ".j2c"
                    shell.run("trace cp " + fname_in + ' ' + destination + '/' + fname_out)

    # {{{ Transcode GOP0, using the same number of subband layers than the last GOP
    fname_in  = "L_" + str(TRLs-1) + '/' + str('%04d' % (pics_per_subband * gop)) + ".jpx"
    fname_out = "L_" + str(TRLs-1) + '/' + "0000.jpx"
    value     = layersub[("L", TRLs-1)]
    transcode_picture(fname_in, fname_out, value)
    # }}}
    # }}}

# --------------------------------------------------------------------
def codestream_point() :

    os.chdir(pwd + "/transcode_quality")
    
    # Create zero texture
    shell.run("mctf create_zero_texture --pixels_in_y=" + str(y_dim) + " --pixels_in_x=" + str(x_dim))

    # KBPS
    p = sub.Popen("mctf info --GOPs=" + str(2) + " --TRLs=" + str(TRLs) + " --FPS=" + str(FPS) + " 2> /dev/null | grep \"Average\" | cut -d \" \" -f 5", shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
    out, err = p.communicate()
    kbps = float(out)

    # Expand
    shell.run("mctf expand --GOPs=" + str(2) + " --TRLs=" + str(TRLs))
    # Video to Images
    shell.run("../../../raw_pgm.sh")

    # PSNR
    p = sub.Popen("mctf psnr --file_A L_0 --file_B ../L_0 --pixels_in_x=" + str(x_dim) + " --pixels_in_y=" + str(y_dim) + " --GOPs=" + str(2) + " --TRLs=" + str(TRLs), shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
    out, err = p.communicate()
    psnr = float(out)
    
    return kbps, psnr

# --------------------------------------------------------------------
def add_layer() :

    if (key[0] == 'R' and try_layersub[key] < 1) or ((key[0] == 'L' or key[0] == 'H') and try_layersub[key] < layers) :
        try_layersub[key] += 1
    else :
        return -1

# --------------------------------------------------------------------
def trace_selection(mode) :
    if mode == -1 :
        shell.run("echo \"--- EMPTY LAYER ---\" >> " + str(pwd) + "/FSO_selection")
    elif mode == 0 :
        shell.run("echo \"\nGOP " + str(gop+1) + " de " + str(GOPs) + " GOPs\n\" >> " + str(pwd) + "/FSO_selection")
        shell.run("echo \"Angle = math.atan((psnr - old_psnr)/(kbps - old_kbps))\n\" >> " + str(pwd) + "/FSO_selection")
    elif mode == 1 :
        shell.run("echo \"" + str(key) + ": " + str(try_layersub[key]) + "\t\t" + str("%.8f"%angle) + "\t= " + "(" + str("%.8f"%psnr) + " - " + str("%.8f"%old_psnr) + ") / (" + str("%.4f"%kbps) + " - " + str("%.4f"%old_kbps) + ")\" >> " + str(pwd) + "/FSO_selection")
    elif mode == 2 :
        shell.run("echo \"ADDED: " + str(point["subband"]) + ": " + str(point["layer"]) + "  THEN: " + str(best_layersub) + "\n\" >> " + str(pwd) + "/FSO_selection")

# --------------------------------------------------------------------
def toFile() :
    # {{{ Save to file
    shell.run("echo \"# KBPS #PSNR\" >> " + str(pwd) + "/FSO_points_gop" + str(gop+1))
    for z in range(0, len(FSO[gop])) :
        shell.run("echo \"" + str(FSO[gop][z]) + "\" >> " + str(pwd) + "/FSO_trace_gop" + str(gop+1))
        if z % 2 == 0 :
            shell.run("echo \"" + str("%.3f"%float(FSO[gop][z]["kbps"])) + "\t" + str("%.3f"%float(FSO[gop][z]["psnr"])) + "\" >> " + str(pwd) + "/FSO_points_gop" + str(gop+1))
        else :
            shell.run("echo \"" + str(FSO[gop][z]) + "\" >> " + str(pwd) + "/FSO_short_gop" + str(gop+1))
            shell.run("echo \"\" >> " + str(pwd) + "/FSO_trace_gop" + str(gop+1))
    # }}}
# --------------------------------------------------------------------
def updatePoint() :

    point["kbps"]    = kbps
    point["psnr"]    = psnr
    point["subband"] = key
    point["layer"]   = best_layersub[key]
    point["angle"]   = angle
    return point

# --------------------------------------------------------------------
def init_layersub(mode) :

    layersub = {}

    if mode == "empty"
        layersub[('L', TRLs-1)] = 0
        for i in range(TRLs-1,0,-1) :
            layersub[('H', i)] = 0
            layersub[('R', i)] = 0

    elif mode == "full"
        layersub[('L', TRLs-1)] = layers
        for i in range(TRLs-1,0,-1) :
            layersub[('H', i)] = layers
            layersub[('R', i)] = 1

    return layersub

# --------------------------------------------------------------------
def gop_video(gop) :
    # {{{ Take original frames from a gop to compute distortion gop by gop.
    namefile = str(path_base) + "/low_" + str(TRLs-1)
    p = sub.Popen("dd"
                  + " if="    + namefile
                  + " of="    + namefile + "_temp"
                  + " skip="  + str(1)
                  + " bs="    + str(int(pixels_in_x * pixels_in_y * 1.5)) # Image size.
                  , shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
    out, err = p.communicate()

    p = sub.Popen("mv " + namefile + "_temp " + namefile, shell=True, stdout=sub.PIPE, stderr=sub.PIPE) # dd no sobreescribe ficheros, por eso es necesario el temporal.
    out, err = p.communicate()
    # }}}


# --------------------------------------------------------------------
# {{{ Compute GOPs and pictures
gop = GOP()
GOP_size = gop.get_size(TRLs)
log.info("GOP_size={}".format(GOP_size))

pictures = (GOPs - 1) * GOP_size + 1
log.info("pictures={}".format(pictures))
# }}}

# --------------------------------------------------------------------
#import ipdb; ipdb.set_trace()

# ----------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------
#               ¡HERE!
# ~/tmp			/tmp				/transcode_quality        
# ~/compresión	/extracción_total	/extracción_parcial
p = sub.Popen("echo $PWD", shell=True, stdout=sub.PIPE, stderr=sub.PIPE)
out, err = p.communicate()
pwd = out.decode('ascii')
pwd = pwd[:len(pwd)-1]

min_angle = -99
min_kbps  = 0.001

# --------------------------------------------------------------------
# {{{ FSO: Pares=point, Impares=layers_per_subband
point   = {}
FSO     = [[]] * (GOPs-1)

#layers = 1 ############################# Jse


for gop in range(0, GOPs-1) :
    log.info("GOP={}/{}".format(gop, GOPs))

    # Reset per gop
    layersub = init_layersub("empty")
    trace_selection(0)
    
    # 0 layers for old values.
    transcode_images(layersub)
    old_kbps, old_psnr = codestream_point()

    full = 0
    while full < (TRLs*2-2) :
        point["angle"] = min_angle
        full = 0
        
        for key, value in layersub.items() :
            try_layersub = layersub.copy()

            # Add one layer to codestream
            if -1 == add_layer() :
                full += 1
                continue

            # Transcode
            transcode_images(try_layersub)
            # Kbps & Psnr
            kbps, psnr = codestream_point()

            if kbps == old_kbps : # easy solution for empty layer
                kbps =+ min_kbps
                trace_selection(-1)

            # Angle = Tan (difference psnr / difference kbps)
            angle = math.atan ( (psnr - old_psnr) / (kbps - old_kbps) )
            trace_selection(1)

            # Save the best codestream during the search
            if point["angle"] < angle :
                best_layersub = try_layersub.copy()
                point         = updatePoint()

        trace_selection(2)
        # New param for next iteration
        layersub = best_layersub.copy()
        old_psnr = point["psnr"]
        old_kbps = point["kbps"]
        FSO[gop].append(point.copy())
        FSO[gop].append(best_layersub.copy())

    print (FSO) # Jse
    # Save the best codestream
    toFile()

sys.exit(0) # Jse












# Images to Video & play
shell.run("(ffmpeg -y -s " + str(x_dim) + "x" + str(y_dim) + " -pix_fmt yuv420p -i L_0/%4d.Y /tmp/out.yuv) > /dev/null 2> /dev/null")
shell.run("(mplayer /tmp/out.yuv -demuxer rawvideo -rawvideo w=" + str(x_dim) + ":h=" + str(y_dim) + " -loop 0 -fps " + str(FPS) + ") > /dev/null 2> /dev/null")

sys.exit(0)

#log.info("try_layersub:{}".format(try_layersub)) #     
wait = input("PRESS ENTER TO CONTINUE.")

log.info("layersub:{}".format(layersub)) #Jse
log.info("try_layersub:{}".format(try_layersub))

log.info("key: " + str(key))
log.info("value: " + str(try_layersub[key]))
#shell.run("mctf create_zero_texture --pixels_in_y=y_dim --pixels_in_x=x_dim")

os.chdir(pwd)
shell.run("echo $PWD")
shell.run("mctf copy --GOPs=2 --TRLs=4 --destination=tmp/transcode_quality")


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

# --------------------------------------------------------------------
''' EJECUCION::::::::::::::::::::::::::::::::::::::::::::::::::
mctf transcode_quality_FSO --GOPs=2 --TRLs=4 --keep_layers=8 --destination=transcode_quality --layers=8 --slope=43000
'''


# -------------------------------------------------------------------- add one layer
'''
if key[0] == 'L' or key[0] == 'H' :
    if try_layersub[key] < layers :
        try_layersub[key] += 1 # Increase one layer for texture subband
    else :
        return -1
else :
    if try_layersub[key] < 1 :
        try_layersub[key] += 1 # Increase one layer for vector
    else :
        return -1

'''


