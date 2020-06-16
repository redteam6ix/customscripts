#!/bin/bash

if [ -z "$1" ]
  then
    echo "Usage: serve <port>"
  else
    cd /home/kali/server
    ls --color --sort=extension -R
    python3 -m http.server $1
fi

