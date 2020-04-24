#!/bin/bash

<<COMMENT
This script grabs the IP-address of the interface input from user. It uses this IP-address
to perfom a complete pingsweep of the last octet of the network. It then returns the IP-addresses
that respond to the echo-request.

@Author: 4gnusd3i
@License: MIT
COMMENT


if [ "$1" == "" ]
then
	printf "You need to specify which interface to get your IP from!\nSyntax: ./script.sh <interface>\n"
	exit 1
else
	printf "Using interface: $1\n"
fi


interface=$1

get_ip()
{
	ip=$(ip addr show $interface | awk '/inet/{print ($2)}' | awk 'FNR==1' \
		| grep -o '[0-9]\{0,3\}\.[0-9]\{0,3\}\.[0-9]\{0,3\}')
	if [ $? != 0 ]
	then
		exit 1
	fi
}


ping_ip()
{
	ping -c 2 $1 > /dev/null
	if [ $? == 0 ]
	then
		printf "IP-address: $i is in use\n"
	fi
}


get_ip

for i in $ip.{1..254}
do
	ping_ip $i &
done

wait
printf "Done!\n"
