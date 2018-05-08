#!/bin/bash

video=~/Videos/mobile_352x288x30x420x300.yuv
GOPs=9
TRLs=6
y_dim=288
x_dim=352
FPS=30
layers=8

usage() {
    echo $0
    echo "  [-v video file name ($video)]"
    echo "  [-g GOPs ($GOPs)]"
    echo "  [-x X dimension ($x_dim)]"
    echo "  [-y Y dimension ($y_dim)]"
    echo "  [-f frames/second ($FPS)]"
    echo "  [-t TRLs ($TRLs)]"
    echo "  [-l layers ($layers)"
    echo "  [-? (help)]"
}

while getopts "v:p:x:y:f:t:g:l:?" opt; do
    case ${opt} in
        v)
            video="${OPTARG}"
	    echo video=$video
            ;;
        x)
            x_dim="${OPTARG}"
	    echo x_dim=$x_dim
            ;;
        y)
            y_dim="${OPTARG}"
	    echo y_dim=$y_dim
            ;;
        f)
            FPS="${OPTARG}"
	    echo FPS=$FPS
            ;;
        t)
            TRLs="${OPTARG}"
	    echo TRLs=$TRLs
            ;;
	g)
            GOPs="${OPTARG}"
	    echo GOPs=$GOPs
            ;;
	l)
            LAYERS="${LAYERS}"
	    echo layers=$layers
            ;;
        ?)
            usage
            exit 0
            ;;
        \?)
            echo "Invalid option: -${OPTARG}" >&2
            usage
            exit 1
            ;;
        :)
            echo "Option -${OPTARG} requires an argument." >&2
            usage
            exit 1
            ;;
    esac
done

set -x

rm -f low_0
ln -s $video low_0
mctf compress --GOPs=$GOPs --TRLs=$TRLs --layers=$LAYERS
mctf info --GOPs=$GOPs --TRLs=$TRLs
subband_layers=`echo $LAYERS*$TRLs | bc`
rm -f DRcurve.dat

for i in `seq 1 $subband_layers`;
do
    echo Running for layers=$i
    mkdir transcode_quality
#    cp motion*.j2c transcode_quality
    cp *type* transcode_quality
    mctf transcode_quality --GOPs=$GOPs --TRLs=$TRLs --keep_layers=$i
    cd transcode_quality
    rate=`mctf info --GOPs=$GOPs --TRLs=$TRLs --FPS=$FPS | grep "rate" | cut -d " " -f 5`
    echo -n $rate >> ../DRcurve.dat
    echo -ne '\t'  >> ../DRcurve.dat
    mctf expand --GOPs=$GOPs --TRLs=$TRLs
    RMSE=`snr --file_A=../low_0 --file_B=low_0 2> /dev/null | grep RMSE | cut -f 3`
    echo -n $RMSE >> ../DRcurve.dat
    echo -ne '\t' >> ../DRcurve.dat
    cat ../layers.txt >> ../DRcurve.dat
    cd ..
    rm -rf transcode_quality
done
set +x
