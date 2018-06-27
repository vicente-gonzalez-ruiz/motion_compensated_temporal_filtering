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

# {{{ Set attenuations among temporal subbands

if TRLs == 1:
    pass
elif TRLs == 2:
    attenuation = [1.0, 1.2460784922]  # [L1/H1]
elif TRLs == 3:
    attenuation = [1.0, 1.2500103877, 1.8652117304]  # [L2/H2, L2/H1]
elif TRLs == 4:
    attenuation = [1.0, 1.1598810146, 2.1224082769, 3.1669663339]
elif TRLs == 5:
    attenuation = [1.0, 1.0877939347, 2.1250255455, 3.8884779989, 5.8022196044]
elif TRLs == 6:
    attenuation = [1.0, 1.0456562538, 2.0788785438, 4.0611276369, 7.4312544148,
            11.0885981772]
elif TRLs == 7:
    attenuation = [1.0, 1.0232370223, 2.0434169985, 4.0625355976, 7.9362383342,
            14.5221257323, 21.6692913386]
elif TRLs == 8:
    attenuation = [1.0, 1.0117165706, 2.0226778348, 4.0393126714, 8.0305936232,
            15.6879129862, 28.7065276104, 42.8346456693]
else:
    sys.stderr.write("Attenuations are not available for " + str(TRLs) +
                     " TRLs. Enter them in transcode_quality.py")
    sys.exit(0)

# }}}

# {{{ Compute GOPs and pictures

gop = GOP()
GOP_size = gop.get_size(TRLs)
log.info("GOP_size={}".format(GOP_size))

pictures = (GOPs - 1) * GOP_size + 1
log.info("pictures={}".format(pictures))

# }}}

# {{{ Create directories

shell.run("mkdir " + destination + "/L_" + str(TRLs - 1))
for subband in range(TRLs-1, 0, -1):
    shell.run("mkdir " + destination + "/R_" + str(subband))
    shell.run("mkdir " + destination + "/H_" + str(subband))

# }}}

#import ipdb; ipdb.set_trace()

# {{{ Transcode each GOP, except GOP0

subband_layers = []

for gop in range(0, GOPs-1):
    log.info("GOP={}/{}".format(gop, GOPs))
    subband_layers = []

    # {{{ Compute slopes of each subband-layer of L<TRLs-1>

    fname = "L_{}/{:04d}.txt".format(TRLs-1, gop+1)  # GOP_0 is not considered

    # Copy slopes to destination
    shell.run("cp " + fname + ' ' + destination + '/' + fname)

    # Read slopes
    with io.open(fname, 'r') as file:
        slopes = file.read().replace(' ', '').replace('\n', '').split(',')
    log.info("{}: {}".format(fname, slopes))

    # Add slopes to the info file of the subband
    with io.open("L_{}.txt".format(TRLs-1), 'a') as file:
        for i in range(len(slopes)-1):
            file.write("{} ".format(slopes[i]))
            subband_layers.append(['L', TRLs-1, layers-i-1,
                                   int(slopes[i]) - slope])
        file.write("{}\n".format(slopes[len(slopes)-1]))
        #print("--------->", slopes[len(slopes)-1])
        subband_layers.append(['L', TRLs-1, 0,
                               int(slopes[len(slopes)-1]) - slope])
    log.info("L_{}: {}".format(TRLs-1, slopes))

    # }}}

    # {{{ Compute slopes of each subband-layer of each H subband

    for subband in range(TRLs - 1, 0, -1):    
        pics_per_GOP = 1 << (TRLs - subband - 1)
        first_pic = pics_per_GOP * gop
        average = [0]*layers
        
        for pic in range(first_pic, first_pic + pics_per_GOP):
            fname = "H_{}/{:04d}.txt".format(subband, pic)
            
            # Copy slopes to destination
            shell.run("cp " + fname + ' ' + destination + '/' + fname)

            # Get slopes
            with io.open(fname, 'r') as file:
                slopes = file.read().replace(' ', '').replace('\n', '').split(',')
            log.info("{}: {}".format(fname, slopes))
            
            for i in range(layers):
                average[i] += int(slopes[i])
                
        for l in range(layers):
            average[l] //= pics_per_GOP
            
        with io.open("H_{}.txt".format(subband), 'a') as file:
            for i in range(len(slopes)-1):
                #file.write("{} ".format(slopes[i]))
                file.write("{} ".format(average[i]))
                #subband_layers.append(('H', subband, layers-i-1, slopes[i]))
                subband_layers.append(['H', subband, layers-i-1,
                                       int((average[i] - slope)
                                           / attenuation[TRLs - subband])])
            #file.write("{}\n".format(slopes[len(slopes)-1]))
            file.write("{}\n".format(average[len(slopes)-1]))
            #subband_layers.append(('H', subband, 0, slopes[len(slopes)-1]))
            subband_layers.append(['H', subband, 0,
                                   int((average[len(slopes)-1] - slope)
                                       / attenuation[TRLs - subband])])
        log.info("H_{}: {}".format(subband, average))

    log.debug("(original) subband layers={}".format(subband_layers))
    
    # }}}

    # {{{ Sort the subband-layers by their relative slope

    subband_layers.sort(key=operator.itemgetter(3), reverse=True)
    log.debug("(after sorting) subband_layers={}".format(subband_layers))

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

sys.exit()
    
# -<<< Transcode

LOW = "L"
HIGH = "H"

pictures = (GOPs - 1) * GOP_size + 1
log.info("pictures={}".format(pictures))

# Transcoding of H subbands
subband = 1
while subband < TRLs:

    pictures = (pictures + 1) // 2
    if slayers_per_subband[('H', subband)] > 0:
        log.info("Transcoding subband H[{}] with {} pictures".format(subband, pictures - 1))

        shell.run("mctf transcode_quality_subband"
                  + " --subband " + HIGH + "_" + str(subband)
                  + " --layers " + str(slayers_per_subband[('H', subband)])
                  + " --pictures " + str(pictures - 1))

        shell.run("trace cp motion_residue_"
                  + str(subband)
                  + "/*.j2c transcode_quality/"
                  + "motion_residue_"
                  + str(subband))

    subband += 1

# Transcoding of L subband
log.info("Transcoding subband L[{}] with {} pictures".format(subband, TRLs - 1))
shell.run("mctf transcode_quality_subband"
          + " --subband " + LOW + "_" + str(TRLs - 1)
          + " --layers " + str(slayers_per_subband[('L', TRLs - 1)])
          + " --pictures " + str(GOPs))

# ->>>


# -<<< Get slopes from .txt files
fname = "L_{}/{:04d}.txt".format(TRLs-1, picture)
with io.open(fname, 'r') as file:
    slopes = file.read().replace(' ','').replace('\n','').split(',')
log.info("{}: {}".format(fname, slopes))
with io.open("L_{}.txt".format(TRLs-1), 'a') as file:
    for i in range(len(slopes)-1):
        file.write("{} ".format(slopes[i]))
    file.write("{}\n".format(slopes[len(slopes)-1]))
log.info("L_{}: {}".format(subband, slopes))

# ->>>

# -<<< Define subband layers

with io.open("L_{}.txt".format(TRLs-1), 'r') as file:
    slopes = file.read().split()
range_of_slopes = int(slopes[0]) - int(slopes[layers-1])
for index, slope in enumerate(slopes):
    subband_layers.append(('L', TRLs-1, layers-index-1, int(slope)-slope))

# ->>>

# -<<< Sort and truncate the list of subband-layers

subband_layers.sort(key=operator.itemgetter(3), reverse=True)
log.info("(after sorting) subband_layers={}".format(subband_layers))

# ->>>

# -<<< Truncate the list

del subband_layers[keep_layers:]
log.info("(after truncating) subband_layers={}".format(subband_layers))

# ->>>



# ->>>

# ->>>



# -<<< Compute slope averages, for each GOP

# H subbands
subband = 1
average = [0]*layers
while subband < TRLs:
    pictures = (pictures + 1) // 2

    for picture in range(pictures-1):
        fname = "H_{}/{:04d}.txt".format(subband, picture)
        with io.open(fname, 'r') as file:
            slopes = file.read().replace(' ','').replace('\n','').split(',')
            log.info("{}: {}".format(fname, slopes))
        for i in range(layers):
            average[i] += int(slopes[i])

        pictures_per_GOP_in_subband = 1 << (TRLs - subband - 1)
        if ((picture+1) % pictures_per_GOP_in_subband) == 0:
            for l in range(layers):
                average[l] //= pictures_per_GOP_in_subband

            log.info("H_{}: {}".format(subband, average))

            with io.open("H_{}.txt".format(subband), 'a') as file:
                for i in range(len(average)-1):
                    file.write("{} ".format(average[i]))
                file.write("{}\n".format(average[len(average)-1]))
            for i in range(layers):
                average[i] = 0

    subband += 1

# L subband
for picture in range(GOPs):
    fname = "L_{}/{:04d}.txt".format(TRLs-1, picture)
    with io.open(fname, 'r') as file:
        slopes = file.read().replace(' ','').replace('\n','').split(',')
    log.info("{}: {}".format(fname, slopes))
    with io.open("L_{}.txt".format(TRLs-1), 'a') as file:
        for i in range(len(slopes)-1):
            file.write("{} ".format(slopes[i]))
        file.write("{}\n".format(slopes[len(slopes)-1]))
    log.info("L_{}: {}".format(subband, slopes))

# ->>>

#import pdb; pdb.set_trace()

# -<<< Define subband_layers: a list of tuples ('L'|'H', subband, layer, slope)

subband_layers = []
    
# L
with io.open("L_{}.txt".format(TRLs-1), 'r') as file:
    slopes = file.read().split()
range_of_slopes = int(slopes[0]) - int(slopes[layers-1])
for index, slope in enumerate(slopes):
    subband_layers.append(('L', TRLs-1, layers-index-1, int(slope)-slope))

# H's
for subband in range(1,TRLs):
    with io.open("H_{}.txt".format(subband)) as file:
        slopes = file.read().split()
    for index, slope in enumerate(slopes):
        #subband_layers.append(('H', TRLs-subband, layers-index-1, int(float(slope)//gain[subband])))
        #subband_layers.append(('H', TRLs-subband, layers-index-1, int(slope)))
        #subband_layers.append(('H', TRLs-subband, layers-index-1, int(float(slope)-range_of_slopes*gain[subband])))
        subband_layers.append(('H', TRLs-subband, layers-index-1, (int(slope)-slope)//gain[subband]))

log.info("subband_layers={}".format(subband_layers))
        
# ->>>

# -<<< Sort and truncate the list of subband-layers

# Sort the subband-layers by their relative slope
subband_layers.sort(key=operator.itemgetter(3), reverse=True)
log.info("(after sorting) subband_layers={}".format(subband_layers))

# Truncate the list
del subband_layers[keep_layers:]
log.info("(after truncating) subband_layers={}".format(subband_layers))

# ->>>

# -<<< Count the number of subband-layers per subband

slayers_per_subband = {}
slayers_per_subband[('L', TRLs-1)] = 0
for i in range(TRLs-1,0,-1):
    slayers_per_subband[('H', i)] = 0

for i in subband_layers:
    slayers_per_subband[(i[0], i[1])] += 1

with io.open("layers.txt", 'w') as file:
    log.info("{}:{}".format(('L', TRLs-1), slayers_per_subband[('L', TRLs-1)]))
    file.write("{}:{} ".format(('L', TRLs-1), slayers_per_subband[('L', TRLs-1)]))
    for i in range(TRLs-1,0,-1):
        log.info("{}:{}".format(('H', i), slayers_per_subband[('H', i)]))
        file.write("{}:{} ".format(('H', i), slayers_per_subband[('H', i)]))
    file.write("\n")

# ->>>

# -<<< Transcoding

LOW = "L"
HIGH = "H"

pictures = (GOPs - 1) * GOP_size + 1
log.info("pictures={}".format(pictures))

# Transcoding of H subbands
subband = 1
while subband < TRLs:

    pictures = (pictures + 1) // 2
    if slayers_per_subband[('H', subband)] > 0:
        log.info("Transcoding subband H[{}] with {} pictures".format(subband, pictures - 1))

        shell.run("mctf transcode_quality_subband"
                  + " --subband " + HIGH + "_" + str(subband)
                  + " --layers " + str(slayers_per_subband[('H', subband)])
                  + " --pictures " + str(pictures - 1))

        shell.run("trace cp motion_residue_"
                  + str(subband)
                  + "/*.j2c transcode_quality/"
                  + "motion_residue_"
                  + str(subband))

    subband += 1

# Transcoding of L subband
log.info("Transcoding subband L[{}] with {} pictures".format(subband, TRLs - 1))
shell.run("mctf transcode_quality_subband"
          + " --subband " + LOW + "_" + str(TRLs - 1)
          + " --layers " + str(slayers_per_subband[('L', TRLs - 1)])
          + " --pictures " + str(GOPs))

# ->>>
