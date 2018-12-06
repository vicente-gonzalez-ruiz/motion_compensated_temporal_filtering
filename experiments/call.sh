# EXAMPLE CALLS
# -----------------------------
#En NODO
#       srun -N 1 -n 1 -p ibcl .sh
# #nohup srun -N 1 -n 1 -p ibcl srun -N 1 -n 1 -p ibcl .sh &> sun_LT.log &

# -----------------------------
# Q= 1,2,4,8,16,32.
# T= "1",2,3,4,5,6,7.
# Search Area= 4 (alls excepts readysetgo 32)
# Blocksize= 16 (Mobile, Container), 32 (Crew), 64 (Crowdrun), 128 (ReadySetGo, Sun)
# -----------------------------


export TRANSCODE_QUALITY="transcode_quality_PLT"
export TRANSCODE_QUALITY="transcode_quality_FSO"

exit 0


#<<COMMENT

# DR_TRANSCODE.SH
#-----------------------------
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &> sun_LT.log &

# DR_CURVE.SH
#-----------------------------

#--- MOBILE -------------------------------------------------------------------------------------------------------------------------------------------------------------------
cd /home/cmaturana/scratch; rm -rf tmp_mobile; mkdir tmp_mobile; cd tmp_mobile
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  mobile_352x288x30x420x300.avi         -l  8  -g  9  -t  5  -b  32  -m  32  -y  288  -x  352 -f 30 # &> PLT_mobile_L8T5.log &

cd /home/cmaturana/scratch; rm -rf tmp_mobile_zero; mkdir tmp_mobile_zero; cd tmp_mobile_zero
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -g  9  -t  5  -b  32  -m  32  -y  288  -x  352 -f 30 # &> PLT_mobile_L8T5.log &

#--- CONTAINER ---------------------------------------------------------------------------------------------------------------------------------------------------------------
cd /home/cmaturana/scratch; rm -rf tmp_container; mkdir tmp_container; cd tmp_container
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  container_352x288x30x420x300.avi      -l  8  -g  9  -t  5  -b  32  -m  32  -y  288  -x  352 -f 30 # &> PLT_container_L8T5.log &

#--- CREW --------------------------------------------------------------------------------------------------------------------------------------------------------------------
cd /home/cmaturana/scratch; rm -rf tmp_crew; mkdir tmp_crew; cd tmp_crew
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  crew_704x576x60x420x600.avi           -l  8  -g  9  -t  5  -b  32  -m  32  -y  576  -x  704 -f 60 # &> PLT_crew_L8T5.log &

cd /home/cmaturana/scratch; rm -rf zero_crew; mkdir zero_crew; cd zero_crew
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -g  9  -t  5  -b  32  -m  32  -y  576  -x  704 -f 60 # &> PLT_crew_L8T5.log &

#--- CROWDRUN -----------------------------------------------------------------------------------------------------------------------------------------------------------------
cd /home/cmaturana/scratch; rm -rf tmp_crowdrun; mkdir tmp_crowdrun; cd tmp_crowdrun
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh  -v  crowdrun_1920x1088x50x420x500.avi      -l  8  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50 # &> crowdrun_L8T5.log # &

cd /home/cmaturana/scratch; rm -rf zero_crowdrun; mkdir zero_crowdrun; cd zero_crowdrun
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50 # &> crowdrun_L8T5.log # &

#--- READYSETGO ---------------------------------------------------------------------------------------------------------------------------------------------------------------
cd /home/cmaturana/scratch; rm -rf tmp_readysetgo; mkdir tmp_readysetgo; cd tmp_readysetgo
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh  -v  readysetgo_3840x2176x120x420x600.avi   -l  8  -b  64  -m  64  -g  9  -t  5  -y  2176  -x  3840  -f  120 # &> readysetgo_L8T5.log # &

cd /home/cmaturana/scratch; rm -rf zero_readysetgo; mkdir zero_readysetgo; cd zero_readysetgo
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -b  64  -m  64  -g  9  -t  5  -y  2176  -x  3840  -f  120 # &> readysetgo_L8T5.log # &

#--- SUN -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
cd /home/cmaturana/scratch; rm -rf tmp_sun; mkdir tmp_sun; cd tmp_sun
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh  -v  sun_4096x4096x0.027x420x129.avi        -l  8  -b  128  -m  128  -g  9  -t  5  -y  4096  -x  4096  -f  0.027 # &> sun_L8T5.log # &

cd /home/cmaturana/scratch; rm -rf zero_sun; mkdir zero_sun; cd zero_sun
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -b  128  -m  128  -g  9  -t  5  -y  4096  -x  4096  -f  0.027 # &> sun_L8T5.log # &

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



exit 0

rm -rf tmp; mkdir tmp; cd tmp
#nohup srun -N 1 -n 1 -p ibcl ../DRcurve.sh   -v  zero.yuv.avi  -l  8  -g  9  -t  5  -y  288  -x  352 &> sun_LT.log &
exit 0





  #  MOBILE  
#------------------------------------

#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  1  -k  1  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &> mobile_L1T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  1  -k  1  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &> mobile_L1T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  1  -k  1  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &> mobile_L1T4.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  1  -k  1  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &> mobile_L1T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  1  -k  1  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &> mobile_L1T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  1  -k  1  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &> mobile_L1T7.log &


#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &> mobile_L2T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &> mobile_L2T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &> mobile_L2T4.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &> mobile_L2T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &> mobile_L2T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &> mobile_L2T7.log &


#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &> mobile_L4T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &> mobile_L4T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &> mobile_L4T4.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &> mobile_L4T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &> mobile_L4T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &> mobile_L4T7.log &


nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &> mobile_L8T2.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &> mobile_L8T3.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &> mobile_L8T4.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &> mobile_L8T5.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &> mobile_L8T6.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &> mobile_L8T7.log &


#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &> mobile_L16T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &> mobile_L16T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &> mobile_L16T4.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &> mobile_L16T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &> mobile_L16T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &> mobile_L16T7.log &
                                                                                              

                                                        
  #  CONTAINER  
#------------------------------------

#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  1  -k  1  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &> container_L1T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  1  -k  1  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &> container_L1T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  1  -k  1  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &> container_L1T4.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  1  -k  1  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &> container_L1T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  1  -k  1  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &> container_L1T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  1  -k  1  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &> container_L1T7.log &


#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &> container_L2T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &> container_L2T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &> container_L2T4.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &> container_L2T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &> container_L2T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &> container_L2T7.log &


#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &> container_L4T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &> container_L4T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &> container_L4T4.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &> container_L4T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &> container_L4T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &> container_L4T7.log &
                                                        

nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &> container_L8T2.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &> container_L8T3.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &> container_L8T4.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &> container_L8T5.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &> container_L8T6.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &> container_L8T7.log &
                                                        

#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &> container_L16T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &> container_L16T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &> container_L16T4.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &> container_L16T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &> container_L16T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &> container_L16T7.log &
                                                        

                                                  

  #  CREW  
#------------------------------------

#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  1  -k  1  -b  32  -r  4  -g  65  -t  2  -y  576  -x  704  -f  60 &> crew_L1T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  1  -k  1  -b  32  -r  4  -g  33  -t  3  -y  576  -x  704  -f  60 &> crew_L1T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  1  -k  1  -b  32  -r  4  -g  17  -t  4  -y  576  -x  704  -f  60 &> crew_L1T4.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  1  -k  1  -b  32  -r  4  -g  9  -t  5  -y  576  -x  704  -f  60 &> crew_L1T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  1  -k  1  -b  32  -r  4  -g  5  -t  6  -y  576  -x  704  -f  60 &> crew_L1T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  1  -k  1  -b  32  -r  4  -g  3  -t  7  -y  576  -x  704  -f  60 &> crew_L1T7.log &
                                                        

#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  2  -k  2  -b  32  -r  4  -g  65  -t  2  -y  576  -x  704  -f  60 &> crew_L2T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  2  -k  2  -b  32  -r  4  -g  33  -t  3  -y  576  -x  704  -f  60 &> crew_L2T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  2  -k  2  -b  32  -r  4  -g  17  -t  4  -y  576  -x  704  -f  60 &> crew_L2T4.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  2  -k  2  -b  32  -r  4  -g  9  -t  5  -y  576  -x  704  -f  60 &> crew_L2T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  2  -k  2  -b  32  -r  4  -g  5  -t  6  -y  576  -x  704  -f  60 &> crew_L2T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  2  -k  2  -b  32  -r  4  -g  3  -t  7  -y  576  -x  704  -f  60 &> crew_L2T7.log &
                                                        

#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  4  -k  4  -b  32  -r  4  -g  65  -t  2  -y  576  -x  704  -f  60 &> crew_L4T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  4  -k  4  -b  32  -r  4  -g  33  -t  3  -y  576  -x  704  -f  60 &> crew_L4T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  4  -k  4  -b  32  -r  4  -g  17  -t  4  -y  576  -x  704  -f  60 &> crew_L4T4.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  4  -k  4  -b  32  -r  4  -g  9  -t  5  -y  576  -x  704  -f  60 &> crew_L4T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  4  -k  4  -b  32  -r  4  -g  5  -t  6  -y  576  -x  704  -f  60 &> crew_L4T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  4  -k  4  -b  32  -r  4  -g  3  -t  7  -y  576  -x  704  -f  60 &> crew_L4T7.log &
                                                        

nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  8  -k  8  -b  32  -r  4  -g  65  -t  2  -y  576  -x  704  -f  60 &> crew_L8T2.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  8  -k  8  -b  32  -r  4  -g  33  -t  3  -y  576  -x  704  -f  60 &> crew_L8T3.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  8  -k  8  -b  32  -r  4  -g  17  -t  4  -y  576  -x  704  -f  60 &> crew_L8T4.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  8  -k  8  -b  32  -r  4  -g  9  -t  5  -y  576  -x  704  -f  60 &> crew_L8T5.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  8  -k  8  -b  32  -r  4  -g  5  -t  6  -y  576  -x  704  -f  60 &> crew_L8T6.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  8  -k  8  -b  32  -r  4  -g  3  -t  7  -y  576  -x  704  -f  60 &> crew_L8T7.log &
                                                        

#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  16  -k  16  -b  32  -r  4  -g  65  -t  2  -y  576  -x  704  -f  60 &> crew_L16T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  16  -k  16  -b  32  -r  4  -g  33  -t  3  -y  576  -x  704  -f  60 &> crew_L16T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  16  -k  16  -b  32  -r  4  -g  17  -t  4  -y  576  -x  704  -f  60 &> crew_L16T4.log &
nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  16  -k  16  -b  32  -r  4  -g  9  -t  5  -y  576  -x  704  -f  60 &> crew_L16T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  16  -k  16  -b  32  -r  4  -g  5  -t  6  -y  576  -x  704  -f  60 &> crew_L16T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  16  -k  16  -b  32  -r  4  -g  3  -t  7  -y  576  -x  704  -f  60 &> crew_L16T7.log &
                                                        
#COMMENT


                              
  #  CROWDRUN  
#------------------------------------

#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  1  -k  1  -b  64  -r  4  -g  65  -t  2  -y  1088  -x  1920  -f  50 &> crowdrun_L1T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  1  -k  1  -b  64  -r  4  -g  33  -t  3  -y  1088  -x  1920  -f  50 &> crowdrun_L1T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  1  -k  1  -b  64  -r  4  -g  17  -t  4  -y  1088  -x  1920  -f  50 &> crowdrun_L1T4.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  1  -k  1  -b  64  -r  4  -g  9  -t  5  -y  1088  -x  1920  -f  50 &> crowdrun_L1T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  1  -k  1  -b  64  -r  4  -g  5  -t  6  -y  1088  -x  1920  -f  50 &> crowdrun_L1T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  1  -k  1  -b  64  -r  4  -g  3  -t  7  -y  1088  -x  1920  -f  50 &> crowdrun_L1T7.log &
                                                        

#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  2  -k  2  -b  64  -r  4  -g  65  -t  2  -y  1088  -x  1920  -f  50 &> crowdrun_L2T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  2  -k  2  -b  64  -r  4  -g  33  -t  3  -y  1088  -x  1920  -f  50 &> crowdrun_L2T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  2  -k  2  -b  64  -r  4  -g  17  -t  4  -y  1088  -x  1920  -f  50 &> crowdrun_L2T4.log &
##nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  2  -k  2  -b  64  -r  4  -g  9  -t  5  -y  1088  -x  1920  -f  50 &> crowdrun_L2T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  2  -k  2  -b  64  -r  4  -g  5  -t  6  -y  1088  -x  1920  -f  50 &> crowdrun_L2T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  2  -k  2  -b  64  -r  4  -g  3  -t  7  -y  1088  -x  1920  -f  50 &> crowdrun_L2T7.log &
                                                        

#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  4  -k  4  -b  64  -r  4  -g  65  -t  2  -y  1088  -x  1920  -f  50 &> crowdrun_L4T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  4  -k  4  -b  64  -r  4  -g  33  -t  3  -y  1088  -x  1920  -f  50 &> crowdrun_L4T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  4  -k  4  -b  64  -r  4  -g  17  -t  4  -y  1088  -x  1920  -f  50 &> crowdrun_L4T4.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  4  -k  4  -b  64  -r  4  -g  9  -t  5  -y  1088  -x  1920  -f  50 &> crowdrun_L4T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  4  -k  4  -b  64  -r  4  -g  5  -t  6  -y  1088  -x  1920  -f  50 &> crowdrun_L4T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  4  -k  4  -b  64  -r  4  -g  3  -t  7  -y  1088  -x  1920  -f  50 &> crowdrun_L4T7.log &
                                                        

#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  8  -k  8  -b  64  -r  4  -g  65  -t  2  -y  1088  -x  1920  -f  50 &> crowdrun_L8T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  8  -k  8  -b  64  -r  4  -g  33  -t  3  -y  1088  -x  1920  -f  50 &> crowdrun_L8T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  8  -k  8  -b  64  -r  4  -g  17  -t  4  -y  1088  -x  1920  -f  50 &> crowdrun_L8T4.log &
srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  8  -k  8  -b  64  -r  4  -g  9  -t  5  -y  1088  -x  1920  -f  50 &> crowdrun_L8T5.log # &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  8  -k  8  -b  64  -r  4  -g  5  -t  6  -y  1088  -x  1920  -f  50 &> crowdrun_L8T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  8  -k  8  -b  64  -r  4  -g  3  -t  7  -y  1088  -x  1920  -f  50 &> crowdrun_L8T7.log &
                                                        

#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  16  -k  16  -b  64  -r  4  -g  65  -t  2  -y  1088  -x  1920  -f  50 &> crowdrun_L16T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  16  -k  16  -b  64  -r  4  -g  33  -t  3  -y  1088  -x  1920  -f  50 &> crowdrun_L16T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  16  -k  16  -b  64  -r  4  -g  17  -t  4  -y  1088  -x  1920  -f  50 &> crowdrun_L16T4.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  16  -k  16  -b  64  -r  4  -g  9  -t  5  -y  1088  -x  1920  -f  50 &> crowdrun_L16T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  16  -k  16  -b  64  -r  4  -g  5  -t  6  -y  1088  -x  1920  -f  50 &> crowdrun_L16T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  16  -k  16  -b  64  -r  4  -g  3  -t  7  -y  1088  -x  1920  -f  50 &> crowdrun_L16T7.log &
                                                        



  #  READYSETGO  
#------------------------------------

#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  1  -k  1  -b  128  -r  4  -g  65  -t  2  -y  2176  -x  3840  -f  120 &> readysetgo_L1T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  1  -k  1  -b  128  -r  4  -g  33  -t  3  -y  2176  -x  3840  -f  120 &> readysetgo_L1T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  1  -k  1  -b  128  -r  4  -g  17  -t  4  -y  2176  -x  3840  -f  120 &> readysetgo_L1T4.log &
##nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  1  -k  1  -b  128  -r  4  -g  9  -t  5  -y  2176  -x  3840  -f  120 &> readysetgo_L1T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  1  -k  1  -b  128  -r  4  -g  5  -t  6  -y  2176  -x  3840  -f  120 &> readysetgo_L1T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  1  -k  1  -b  128  -r  4  -g  3  -t  7  -y  2176  -x  3840  -f  120 &> readysetgo_L1T7.log &
                                                        

#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  128  -r  4  -g  65  -t  2  -y  2176  -x  3840  -f  120 &> readysetgo_L2T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  128  -r  4  -g  33  -t  3  -y  2176  -x  3840  -f  120 &> readysetgo_L2T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  128  -r  4  -g  17  -t  4  -y  2176  -x  3840  -f  120 &> readysetgo_L2T4.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  128  -r  4  -g  9  -t  5  -y  2176  -x  3840  -f  120 &> readysetgo_L2T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  128  -r  4  -g  5  -t  6  -y  2176  -x  3840  -f  120 &> readysetgo_L2T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  128  -r  4  -g  3  -t  7  -y  2176  -x  3840  -f  120 &> readysetgo_L2T7.log &
                                                        

#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  128  -r  4  -g  65  -t  2  -y  2176  -x  3840  -f  120 &> readysetgo_L4T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  128  -r  4  -g  33  -t  3  -y  2176  -x  3840  -f  120 &> readysetgo_L4T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  128  -r  4  -g  17  -t  4  -y  2176  -x  3840  -f  120 &> readysetgo_L4T4.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  128  -r  4  -g  9  -t  5  -y  2176  -x  3840  -f  120 &> readysetgo_L4T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  128  -r  4  -g  5  -t  6  -y  2176  -x  3840  -f  120 &> readysetgo_L4T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  128  -r  4  -g  3  -t  7  -y  2176  -x  3840  -f  120 &> readysetgo_L4T7.log &
                                                        

#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  128  -r  4  -g  65  -t  2  -y  2176  -x  3840  -f  120 &> readysetgo_L8T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  128  -r  4  -g  33  -t  3  -y  2176  -x  3840  -f  120 &> readysetgo_L8T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  128  -r  4  -g  17  -t  4  -y  2176  -x  3840  -f  120 &> readysetgo_L8T4.log &
srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  128  -r  4  -g  9  -t  5  -y  2176  -x  3840  -f  120 &> readysetgo_L8T5.log # &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  128  -r  4  -g  5  -t  6  -y  2176  -x  3840  -f  120 &> readysetgo_L8T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  128  -r  4  -g  3  -t  7  -y  2176  -x  3840  -f  120 &> readysetgo_L8T7.log &
                                                        

#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  128  -r  4  -g  65  -t  2  -y  2176  -x  3840  -f  120 &> readysetgo_L16T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  128  -r  4  -g  33  -t  3  -y  2176  -x  3840  -f  120 &> readysetgo_L16T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  128  -r  4  -g  17  -t  4  -y  2176  -x  3840  -f  120 &> readysetgo_L16T4.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  128  -r  4  -g  9  -t  5  -y  2176  -x  3840  -f  120 &> readysetgo_L16T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  128  -r  4  -g  5  -t  6  -y  2176  -x  3840  -f  120 &> readysetgo_L16T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  128  -r  4  -g  3  -t  7  -y  2176  -x  3840  -f  120 &> readysetgo_L16T7.log &
                                                        



                                                        
  #  SUN  
#------------------------------------

#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  1  -k  1  -b  128  -r  0  -g  65  -t  2  -y  4096  -x  4096  -f  0.027 &> sun_L1T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  1  -k  1  -b  128  -r  0  -g  33  -t  3  -y  4096  -x  4096  -f  0.027 &> sun_L1T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  1  -k  1  -b  128  -r  0  -g  17  -t  4  -y  4096  -x  4096  -f  0.027 &> sun_L1T4.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  1  -k  1  -b  128  -r  0  -g  9  -t  5  -y  4096  -x  4096  -f  0.027 &> sun_L1T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  1  -k  1  -b  128  -r  0  -g  5  -t  6  -y  4096  -x  4096  -f  0.027 &> sun_L1T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  1  -k  1  -b  128  -r  0  -g  3  -t  7  -y  4096  -x  4096  -f  0.027 &> sun_L1T7.log &
                                                        

#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  2  -k  2  -b  128  -r  0  -g  65  -t  2  -y  4096  -x  4096  -f  0.027 &> sun_L2T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  2  -k  2  -b  128  -r  0  -g  33  -t  3  -y  4096  -x  4096  -f  0.027 &> sun_L2T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  2  -k  2  -b  128  -r  0  -g  17  -t  4  -y  4096  -x  4096  -f  0.027 &> sun_L2T4.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  2  -k  2  -b  128  -r  0  -g  9  -t  5  -y  4096  -x  4096  -f  0.027 &> sun_L2T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  2  -k  2  -b  128  -r  0  -g  5  -t  6  -y  4096  -x  4096  -f  0.027 &> sun_L2T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  2  -k  2  -b  128  -r  0  -g  3  -t  7  -y  4096  -x  4096  -f  0.027 &> sun_L2T7.log &
                                                        

#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  4  -k  4  -b  128  -r  0  -g  65  -t  2  -y  4096  -x  4096  -f  0.027 &> sun_L4T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  4  -k  4  -b  128  -r  0  -g  33  -t  3  -y  4096  -x  4096  -f  0.027 &> sun_L4T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  4  -k  4  -b  128  -r  0  -g  17  -t  4  -y  4096  -x  4096  -f  0.027 &> sun_L4T4.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  4  -k  4  -b  128  -r  0  -g  9  -t  5  -y  4096  -x  4096  -f  0.027 &> sun_L4T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  4  -k  4  -b  128  -r  0  -g  5  -t  6  -y  4096  -x  4096  -f  0.027 &> sun_L4T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  4  -k  4  -b  128  -r  0  -g  3  -t  7  -y  4096  -x  4096  -f  0.027 &> sun_L4T7.log &
                                                        

#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  8  -k  8  -b  128  -r  0  -g  65  -t  2  -y  4096  -x  4096  -f  0.027 &> sun_L8T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  8  -k  8  -b  128  -r  0  -g  33  -t  3  -y  4096  -x  4096  -f  0.027 &> sun_L8T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  8  -k  8  -b  128  -r  0  -g  17  -t  4  -y  4096  -x  4096  -f  0.027 &> sun_L8T4.log &
srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  8  -k  8  -b  128  -r  0  -g  9  -t  5  -y  4096  -x  4096  -f  0.027 &> sun_L8T5.log # &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  8  -k  8  -b  128  -r  0  -g  5  -t  6  -y  4096  -x  4096  -f  0.027 &> sun_L8T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  8  -k  8  -b  128  -r  0  -g  3  -t  7  -y  4096  -x  4096  -f  0.027 &> sun_L8T7.log &
                                                        

#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  16  -k  16  -b  128  -r  0  -g  65  -t  2  -y  4096  -x  4096  -f  0.027 &> sun_L16T2.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  16  -k  16  -b  128  -r  0  -g  33  -t  3  -y  4096  -x  4096  -f  0.027 &> sun_L16T3.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  16  -k  16  -b  128  -r  0  -g  17  -t  4  -y  4096  -x  4096  -f  0.027 &> sun_L16T4.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  16  -k  16  -b  128  -r  0  -g  9  -t  5  -y  4096  -x  4096  -f  0.027 &> sun_L16T5.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  16  -k  16  -b  128  -r  0  -g  5  -t  6  -y  4096  -x  4096  -f  0.027 &> sun_L16T6.log &
#nohup srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  16  -k  16  -b  128  -r  0  -g  3  -t  7  -y  4096  -x  4096  -f  0.027 &> sun_L16T7.log &
                                                        


exit 0



# YUV to AVI
#x264 --input-res 352x288   --qp 0 -o container_352x288x30x420x300.avi          container_352x288x30x420x300.yuv
#x264 --input-res 352x288   --qp 0 -o mobile_352x288x30x420x300.avi             mobile_352x288x30x420x300.yuv
#x264 --input-res 704x576   --qp 0 -o crew_704x576x60x420x600.avi               crew_704x576x60x420x600.yuv
#x264 --input-res 1920x1088 --qp 0 -o crowdrun_1920x1088x50x420x500.avi         crowdrun_1920x1088x50x420x500.yuv
#x264 --input-res 3840x2176 --qp 0 -o readysetgo_3840x2176x120x420x600.avi      readysetgo_3840x2176x120x420x600.yuv
#x264 --input-res 4096x4096 --qp 0 -o sun_4096x4096x0.027x420x129.avi           sun_4096x4096x0.027x420x129.yuv
