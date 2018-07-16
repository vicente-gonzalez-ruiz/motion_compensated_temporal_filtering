#!/bin/bash

video_dir=~/Videos
video=$video_dir/container_352x288x30x420x300.avi
# ffmpeg -t 10 -s 352x288 -f rawvideo -pix_fmt rgb24 -r 30 -i /dev/zero ~/Videos/zero_352x288x30x420x300.avi
#video=~/Videos/zero_352x288x30x420x300.avi
GOPs=2
TRLs=5
y_dim=288
x_dim=352
FPS=30
layers=8  # Be careful, unable to handle more than 10 quality layers
	  # (reason: kdu_compress's output format)
slope=43000

__debug__=0
BPP=8
MCTF_QUANTIZER=automatic

usage() {
    echo $0
    echo "  [-v video file name ($video)]"
    echo "  [-g GOPs ($GOPs)]"
    echo "  [-x X dimension ($x_dim)]"
    echo "  [-y Y dimension ($y_dim)]"
    echo "  [-f frames/second ($FPS)]"
    echo "  [-t TRLs ($TRLs)]"
    echo "  [-l layers ($layers)"
    echo "  [-s slope ($slope)]"
    echo "  [-? (help)]"
}

while getopts "v:p:x:y:f:t:g:l:s:?" opt; do
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
            layers="${OPTARG}"
	    echo layers=$layers
            ;;
	s)
	    slope="${OPTARG}"
	    echo slope=$slope
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

if [ $BPP -eq 16 ]; then

    RAWTOPGM () {
	local input_image=$1
	local x_dim=$2
	local y_dim=$3
	local output_image=$4
	(uchar2ushort < $input_image > tmp_1) 2> /dev/null
	rawtopgm -bpp 2 $x_dim $y_dim < tmp_1 > $output_image
	rm tmp_1
    }

    PGMTORAW () {
	local input_image=$1
	local output_image=$2
	convert -endian MSB $input_image tmp_1.gray
	(ushort2uchar < tmp_1.gray > $output_image) 2> /dev/null
	rm tmp_1.gray
    }
    
else

    RAWTOPGM () {
	local input_image=$1
	local x_dim=$2
	local y_dim=$3
	local output_image=$4
	rawtopgm $x_dim $y_dim < $input_image > $output_image
    }

    PGMTORAW () {
	local input_image=$1
	local output_image=$2
	convert $input_image tmp_1.gray
	mv tmp_1.gray $output_image
    }
    
fi

if [ $__debug__ -eq 1 ]; then
    set -x
fi

rm -rf L_0
mkdir L_0
number_of_images=`echo "2^($TRLs-1)*($GOPs-1)+1" | bc`
(ffmpeg -i $video -c:v rawvideo -pix_fmt yuv420p -vframes $number_of_images L_0/%4d.Y) > /dev/null 2> /dev/null
x_dim_2=`echo $x_dim/2 | bc`
y_dim_2=`echo $y_dim/2 | bc`
img=1
while [ $img -le $number_of_images ]; do
    _img=$(printf "%04d" $img)
    let img_1=img-1
    _img_1=$(printf "%04d" $img_1)

    input=L_0/$_img.Y
    output=L_0/${_img_1}_0.pgm
    RAWTOPGM $input $x_dim $y_dim $output

    input=L_0/$_img.U
    output=L_0/${_img_1}_1.pgm
    RAWTOPGM $input $x_dim_2 $y_dim_2 $output    
    
    input=L_0/$_img.V
    output=L_0/${_img_1}_2.pgm
    RAWTOPGM $input $x_dim_2 $y_dim_2 $output
    let img=img+1 
done

mctf compress --GOPs=$GOPs --TRLs=$TRLs --slope=$slope --layers=$layers
mctf info --GOPs=$GOPs --TRLs=$TRLs

name=${video}_${GOPs}_${TRLs}_${y_dim}_${x_dim}_${FPS}_${layers}_${slope}_${BPP}_${MCTF_QUANTIZER}_DRcurve.dat
echo Generating $name
rm -f $name

echo \# video=$video >> $name
echo \# GOPs=$GOPs >> $name
echo \# TRLs=$TRLs >> $name
echo \# y_dim=$y_dim >> $name
echo \# x_dim=$x_dim >> $name
echo \# FPS=$FPS >> $name
echo \# layers=$layers >> $name
echo \# slope=$slope >> $name
echo \# BPP=$BPP >> $name
echo \# MCTF_QUANTIZER=$MCTF_QUANTIZER >> $name

subband_layers=`echo $layers*$TRLs | bc`
for i in `seq 1 $subband_layers`; do
    echo Running for $i quality layers
    mkdir transcode_quality
    mctf transcode_quality --GOPs=$GOPs --TRLs=$TRLs --keep_layers=$i \
	 --destination="transcode_quality" --layers=$layers --slope=$slope
    cd transcode_quality
    mctf create_zero_texture --pixels_in_y=$y_dim --pixels_in_x=$x_dim
    rate=`mctf info --GOPs=$GOPs --TRLs=$TRLs --FPS=$FPS | grep "rate" | cut -d " " -f 5`
    echo -n $rate >> $name
    echo -ne '\t' >> $name
    mctf expand --GOPs=$GOPs --TRLs=$TRLs
    img=1
    while [ $img -le $number_of_images ]; do
	_img=$(printf "%04d" $img)
	let img_1=img-1
	_img_1=$(printf "%04d" $img_1)
    
	input=L_0/${_img_1}_0.pgm
	output=L_0/$_img.Y
	PGMTORAW $input $output
    
	input=L_0/${_img_1}_1.pgm
	output=L_0/$_img.U
	PGMTORAW $input $output
    
	input=L_0/${_img_1}_2.pgm
	output=L_0/$_img.V
	PGMTORAW $input $output

	let img=img+1 
    done

    RMSE=`mctf psnr --file_A L_0 --file_B ../L_0 --pixels_in_x=$x_dim --pixels_in_y=$y_dim --GOPs=$GOPs --TRLs=$TRLs`
    echo -n $RMSE >> $name
    echo -ne '\n' >> $name

    if [ $__debug__ -eq 1 ]; then
	
	(ffmpeg -y -s ${x_dim}x${y_dim} -pix_fmt yuv420p -i L_0/%4d.Y tmp_out.yuv) > /dev/null 2> /dev/null
	(mplayer tmp_out.yuv -demuxer rawvideo -rawvideo w=$x_dim:h=$y_dim -loop 0 -fps $FPS) > /dev/null 2> /dev/null
	
    fi
    
    cd ..
    rm -rf transcode_quality
done

if [ $__debug__ -eq 1 ]; then
    set +x
fi

