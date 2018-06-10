#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

# Show data-rate information of the MCTF structure:
#
# 0 1 2 3 4 5 6 7 8
# 0               8 L_3
#         4         H_3
#     2       6     H_2
#   1   3   5   7   H_1

import sys
import io
from GOP import GOP
from arguments_parser import arguments_parser
import traceback
import os
from colorlog import ColorLog
import logging

log = ColorLog(logging.getLogger("info"))
log.setLevel('INFO')

parser = arguments_parser(description="Show information.")
parser.add_argument("--FPS",
                    help="Frames Per Second",
                    default=30)
parser.GOPs()
parser.TRLs()

args = parser.parse_known_args()[0]
FPS = int(args.FPS)
GOPs = int(args.GOPs)
TRLs = int(args.TRLs)

gop = GOP()
GOP_size = gop.get_size(TRLs)
pictures = GOP_size*(GOPs-1)+1
# Weighting value, to be applied between the GOP0, and the rest.
average_ponderation = (pictures-1.0)/pictures
GOP0_time = 1.0/FPS
GOP_time = float(GOP_size)/FPS

IMG_EXT = os.environ["MCTF_IMG_EXT"]

sys.stdout.write("\n" + sys.argv[0] + ":\n\n")
sys.stdout.write("TRLs           = " + str(TRLs) + " temporal resolution levels\n")
sys.stdout.write("Pictures       = " + str(pictures) + " pictures\n")
sys.stdout.write("FPS            = " + str(FPS) + " frames/second\n")
sys.stdout.write("GOP size       = " + str(GOP_size) + " pictures\n")
sys.stdout.write("Number of GOPs = " + str(GOPs) + " groups of pictures\n")
sys.stdout.write("Frame time     = " + str(GOP0_time) + " seconds\n")
sys.stdout.write("GOP time       = " + str(GOP_time) + " seconds\n")
sys.stdout.write("Total time     = " + str(pictures/FPS) + " seconds\n")
sys.stdout.write("\nAll the values are given in thousands (1000) of bits per second (Kbps).\n")

# Frame types
F_file = [None]
for subband in range(1, TRLs):
    F_file.append(io.open("frame_types_" + str(subband)))

# Table header.

# First line. (TRL4 TRL3 TRL2 TRL1 TRL0).
sys.stdout.write("\n     ")
sys.stdout.write("    TRL" + str(TRLs-1))

for i in range(TRLs-1, 0, -1):
    sys.stdout.write("           ")
    for j in range(0, 2**(TRLs-1-i)):
        sys.stdout.write(" ")
    sys.stdout.write("TRL" + str(i-1))
sys.stdout.write("\n")

# Second line. (GOP L_4 motion_4+H_4 motion_3+Ht_3 motion_2+H2 motion_1+H_1 Total Average).
sys.stdout.write("GOP#")
sys.stdout.write("      L_" + str(TRLs-1))

for i in range(TRLs-1, 0, -1):
    for j in range(0, 2**(TRLs-1-i)):
        sys.stdout.write(" ")
    sys.stdout.write("motion_" + str(i) + " H_" + str(i))
sys.stdout.write("    Total Average\n")

# Third line. (--------------------------------------)
sys.stdout.write("---- ")
sys.stdout.write("-------- ")
for i in range(TRLs-1, 0, -1):
    for j in range(0, 2**(TRLs-1-i)):
        sys.stdout.write("-")
    sys.stdout.write("-------------- ")
sys.stdout.write("-------- -------\n")

# Computations

# GOP 0. The GOP0 is formed by the first picture in L_<TRLs-1>.
length = 0
filename = "L_" + str(TRLs - 1) + "/" + "%04d" % 0 + "." + IMG_EXT
try:
    with io.open(filename, "rb") as file:
        file.seek(0, 2)
        length += file.tell()
except:
    pass

Kbps_total = 0
Kbps_total_pro = 0

Kbps = float(length) * 8.0 / GOP0_time / 1000.0
sys.stdout.write("0000 %8d " % Kbps)
Kbps_total += Kbps
Kbps_L0 = Kbps_total

for subband in range(TRLs-1, 0, -1):
    for j in range(0, 2**(TRLs-1-subband)) :
        sys.stdout.write("-")
    sys.stdout.write("%7d " % 0)
    sys.stdout.write("%6d " % 0)

sys.stdout.write("%8d" % Kbps_total)
sys.stdout.write("%8d\n" % Kbps_L0)

# Rest of GOPs
for GOP_number in range(GOPs-1):
    
    Kbps_total = 0

    sys.stdout.write("%3s " % '%04d' % (GOP_number+1))

    # L
    length = 0
    filename = "L_" + str(TRLs - 1) + "/" + "%04d" % GOP_number + "." + IMG_EXT
    try:
        with io.open(filename, "rb") as file:
            file.seek(0, 2)
            length += file.tell()
    except:
        log.error("Exception {}".format(traceback.format_exc()))
        sys.exit(-1)

    Kbps = float(length) * 8.0 / GOP_time / 1000.0
    sys.stdout.write("%8d " % int(round(Kbps)))
    Kbps_total += Kbps

    # Rest of subbands
    pics_in_subband = 1
    for subband in range(TRLs-1, 0, -1):

        #import ipdb; ipdb.set_trace()

        # Frame types
        for i in range(pics_in_subband):
            frame_type = F_file[subband].read(1)
            #types_frame[TRLs - subband].append(frame_type)
            #sys.stdout.write(frame_type.decode('utf-8'))
            sys.stdout.write(frame_type)
            
        # Motion
        length = 0
        for i in range(pics_in_subband):
            filename = "motion_residue_" + str(subband) + "/" + "%04d" % (GOP_number*(pics_in_subband-1)+i) + ".j2c"
            try:
                with io.open(filename, "rb") as file:
                    file.seek(0, 2)
                    length += file.tell()
            except:
                log.error("Exception {}".format(traceback.format_exc()))
                sys.exit(-1)

        Kbps = float(length) * 8.0 / GOP_time / 1000.0
        sys.stdout.write("%7d " % int(round(Kbps)))
        Kbps_total += Kbps

        # Texture
        for i in range(pics_in_subband):
            filename = "H_" + str(subband) + "/" + "%04d" % (GOP_number*(pics_in_subband-1)+i) + "." + IMG_EXT
            try:
                with io.open(filename, "rb") as file:
                    file.seek(0, 2)
                    length += file.tell()
            except:
                log.error("Exception {}".format(traceback.format_exc()))
                sys.exit(-1)
                
        Kbps = float(length) * 8.0 / GOP_time / 1000.0
        sys.stdout.write("%6d " % int(round(Kbps)))
        Kbps_total += Kbps

        pics_in_subband *= 2

    Kbps_total_pro += Kbps_total
    Kbps_average = Kbps_total_pro/(GOP_number+1)+(Kbps_L0/(GOP_size*(GOP_number+1)))
    

    sys.stdout.write("%8d" % Kbps_total)
    sys.stdout.write("%8d" % Kbps_average)
    sys.stdout.write("\n")

sys.stdout.write("\nAverage bit-rate (Kbps) = {}\n".format(Kbps_average))
'''



# GOP n. GOPs are formed by a number of subbands.
#------------------------------------------------
for GOP_number in range(1, self.GOPs+1) :
    total = 0 # Total Kbps
    sys.stdout.write("%3s " % '%04d' % GOP_number)


    # SUBBANDA L. Each new picture represents a new GOP.
    #-------------------------------------------------
    L_next_GOP = self.find_next_EOC_texture(L_file)
    L_bytes    = L_next_GOP - L_prev_GOP
    self.bytes_frames_T[0].append(L_bytes) # Bytes per frame

    L_prev_GOP                   = L_next_GOP
    L_Kbps                       = float(L_bytes) * 8.0 / GOP_time / 1000.0
    self.Kbps_H[GOP_number].append(L_Kbps)
    self.average_L              += L_Kbps
    total                       += L_Kbps

    sys.stdout.write("%8d " % int(L_Kbps))


    # SUBBANDAS H. Depending on the level of temporal resolution, each GOP generates a number of different pictures.
    pics_in_GOP = 1
    for subband in range(self.TRLs-1, 0, -1) :

        # Frame_types.
        #-------------
        for i in range(0, pics_in_GOP) :
            frame_type = F_file[subband].read(1)
            self.types_frame[self.TRLs - subband].append(frame_type)
            sys.stdout.write(frame_type.decode('utf-8'))


        # Motion.
        #--------
        for i in range(0, pics_in_GOP) :
            next_picture = self.find_next_EOC_motion(M_file[subband])
            self.bytes_frames_M[self.TRLs - subband].append(next_picture - M_prev_picture[subband]) # Bytes per frame
            M_prev_picture[subband] = next_picture

        M_Kbps = float(next_picture - M_prev_GOP[subband]) * 8.0 / GOP_time / 1000.0

        self.Kbps_M[GOP_number-1].append(M_Kbps)
        self.average_M[subband]       += M_Kbps
        total                         += M_Kbps
        sys.stdout.write("%7d " %    int(M_Kbps))

        #import ipdb; ipdb.set_trace()
        M_prev_picture[subband] = M_prev_GOP[subband] = next_picture

        # High frecuency.
        #----------------
        for i in range(0, pics_in_GOP):
            with io.open("H_" + str(subband) + "_" + "%04d" % g*GOP_size+i + "_U" + ".j2c", "rb" as file):
                file.seek(0, 2)
                self.bytes_frames_T[self.TRLs - subband].append(file.tell())
            next_picture = self.find_next_EOC_texture(H_file[subband])
            self.bytes_frames_T[self.TRLs - subband].append(next_picture - H_prev_picture[subband]) # Bytes per frame
            H_prev_picture[subband] = next_picture

        H_Kbps = float(next_picture - H_prev_GOP[subband]) * 8.0 / GOP_time / 1000.0

        self.Kbps_H[GOP_number].append(H_Kbps)
        self.average_H[subband]     += H_Kbps
        total                       += H_Kbps
        sys.stdout.write("%6d " %  int(H_Kbps))

        H_prev_picture[subband] = H_prev_GOP[subband] = next_picture

        pics_in_GOP *= 2

    sys.stdout.write("%8d\n" % total)
    self.average_total      += total
    self.Kbps_HM_total.append (total) # < Jse

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

    if Vpic % GOP_size == 0 : # Is a L picture. Then add picture 0, from L, from GOPx
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
    if pic % GOP_size == 0 : # Is a L picture. Then add picture 0, from L, from GOPx
        bytes_frames_MCTF.append( self.bytes_frames_TM[0][pic/GOP_size] )

    else : # Is not a L picture. Then add picture 0 & 1, from L, from GOPx

        ## pic is the picture number 'picture_number' from subband 'sub'.
        picture_number = pic / 2.0
        sub          = 1
        check_call("echo \"pic " + str(pic) + "\tpicture_number " + str(picture_number) + "\tsub " + str(sub) + "\" >> " + "info_picIdentifier", shell=True)
        while (picture_number - int(picture_number)) == 0.0 :
            picture_number /= 2.0
            sub          += 1
            check_call("echo \"pic " + str(pic) + "\tpicture_number " + str(picture_number) + "\tsub " + str(sub) + "\" >> " + "info_picIdentifier", shell=True)
        check_call("echo \"sub --> " + str(sub) + "\" >> " + "info_picIdentifier", shell=True)

        # Frame type = 'I'
        if self.types_frame[self.TRLs-sub][int(picture_number)] == 'I' :
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
self.average_L = (L_Kbps_GOP0 * (1 - average_ponderation)) + ((self.average_L / GOPs) * average_ponderation) # MEDIA SEMI PONDERADA
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
self.average_total = (L_Kbps_GOP0 * (1 - average_ponderation)) + (self.average_total * average_ponderation) # MEDIA SEMI PONDERADA
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
print ("M_prev_picture\t"  + str(M_prev_picture))
print ("H_prev_picture\t"  + str(H_prev_picture))

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
print ("Kbps_M\n"                    + str(self.Kbps_M))
print (" ")
print ("Kbps_H\n"                    + str(self.Kbps_H))
print (" ")
print ("Kbps_HM_total\n"             + str(self.Kbps_HM_total))
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
def Kbps(self):
    return self.Kbps_M,    self.Kbps_H,    self.Kbps_HM_total

## Returns mean values of the instance.
#  @param self Refers to object.
#  @returns Average Kbps of:
#  - Motion, 
#  - Textures and 
#  - Both together.
def Kbps_average(self):
    return self.average_M, self.average_H, self.average_total
'''
