#!/bin/bash

## Builder
function build() {
  rm -rf /var/lib/virt-maker/providers/*
  cp /opt/virt-maker/providers/* /var/lib/virt-maker/providers/
  killall virt-builder
  killall virt-maker
  clear
  date
  echo ""
  echo ""
  echo ""
  sleep 7
  python /opt/virt-maker/virt-maker.py -f /opt/virt-maker/examples/from.vbp -b &
  sleep 1
}

clear
while [ 1 == 1 ]
do
  inotifywait -q -r -e create /opt/virt-maker/ && bash install
  #inotifywait -q -r -e create /opt/virt-maker/ && build
  #inotifywait -q -r -e modify,attrib,close_write,move,create,delete /opt/virt-maker/ && build
done