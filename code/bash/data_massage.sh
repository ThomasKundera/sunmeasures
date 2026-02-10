#!/bin/bash

export kBATCH="2025_08_22"
export kSIZE=2000

export INDATADIR="localdata/${kBATCH}"
export OUTDATADIR="data/${kBATCH}"

mkdir -p $OUTDATADIR/${kSIZE}_sun
mkdir -p "data/time_ref"

function do_resize() {
    src=$1
    dst=$2

    echo "For: $src to $dst"
    #rm -f $dst
    convert $src -resize ${kSIZE}x${kSIZE} $dst
    # Remove all exifs but for:
    # Body name
    # Lens focale
    # date
    exiftool -overwrite_original -all= -tagsfromfile @ -exif:Model -Exif:ExposureTime -Exif:FocalLength -Exif:DateTimeOriginal $dst
}

export -f do_resize

function picture_resize() {
    imgf=$1
    img=`basename $imgf`
    do_resize $imgf $OUTDATADIR/${kSIZE}_sun/$img
}

export -f picture_resize

function do_copy() {
    src=$1
    dst=$2

    echo "For: $src to $dst"
    #rm -f $dst
    cp -f $src $dst
    exiftool -overwrite_original -all= -tagsfromfile @ -exif:Model -Exif:ExposureTime -Exif:FocalLength -Exif:DateTimeOriginal $dst
}

export -f do_copy

function picture_copy() {
    imgf=$1
    img=`basename $imgf`
    do_copy $imgf "data/time_ref/$img"
}

export -f picture_copy

IMGLIST=`ls $INDATADIR/full_sun/*.JPG`

parallel picture_resize ::: $IMGLIST

IMGLIST=`ls $INDATADIR/time_ref/*.JPG`

parallel picture_copy ::: $IMGLIST
