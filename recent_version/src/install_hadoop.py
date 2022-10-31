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


def hadoop_setup_commands():
    """
    This function sets up the environment for hadoop.
    """
    return """
#!/bin/bash
yes | sudo apt update
yes | sudo apt install default-jdk
wget https://downloads.apache.org/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz
tar -xzvf hadoop-3.3.1.tar.gz
rm hadoop-3.3.1.tar.gz
sudo mv hadoop-3.3.1 /usr/local/hadoop
link_to_java=$(readlink -f /usr/bin/java | sed "s:bin/java::")
echo "export JAVA_HOME=$link_to_java" >> /usr/local/hadoop/etc/hadoop/hadoop-env.sh
sed -i -e 's/\\r$//' config_hadoop_file.sh
chmod +x config_hadoop_file.sh
bash config_hadoop_file.sh
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


def install_hadoop(ip):
    """
    This function install hadoop on the selected instance.
    ip : the ip of the instance
    """
    # Setting Up SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_connect_with_retry(ssh, ip, 0)
    print("Connected through SSH!")

    # Installing Hadoop
    print("Installing Hadoop...")
    stdin, stdout, stderr = ssh.exec_command(hadoop_setup_commands())
    old_stdout = sys.stdout
    log_file = open("logfile.log", "w")
    print('env setup done \n stdout:', stdout.read(), file=log_file)
    log_file.close()
    print("Hadoop installed!")

    ssh.close()


print("\n############### Installing Hadoop ###############\n")

install_hadoop(ip)

print("Hadoop App Deployed On EC2 Instance!")
