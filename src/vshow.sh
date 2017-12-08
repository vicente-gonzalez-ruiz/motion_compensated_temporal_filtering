#!/bin/bash

fps=30
height=288
video="low_0"
width=352

usage() {
    echo $0
    echo "Shows a RAW YUV video."
    echo "  [-f (FPS, \"$fps\" by default)]"
    echo "  [-h (height, \"$height\" by default)]"
    echo "  [-v (video, \"$video\" by default)]"
    echo "  [-w (width, \"$width\" by default)]"
    echo "  [-? (help)]"
}

echo $0: parsing: $@

while getopts "h:v:w:?" opt; do
    case ${opt} in
	f)
            fps="${OPTARG}"
            ;;
	h)
            height="${OPTARG}"
            ;;
	w)
            width="${OPTARG}"
            ;;
	v)
	    video="${OPTARG}"
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
    esac
done

echo "Showing" $video

set -x
mplayer $video -demuxer rawvideo -rawvideo w=$width:h=$height -loop 0 -fps $fps > /dev/null 2> /dev/null &
set +x
