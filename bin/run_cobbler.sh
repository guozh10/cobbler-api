#!/bin/bash
####################################################
##########start configure cobbler ##################
####################################################

DIR=$(cd `dirname $0`; cd ../;pwd)
run="$DIR/main.py"
sta=$1
sum=$2
netmask=$3
gateway=$4
profile=$5
####################ip address write "bin/host" file#####################################
if [ "$sta"  == "start" ] ;then
   if [ -e $run ];then
      echo "zhaodao $run"
      python $run  $sum  $netmask $gateway $profile
   else
      echo "not file  $run"
   fi

elif [ "$sta" == "help" ]  ;then
   echo "configure host IP and ./bin/host"
   echo "./bin/run_cobbler.sh start 2  255.255.255.0 192.168.100.254 Centos-7.5-x86_64"
fi 

