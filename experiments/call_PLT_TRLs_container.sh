# DR_CURVE.SH
#//////////////

				
salta(){
	cd /home/cmaturana/scratch
	rm -rf $1
	mkdir $1
	cd $1
}
#/- container ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

### 1 ##########################################################################
salta container_1TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  container_352x288x30x420x300.avi      -l  8  -g  129  -t  1  -b  32  -m  32  -y  288  -x  352 -f 30

salta zero_container_1TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                          -l  8  -g  129  -t  1  -b  32  -m  32  -y  288  -x  352 -f 30

exit 0
### 2 ##########################################################################
salta container_2TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  container_352x288x30x420x300.avi      -l  8  -g  65  -t  2  -b  32  -m  32  -y  288  -x  352 -f 30

salta zero_container_2TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                          -l  8  -g  65  -t  2  -b  32  -m  32  -y  288  -x  352 -f 30

### 3 ##########################################################################
salta container_3TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  container_352x288x30x420x300.avi      -l  8  -g  33  -t  3  -b  32  -m  32  -y  288  -x  352 -f 30

salta zero_container_3TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                          -l  8  -g  33  -t  3  -b  32  -m  32  -y  288  -x  352 -f 30

### 4 ##########################################################################
salta container_4TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  container_352x288x30x420x300.avi      -l  8  -g  17  -t  4  -b  32  -m  32  -y  288  -x  352 -f 30

salta zero_container_4TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                          -l  8  -g  17  -t  4  -b  32  -m  32  -y  288  -x  352 -f 30

### 5 ##########################################################################
salta container_5TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  container_352x288x30x420x300.avi     -l  8  -g  9  -t  5  -b  32  -m  32  -y  288  -x  352 -f 30

salta zero_container_5TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -g  9  -t  5  -b  32  -m  32  -y  288  -x  352 -f 30

### 6 ##########################################################################
salta container_6TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  container_352x288x30x420x300.avi      -l  8  -g  5  -t  6  -b  32  -m  32  -y  288  -x  352 -f 30

salta zero_container_6TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                          -l  8  -g  5  -t  6  -b  32  -m  32  -y  288  -x  352 -f 30

### 7 ##########################################################################
salta container_7TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  container_352x288x30x420x300.avi      -l  8  -g  3  -t  7  -b  32  -m  32  -y  288  -x  352 -f 30

salta zero_container_7TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                          -l  8  -g  3  -t  7  -b  32  -m  32  -y  288  -x  352 -f 30


   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #

### 1 ##########################################################################
salta container_5TRL_1L
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  container_352x288x30x420x300.avi      -l  1  -g  9  -t  5  -b  32  -m  32  -y  288  -x  352 -f 30

salta zero_container_5TRL_1L
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                          -l  1  -g  9  -t  5  -b  32  -m  32  -y  288  -x  352 -f 30

### 4 ##########################################################################
salta container_5TRL_4L
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  container_352x288x30x420x300.avi      -l  4  -g  9  -t  5  -b  32  -m  32  -y  288  -x  352 -f 30

salta zero_container_5TRL_4L
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                          -l  4  -g  9  -t  5  -b  32  -m  32  -y  288  -x  352 -f 30


exit 0
