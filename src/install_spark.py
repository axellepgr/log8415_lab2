import paramiko
import time
import sys
import json

AWS_REGION = 'us-east-1'
DESTINATION_PATH = '~'


with open('collected_data.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)
    openfile.close()

ip = json_object["ip"]


def spark_setup_commands():
    """
    This function sets up the environment for spark.
    """
    return """
#!/bin/bash
sudo apt install curl mlocate git scala -y
wget https://dlcdn.apache.org/spark/spark-3.3.1/spark-3.3.1-bin-hadoop3.tgz
tar xvf spark-3.3.1-bin-hadoop3.tgz
rm spark-3.3.1-bin-hadoop3.tgz
sudo mv spark-3.3.1-bin-hadoop3 /usr/local/spark
sed -i -e 's/\\r$//' config_spark_file.sh
chmod +x config_spark_file.sh
cat config_spark_file.sh >> ~/.bashrc
source ~/.bashrc
source ~/.bashrc
cp /usr/local/spark/conf/log4j2.properties.template /usr/local/spark/conf/log4j2.properties
sed -i 's/rootLogger.level = info/rootLogger.level = warn/g' /usr/local/spark/conf/log4j2.properties
EOF
"""


def ssh_connect_with_retry(ssh, ip_address, retries):
    """
    This function connects via ssh on the instance.
    ssh : ssh
    ip_address : the ip address of the instance
    retries : the number of tries before it fails.
    """
    if retries > 3:
        return False
    privkey = paramiko.RSAKey.from_private_key_file(
        'labsuser.pem')
    interval = 2
    try:
        retries += 1
        print('SSH into the instance: {}'.format(ip_address))
        ssh.connect(hostname=ip_address,
                    username="ubuntu", pkey=privkey)
        return True
    except Exception as e:
        print(e)
        time.sleep(interval)
        print('Retrying SSH connection to {}'.format(ip_address))
        ssh_connect_with_retry(ssh, ip_address, retries)


def install_spark(ip):
    """
    This function install spark on the selected instance.
    ip : the ip of the instance
    """
    # Setting Up SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_connect_with_retry(ssh, ip, 0)
    print("Connected through SSH!")

    stdin, stdout, stderr = ssh.exec_command(spark_setup_commands())
    old_stdout = sys.stdout
    log_file = open("logfile.log", "w")
    print('env setup done \n stdout:', stdout.read(), file=log_file)
    log_file.close()
    print("Spark installed!")

    ssh.close()


print("\n############### Installing Spark ###############\n")

install_spark(ip)

print("Spark App Deployed On EC2 Instance!")
