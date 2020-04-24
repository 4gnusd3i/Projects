#!/bin/bash

<<COMMENT
This is a specialized script I made to be run from a crontab. It was made to take a backup
of the /home directory. The backup would be archived and compressed before beeing encrypted by gpg with predefined usercredentials. The encrypted backup would then be transfered to another client on the network with predefineds ssh credentials. Since this script would be run as cronjob, it would
also search for backups older than 7 days. All of the above actions would be logged.

@Author: 4gnusd3i
@License: MIT
COMMENT

# Variables
LOG="/home/<USER>/Scripts/autobackup/backup.log"
BACKUP="/home/<USER>/Scripts/autobackup/backup_$( date +%d.%m.%Y-%H:%M ).tar.bz2"
EXCLUDE="/home/<USER>/Script/autobackup"
REMOTE="<REMOTE_USER>@<REMOTE_IP>:/home/<REMOTE_USER>/remote_backup"

date &>> $LOG
tar -cjvf $BACKUP --exclude=$EXCLUDE --ignore-failed-read /home &>> $LOG
gpg -e -r "<GPG_USER>" --batch --yes $BACKUP &>> $LOG
rsync -avh -e ssh "$BACKUP.gpg" $REMOTE &>> $LOG
find $EXCLUDE -type f -name '*.tar.*' -mtime +7 -exec rm -v {} \; &>> $LOG
printf "\t\tBackup completed\n" &>> $LOG
