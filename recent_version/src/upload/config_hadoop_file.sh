#! /bin/bash
cd ~/.ssh
echo | ssh-keygen -P ''
cat id_rsa.pub >> authorized_keys
cd ~
/usr/local/hadoop/sbin/start-dfs.sh
export PATH=$PATH:/usr/local/hadoop/bin