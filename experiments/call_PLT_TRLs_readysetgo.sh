# DR_CURVE.SH
#//////////////

				
function salta {
	cd /home/cmaturana/scratch
	rm -rf $1
	mkdir $1
	cd $1
}
#/- readysetgo ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

### 1 ##########################################################################
salta readysetgo_1TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh  -v  readysetgo_3840x2176x120x420x600.avi   -l  8  -b  64  -m  64  -g  9  -t  5  -y  2176  -x  3840  -f  120

salta zero_readysetgo_1TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -b  64  -m  64  -g  9  -t  5  -y  2176  -x  3840  -f  120

### 2 ##########################################################################
salta readysetgo_2TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh  -v  readysetgo_3840x2176x120x420x600.avi   -l  8  -b  64  -m  64  -g  9  -t  5  -y  2176  -x  3840  -f  120

salta zero_readysetgo_2TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -b  64  -m  64  -g  9  -t  5  -y  2176  -x  3840  -f  120

### 3 ##########################################################################
salta readysetgo_3TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh  -v  readysetgo_3840x2176x120x420x600.avi   -l  8  -b  64  -m  64  -g  9  -t  5  -y  2176  -x  3840  -f  120

salta zero_readysetgo_3TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -b  64  -m  64  -g  9  -t  5  -y  2176  -x  3840  -f  120

### 4 ##########################################################################
salta readysetgo_4TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh  -v  readysetgo_3840x2176x120x420x600.avi   -l  8  -b  64  -m  64  -g  9  -t  5  -y  2176  -x  3840  -f  120

salta zero_readysetgo_4TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -b  64  -m  64  -g  9  -t  5  -y  2176  -x  3840  -f  120

### 5 ##########################################################################
salta readysetgo_5TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh  -v  readysetgo_3840x2176x120x420x600.avi   -l  8  -b  64  -m  64  -g  9  -t  5  -y  2176  -x  3840  -f  120

salta zero_readysetgo_5TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -b  64  -m  64  -g  9  -t  5  -y  2176  -x  3840  -f  120

### 6 ##########################################################################
salta readysetgo_6TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh  -v  readysetgo_3840x2176x120x420x600.avi   -l  8  -b  64  -m  64  -g  9  -t  5  -y  2176  -x  3840  -f  120

salta zero_readysetgo_6TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -b  64  -m  64  -g  9  -t  5  -y  2176  -x  3840  -f  120

### 7 ##########################################################################
salta readysetgo_7TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh  -v  readysetgo_3840x2176x120x420x600.avi   -l  8  -b  64  -m  64  -g  9  -t  5  -y  2176  -x  3840  -f  120

salta zero_readysetgo_7TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -b  64  -m  64  -g  9  -t  5  -y  2176  -x  3840  -f  120


   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #

### 1 ##########################################################################
salta readysetgo_5TRL_1L
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  readysetgo_3840x2176x120x420x600.avi   -l  1  -b  64  -m  64  -g  9  -t  5  -y  2176  -x  3840  -f  120

salta zero_readysetgo_5TRL_1L
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  1  -b  64  -m  64  -g  9  -t  5  -y  2176  -x  3840  -f  120

### 4 ##########################################################################
salta readysetgo_5TRL_4L
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  readysetgo_3840x2176x120x420x600.avi   -l  4  -b  64  -m  64  -g  9  -t  5  -y  2176  -x  3840  -f  120

salta zero_readysetgo_5TRL_4L
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  4  -b  64  -m  64  -g  9  -t  5  -y  2176  -x  3840  -f  120



exit 0

