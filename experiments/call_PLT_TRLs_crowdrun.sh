# DR_CURVE.SH
#//////////////

				
function salta {
	cd /home/cmaturana/scratch
	rm -rf $1
	mkdir $1
	cd $1
}
#/- crowdrun ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

### 1 ##########################################################################
salta crowdrun_1TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh  -v  crowdrun_1920x1088x50x420x500.avi      -l  8  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50

salta zero_crowdrun_1TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50

### 2 ##########################################################################
salta crowdrun_2TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh  -v  crowdrun_1920x1088x50x420x500.avi      -l  8  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50

salta zero_crowdrun_2TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50

### 3 ##########################################################################
salta crowdrun_3TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh  -v  crowdrun_1920x1088x50x420x500.avi      -l  8  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50

salta zero_crowdrun_3TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50

### 4 ##########################################################################
salta crowdrun_4TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh  -v  crowdrun_1920x1088x50x420x500.avi      -l  8  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50

salta zero_crowdrun_4TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50

### 5 ##########################################################################
salta crowdrun_5TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh  -v  crowdrun_1920x1088x50x420x500.avi      -l  8  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50

salta zero_crowdrun_5TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50

### 6 ##########################################################################
salta crowdrun_6TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh  -v  crowdrun_1920x1088x50x420x500.avi      -l  8  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50

salta zero_crowdrun_6TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50

### 7 ##########################################################################
salta crowdrun_7TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh  -v  crowdrun_1920x1088x50x420x500.avi      -l  8  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50

salta zero_crowdrun_7TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50



   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #

### 1 ##########################################################################
salta crowdrun_5TRL_1L
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  crowdrun_1920x1088x50x420x500.avi      -l  1  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50

salta zero_crowdrun_5TRL_1L
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  1  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50

### 4 ##########################################################################
salta crowdrun_5TRL_4L
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  crowdrun_1920x1088x50x420x500.avi      -l  4  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50

salta zero_crowdrun_5TRL_4L
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  4  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50



exit 0
