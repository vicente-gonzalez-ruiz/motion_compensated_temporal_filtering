#!/usr/bin/python
# -*- coding: iso-8859-15 -*-


## @file info_j2k.py
#  The size in bytes, and a codestream Kbps, even detailed subband
#  level and neglecting headers, from a J2K codestream.
#
#  @authors Jose Carmelo Maturana-Espinosa\n Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.
#
## @package info_j2k
#  The size in bytes, and a codestream Kbps, even detailed subband
#  level and neglecting headers, from a J2K codestream.

from info import info
from MCTF_parser import MCTF_parser


## Class info for J2K codec.
class info_j2k(info):


    ## Find the length of JPEG 2000 image.
    #  @param self Refers to object.
    #  @param file JPEG 2000 image.
    #  @return Length of JPEG 2000 image
    def find_next_EOC_texture(self, file):
        if file == None:
            return 0
        else:
            return int(file.readline())


    ## Find the length of motion.
    #  @param self Refers to object.
    #  @param file Motion file.
    #  @return Length of motion.
    def find_next_EOC_motion(self, file):
        if file == None:
            return 0
        else:
            return int(file.readline())


    ## Open a sizes files.
    #  @param self Refers to object.
    #  @param codestream_filename Codestream filename.
    #  @return Size file.
    def open_codestream(self, codestream_filename):
        try:
            return open(codestream_filename, 'rb')
        except IOError:
            return None


    ## Bytes per frame in MCTF context.
    #  @param self Refers to object.
    #  @param bytes_frame_TM Size frames without MCTF order.
    #  @return Size frame.
    #def sizeFrame_MCTF(self, bytes_frame_TM):





## Main function.
def main():

    parser = MCTF_parser(description="Info.")
    parser.add_argument("--GOPs",          help="number of GOPs to process. (Default = {})".format(info.GOPs))
    parser.add_argument("--TRLs",          help="number of iterations of the temporal transform + 1. (Default = {})".format(info.TRLs))
    parser.add_argument("--FPS",           help="frames per second. (Default = {})".format(info.FPS))

    args = parser.parse_known_args()[0]
    if args.GOPs:
        info.GOPs = int(args.GOPs)
    if args.TRLs:
        info.TRLs = int(args.TRLs)
    if args.FPS:
        info.FPS  = float(args.FPS)


    x=info_j2k(info.GOPs, info.TRLs, info.FPS) #x=info_j2k() # ?


if __name__ == '__main__':
    main()
