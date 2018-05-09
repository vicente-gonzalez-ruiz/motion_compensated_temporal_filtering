#!/bin/bash

low_fn  = "low_0/"
even_fn = "even_1/"
odd_fn  = "odd_1/"
images  = 33

usage() {
    echo $0
    echo "Forward Lazzy wavelet transform over the time domain"
    echo "  [-e even images ($even)]"
    echo "  [-o odd images ($odd)]"
    echo "  [-l low images ($low)]"
    echo "  [-i images ($images)]"
    echo "  [-? (help)]"
}

(echo $0 $@ 1>&2)

while getopts "e:o:l:i:?" opt; do
    case ${opt} in
	e)
	    even="${OPTARG}"
	    echo even=$even
	    ;;
	o)
	    odd="${OPTARG}"
	    echo odd=$odd
	    ;;
	l)
	    low="${OPTARG}"
	    echo low=$low
	    ;;
	i)
	    images="${OPTARG}"
	    echo images=$images
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

ln -s ${even}"0000_Y" $low
ln -s ${even}"0000_U" $low
ln -s ${even}"0000_V" $low

image = 0
while [ $image -le ((images/2)) ]
do
    _odd=(($image*2+1))
    ln -s $odd$(printf "%04d_Y" $image) $low$(printf "%04d_Y" $_odd)
    ln -s $odd$(printf "%04d_U" $image) $low$(printf "%04d_U" $_odd)
    ln -s $odd$(printf "%04d_V" $image) $low$(printf "%04d_V" $_odd)

    _even=(($image*2+1))
    ln -s $even$(printf "%04d_Y" $image) $low$(printf "%04d_Y" $_even)
    ln -s $even$(printf "%04d_U" $image) $low$(printf "%04d_U" $_even)
    ln -s $even$(printf "%04d_V" $image) $low$(printf "%04d_V" $_even)

    ((image++))
done
