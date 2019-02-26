# EXAMPLE CALLS
# -----------------------------
#En NODO
#       srun -N 1 -n 1 -p iball .sh
# #srun -N 1 -n 1 -p iball srun -N 1 -n 1 -p iball .sh  & # &> sun_LT.log &

# -----------------------------
# Q= 1,2,4,8,16,32.
# T= "1",2,3,4,5,6,7.
# Search Area= 4 (alls excepts readysetgo 32)
# Blocksize= 16 (Mobile, Container), 32 (Crew), 64 (Crowdrun), 128 (ReadySetGo, Sun)
# -----------------------------


export TRANSCODE_QUALITY="transcode_quality_PLT"
export TRANSCODE_QUALITY="transcode_quality_FSO"



exit 0
rm -rf tmp4; mkdir tmp4; cd tmp4
srun -N 1 -n 1 -p iball ../basic.sh -v ../Videos/readysetgo_3840x2176x120x420x600.avi -x 3840 -y 2176 -f 120 -S 4 -g 2 -t 5 -b 64 -B 64 &
rm -rf tmp8; mkdir tmp8; cd tmp8
srun -N 1 -n 1 -p iball ../basic.sh -v ../Videos/readysetgo_3840x2176x120x420x600.avi -x 3840 -y 2176 -f 120 -S 8 -g 2 -t 5 -b 64 -B 64 &
rm -rf tmp16; mkdir tmp16; cd tmp16
srun -N 1 -n 1 -p iball ../basic.sh -v ../Videos/readysetgo_3840x2176x120x420x600.avi -x 3840 -y 2176 -f 120 -S 16 -g 2 -t 5 -b 64 -B 64 &
rm -rf tmp32; mkdir tmp32; cd tmp32
srun -N 1 -n 1 -p iball ../basic.sh -v ../Videos/readysetgo_3840x2176x120x420x600.avi -x 3840 -y 2176 -f 120 -S 32 -g 2 -t 5 -b 64 -B 64 &
rm -rf tmp64; mkdir tmp64; cd tmp64
srun -N 1 -n 1 -p iball ../basic.sh -v ../Videos/readysetgo_3840x2176x120x420x600.avi -x 3840 -y 2176 -f 120 -S 64 -g 2 -t 5 -b 64 -B 64 &
rm -rf tmp128; mkdir tmp128; cd tmp128
srun -N 1 -n 1 -p iball ../basic.sh -v ../Videos/readysetgo_3840x2176x120x420x600.avi -x 3840 -y 2176 -f 120 -S 128 -g 2 -t 5 -b 64 -B 64 &
rm -rf tmp128_128; mkdir tmp128_128; cd tmp128_128
srun -N 1 -n 1 -p iball ../basic.sh -v ../Videos/readysetgo_3840x2176x120x420x600.avi -x 3840 -y 2176 -f 120 -S 128 -g 2 -t 5 -b 128 -B 128 &

cd ..

exit 0








rm -rf tmp
mkdir tmp
cd tmp
srun -N 1 -n 1 --exclusive -p iball ../basic.sh  -v  ../Videos/readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -g  2  -t  5  -y  2176  -x  3840  -f  120 -s 45000 &
#srun -N 1 -n 1 --exclusive -p iball ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  64  -m  64  -r  8  -g  2  -t  5  -y  2176  -x  3840  -f  120 -s 45000 &

exit 0



./call_PLT_TRLs_sun_58.sh &
./call_PLT_TRLs_sun_58z.sh &

srun -N 1 -n 1 --exclusive -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  64  -m  64  -r  8  -g  9  -t  5  -y  2176  -x  3840  -f  120 &
srun -N 1 -n 1 --exclusive -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  64  -m  64  -r  16  -g  9  -t  5  -y  2176  -x  3840  -f  120 &

#srun -N 1 -n 1 --exclusive -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  4  -k  4  -b  128  -m  128  -r  0  -g  9  -t  5  -y  4096  -x  4096  -f  0.027  &
exit 0

<<COMMENT

exit 0

./call_PLT_TRLs_sun_7.sh &
./call_PLT_TRLs_sun_51.sh &
./call_PLT_TRLs_sun_54.sh &
./call_PLT_TRLs_sun_58.sh &

./call_PLT_TRLs_sun_7z.sh &
./call_PLT_TRLs_sun_51z.sh &
./call_PLT_TRLs_sun_54z.sh &
./call_PLT_TRLs_sun_58z.sh &

exit 0

./call_PLT_TRLs_container.sh &
./call_PLT_TRLs_crew.sh &
./call_PLT_TRLs_crowdrun.sh &
./call_PLT_TRLs_crowdrun_.sh &
./call_PLT_TRLs_mobile.sh &
./call_PLT_TRLs_readysetgo.sh &
./call_PLT_TRLs_readysetgo_.sh &
./call_PLT_TRLs_sun.sh &
./call_PLT_TRLs_sun_.sh &

exit 0




# DR_TRANSCODE.SH
#-----------------------------
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30  & # &> sun_LT.log &

exit 0





  #  MOBILE  
#------------------------------------
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30  & # &> mobile_L2T2.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30  & # &> mobile_L2T3.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30  & # &> mobile_L2T4.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30  & # &> mobile_L2T5.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30  & # &> mobile_L2T6.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30  & # &> mobile_L2T7.log &


#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30  & # &> mobile_L4T2.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30  & # &> mobile_L4T3.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30  & # &> mobile_L4T4.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30  & # &> mobile_L4T5.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30  & # &> mobile_L4T6.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30  & # &> mobile_L4T7.log &


srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30  & # &> mobile_L8T2.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30  & # &> mobile_L8T3.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30  & # &> mobile_L8T4.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30  & # &> mobile_L8T5.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30  & # &> mobile_L8T6.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30  & # &> mobile_L8T7.log &


#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30  & # &> mobile_L16T2.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30  & # &> mobile_L16T3.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30  & # &> mobile_L16T4.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30  & # &> mobile_L16T5.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30  & # &> mobile_L16T6.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  mobile_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30  & # &> mobile_L16T7.log &
                                                                                              

                                                        
  #  CONTAINER  
#------------------------------------
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30  & # &> container_L2T2.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30  & # &> container_L2T3.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30  & # &> container_L2T4.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30  & # &> container_L2T5.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30  & # &> container_L2T6.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30  & # &> container_L2T7.log &


#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30  & # &> container_L4T2.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30  & # &> container_L4T3.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30  & # &> container_L4T4.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30  & # &> container_L4T5.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30  & # &> container_L4T6.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30  & # &> container_L4T7.log &
                                                        

srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30  & # &> container_L8T2.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30  & # &> container_L8T3.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30  & # &> container_L8T4.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30  & # &> container_L8T5.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30  & # &> container_L8T6.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30  & # &> container_L8T7.log &
                                                        

#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30  & # &> container_L16T2.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30  & # &> container_L16T3.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30  & # &> container_L16T4.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30  & # &> container_L16T5.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30  & # &> container_L16T6.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  container_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30  & # &> container_L16T7.log &
                                                        

                                                  

  #  CREW  
#------------------------------------
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  2  -k  2  -b  32  -r  4  -g  65  -t  2  -y  576  -x  704  -f  60  & # &> crew_L2T2.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  2  -k  2  -b  32  -r  4  -g  33  -t  3  -y  576  -x  704  -f  60  & # &> crew_L2T3.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  2  -k  2  -b  32  -r  4  -g  17  -t  4  -y  576  -x  704  -f  60  & # &> crew_L2T4.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  2  -k  2  -b  32  -r  4  -g  9  -t  5  -y  576  -x  704  -f  60  & # &> crew_L2T5.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  2  -k  2  -b  32  -r  4  -g  5  -t  6  -y  576  -x  704  -f  60  & # &> crew_L2T6.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  2  -k  2  -b  32  -r  4  -g  3  -t  7  -y  576  -x  704  -f  60  & # &> crew_L2T7.log &
                                                        

#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  4  -k  4  -b  32  -r  4  -g  65  -t  2  -y  576  -x  704  -f  60  & # &> crew_L4T2.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  4  -k  4  -b  32  -r  4  -g  33  -t  3  -y  576  -x  704  -f  60  & # &> crew_L4T3.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  4  -k  4  -b  32  -r  4  -g  17  -t  4  -y  576  -x  704  -f  60  & # &> crew_L4T4.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  4  -k  4  -b  32  -r  4  -g  9  -t  5  -y  576  -x  704  -f  60  & # &> crew_L4T5.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  4  -k  4  -b  32  -r  4  -g  5  -t  6  -y  576  -x  704  -f  60  & # &> crew_L4T6.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  4  -k  4  -b  32  -r  4  -g  3  -t  7  -y  576  -x  704  -f  60  & # &> crew_L4T7.log &
                                                        

srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  8  -k  8  -b  32  -r  4  -g  65  -t  2  -y  576  -x  704  -f  60  & # &> crew_L8T2.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  8  -k  8  -b  32  -r  4  -g  33  -t  3  -y  576  -x  704  -f  60  & # &> crew_L8T3.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  8  -k  8  -b  32  -r  4  -g  17  -t  4  -y  576  -x  704  -f  60  & # &> crew_L8T4.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  8  -k  8  -b  32  -r  4  -g  9  -t  5  -y  576  -x  704  -f  60  & # &> crew_L8T5.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  8  -k  8  -b  32  -r  4  -g  5  -t  6  -y  576  -x  704  -f  60  & # &> crew_L8T6.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  8  -k  8  -b  32  -r  4  -g  3  -t  7  -y  576  -x  704  -f  60  & # &> crew_L8T7.log &
                                                        

#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  16  -k  16  -b  32  -r  4  -g  65  -t  2  -y  576  -x  704  -f  60  & # &> crew_L16T2.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  16  -k  16  -b  32  -r  4  -g  33  -t  3  -y  576  -x  704  -f  60  & # &> crew_L16T3.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  16  -k  16  -b  32  -r  4  -g  17  -t  4  -y  576  -x  704  -f  60  & # &> crew_L16T4.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  16  -k  16  -b  32  -r  4  -g  9  -t  5  -y  576  -x  704  -f  60  & # &> crew_L16T5.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  16  -k  16  -b  32  -r  4  -g  5  -t  6  -y  576  -x  704  -f  60  & # &> crew_L16T6.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crew_704x576x60x420x600.avi  -l  16  -k  16  -b  32  -r  4  -g  3  -t  7  -y  576  -x  704  -f  60  & # &> crew_L16T7.log &
                                                        




  #  CROWDRUN
#------------------------------------
srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  1  -k  1  -b  64  -m  64  -r  4  -g  9  -t  5  -y  1088  -x  1920  -f  50  & # &> crowdrun_L8T5.log # &

#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  2  -k  2  -b  64  -m  64  -r  4  -g  65  -t  2  -y  1088  -x  1920  -f  50  & # &> crowdrun_L2T2.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  2  -k  2  -b  64  -m  64  -r  4  -g  33  -t  3  -y  1088  -x  1920  -f  50  & # &> crowdrun_L2T3.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  2  -k  2  -b  64  -m  64  -r  4  -g  17  -t  4  -y  1088  -x  1920  -f  50  & # &> crowdrun_L2T4.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  2  -k  2  -b  64  -m  64  -r  4  -g  9  -t  5  -y  1088  -x  1920  -f  50  & # &> crowdrun_L2T5.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  2  -k  2  -b  64  -m  64  -r  4  -g  5  -t  6  -y  1088  -x  1920  -f  50  & # &> crowdrun_L2T6.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  2  -k  2  -b  64  -m  64  -r  4  -g  3  -t  7  -y  1088  -x  1920  -f  50  & # &> crowdrun_L2T7.log &


#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  4  -k  4  -b  64  -m  64  -r  4  -g  65  -t  2  -y  1088  -x  1920  -f  50  & # &> crowdrun_L4T2.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  4  -k  4  -b  64  -m  64  -r  4  -g  33  -t  3  -y  1088  -x  1920  -f  50  & # &> crowdrun_L4T3.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  4  -k  4  -b  64  -m  64  -r  4  -g  17  -t  4  -y  1088  -x  1920  -f  50  & # &> crowdrun_L4T4.log &
# srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  4  -k  4  -b  64  -m  64  -r  4  -g  9  -t  5  -y  1088  -x  1920  -f  50  & # &> crowdrun_L4T5.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  4  -k  4  -b  64  -m  64  -r  4  -g  5  -t  6  -y  1088  -x  1920  -f  50  & # &> crowdrun_L4T6.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  4  -k  4  -b  64  -m  64  -r  4  -g  3  -t  7  -y  1088  -x  1920  -f  50  & # &> crowdrun_L4T7.log &


# srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  8  -k  8  -b  64  -m  64  -r  4  -g  65  -t  2  -y  1088  -x  1920  -f  50  & # &> crowdrun_L8T2.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  8  -k  8  -b  64  -m  64  -r  4  -g  33  -t  3  -y  1088  -x  1920  -f  50  & # &> crowdrun_L8T3.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  8  -k  8  -b  64  -m  64  -r  4  -g  17  -t  4  -y  1088  -x  1920  -f  50  & # &> crowdrun_L8T4.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  8  -k  8  -b  64  -m  64  -r  4  -g  9  -t  5  -y  1088  -x  1920  -f  50  & # &> crowdrun_L8T5.log # &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  8  -k  8  -b  64  -m  64  -r  4  -g  5  -t  6  -y  1088  -x  1920  -f  50  & # &> crowdrun_L8T6.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  8  -k  8  -b  64  -m  64  -r  4  -g  3  -t  7  -y  1088  -x  1920  -f  50  & # &> crowdrun_L8T7.log &


#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  16  -k  16  -b  64  -m  64  -r  4  -g  65  -t  2  -y  1088  -x  1920  -f  50  & # &> crowdrun_L16T2.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  16  -k  16  -b  64  -m  64  -r  4  -g  33  -t  3  -y  1088  -x  1920  -f  50  & # &> crowdrun_L16T3.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  16  -k  16  -b  64  -m  64  -r  4  -g  17  -t  4  -y  1088  -x  1920  -f  50  & # &> crowdrun_L16T4.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  16  -k  16  -b  64  -m  64  -r  4  -g  9  -t  5  -y  1088  -x  1920  -f  50  & # &> crowdrun_L16T5.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  16  -k  16  -b  64  -m  64  -r  4  -g  5  -t  6  -y  1088  -x  1920  -f  50  & # &> crowdrun_L16T6.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  16  -k  16  -b  64  -m  64  -r  4  -g  3  -t  7  -y  1088  -x  1920  -f  50  & # &> crowdrun_L16T7.log &


COMMENT


  #  READYSETGO
#------------------------------------
srun -N 1 -n 1 -p ibcl ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  1  -k  1  -b  64  -m  64  -r  4  -g  9  -t  5  -y  2176  -x  3840  -f  120 & # > readysetgo_L8T5.log # &

#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  64  -m  64  -r  4  -g  65  -t  2  -y  2176  -x  3840  -f  120  & # &> readysetgo_L2T2.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  64  -m  64  -r  4  -g  33  -t  3  -y  2176  -x  3840  -f  120  & # &> readysetgo_L2T3.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  64  -m  64  -r  4  -g  17  -t  4  -y  2176  -x  3840  -f  120  & # &> readysetgo_L2T4.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  64  -m  64  -r  4  -g  9  -t  5  -y  2176  -x  3840  -f  120  & # &> readysetgo_L2T5.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  64  -m  64  -r  4  -g  5  -t  6  -y  2176  -x  3840  -f  120  & # &> readysetgo_L2T6.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  64  -m  64  -r  4  -g  3  -t  7  -y  2176  -x  3840  -f  120  & # &> readysetgo_L2T7.log &
                                                        

#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  64  -m  64  -r  4  -g  65  -t  2  -y  2176  -x  3840  -f  120  & # &> readysetgo_L4T2.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  64  -m  64  -r  4  -g  33  -t  3  -y  2176  -x  3840  -f  120  & # &> readysetgo_L4T3.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  64  -m  64  -r  4  -g  17  -t  4  -y  2176  -x  3840  -f  120  & # &> readysetgo_L4T4.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  64  -m  64  -r  4  -g  9  -t  5  -y  2176  -x  3840  -f  120  & # &> readysetgo_L4T5.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  64  -m  64  -r  4  -g  5  -t  6  -y  2176  -x  3840  -f  120  & # &> readysetgo_L4T6.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  64  -m  64  -r  4  -g  3  -t  7  -y  2176  -x  3840  -f  120  & # &> readysetgo_L4T7.log &
                                                        

srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  64  -m  64  -r  4  -g  65  -t  2  -y  2176  -x  3840  -f  120  & # &> readysetgo_L8T2.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  64  -m  64  -r  4  -g  33  -t  3  -y  2176  -x  3840  -f  120  & # &> readysetgo_L8T3.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  64  -m  64  -r  4  -g  17  -t  4  -y  2176  -x  3840  -f  120  & # &> readysetgo_L8T4.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  64  -m  64  -r  4  -g  9  -t  5  -y  2176  -x  3840  -f  120 & # > readysetgo_L8T5.log # &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  64  -m  64  -r  4  -g  5  -t  6  -y  2176  -x  3840  -f  120  & # &> readysetgo_L8T6.log &
srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  64  -m  64  -r  4  -g  3  -t  7  -y  2176  -x  3840  -f  120  & # &> readysetgo_L8T7.log &
                                                        

#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  64  -m  64  -r  4  -g  65  -t  2  -y  2176  -x  3840  -f  120  & # &> readysetgo_L16T2.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  64  -m  64  -r  4  -g  33  -t  3  -y  2176  -x  3840  -f  120  & # &> readysetgo_L16T3.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  64  -m  64  -r  4  -g  17  -t  4  -y  2176  -x  3840  -f  120  & # &> readysetgo_L16T4.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  64  -m  64  -r  4  -g  9  -t  5  -y  2176  -x  3840  -f  120  & # &> readysetgo_L16T5.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  64  -m  64  -r  4  -g  5  -t  6  -y  2176  -x  3840  -f  120  & # &> readysetgo_L16T6.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  64  -m  64  -r  4  -g  3  -t  7  -y  2176  -x  3840  -f  120  & # &> readysetgo_L16T7.log &
                                                        
exit 0


                                                        
  #  SUN
#------------------------------------
srun -N 1 -n 1 --exclusive -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  1  -k  1  -b  128  -m  128  -r  0  -g  9  -t  5  -y  4096  -x  4096  -f  0.027  & # &> sun_L8T5.log # &

#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  2  -k  2  -b  128  -m  128  -r  0  -g  65  -t  2  -y  4096  -x  4096  -f  0.027  & # &> sun_L2T2.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  2  -k  2  -b  128  -m  128  -r  0  -g  33  -t  3  -y  4096  -x  4096  -f  0.027  & # &> sun_L2T3.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  2  -k  2  -b  128  -m  128  -r  0  -g  17  -t  4  -y  4096  -x  4096  -f  0.027  & # &> sun_L2T4.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  2  -k  2  -b  128  -m  128  -r  0  -g  9  -t  5  -y  4096  -x  4096  -f  0.027  & # &> sun_L2T5.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  2  -k  2  -b  128  -m  128  -r  0  -g  5  -t  6  -y  4096  -x  4096  -f  0.027  & # &> sun_L2T6.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  2  -k  2  -b  128  -m  128  -r  0  -g  3  -t  7  -y  4096  -x  4096  -f  0.027  & # &> sun_L2T7.log &


#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  4  -k  4  -b  128  -m  128  -r  0  -g  65  -t  2  -y  4096  -x  4096  -f  0.027  & # &> sun_L4T2.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  4  -k  4  -b  128  -m  128  -r  0  -g  33  -t  3  -y  4096  -x  4096  -f  0.027  & # &> sun_L4T3.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  4  -k  4  -b  128  -m  128  -r  0  -g  17  -t  4  -y  4096  -x  4096  -f  0.027  & # &> sun_L4T4.log &
srun -N 1 -n 1 --exclusive -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  4  -k  4  -b  128  -m  128  -r  0  -g  9  -t  5  -y  4096  -x  4096  -f  0.027  & # &> sun_L4T5.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  4  -k  4  -b  128  -m  128  -r  0  -g  5  -t  6  -y  4096  -x  4096  -f  0.027  & # &> sun_L4T6.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  4  -k  4  -b  128  -m  128  -r  0  -g  3  -t  7  -y  4096  -x  4096  -f  0.027  & # &> sun_L4T7.log &


#srun -N 1 -n 1 --exclusive -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  8  -k  8  -b  128  -m  128  -r  0  -g  65  -t  2  -y  4096  -x  4096  -f  0.027  & # &> sun_L8T2.log &
#srun -N 1 -n 1 --exclusive -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  8  -k  8  -b  128  -m  128  -r  0  -g  33  -t  3  -y  4096  -x  4096  -f  0.027  & # &> sun_L8T3.log &
#srun -N 1 -n 1 --exclusive -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  8  -k  8  -b  128  -m  128  -r  0  -g  17  -t  4  -y  4096  -x  4096  -f  0.027  & # &> sun_L8T4.log &
#srun -N 1 -n 1 --exclusive -p ibmulticore ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  8  -k  8  -b  128  -m  128  -r  0  -g  9  -t  5  -y  4096  -x  4096  -f  0.027  & # &> sun_L8T5.log # &
#srun -N 1 -n 1 --exclusive -p ibmulticore ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  8  -k  8  -b  128  -m  128  -r  0  -g  5  -t  6  -y  4096  -x  4096  -f  0.027  & # &> sun_L8T6.log &
#srun -N 1 -n 1 --exclusive -p ibmulticore ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  8  -k  8  -b  128  -m  128  -r  0  -g  3  -t  7  -y  4096  -x  4096  -f  0.027  & # &> sun_L8T7.log &


#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  16  -k  16  -b  128  -m  128  -r  0  -g  65  -t  2  -y  4096  -x  4096  -f  0.027  & # &> sun_L16T2.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  16  -k  16  -b  128  -m  128  -r  0  -g  33  -t  3  -y  4096  -x  4096  -f  0.027  & # &> sun_L16T3.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  16  -k  16  -b  128  -m  128  -r  0  -g  17  -t  4  -y  4096  -x  4096  -f  0.027  & # &> sun_L16T4.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  16  -k  16  -b  128  -m  128  -r  0  -g  9  -t  5  -y  4096  -x  4096  -f  0.027  & # &> sun_L16T5.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  16  -k  16  -b  128  -m  128  -r  0  -g  5  -t  6  -y  4096  -x  4096  -f  0.027  & # &> sun_L16T6.log &
#srun -N 1 -n 1 -p iball ./DR_transcode.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  16  -k  16  -b  128  -m  128  -r  0  -g  3  -t  7  -y  4096  -x  4096  -f  0.027  & # &> sun_L16T7.log &



exit 0



# YUV to AVI
#x264 --input-res 352x288   --qp 0 -o container_352x288x30x420x300.avi          container_352x288x30x420x300.yuv
#x264 --input-res 352x288   --qp 0 -o mobile_352x288x30x420x300.avi             mobile_352x288x30x420x300.yuv
#x264 --input-res 704x576   --qp 0 -o crew_704x576x60x420x600.avi               crew_704x576x60x420x600.yuv
#x264 --input-res 1920x1088 --qp 0 -o crowdrun_1920x1088x50x420x500.avi         crowdrun_1920x1088x50x420x500.yuv
#x264 --input-res 3840x2176 --qp 0 -o readysetgo_3840x2176x120x420x600.avi      readysetgo_3840x2176x120x420x600.yuv
#x264 --input-res 4096x4096 --qp 0 -o sun_4096x4096x0.027x420x129.avi           sun_4096x4096x0.027x420x129.yuv
