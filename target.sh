#!/bin/bash

#unset tun0
export tun0=$(/scripts/showip.sh)

if [ -z "$1" ]
then
	#unset dir
	echo "Cannot set target \$ip, \$url, or \$urls"
	echo "Usage: target <target IP>"
	echo "Setting \$dir to $PWD and \$tun0 to $tun0"
	export dir=$PWD
else
	#unset dir
	#unset ip
	echo "Setting \$ip to $1 and \$tun0 to $tun0"
	echo "Setting \$url to http://$1 and \$urls to https://$1"
	echo "Setting \$dir to $PWD"
	export url=http://$1
	export urls=https://$1
	export ip=$1
	export dir=$PWD
fi


