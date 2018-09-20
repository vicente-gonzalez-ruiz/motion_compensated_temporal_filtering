# EXAMPLE CALLS
# -----------------------------
##En NODO
#       srun -N 1 -n 1 -p ibmulticore2 .sh
# nohup srun -N 1 -n 1 -p ibcl srun -N 1 -n 1 -p ibmulticore2 .sh &



# -----------------------------
# Q= 1,2,4,8,16,32.
# T= "1",2,3,4,5,6,7.
# Search Area= 4 (alls excepts readysetgo 32)
# Blocksize= 16 (Mobile, Container), 32 (Crew), 64 (Crowdrun), 128 (ReadySetGo, Sun)

#<<COMMENT
  #  MOBILE  -------------------------------------------------------------------                                                  
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  1  -k  1  -b  16  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  1  -k  1  -b  16  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  1  -k  1  -b  16  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  1  -k  1  -b  16  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  1  -k  1  -b  16  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  1  -k  1  -b  16  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &

  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  2  -k  2  -b  16  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  2  -k  2  -b  16  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  2  -k  2  -b  16  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  2  -k  2  -b  16  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  2  -k  2  -b  16  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  2  -k  2  -b  16  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &

  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  4  -k  4  -b  16  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  4  -k  4  -b  16  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  4  -k  4  -b  16  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  4  -k  4  -b  16  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  4  -k  4  -b  16  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  4  -k  4  -b  16  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &

  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  8  -k  8  -b  16  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  8  -k  8  -b  16  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  8  -k  8  -b  16  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  8  -k  8  -b  16  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  8  -k  8  -b  16  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  8  -k  8  -b  16  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &

  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  16  -k  16  -b  16  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  16  -k  16  -b  16  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  16  -k  16  -b  16  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  16  -k  16  -b  16  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  16  -k  16  -b  16  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  16  -k  16  -b  16  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  32  -k  32  -b  16  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  32  -k  32  -b  16  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  32  -k  32  -b  16  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  32  -k  32  -b  16  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  32  -k  32  -b  16  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  mobile_352x288x30x420x300.avi  -l  32  -k  32  -b  16  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &
                                                        

                                                        
  #  CONTAINER  -------------------------------------------------------------------                                                  
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  1  -k  1  -b  16  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  1  -k  1  -b  16  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  1  -k  1  -b  16  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  1  -k  1  -b  16  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  1  -k  1  -b  16  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  1  -k  1  -b  16  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  2  -k  2  -b  16  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  2  -k  2  -b  16  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  2  -k  2  -b  16  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  2  -k  2  -b  16  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  2  -k  2  -b  16  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  2  -k  2  -b  16  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  4  -k  4  -b  16  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  4  -k  4  -b  16  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  4  -k  4  -b  16  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  4  -k  4  -b  16  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  4  -k  4  -b  16  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  4  -k  4  -b  16  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  8  -k  8  -b  16  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  8  -k  8  -b  16  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  8  -k  8  -b  16  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  8  -k  8  -b  16  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  8  -k  8  -b  16  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  8  -k  8  -b  16  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  16  -k  16  -b  16  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  16  -k  16  -b  16  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  16  -k  16  -b  16  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  16  -k  16  -b  16  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  16  -k  16  -b  16  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  16  -k  16  -b  16  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  32  -k  32  -b  16  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  32  -k  32  -b  16  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  32  -k  32  -b  16  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  32  -k  32  -b  16  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  32  -k  32  -b  16  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  container_352x288x30x420x300.avi  -l  32  -k  32  -b  16  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &
                                                        
                                                
                                                        
                                                        
  #  CREW  -------------------------------------------------------------------                                                  
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  1  -k  1  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  1  -k  1  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  1  -k  1  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  1  -k  1  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  1  -k  1  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  1  -k  1  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  2  -k  2  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  4  -k  4  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  8  -k  8  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  16  -k  16  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  32  -k  32  -b  32  -r  4  -g  65  -t  2  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  32  -k  32  -b  32  -r  4  -g  33  -t  3  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  32  -k  32  -b  32  -r  4  -g  17  -t  4  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  32  -k  32  -b  32  -r  4  -g  9  -t  5  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  32  -k  32  -b  32  -r  4  -g  5  -t  6  -y  288  -x  352  -f  30 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crew_352x288x30x420x300.avi  -l  32  -k  32  -b  32  -r  4  -g  3  -t  7  -y  288  -x  352  -f  30 &
                
#COMMENT
exit 0

                              
  #  CROWDRUN  -------------------------------------------------------------------                                                  
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  1  -k  1  -b  64  -r  4  -g  65  -t  2  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  1  -k  1  -b  64  -r  4  -g  33  -t  3  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  1  -k  1  -b  64  -r  4  -g  17  -t  4  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  1  -k  1  -b  64  -r  4  -g  9  -t  5  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  1  -k  1  -b  64  -r  4  -g  5  -t  6  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  1  -k  1  -b  64  -r  4  -g  3  -t  7  -y  1920  -x  1088  -f  50 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  2  -k  2  -b  64  -r  4  -g  65  -t  2  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  2  -k  2  -b  64  -r  4  -g  33  -t  3  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  2  -k  2  -b  64  -r  4  -g  17  -t  4  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  2  -k  2  -b  64  -r  4  -g  9  -t  5  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  2  -k  2  -b  64  -r  4  -g  5  -t  6  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  2  -k  2  -b  64  -r  4  -g  3  -t  7  -y  1920  -x  1088  -f  50 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  4  -k  4  -b  64  -r  4  -g  65  -t  2  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  4  -k  4  -b  64  -r  4  -g  33  -t  3  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  4  -k  4  -b  64  -r  4  -g  17  -t  4  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  4  -k  4  -b  64  -r  4  -g  9  -t  5  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  4  -k  4  -b  64  -r  4  -g  5  -t  6  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  4  -k  4  -b  64  -r  4  -g  3  -t  7  -y  1920  -x  1088  -f  50 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  8  -k  8  -b  64  -r  4  -g  65  -t  2  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  8  -k  8  -b  64  -r  4  -g  33  -t  3  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  8  -k  8  -b  64  -r  4  -g  17  -t  4  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  8  -k  8  -b  64  -r  4  -g  9  -t  5  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  8  -k  8  -b  64  -r  4  -g  5  -t  6  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  8  -k  8  -b  64  -r  4  -g  3  -t  7  -y  1920  -x  1088  -f  50 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  16  -k  16  -b  64  -r  4  -g  65  -t  2  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  16  -k  16  -b  64  -r  4  -g  33  -t  3  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  16  -k  16  -b  64  -r  4  -g  17  -t  4  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  16  -k  16  -b  64  -r  4  -g  9  -t  5  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  16  -k  16  -b  64  -r  4  -g  5  -t  6  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  16  -k  16  -b  64  -r  4  -g  3  -t  7  -y  1920  -x  1088  -f  50 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  32  -k  32  -b  64  -r  4  -g  65  -t  2  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  32  -k  32  -b  64  -r  4  -g  33  -t  3  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  32  -k  32  -b  64  -r  4  -g  17  -t  4  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  32  -k  32  -b  64  -r  4  -g  9  -t  5  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  32  -k  32  -b  64  -r  4  -g  5  -t  6  -y  1920  -x  1088  -f  50 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  crowdrun_1920x1088x50x420x500.avi  -l  32  -k  32  -b  64  -r  4  -g  3  -t  7  -y  1920  -x  1088  -f  50 &
                                                        
  #  READYSETGO  -------------------------------------------------------------------                                                  
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  1  -k  1  -b  128  -r  4  -g  65  -t  2  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  1  -k  1  -b  128  -r  4  -g  33  -t  3  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  1  -k  1  -b  128  -r  4  -g  17  -t  4  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  1  -k  1  -b  128  -r  4  -g  9  -t  5  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  1  -k  1  -b  128  -r  4  -g  5  -t  6  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  1  -k  1  -b  128  -r  4  -g  3  -t  7  -y  3840  -x  2176  -f  120 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  128  -r  4  -g  65  -t  2  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  128  -r  4  -g  33  -t  3  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  128  -r  4  -g  17  -t  4  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  128  -r  4  -g  9  -t  5  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  128  -r  4  -g  5  -t  6  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  128  -r  4  -g  3  -t  7  -y  3840  -x  2176  -f  120 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  128  -r  4  -g  65  -t  2  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  128  -r  4  -g  33  -t  3  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  128  -r  4  -g  17  -t  4  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  128  -r  4  -g  9  -t  5  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  128  -r  4  -g  5  -t  6  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  128  -r  4  -g  3  -t  7  -y  3840  -x  2176  -f  120 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  128  -r  4  -g  65  -t  2  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  128  -r  4  -g  33  -t  3  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  128  -r  4  -g  17  -t  4  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  128  -r  4  -g  9  -t  5  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  128  -r  4  -g  5  -t  6  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  128  -r  4  -g  3  -t  7  -y  3840  -x  2176  -f  120 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  128  -r  4  -g  65  -t  2  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  128  -r  4  -g  33  -t  3  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  128  -r  4  -g  17  -t  4  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  128  -r  4  -g  9  -t  5  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  128  -r  4  -g  5  -t  6  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  128  -r  4  -g  3  -t  7  -y  3840  -x  2176  -f  120 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  32  -k  32  -b  128  -r  4  -g  65  -t  2  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  32  -k  32  -b  128  -r  4  -g  33  -t  3  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  32  -k  32  -b  128  -r  4  -g  17  -t  4  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  32  -k  32  -b  128  -r  4  -g  9  -t  5  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  32  -k  32  -b  128  -r  4  -g  5  -t  6  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  32  -k  32  -b  128  -r  4  -g  3  -t  7  -y  3840  -x  2176  -f  120 &
                                                        
  #  READYSETGO  -------------------------------------------------------------------                                                  
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  1  -k  1  -b  128  -r  32  -g  65  -t  2  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  1  -k  1  -b  128  -r  32  -g  33  -t  3  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  1  -k  1  -b  128  -r  32  -g  17  -t  4  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  1  -k  1  -b  128  -r  32  -g  9  -t  5  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  1  -k  1  -b  128  -r  32  -g  5  -t  6  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  1  -k  1  -b  128  -r  32  -g  3  -t  7  -y  3840  -x  2176  -f  120 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  128  -r  32  -g  65  -t  2  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  128  -r  32  -g  33  -t  3  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  128  -r  32  -g  17  -t  4  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  128  -r  32  -g  9  -t  5  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  128  -r  32  -g  5  -t  6  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  2  -k  2  -b  128  -r  32  -g  3  -t  7  -y  3840  -x  2176  -f  120 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  128  -r  32  -g  65  -t  2  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  128  -r  32  -g  33  -t  3  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  128  -r  32  -g  17  -t  4  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  128  -r  32  -g  9  -t  5  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  128  -r  32  -g  5  -t  6  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  4  -k  4  -b  128  -r  32  -g  3  -t  7  -y  3840  -x  2176  -f  120 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  128  -r  32  -g  65  -t  2  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  128  -r  32  -g  33  -t  3  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  128  -r  32  -g  17  -t  4  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  128  -r  32  -g  9  -t  5  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  128  -r  32  -g  5  -t  6  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  8  -k  8  -b  128  -r  32  -g  3  -t  7  -y  3840  -x  2176  -f  120 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  128  -r  32  -g  65  -t  2  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  128  -r  32  -g  33  -t  3  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  128  -r  32  -g  17  -t  4  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  128  -r  32  -g  9  -t  5  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  128  -r  32  -g  5  -t  6  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  16  -k  16  -b  128  -r  32  -g  3  -t  7  -y  3840  -x  2176  -f  120 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  32  -k  32  -b  128  -r  32  -g  65  -t  2  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  32  -k  32  -b  128  -r  32  -g  33  -t  3  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  32  -k  32  -b  128  -r  32  -g  17  -t  4  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  32  -k  32  -b  128  -r  32  -g  9  -t  5  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  32  -k  32  -b  128  -r  32  -g  5  -t  6  -y  3840  -x  2176  -f  120 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  readysetgo_3840x2176x120x420x600.avi  -l  32  -k  32  -b  128  -r  32  -g  3  -t  7  -y  3840  -x  2176  -f  120 &
                                                        
                                                        
  #  SUN  -------------------------------------------------------------------                                                  
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  1  -k  1  -b  128  -r  4  -g  65  -t  2  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  1  -k  1  -b  128  -r  4  -g  33  -t  3  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  1  -k  1  -b  128  -r  4  -g  17  -t  4  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  1  -k  1  -b  128  -r  4  -g  9  -t  5  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  1  -k  1  -b  128  -r  4  -g  5  -t  6  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  1  -k  1  -b  128  -r  4  -g  3  -t  7  -y  4096  -x  4096  -f  0,027 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  2  -k  2  -b  128  -r  4  -g  65  -t  2  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  2  -k  2  -b  128  -r  4  -g  33  -t  3  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  2  -k  2  -b  128  -r  4  -g  17  -t  4  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  2  -k  2  -b  128  -r  4  -g  9  -t  5  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  2  -k  2  -b  128  -r  4  -g  5  -t  6  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  2  -k  2  -b  128  -r  4  -g  3  -t  7  -y  4096  -x  4096  -f  0,027 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  4  -k  4  -b  128  -r  4  -g  65  -t  2  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  4  -k  4  -b  128  -r  4  -g  33  -t  3  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  4  -k  4  -b  128  -r  4  -g  17  -t  4  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  4  -k  4  -b  128  -r  4  -g  9  -t  5  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  4  -k  4  -b  128  -r  4  -g  5  -t  6  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  4  -k  4  -b  128  -r  4  -g  3  -t  7  -y  4096  -x  4096  -f  0,027 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  8  -k  8  -b  128  -r  4  -g  65  -t  2  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  8  -k  8  -b  128  -r  4  -g  33  -t  3  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  8  -k  8  -b  128  -r  4  -g  17  -t  4  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  8  -k  8  -b  128  -r  4  -g  9  -t  5  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  8  -k  8  -b  128  -r  4  -g  5  -t  6  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  8  -k  8  -b  128  -r  4  -g  3  -t  7  -y  4096  -x  4096  -f  0,027 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  16  -k  16  -b  128  -r  4  -g  65  -t  2  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  16  -k  16  -b  128  -r  4  -g  33  -t  3  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  16  -k  16  -b  128  -r  4  -g  17  -t  4  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  16  -k  16  -b  128  -r  4  -g  9  -t  5  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  16  -k  16  -b  128  -r  4  -g  5  -t  6  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  16  -k  16  -b  128  -r  4  -g  3  -t  7  -y  4096  -x  4096  -f  0,027 &
                                                        
  #  layers  block_size  Search_range  Nº_gops  TRLs  Y  X  Frames                                      
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  32  -k  32  -b  128  -r  4  -g  65  -t  2  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  32  -k  32  -b  128  -r  4  -g  33  -t  3  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  32  -k  32  -b  128  -r  4  -g  17  -t  4  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  32  -k  32  -b  128  -r  4  -g  9  -t  5  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  32  -k  32  -b  128  -r  4  -g  5  -t  6  -y  4096  -x  4096  -f  0,027 &
nohup srun -N 1 -n 1 -p ibcl ./basic.sh  -v  sun_4096x4096x0.027x420x129.avi  -l  32  -k  32  -b  128  -r  4  -g  3  -t  7  -y  4096  -x  4096  -f  0,027 &







exit 0
nohup srun -N 1 -n 1 -p ibcl srun -N 1 -n 1 -p ibmulticore  ./basic.sh -v mobile_352x288x30x420x300.avi   -l 1  -k 1     -b 16       -r 4            -g 2        -t 1    -y 288  -x 352  -f 30 &
exit 0



# YUV to AVI
#x264 --input-res 352x288 --qp 0 -o container_352x288x30x420x300.avi         container_352x288x30x420x300.yuv
#x264 --input-res 352x288 --qp 0 -o mobile_352x288x30x420x300.avi            mobile_352x288x30x420x300.yuv
#x264 --input-res 704x576 --qp 0 -o crew_704x576x60x420x600.avi              crew_704x576x60x420x600.yuv
#x264 --input-res 1920x1088 --qp 0 -o crowdrun_1920x1088x50x420x500.avi      crowdrun_1920x1088x50x420x500.yuv
#x264 --input-res 3840x2176 --qp 0 -o readysetgo_3840x2176x120x420x600.avi   readysetgo_3840x2176x120x420x600.yuv
#x264 --input-res 4096x4096 --qp 0 -o sun_4096x4096x0.027x420x129.avi        sun_4096x4096x0.027x420x129.yuv
