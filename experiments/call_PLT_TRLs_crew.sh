# DR_CURVE.SH
#//////////////

				
function salta {
	cd /home/cmaturana/scratch
	rm -rf $1
	mkdir $1
	cd $1
}
#/- crew ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

### 1 ##########################################################################
salta crew_1TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  crew_704x576x60x420x600.avi           -l  8  -g  9  -t  5  -b  32  -m  32  -y  576  -x  704 -f 60

salta zero_crew_1TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -g  9  -t  5  -b  32  -m  32  -y  576  -x  704 -f 60

### 2 ##########################################################################
salta crew_2TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  crew_704x576x60x420x600.avi           -l  8  -g  9  -t  5  -b  32  -m  32  -y  576  -x  704 -f 60

salta zero_crew_2TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -g  9  -t  5  -b  32  -m  32  -y  576  -x  704 -f 60

### 3 ##########################################################################
salta crew_3TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  crew_704x576x60x420x600.avi           -l  8  -g  9  -t  5  -b  32  -m  32  -y  576  -x  704 -f 60

salta zero_crew_3TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -g  9  -t  5  -b  32  -m  32  -y  576  -x  704 -f 60

### 4 ##########################################################################
salta crew_4TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  crew_704x576x60x420x600.avi           -l  8  -g  9  -t  5  -b  32  -m  32  -y  576  -x  704 -f 60

salta zero_crew_4TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -g  9  -t  5  -b  32  -m  32  -y  576  -x  704 -f 60

### 5 ##########################################################################
salta crew_5TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  crew_704x576x60x420x600.avi           -l  8  -g  9  -t  5  -b  32  -m  32  -y  576  -x  704 -f 60

salta zero_crew_5TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -g  9  -t  5  -b  32  -m  32  -y  576  -x  704 -f 60

### 6 ##########################################################################
salta crew_6TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  crew_704x576x60x420x600.avi           -l  8  -g  9  -t  5  -b  32  -m  32  -y  576  -x  704 -f 60

salta zero_crew_6TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -g  9  -t  5  -b  32  -m  32  -y  576  -x  704 -f 60

### 7 ##########################################################################
salta crew_7TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  crew_704x576x60x420x600.avi           -l  8  -g  9  -t  5  -b  32  -m  32  -y  576  -x  704 -f 60

salta zero_crew_7TRL
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  8  -g  9  -t  5  -b  32  -m  32  -y  576  -x  704 -f 60


   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### 
   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #

### 1 ##########################################################################
salta crew_5TRL_1L
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  crew_704x576x60x420x600.avi           -l  1  -g  9  -t  5  -b  32  -m  32  -y  576  -x  704 -f 60

salta zero_crew_5TRL_1L
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  1  -g  9  -t  5  -b  32  -m  32  -y  576  -x  704 -f 60

### 4 ##########################################################################
salta crew_5TRL_4L
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  crew_704x576x60x420x600.avi           -l  4  -g  9  -t  5  -b  32  -m  32  -y  576  -x  704 -f 60

salta zero_crew_5TRL_4L
srun -N 1 -n 1 -p ibmulticore ../DRcurve.sh   -v  zero.yuv.avi                         -l  4  -g  9  -t  5  -b  32  -m  32  -y  576  -x  704 -f 60



exit 0
