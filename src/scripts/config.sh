sed -i 's/# export JAVA_HOME=/export JAVA_HOME=\/usr\/lib\/jvm\/java-11-openjdk-amd64\//' /usr/local/hadoop/etc/hadoop/hadoop-env.sh
cd /usr/local/hadoop/sbin
# install Java, maybe no need ?
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
mv ~/time.sh /usr/local/hadoop/sbin
mv ~/WordCount.java /usr/local/hadoop/sbin
(cd /usr/local/hadoop/sbin/ ; sh run_hadoop.sh)