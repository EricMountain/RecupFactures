#!/bin/bash

#set -x

cd `dirname $0`

. ../data/env

case $1 in
    Ameli|FranceTelecom)
        (./$1.py 2>&1 | mail -s "Relevé $1" $AmeliAndFT_RECIPIENTS) &
        ;;
    ScolInfo)
        #(./$1.py 2>&1 | mail -s "Scolinfo $1" $ScolInfo_RECIPIENTS) &
        ./$1.py
        ;;
    *)
        echo "$1 not supported, check `pwd`/$0" | mail -s "Relevé $1 not supported" $Error_RECIPIENTS
esac
