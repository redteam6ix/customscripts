#!/bin/sh

###########################################################
#### an application list parser                        ####
#### need to have searchsploit installed               ####
#### but if you dont, why are you even using this?     ####
#### good to see if any installed apps are vulnerable  ####
#### set to not show whitepapers etc.                  ####
####                                                   ####
#### --iamgroot                                        ####
###########################################################

#### show usage and check for min 1 arg
if [ -z $1 ]
then
	echo "Usage: $0 <apps file> [<distro>] [<exploit type>]"
	echo ""
	echo "Distros:"
	echo "        0    -    automatic best guess (default)"
	echo "        1    -    debian"
	echo "        2    -    redhat"
	echo ""
	echo "Exploit Types:"
	echo "        0    -    local exploits (default)"
	echo "        1    -    remote exploits"
	echo "        2    -    both local and remote"
	echo "        3    -    all, including dos and webapps"
	exit 0
fi

#### declare variables and assign args to vars
if [ -z $2 ]
then
	distro=0
else
	distro=$2
fi

if [ -z $3 ]
then
	type=0
else
	type=$3
fi

if [ "$distro" = "1" ]
then
	echo "distro set to debian..."
elif [ "$distro" = "2" ]
then
	echo "distro set to redhat..."
else 
	echo "distro unspecified, will try to guess..."
	distro=0
fi

if [ "$type" = "1" ]
then
	echo "showing only remote exploits..."
	filter='grep /remote/|grep -iv kernel|grep -iv "windows/"|grep -iv "macos/"'
elif [ "$type" = "2" ]
then
	echo "showing both local and remote exploits..."
	filter='grep "/remote/\|/local/"|grep -iv kernel|grep -iv "windows/"|grep -iv "macos/"'
elif [ "$type" = "3" ]
then
	echo "showing all exploits including dos and webapps..."
	filter='grep "/remote/\|/local/\|/dos/\|/webapps/"|grep -iv kernel|grep -iv "windows/"|grep -iv "macos/"'
else
	echo "showing only local exploits..."
	filter='grep /local/|grep -iv kernel|grep -iv "windows/"|grep -iv "macos/"'
fi

#### guess distro
if [ "$distro" = "0" ]
then
	if grep -q "^ii  " $1
	then
		echo "debian guessed..."
		distro=1
	else
		echo "redhat guessed..."
		distro=2
	fi
fi

echo $distro
echo $type
echo $filter

#### draw headers
echo ""
searchsploit 11111 | head -n 3

#### debian parse
if [ "$distro" = "1" ]
then
	while read -r i
	do
		app=$(echo $i | tr -s ' ' | cut -f 2 -d ' '| sed 's/-/ /g' | sed 's/:/ /g') 
		ver=$(echo $i | tr -s ' ' | cut -f 3 -d ' '| cut -f 1 -d '-'| cut -f 1 -d '+'| cut -f 1-2 -d '.') # less precise, to increase precision remove | cut -f 1-2 -d '.'
		echo "searching for $app $ver..."
		if (searchsploit $app $ver | eval $filter | grep -is "$app")
		then
			echo ""
		else
			echo -n "\r\033[1A\033[0K"
		fi
	done < $1
fi

#### redhat parse
if [ "$distro" = "2" ]
then
	while read -r i
	do
		app=$(echo $i | rev | cut -f 3- -d '-' | rev | sed 's/-/ /g' | sed 's/:/ /g') 
		ver=$(echo $i | rev | cut -f 2 -d '-' | rev | cut -f 1 -d '+'| cut -f 1-2 -d '.') # less precise, to increase precision remove | cut -f 1-2 -d '.'
		echo "searching for $app $ver..."
		if (searchsploit $app $ver | eval $filter | grep -is "$app")
		then
			echo ""
		else
			echo -n "\r\033[1A\033[0K"
		fi
	done < $1	
fi
echo ""
echo "Script complete"
