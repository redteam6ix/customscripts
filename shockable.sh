if [ -z "$1" ]
then
	echo "Usage: shockable <url>/<cgi-path>/"
else
	wfuzz -c -z file,/usr/share/wordlists/words-big.txt --hc 404,403 $1FUZZ.cgi
	wfuzz -c -z file,/usr/share/wordlists/words-big.txt --hc 404,403 $1FUZZ.sh
	wfuzz -c -z file,/usr/share/wordlists/dir-med.txt --hc 404,403 $1FUZZ.cgi
	wfuzz -c -z file,/usr/share/wordlists/dir-med.txt --hc 404,403 $1FUZZ.sh
fi

