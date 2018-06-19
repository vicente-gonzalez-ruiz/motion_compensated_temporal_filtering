#!/bin/bash

#video=~/Videos/mobile_352x288x30x420x300.avi
video=~/Videos/container_352x288x30x420x300.avi
#GOPs=9
#TRLs=2
GOPs=2
TRLs=6
y_dim=288
x_dim=352
FPS=30
keep_layers=8
slope=0
#slope=40000
slope=39000

usage() {
    echo $0
    echo "  [-v video file name ($video)]"
    echo "  [-g GOPs ($GOPs)]"
    echo "  [-x X dimension ($x_dim)]"
    echo "  [-y Y dimension ($y_dim)]"
    echo "  [-f frames/second ($FPS)]"
    echo "  [-t TRLs ($TRLs)]"
    echo "  [-k keep layers ($keep_layers)]"
    echo "  [-? xf(help)]"
}

(echo $0 $@ 1>&2)

while getopts "v:p:x:y:f:t:g:k:?" opt; do
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
	k)
	    keep_layers="${OPTARG}"
	    echo keep_layers=$keep_layers
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

MCTF_QUANTIZER=automatic

rm -rf L_0
mkdir L_0
number_of_images=`echo "2^($TRLs-1)*($GOPs-1)+1" | bc`
ffmpeg -i $video -c:v rawvideo -pix_fmt yuv420p -vframes $number_of_images L_0/%4d.Y
x_dim_2=`echo $x_dim/2 | bc`
y_dim_2=`echo $y_dim/2 | bc`
img=1
while [ $img -le $number_of_images ]; do
    _img=$(printf "%04d" $img)
    let img_1=img-1
    _img_1=$(printf "%04d" $img_1)
    (uchar2short < L_0/$_img.Y > /tmp/1) 2> /dev/null
    rawtopgm -bpp 2   $x_dim   $y_dim < /tmp/1 > L_0/${_img_1}_0.pgm
    (uchar2short < L_0/$_img.U > /tmp/1) 2> /dev/null
    rawtopgm -bpp 2 $x_dim_2 $y_dim_2 < /tmp/1 > L_0/${_img_1}_1.pgm
    (uchar2short < L_0/$_img.V > /tmp/1) 2> /dev/null
    rawtopgm -bpp 2 $x_dim_2 $y_dim_2 < /tmp/1 > L_0/${_img_1}_2.pgm
    let img=img+1 
done

mctf create_zero_texture
mctf compress --GOPs=$GOPs --TRLs=$TRLs --slope=$slope
mctf info --GOPs=$GOPs --TRLs=$TRLs
mkdir tmp
mctf copy --GOPs=$GOPs --TRLs=$TRLs --destination="tmp"
cd tmp
mctf info --GOPs=$GOPs --TRLs=$TRLs
mctf expand --GOPs=$GOPs --TRLs=$TRLs
img=1
while [ $img -le $number_of_images ]; do
    _img=$(printf "%04d" $img)
    let img_1=img-1
    _img_1=$(printf "%04d" $img_1)
    convert -endian MSB L_0/${_img_1}_0.pgm /tmp/1.gray
    (short2uchar < /tmp/1.gray > L_0/$_img.Y) 2> /dev/null
    convert -endian MSB L_0/${_img_1}_1.pgm /tmp/1.gray
    (short2uchar < /tmp/1.gray > L_0/$_img.U) 2> /dev/null
    convert -endian MSB L_0/${_img_1}_2.pgm /tmp/1.gray
    (short2uchar < /tmp/1.gray > L_0/$_img.V) 2> /dev/null
    let img=img+1 
done
ffmpeg -y -s ${x_dim}x${y_dim} -pix_fmt yuv420p -i L_0/%4d.Y /tmp/out.yuv
mplayer /tmp/out.yuv -demuxer rawvideo -rawvideo w=$x_dim:h=$y_dim -loop 0 -fps $FPS
exit
mkdir transcode_quality
mctf copy --GOPs=$GOPs --TRLs=$TRLs --destination="transcode_quality"
mctf transcode_quality --GOPs=$GOPs --TRLs=$TRLs --keep_layers=$keep_layers
cd transcode_quality
mctf info --GOPs=$GOPs --TRLs=$TRLs
mctf expand --GOPs=$GOPs --TRLs=$TRLs

img=1
while [ $img -le $number_of_images ]; do
    _img=$(printf "%04d" $img)
    let img_1=img-1
    _img_1=$(printf "%04d" $img_1)
    cp L_0/${_img_1}_0.pgm L_0/$_img.Y
    cp L_0/${_img_1}_1.pgm L_0/$_img.U
    cp L_0/${_img_1}_2.pgm L_0/$_img.V
    let img=img+1 
done
ffmpeg -y -s ${x_dim}x${y_dim} -pix_fmt yuv420p -i L_0/%4d.Y /tmp/out.yuv
mplayer /tmp/out.yuv -demuxer rawvideo -rawvideo w=$x_dim:h=$y_dim -loop 0 -fps $FPS

