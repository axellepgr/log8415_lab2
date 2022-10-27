#! /bin/bash

sed -i 's/# export JAVA_HOME=/export JAVA_HOME=\/usr\/lib\/jvm\/java-11-openjdk-amd64\//' /usr/local/hadoop/etc/hadoop/hadoop-env.sh
# install Java
sudo apt-get update
yes | sudo apt-get install openjdk-11-jdk
# Solving key problems
cd ~/.ssh
echo | ssh-keygen -P ''
cat id_rsa.pub >> authorized_keys
# start
cd /usr/local/hadoop/sbin
./start-dfs.sh
cd ~/.ssh
export HADOOP_INSTALL=/usr/local/hadoop && export PATH=$HADOOP_INSTALL/bin:$PATH
export PATH=$PATH:/usr/local/hadoop/bin/

mv ~/run_hadoop.sh /usr/local/hadoop/sbin
mv ~/WordCount.java /usr/local/hadoop/sbin
read -p "All good ? (y/n): " y
if [[ $y == 'y' ]]
then
        (cd /usr/local/hadoop/sbin/ ; sh run_hadoop.sh)
else
        echo "try running cd /usr/local/hadoop/sbin/ && sh run_hadoop.sh "
        exit 0
fi
echo -e "\nIf that failed, try running : \n"
echo -e "$              cd /usr/local/hadoop/sbin/ && sh run_hadoop.sh \n"