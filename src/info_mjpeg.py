#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-


## @file info_mjpeg.py
#  The size in bytes, and a codestream Kbps, even detailed subband
#  level and neglecting headers, from a MJPEG codestream.
#
#  @authors Vicente Gonzalez-Ruiz.
#  @date Last modification: 2015, January 7.
#
## @package info_mjpeg
#  The size in bytes, and a codestream Kbps, even detailed subband
#  level and neglecting headers, from a MJPEG codestream.


from info import info

## Class info for MJPEG codec.
class info_mjpeg(info):

    ## Find the next End Of fame's Code-stream (FFD9) in a Motion JPEG code-stream.
    #  @param self Refers to object.
    #  @param file Motion JPEG image.
    #  @return Length of Motion JPEG image.
    def find_next_EOC_texture(self, file):
        byte = file.read(1)
        #print byte
        while byte != '':
            #sys.stdout.write(byte)
            if byte == '\xff':
                #print "\xff"
                byte = file.read(1)
                if byte == '\xd8':
                    return file.tell()
            byte = file.read(1)
        return file.tell()


    ## Find the next End Of fame's Code-stream (FFD9) in a Motion JPEG code-stream.
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


    ## Open a Motion JPEG code-stream.
    #  @param self Refers to object.
    #  @param codestream_filename Codestream filename.
    #  @return File descriptor.
    def open_codestream(self, codestream_filename):
        return open(codestream_filename + ".mjpeg", 'rb')


## Instance of the class: info_mjpeg.
x=info_jpg()
