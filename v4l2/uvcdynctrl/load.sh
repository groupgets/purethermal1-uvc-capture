#!/bin/sh

device=${1:-/dev/video0}
xml=${2:-pt1.xml}

echo Loading control definition file $xml for $device
uvcdynctrl -d $device -i $xml -v
