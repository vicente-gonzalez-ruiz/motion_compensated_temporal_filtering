#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

## @file info_mj2k.py
#  The size in bytes, and a codestream Kbps, even detailed subband
#  level and neglecting headers, from a MJ2K codestream.
#
#  @authors Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.
#
## @package info_mj2k
#  The size in bytes, and a codestream Kbps, even detailed subband
#  level and neglecting headers, from a MJ2K codestream.

from info import info

## Class info for MJ2K codec.
class info_mj2k(info):


    ## Find the next End Of fame's Code-stream (FFD9) in a Motion JPEG 2000 code-stream.
    #  @param self Refers to object.
    #  @param file Motion JPEG 2000 image.
    #  @return Length of Motion JPEG 2000 image.
    def find_next_EOC_texture(self, file):
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


    ## Find the next End Of fame's Code-stream (FFD9) in a Motion JPEG 2000 code-stream.
    #  @param self Refers to object.
    #  @param file Motion file.
    #  @return Length of motion.
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


    ## Open a Motion JPEG 2000 code-stream.
    #  @param self Refers to object.
    #  @param codestream_filename Codestream filename.
    #  @return File descriptor.
    def open_codestream(self, codestream_filename):
        return open(codestream_filename + ".mjc", 'rb')


## Instance of the class: info_mj2k.
x=info_mj2k()
