#!/bin/bash

GOPs=2
TRLs=4
y_dim=288
x_dim=352


__debug__=0
BPP=8
MCTF_QUANTIZER=automatic

usage() {
    echo $0
    echo "  [-g GOPs ($GOPs)]"
    echo "  [-x X dimension ($x_dim)]"
    echo "  [-y Y dimension ($y_dim)]"
    echo "  [-t TRLs ($TRLs)]"
    echo "  [-? (help)]"
}

(echo $0 $@ 1>&2)

while getopts "v:p:x:y:f:t:g:l:k:s:?" opt; do
    case ${opt} in
	x)
	    x_dim="${OPTARG}"
	    echo x_dim=$x_dim
	    ;;
	y)
	    y_dim="${OPTARG}"
	    echo y_dim=$y_dim
	    ;;
	t)
	    TRLs="${OPTARG}"
	    echo TRLs=$TRLs
	    ;;
	g)
	    GOPs="${OPTARG}"
	    echo GOPs=$GOPs
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
	(uchar2ushort < $input_image > /tmp/1) 2> /dev/null
	#(add Short 32768 < /tmp/1 > /tmp/2) 2> /dev/null
	rawtopgm -bpp 2 $x_dim $y_dim < /tmp/1 > $output_image
    }

    PGMTORAW () {
	local input_image=$1
	local output_image=$2
	convert -endian MSB $input_image /tmp/1.gray
	#(add Short -32768 < /tmp/1.gray > /tmp/2) 2> /dev/null
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

# ----------------------------------------------

if [ $__debug__ -eq 1 ]; then
    set -x
fi

number_of_images=`echo "2^($TRLs-1)*($GOPs-1)+1" | bc`
echo "Number of images " $number_of_images

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

if [ $__debug__ -eq 1 ]; then
    set +x
fi

