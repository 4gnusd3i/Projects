# Autobackup
This is a specialized script I made to be run from a crontab. It was made to take a backup
of the /home directory. The backup would be archived and compressed before beeing encrypted by gpg with predefined usercredentials. The encrypted backup would then be transfered to another client on the network with predefineds ssh credentials. Since this script would be run as cronjob, it would
also search for backups older than 7 days. All of the above actions would be logged.

This script will not work without modifications to suit your specifications!
It also requires GPG and SSH to be fully configured before use!
