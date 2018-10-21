#!/bin/bash

# log.info("output = {}".format(out))

video="mobile_352x288x30x420x300"
GOPs=2
TRLs=4
y_dim=288
x_dim=352
FPS=30
layers=8    # Be careful, unable to handle more than 10 quality layers
	        # (reason: kdu_compress's output format)
keep_layers=8
slope=43000
block_size=16
search_range=4


# Transcode algorithm.
export TRANSCODE_QUALITY="transcode_quality_FSO" # "transcode_quality_PLT"


__debug__=1
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
    echo "  [-l layers ($layers)]"
    echo "  [-k keep layers ($keep_layers)]"
    echo "  [-s slope ($slope)]"
    echo "  [-b block_size ($block_size)]"
    echo "  [-r search_range ($search_range)]"
    echo "  [-? (help)]"
}

(echo $0 $@ 1>&2)

while getopts "v:p:x:y:f:t:g:l:k:s:b:r:?" opt; do
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
	k)
	    keep_layers="${OPTARG}"
	    echo keep_layers=$keep_layers
	    ;;
	s)
	    slope="${OPTARG}"
	    echo slope=$slope
	    ;;
	b)
	    block_size="${OPTARG}"
	    echo block_size=$block_size
	    ;;
	r)
	    search_range="${OPTARG}"
	    echo search_range=$search_range
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

dir="L"$layers"_T"$TRLs"_BS"$block_size"_SR"$search_range"_G"$GOPs"_"$video
rm -rf $dir; mkdir $dir; cd $dir
video="/nfs/cmaturana/Videos/"$video


if [ $BPP -eq 16 ]; then

    RAWTOPGM () {
	local input_image=$1
	local x_dim=$2
	local y_dim=$3
	local output_image=$4
	(uchar2ushort < $input_image > /tmp/1) 2> /dev/null
	rawtopgm -bpp 2 $x_dim $y_dim < /tmp/1 > $output_image
    }

    PGMTORAW () {
	local input_image=$1
	local output_image=$2
	convert -endian MSB $input_image /tmp/1.gray
	(ushort2uchar < /tmp/1.gray > $output_image) 2> /dev/null
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
	convert $input_image /tmp/1.gray
	mv /tmp/1.gray $output_image
    }
    
fi


# ============================================================================== PGM RAW
IMG_YUV() {
    img=1
    while [ $img -le $number_of_images ]; do
        _img=$(printf "%04d" $img)
        img_1=$((img-1))
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
        img=$((img+1))
    done
}



if [ $__debug__ -eq 1 ]; then
    set -x
    set -e
    set -o errexit
fi

# ============================================================================== COMPRESS PGM RAW original
rm -rf L_0
mkdir L_0
number_of_images=`echo "2^($TRLs-1)*($GOPs-1)+1" | bc`
if [ $__debug__ -eq 1 ]; then
   ffmpeg -i $video -c:v rawvideo -pix_fmt yuv420p -vframes $number_of_images L_0/%4d.Y
fi
(ffmpeg -i $video -c:v rawvideo -pix_fmt yuv420p -vframes $number_of_images L_0/%4d.Y) > /dev/null 2> /dev/null

x_dim_2=`echo $x_dim/2 | bc`
y_dim_2=`echo $y_dim/2 | bc`
IMG_YUV


mctf compress --GOPs=$GOPs --TRLs=$TRLs --slope=$slope --layers=$layers --block_size=$block_size --search_range=$search_range --pixels_in_y=$y_dim --pixels_in_x=$x_dim
mctf info --GOPs=$GOPs --TRLs=$TRLs --FPS=$FPS

# ============================================================================== CREATE ZERO TEXTURE TO KBPS HEADERS CALCULATION
mkdir zero_texture
cd zero_texture

x_dim_video=`echo $x_dim*$number_of_images*1.5/1 | bc`
mctf create_zero_texture --file=zero.yuv --pixels_in_y=$y_dim --pixels_in_x=$x_dim_video    # zero.yuv
x264 --input-res $x_dim"x"$y_dim --qp 0 -o zero.yuv.avi zero.yuv                            # .yuv to .avi

rm -rf L_0
mkdir L_0
if [ $__debug__ -eq 1 ]; then
    ffmpeg -i zero.yuv.avi -c:v rawvideo -pix_fmt yuv420p -vframes $number_of_images L_0/%4d.Y
fi
(ffmpeg -i zero.yuv.avi -c:v rawvideo -pix_fmt yuv420p -vframes $number_of_images L_0/%4d.Y) > /dev/null 2> /dev/null

IMG_YUV

#mctf create_zero_texture  --pixels_in_y=$y_dim --pixels_in_x=$x_dim
mctf compress --GOPs=$GOPs --TRLs=$TRLs --slope=$slope --layers=$layers --block_size=$block_size --search_range=$search_range --pixels_in_y=$y_dim --pixels_in_x=$x_dim
cd ..

# ============================================================================== TRANSCODE
mkdir transcode_quality
mctf $TRANSCODE_QUALITY --GOPs=$GOPs --TRLs=$TRLs --keep_layers=$keep_layers --destination="transcode_quality" --layers=$layers --slope=$slope --FPS=$FPS --pixels_in_y=$y_dim --pixels_in_x=$x_dim --video=$video --block_size=$block_size --search_range=$search_range

if [ $__debug__ -eq 1 ]; then
    set +x
fi

exit 0 # Jse




##read -n1 -r -p "Press any key to continue..." key


<<comment
# ============================================================================== EXPAND PGM RAW original
mkdir tmp
mctf copy --GOPs=$GOPs --TRLs=$TRLs --destination="tmp"
cd tmp
mctf info --GOPs=$GOPs --TRLs=$TRLs --FPS=$FPS
mctf expand --GOPs=$GOPs --TRLs=$TRLs --block_size=$block_size --search_range=$search_range --pixels_in_y=$y_dim --pixels_in_x=$x_dim

img=1
while [ $img -le $number_of_images ]; do
    _img=$(printf "%04d" $img)
    img_1=$((img-1))
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

    img=$((img+1))
done
mctf psnr --file_A L_0 --file_B ../L_0 --pixels_in_x=$x_dim --pixels_in_y=$y_dim --GOPs=$GOPs --TRLs=$TRLs

(ffmpeg -y -s ${x_dim}x${y_dim} -pix_fmt yuv420p -i L_0/%4d.Y /tmp/out.yuv) > /dev/null 2> /dev/null || true
#(mplayer /tmp/out.yuv -demuxer rawvideo -rawvideo w=$x_dim:h=$y_dim -loop 0 -fps $FPS) > /dev/null 2> /dev/null || true






img=1
while [ $img -le $number_of_images ]; do
    _img=$(printf "%04d" $img)
    img_1=$((img-1))
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
    img=$((img+1))
done

comment


