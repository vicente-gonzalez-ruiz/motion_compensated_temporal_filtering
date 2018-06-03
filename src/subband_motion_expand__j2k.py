#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# {{{ Imports

from shell import Shell as shell
from arguments_parser import arguments_parser
from colorlog import log

# }}}

# {{{ Defs

COMPONENTS = 4
BYTES_PER_COMPONENT = 2
BITS_PER_COMPONENT = BYTES_PER_COMPONENT * 8
spatial_dwt_levels = 0 # 1 # SRLs - 1

# }}}

# {{{ Arguments parsing

parser = arguments_parser(description="Expands the motion data using JPEG 2000.")

parser.add_argument("--blocks_in_x",
                    help="number of blocks in the X direction.",
                    default=11)
parser.add_argument("--blocks_in_y",
                    help="number of blocks in the Y direction.",
                    default=9)
parser.add_argument("--fields",
                    help="number of fields in to expand.",
                    default=2)
parser.add_argument("--file",
                    help="name of the file with the motion fields.",
                    default="")

args = parser.parse_known_args()[0]

blocks_in_x = int(args.blocks_in_x)
log.info("blocks_in_x={}".format(blocks_in_x))

blocks_in_y = int(args.blocks_in_y)
log.info("blocks_in_x={}".format(blocks_in_x))

bytes_per_field = blocks_in_x * blocks_in_y * BYTES_PER_COMPONENT

fields = int(args.fields)
log.info("fields={}".format(fields))

file = args.file
log.info("file={}".format(file))

# }}}

# Expand each field.
#-------------------
for comp_number in range (0, COMPONENTS) :

    # Decode components.
    #-------------------
    for campoMov_number in range (0, fields) :

        ## Refers to a particular component from a field of movement.
        campoMov_name = file + "_" + str('%04d' % campoMov_number) + "_" + str(comp_number)

        try:
            ## File compressed motion vectors. If there is no vector
            #  file, a file is created with linear movement. That is,
            #  a file of zeros.
            f = open(campoMov_name + ".j2c", "rb")
            f.close()

            try:
                check_call("trace kdu_expand"
                           + " -i " + str(campoMov_name) + ".j2c"
                           + " -o " + str(campoMov_name) + ".rawl"
                           , shell=True)
            except CalledProcessError:
                sys.exit(-1)

        except: 
            # If there is no vector file, a file is created with
            # linear movement. That is, a file of zeros.
            # check_call("echo Motion interpolation..", shell=True)
            # raw_input("")
            
            f = open(campoMov_name + ".rawl", "wb")
            for a in range(BYTES_COMPONENT * blocks_in_y * blocks_in_x) :
                f.write(struct.pack('h', 0))
            f.close()

# Multiplexing.
#--------------
for campoMov_number in range (0, fields) :

    try:
        ## Component 1.
        f0 = open(file + "_" + str('%04d' % campoMov_number) + "_0" + ".rawl", "rb")
        ## Component 2.
        f1 = open(file + "_" + str('%04d' % campoMov_number) + "_1" + ".rawl", "rb")
        ## Component 3.
        f2 = open(file + "_" + str('%04d' % campoMov_number) + "_2" + ".rawl", "rb")
        ## Component 4.
        f3 = open(file + "_" + str('%04d' % campoMov_number) + "_3"  + ".rawl", "rb")
        # Component 1, Component 2, Component 3 y Component 4.
        f  = open(file + "_" + str('%04d' % campoMov_number) + ".join", "wb")

        while 1 : # 792 -> 198 -> 49.5
            ## Multiplexing all components.
            comps = f0.read(BYTES_COMPONENT) + f1.read(BYTES_COMPONENT) + f2.read(BYTES_COMPONENT) + f3.read(BYTES_COMPONENT)
            if len(comps) == (BYTES_COMPONENT * COMPONENTS) :
                f.write(comps)
            else :
                break

        f0.close()
        f1.close()
        f2.close()
        f3.close()
        f.close()

    except CalledProcessError :
        sys.exit(-1)

# cat file_????.join > file
check_call("trace cat " + file + "_????.join > " + file, shell=True)

