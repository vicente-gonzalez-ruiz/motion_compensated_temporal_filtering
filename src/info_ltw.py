#!/usr/bin/python
# -*- coding: iso-8859-15 -*-


## @file info_ltw.py
#  The size in bytes, and a codestream Kbps, even detailed subband
#  level and neglecting headers, from a LTW codestream.
#
#  @authors Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.
#
## @package info_ltw
#  The size in bytes, and a codestream Kbps, even detailed subband
#  level and neglecting headers, from a LTW codestream.

from info import info

## Class info for LTW codec.
class info_ltw(info):


    ## Current image number.
    image_number = 0


    ## Find the length of a color LTW image. Find next EOC texture.
    #  @param self Refers to object.
    #  @param file Color LTW image.
    #  @return Length of a color LTW image.
    def find_next_EOC_texture(self, file):
        return int(file.readline())


    ## Find the next End Of fame's Code-stream (FFD9) in a Motion JPEG 2000 code-stream.
    #  @param self Refers to object.
    #  @param file Motion file.
    #  @return Position of next End Of fame's Code-stream.
    def find_next_EOC_motion(self, file):
        byte = file.read(1)
        #print "Buscando ..."
        #print byte
        while byte != '':
            #sys.stdout.write(byte)
            if byte == '\xff':
                #print "\xff"
                byte = file.read(1)
                if byte == '\xd9':
                    return file.tell()
            byte = file.read(1)
        return file.tell()


    ## Open a LTW code-stream.
    #  @param self Refers to object.
    #  @param codestream_filename Codestream filename.
    #  @return File descriptor.
    def open_codestream(self, codestream_filename):
        return open(codestream_filename + ".ltw", 'rb')


## Instance of the class: info_ltw.
x=info_ltw()
