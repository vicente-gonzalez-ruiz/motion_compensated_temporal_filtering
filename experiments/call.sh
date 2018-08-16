# EXAMPLE CALLS
# -----------------------------
##En NODO
#       srun -N 1 -n 1 -p ibmulticore .sh
# nohup srun -N 1 -n 1 -p ibmulticore .sh &



# -----------------------------
# Q=1,2,4,8,16,32
# T=1,2,3,4,5,6,7.
# Search Area=4 (alls excepts readysetgo 32)
# Blocksize= 16 (Mobile, Container), 32 (Crew), 64 (Crowdrun), 128 (ReadySetGo, Sun)

#srun -N 1 -n 1 -p ibmulticore ./basic.sh -v mobile_352x288x30x420x300.avi -g 3 -t 4 -y 288 -x 352 -f 30 -l 8 -k 8

#                                                                             layers          block_size  Search_range    Nº_gops     TRLs    Y       X       Frames
                                ./basic.sh -v mobile_352x288x30x420x300.avi   -l 1  -k 1     -b 16       -r 4            -g 2        -t 1    -y 288  -x 352  -f 30
exit 0
srun -N 1 -n 1 -p ibmulticore2  ./basic.sh -v mobile_352x288x30x420x300.avi   -l 1  -k 1     -b 16       -r 4            -g 2        -t 1    -y 288  -x 352  -f 30
exit 0





# YUV to AVI
#x264 --input-res 352x288 --qp 0 -o container_352x288x30x420x300.avi         container_352x288x30x420x300.yuv
#x264 --input-res 352x288 --qp 0 -o mobile_352x288x30x420x300.avi            mobile_352x288x30x420x300.yuv
#x264 --input-res 704x576 --qp 0 -o crew_704x576x60x420x600.avi              crew_704x576x60x420x600.yuv
#x264 --input-res 1920x1088 --qp 0 -o crowdrun_1920x1088x50x420x500.avi      crowdrun_1920x1088x50x420x500.yuv
#x264 --input-res 3840x2176 --qp 0 -o readysetgo_3840x2176x120x420x600.avi   readysetgo_3840x2176x120x420x600.yuv
#x264 --input-res 4096x4096 --qp 0 -o sun_4096x4096x0.027x420x129.avi        sun_4096x4096x0.027x420x129.yuv
