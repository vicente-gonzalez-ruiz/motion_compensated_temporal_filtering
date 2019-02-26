# DR_CURVE.SH
#//////////////

				
salta(){
	cd /home/cmaturana/scratch
	rm -rf $1
	mkdir $1
	cd $1
}
#/- crowdrun ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


### 6 ##########################################################################
salta crowdrun_6TRL
srun -N 1 -n 1 -p iball ../DRcurve.sh  -v  crowdrun_1920x1088x50x420x500.avi      -l  8  -b  64  -m  64  -g  5  -t  6  -y  1088  -x  1920  -f  50

salta zero_crowdrun_6TRL
srun -N 1 -n 1 -p iball ../DRcurve.sh   -v  zero.yuv.avi                          -l  8  -b  64  -m  64  -g  5  -t  6  -y  1088  -x  1920  -f  50

### 7 ##########################################################################
salta crowdrun_7TRL
srun -N 1 -n 1 -p iball ../DRcurve.sh  -v  crowdrun_1920x1088x50x420x500.avi      -l  8  -b  64  -m  64  -g  3  -t  7  -y  1088  -x  1920  -f  50

salta zero_crowdrun_7TRL
srun -N 1 -n 1 -p iball ../DRcurve.sh   -v  zero.yuv.avi                          -l  8  -b  64  -m  64  -g  3  -t  7  -y  1088  -x  1920  -f  50



   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #

### 1 ##########################################################################
salta crowdrun_5TRL_1L
srun -N 1 -n 1 -p iball ../DRcurve.sh   -v  crowdrun_1920x1088x50x420x500.avi     -l  1  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50

salta zero_crowdrun_5TRL_1L
srun -N 1 -n 1 -p iball ../DRcurve.sh   -v  zero.yuv.avi                          -l  1  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50

### 4 ##########################################################################
salta crowdrun_5TRL_4L
srun -N 1 -n 1 -p iball ../DRcurve.sh   -v  crowdrun_1920x1088x50x420x500.avi     -l  4  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50

salta zero_crowdrun_5TRL_4L
srun -N 1 -n 1 -p iball ../DRcurve.sh   -v  zero.yuv.avi                          -l  4  -b  64  -m  64  -g  9  -t  5  -y  1088  -x  1920  -f  50



exit 0
