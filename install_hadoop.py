import paramiko
import time
import sys
import boto3

AWS_REGION = 'us-east-1'


def envsetup(instanceID):
    str_instanceID = str(instanceID)
    return """
#!/bin/bash
yes | sudo apt update
yes | sudo apt install default-jdk
wget https://downloads.apache.org/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz
tar -xzvf hadoop-3.3.1.tar.gz
sudo mv hadoop-3.3.1 /usr/local/hadoop
readlink -f /usr/bin/java | sed "s:bin/java::"
mkdir input
cd input
curl https://www.gutenberg.org/cache/epub/4300/pg4300.txt > pg4300.txt
sudo mv input /usr/local/hadoop/hdfs/input
EOF
"""

'''
cd /usr/local/hadoop/sbin/start-all.sh
export JAVA_HOME=/home/sagar/Downloads/jdk1.8.0_311
deploy = """
sudo adduser hdoopTP
su - hdoopTP
wget https://downloads.apache.org/hadoop/common/hadoop-3.2.4/hadoop-3.2.4.tar.gz
tar xzf hadoop-3.2.1.tar.gz
"""
'''

def ssh_connect_with_retry(ssh, ip_address, retries):
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


def get_id_ips():
    ec2_client = boto3.client("ec2", region_name=AWS_REGION)
    reservations = ec2_client.describe_instances(Filters=[
        {
            "Name": "instance-state-name",
            "Values": ["running"],
        }
    ]).get("Reservations")
    ids = []
    print("Found the following instances: \n")
    for reservation in reservations:
        for instance in reservation["Instances"]:
            instance_id = instance["InstanceId"]
            instance_type = instance["InstanceType"]
            public_ip = instance["PublicIpAddress"]
            private_ip = instance["PrivateIpAddress"]
            ids.append((instance_id, public_ip))
            print(f"instance id :{instance_id}, instance type: {instance_type}, public ip:{public_ip}, private ip:{private_ip}")
    print("\n")
    return ids


def deploy_hadoop(id_ip, instance_nb):
    ip_address = id_ip[1]
    print(ip_address)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_connect_with_retry(ssh, ip_address, 0)
    print('this is id_ip[0]', id_ip[0])
    stdin, stdout, stderr = ssh.exec_command(envsetup(id_ip[0]))
    old_stdout = sys.stdout
    log_file = open("logfile.log", "w")
    print('env setup done \n stdout:', stdout.read(), file=log_file)
    log_file.close()
    #print('env setup done \n stdout:', stdout.read())
    #stdin, stdout, stderr = ssh.exec_command(deploy)
    print('Deployment done for instance number ' + str(instance_nb) + '\n')
    ssh.close()


def deploy_app():
    instances_IDs_IPs = get_id_ips()
    id_ip = instances_IDs_IPs[0]
    print(id_ip)
    instance_count = 0
    t = {}
    deploy_hadoop(id_ip, instance_count)



print("\n############### Installing Hadoop ###############\n")

deploy_app()

print("Hadoop App Deployed On EC2 Instance!")