#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

# MCTF structure:
# 0 1 2 3 4 5 6 7 8
# 0               8 L_3
#         4         H_3
#     2       6     H_2
#   1   3   5   7   H_1

import os
import sys
import getopt
import display
import math
import subprocess as     sub
from   subprocess import check_call
from   GOP        import GOP

class info(GOP):

    # Number of GOPs (Group of Pictures) in the sequence.
    GOPs = 2
    
    # Number of Temporal Resolution Level.
    TRLs = 2

    #  Frames per Second.
    FPS  = 30

    def __init__(self, GOPs, TRLs, FPS) :

        self.GOPs = GOPs
        self.TRLs = TRLs
        self.FPS  = FPS
        GOP_size            = GOP.get_size(self, self.TRLs) # number_of_GOPs = int(math.ceil((self.pictures * 1.0)/ GOP_size))
        pictures            = GOP_size * self.GOPs + 1
        # Weighting value, to be applied between the GOP0, and the rest.
        average_ponderation = (pictures - 1.0) / pictures
        GOP0_time           = 1.0              / self.FPS
        GOP_time            = float(GOP_size)  / self.FPS

        #sys.stdout.write("\n\n"              + sys.argv[0]    + "\n")
        sys.stdout.write("TRLs           = " + str(self.TRLs) + "\n")
        sys.stdout.write("Pictures       = " + str(pictures)  + "\n")
        sys.stdout.write("FPS            = " + str(self.FPS)  + "\n")
        sys.stdout.write("GOP size       = " + str(GOP_size)  + "\n")
        sys.stdout.write("Number of GOPs = " + str(self.GOPs) + "\n")
        sys.stdout.write("Frame time     = " + str(GOP0_time) + "\n")
        sys.stdout.write("GOP   time     = " + str(GOP_time)  + "\n")
        sys.stdout.write("All the values are given in thousands (1000) of bits per second (Kbps).\n\n")

        # Table header.

        # First line. (TRL4 TRL3 TRL2 TRL1 TRL0).
        sys.stdout.write("\n     ");
        sys.stdout.write("    TRL" + str(self.TRLs-1))

        for i in range(self.TRLs-1, 0, -1):
            sys.stdout.write("           ")
            for j in range(0, 2**(self.TRLs-1-i)):
                sys.stdout.write(" ")
            sys.stdout.write("TRL" + str(i-1))
        sys.stdout.write("\n")

        # Second line. (GOP low_4 motion_4+high_4 motion_3+hight_3 motion_2+high2 motion_1+high_1 Total).
        sys.stdout.write("GOP#")
        sys.stdout.write("    low_" +  str(self.TRLs-1))

        for i in range(self.TRLs-1, 0, -1):
            for j in range(0, 2**(self.TRLs-1-i)):
                sys.stdout.write(" ")
            sys.stdout.write("motion_" + str(i) + " high_" + str(i))
        sys.stdout.write("    Total\n")

        # Third line. (--------------------------------------)
        sys.stdout.write("---- ")
        sys.stdout.write("-------- ")
        for i in range(self.TRLs-1, 0, -1):
            for j in range(0, 2**(self.TRLs-1-i)):
                sys.stdout.write("-")
            sys.stdout.write("-------------- ")
        sys.stdout.write("--------\n")

        # Displays the bit-rate of each subband of each
        # GOP. Therefore, an array of integers, to store for each
        # subband, the bit-rate required of the previous GOP. The
        # bit-rate of the current GOP for each subband, is calculated
        # by subtracting the value for the previous GOP, less the
        # present value. Recall that the files with the code-streams,
        # are traversed sequentially, and there is a file for each
        # subband). Means for each subband are also reported?
        M_prev_GOP   = [0] * self.TRLs
        H_prev_GOP   = [0] * self.TRLs
        M_prev_image = [0] * self.TRLs
        H_prev_image = [0] * self.TRLs

        # List type frame.
        self.types_frame     = [None] + [[] for x in xrange (self.TRLs-1)]   # [None, F, F, ..., F]

        # Calculation of bytes (textures and motion) per frame.
        self.bytes_frames_M  = [None] + [[] for x in xrange (self.TRLs-1)]   # [None, M, M, ..., M]
        self.bytes_frames_T  = [[] for x in xrange (self.TRLs)]              # [L,    H, H, ..., H]
        self.bytes_frames_TM = [[] for x in xrange (self.TRLs)]              # [L,    H, H, ..., H]

        # Calculation of bit-rates.

        # List kbps of high frequency subbands.
        self.kbps_H          = [[] for x in xrange (self.GOPs+1)]
        # List kbps of motion vectors.
        self.kbps_M          = [[] for x in xrange (self.GOPs)]
        # List kbps of high frequency subbands and motion vectors.
        self.kbps_HM_total   = []
        #self.info_RMSE      = []

        # Average kbps of motion.
        self.average_M     = [0] * (self.TRLs + 1)
        # Average kbps of high frecuency subbands.
        self.average_H     = [0] * (self.TRLs + 1)
        # Average kbps of low frecuency subbands.
        self.average_L     = 0
        # Average kbps of codestream.
        self.average_total = 0

        L_file  = self.open_codestream("low_" + str(self.TRLs - 1) + ".j2c") # L
        H_file  = [None]                                                     # H
        M_file  = [None]                                                     # M
        F_file  = [None]                                                     # Frame types

        for subband in range(1, self.TRLs) :
            H_file.append(self.open_codestream("high_"           + str(subband) + ".j2c"))
            M_file.append(self.open_codestream("motion_residue_" + str(subband) + ".mjc"))
            F_file.append(self.open_codestream("frame_types_"    + str(subband)         ))

        # GOP 0. The GOP0 is formed by the first image in low_<TRLs-1>.
        L_prev_GOP = self.find_next_EOC_texture(L_file)
        self.bytes_frames_T[0].append(L_prev_GOP) # Bytes per frame

        L_kbps_GOP0 = float(L_prev_GOP) * 8.0 / GOP0_time / 1000.0
        self.kbps_H    [0].append(L_kbps_GOP0)
        self.kbps_HM_total.append(L_kbps_GOP0)

        sys.stdout.write("0000 %8d " % L_kbps_GOP0)

        for subband in range(self.TRLs-1, 0, -1):
            for j in range(0, 2**(self.TRLs-1-subband)) :
                sys.stdout.write("-")
            sys.stdout.write("%7d " % 0)
            sys.stdout.write("%6d " % 0)

        sys.stdout.write("%8d\n" % L_kbps_GOP0)


        # GOP n. GOPs are formed by a number of subbands.
        #------------------------------------------------
        for GOP_number in range(1, self.GOPs+1) :
            total = 0 # Total Kbps
            sys.stdout.write("%3s " % '%04d' % GOP_number)


            # SUBBANDA L. Each new image represents a new GOP.
            #-------------------------------------------------
            L_next_GOP = self.find_next_EOC_texture(L_file)
            L_bytes    = L_next_GOP - L_prev_GOP
            self.bytes_frames_T[0].append(L_bytes) # Bytes per frame

            L_prev_GOP                   = L_next_GOP
            L_kbps                       = float(L_bytes) * 8.0 / GOP_time / 1000.0
            self.kbps_H[GOP_number].append(L_kbps)
            self.average_L              += L_kbps
            total                       += L_kbps

            sys.stdout.write("%8d " % int(L_kbps))


            # SUBBANDAS H. Depending on the level of temporal resolution, each GOP generates a number of different images.
            #-------------------------------------------------------------------------------------------------------------
            pics_in_GOP = 1
            for subband in range(self.TRLs-1, 0, -1) :

                # Frame_types.
                #-------------
                for i in range(0, pics_in_GOP) :
                    frame_type = F_file[subband].read(1)
                    self.types_frame[self.TRLs - subband].append(frame_type)
                    sys.stdout.write("%s" % frame_type)


                # Motion.
                #--------
                for i in range(0, pics_in_GOP) :
                    next_image = self.find_next_EOC_motion(M_file[subband])
                    self.bytes_frames_M[self.TRLs - subband].append(next_image - M_prev_image[subband]) # Bytes per frame
                    M_prev_image[subband] = next_image

                M_kbps = float(next_image - M_prev_GOP[subband]) * 8.0 / GOP_time / 1000.0

                self.kbps_M[GOP_number-1].append(M_kbps)
                self.average_M[subband]       += M_kbps
                total                         += M_kbps
                sys.stdout.write("%7d " %    int(M_kbps))

		M_prev_image[subband] = M_prev_GOP[subband] = next_image

                # High frecuency.
                #----------------
                for i in range(0, pics_in_GOP) :
                    next_image = self.find_next_EOC_texture(H_file[subband])
                    self.bytes_frames_T[self.TRLs - subband].append(next_image - H_prev_image[subband]) # Bytes per frame
                    H_prev_image[subband] = next_image

                H_kbps = float(next_image - H_prev_GOP[subband]) * 8.0 / GOP_time / 1000.0

                self.kbps_H[GOP_number].append(H_kbps)
                self.average_H[subband]     += H_kbps
                total                       += H_kbps
                sys.stdout.write("%6d " %  int(H_kbps))

                H_prev_image[subband] = H_prev_GOP[subband] = next_image

                pics_in_GOP *= 2

            sys.stdout.write("%8d\n" % total)
            self.average_total      += total
            self.kbps_HM_total.append (total) # < Jse

        quit()
            
        # Bytes per frame TM = M + T (Per subband)
        #-----------------------------------------
        self.bytes_frames_TM[0] = self.bytes_frames_T[0][:]
        for sub in range(1, self.TRLs) :
            for pic in range(0, len(self.bytes_frames_M[sub])) :
                self.bytes_frames_TM[sub].append(self.bytes_frames_M[sub][pic] + self.bytes_frames_T[sub][pic])

        # Bytes per frame TM (Per subband) to (Frame per frame)
        #------------------------------------------------------
        self.bytes_frames_TM_perframe = []

        # Add bytes to L frames.
        for Vpic in range(0, pictures) :

            if Vpic % GOP_size == 0 : # Is a L image. Then add image 0, from L, from GOPx
                self.bytes_frames_TM_perframe.append( self.bytes_frames_TM[0][Vpic/GOP_size] )
            else :
                # Add bytes Hs & Ms, to Hs frames.
                pic = Vpic
                for sub in range(1, self.TRLs) :
                    pic /= 2.0
                    if pic - int(pic) > 0.0 :
                        self.bytes_frames_TM_perframe.append( self.bytes_frames_TM[self.TRLs-sub][int(pic)] )
                        break

        # bytes_frames_MCTF. (Frame per frame)
        #---------------------------------------
        bytes_frames_MCTF = []

        # Add bytes of subband L to all frames.
        for pic in range(0, pictures) :
            if pic % GOP_size == 0 : # Is a L image. Then add image 0, from L, from GOPx
                bytes_frames_MCTF.append( self.bytes_frames_TM[0][pic/GOP_size] )

            else : # Is not a L image. Then add image 0 & 1, from L, from GOPx

                ## pic is the image number 'image_number' from subband 'sub'.
                image_number = pic / 2.0
                sub          = 1
                check_call("echo \"pic " + str(pic) + "\timage_number " + str(image_number) + "\tsub " + str(sub) + "\" >> " + "info_picIdentifier", shell=True)
                while (image_number - int(image_number)) == 0.0 :
                    image_number /= 2.0
                    sub          += 1
                    check_call("echo \"pic " + str(pic) + "\timage_number " + str(image_number) + "\tsub " + str(sub) + "\" >> " + "info_picIdentifier", shell=True)
                check_call("echo \"sub --> " + str(sub) + "\" >> " + "info_picIdentifier", shell=True)

                # Frame type = 'I'
                if self.types_frame[self.TRLs-sub][int(image_number)] == 'I' :
                    bytes_frames_MCTF.append( 0 )
                # Frame type = 'B'
                else :
                    bytes_frames_MCTF.append( self.bytes_frames_TM[0][pic/GOP_size] + self.bytes_frames_TM[0][(pic/GOP_size)+1] )


        # Add bytes Hs & Ms as MCTF, to each frame of Hs.
        for Vpic in range(0, pictures) :
            pic = Vpic
            for sub in range(1, self.TRLs) :
                pic /= 2.0
                if pic - int(pic) > 0.0 :
                    if self.types_frame[self.TRLs-sub][int(pic)] == 'I' :
                        bytes_frames_MCTF[Vpic] += self.bytes_frames_T [self.TRLs-sub][int(pic)]
                        break
                    else :
                        bytes_frames_MCTF[Vpic] += self.bytes_frames_TM[self.TRLs-sub][int(pic)]


        # bytes_frames_MCTF_Average (Frame per frame)
        #----------------------------------------------
        bytes_frames_MCTF_average = [0] * (GOP_size + 1)

        # Ls
        for gop in range(0, GOPs+1) :
            bytes_frames_MCTF_average[0] += bytes_frames_MCTF[gop*GOP_size]
        bytes_frames_MCTF_average[0] /= (GOPs + 1.0)

        # Hs
        for Vpic in range(1, GOP_size+1) :
            for gop in range(0, GOPs) :
                bytes_frames_MCTF_average[Vpic] += bytes_frames_MCTF[Vpic + (gop*GOP_size)]

        for Vpic in range(1, GOP_size+1) :
            bytes_frames_MCTF_average[Vpic] /= GOPs * 1.0

        # PRINT: Formatted for gnuplot.
        for pic in range (0, len(self.bytes_frames_TM_perframe)) :
            check_call("echo \"" + str(pic) + "\t " + str(self.bytes_frames_TM_perframe[pic]) + "\" >> " + "info_bytesFrames_perframe",         shell=True)
        for pic in range (0, len(bytes_frames_MCTF)) :
            check_call("echo \"" + str(pic) + "\t " + str(bytes_frames_MCTF[pic])             + "\" >> " + "info_bytesFrames_MCTF",             shell=True)
        for pic in range (0, len(bytes_frames_MCTF_average)) :
            check_call("echo \"" + str(pic) + "\t " + str(bytes_frames_MCTF_average[pic])     + "\" >> " + "info_bytesFrames_MCTF_averageGOPs", shell=True)

        # PRINT averages.
        #----------------
        sys.stdout.write("---- ")
        sys.stdout.write("-------- ")
        for subband in range(self.TRLs-1, 0, -1) :
            for j in range(0, 2**(self.TRLs-1-subband)) :
                sys.stdout.write("-")
            sys.stdout.write("-------------- ")
        sys.stdout.write("--------\n")
        sys.stdout.write("Average")

        # Average L.
        #-----------
        self.average_L = (L_kbps_GOP0 * (1 - average_ponderation)) + ((self.average_L / GOPs) * average_ponderation) # MEDIA SEMI PONDERADA
        sys.stdout.write("%6d " % int(self.average_L))

        for subband in range(self.TRLs-1, 0, -1) :
            for j in range(0, 2**(self.TRLs-1-subband)) :
                sys.stdout.write(" ")

            # Average Motion and High frecuency.
            #-----------------------------------
            self.average_M[subband] = self.average_M[subband] / self.GOPs
            self.average_H[subband] = self.average_H[subband] / self.GOPs
            sys.stdout.write("%7d " % int(self.average_M[subband]))
            sys.stdout.write("%6d " % int(self.average_H[subband]))

        # Total average.
        #---------------
        self.average_total /= self.GOPs
        self.average_total = (L_kbps_GOP0 * (1 - average_ponderation)) + (self.average_total * average_ponderation) # MEDIA SEMI PONDERADA
        sys.stdout.write("%8d\n" % int(self.average_total))

        quit()
        
        self.average_M.reverse()                      # < Jse
        self.average_H.reverse()                      # < Jse
        self.average_M = self.average_M[1:-1]         # < Jse
        self.average_H = self.average_H[1:-1]         # < Jse
        self.average_H.insert(0, self.average_L)      # < Jse

        # < Jse   SAMPLE DATA PERFORMANCE

        print (" ")
        print ("M_prev_GOP\t"    + str(M_prev_GOP))
        print ("H_prev_GOP\t"    + str(H_prev_GOP))
        print ("M_prev_image\t"  + str(M_prev_image))
        print ("H_prev_image\t"  + str(H_prev_image))

        print (" ")
        print ("Frame_Types\n"               + str(self.types_frame))
        print (" ")
        print ("Bytes_frames_M\n"            + str(self.bytes_frames_M))
        print (" ")
        print ("Bytes_frames_T\n"            + str(self.bytes_frames_T))
        print (" ")
        print ("Bytes_frames_TM\n"           + str(self.bytes_frames_TM))
        print (" ")
        print ("Bytes_frames_TM_perframe\n"  + str(self.bytes_frames_TM_perframe))
        print (" ")
        print ("Bytes_frames_MCTF\n"         + str(bytes_frames_MCTF))
        print (" ")
        print ("Bytes_frames_MCTF_average\n" + str(bytes_frames_MCTF_average))
        print (" ")
        print ("kbps_M\n"                    + str(self.kbps_M))
        print (" ")
        print ("kbps_H\n"                    + str(self.kbps_H))
        print (" ")
        print ("kbps_HM_total\n"             + str(self.kbps_HM_total))
        print (" ")
        print ("average_M\n"                 + str(self.average_M))
        print (" ")
        print ("average_H\n"                 + str(self.average_H))
        print (" ")
        print ("average_total\t"             + str(self.average_total))
        print (" ")
        # > Jse

    ## Returns values of the instance.
    #  @param self Refers to object.
    #  @returns Kbps of:
    #  - Motion, 
    #  - Textures and 
    #  - Both together.
    def kbps(self):
        return self.kbps_M,    self.kbps_H,    self.kbps_HM_total

    ## Returns mean values of the instance.
    #  @param self Refers to object.
    #  @returns Average kbps of:
    #  - Motion, 
    #  - Textures and 
    #  - Both together.
    def kbps_average(self):
        return self.average_M, self.average_H, self.average_total
