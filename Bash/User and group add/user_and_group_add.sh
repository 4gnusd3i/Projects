#!/bin/bash

<<COMMENT
This script takes 4 arguments from the user in order to create a usergroup
with a specified groupid, before creating new users from a textfile and
assigning them a specified shell and a default password.

@Author: 4gnusd3i
@License: MIT
COMMENT

# Arguments
groupname=$1
groupid=$2
userfile=$3
usershell=$4

# Password scheme is username$number
number="1234"

# Helptext for user
helptext()
{
	printf "Usage: ./script.sh arg1 arg2 arg3 arg4
	arg1 = The name you want for the user group
	arg2 = The ID you want for the user group
	arg3 = The file with a list of usernames
	arg4 = The shelltype you would like to assign users\n"
}

# Error message for user
error()
{
	printf "Something went wrong, please read the error message!\n"
}

# Tests for -h as first argument and that checks that all arguments are present
if [ "$1" == "-h" ]
then
	helptext
	exit 0
elif  [ "$1" == "" ] || [ "$2" == "" ] || [ "$3" == "" ] || [ "$4" == "" ]
then
	printf "Missing arguments!\n"
	helptext
	exit 1
fi

# Creation of group with specified groupid
groupadd $groupname -g $groupid
if [ $? != 0 ]
then
	error
	exit 1
fi
printf "Created usergroup $groupname with the group id $groupid\n\n"


# Creation of users from file and create default password
for user in $( cat $userfile )
do
	useradd -N -g "$groupid" -m -s "$shell" "$user"
	if [ $? -eq 0 ]
	then
		printf "User $user was created!\n"
		printf $user:"$user$number" | chpasswd
		if [ $? -eq 0 ]
		then
			printf "Created password for $user: $user$number\n"
		else
			echo "Something went wrong while creating a password!"
			exit 1
		fi
	else
		echo "Something went wrong while creating a user!"
		exit 1
	fi
done

# Counts number of users in userfile and prints
number_users=$( wc -l $userfile | awk '{ print $1 }')
printf "\n$number_users users were created!\n"
