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
mv ~/get_files.sh /usr/local/hadoop/sbin
mv ~/time.sh /usr/local/hadoop/sbin
mv ~/experiment_files.txt /usr/local/hadoop/sbin
mv ~/WordCount.java /usr/local/hadoop/sbin

# Retrieving files and running hadoop 
(cd /usr/local/hadoop/sbin/ ; bash get_files.sh)
echo "######### Start Hadoop #########"
(cd /usr/local/hadoop/sbin/ ; bash time.sh)
echo -e "\nIf that failed, try running : \n"
echo -e "$              cd /usr/local/hadoop/sbin/ && bash <your_file>.sh \n"
