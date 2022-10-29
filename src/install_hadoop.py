import paramiko
import scp
import time
import sys
import boto3
import os
from os import getenv, path, system
from os import listdir
from os.path import isfile, join
from scp import SCPClient

AWS_REGION = 'us-east-1'
DESTINATION_PATH = '~'
DESTINATION_PATH_2 = '~/usr/local/hadoop/sbin'
files_list1 = [f for f in listdir("code/") if isfile(join("code/", f))]
FILE1 = [f'code/{f}' for f in files_list1]
files_list2 = [f for f in listdir("scripts/") if isfile(join("scripts/", f))]
FILES = [f'scripts/{f}' for f in files_list2]
DATASET = "TP2-dataset.zip"

def envsetup(instanceID):
    """
    This function sets up the environment on the selected instance.
    instanceID : the id of the instance
    """
    str_instanceID = str(instanceID)
    return """
#!/bin/bash
yes | sudo apt update
yes | sudo apt install default-jdk
wget https://downloads.apache.org/hadoop/common/hadoop-3.3.1/hadoop-3.3.1.tar.gz
tar -xzvf hadoop-3.3.1.tar.gz
sudo mv hadoop-3.3.1 /usr/local/hadoop
readlink -f /usr/bin/java | sed "s:bin/java::"
curl https://archive.apache.org/dist/spark/spark-2.0.0/spark-2.0.0.tgz > spark-2.0.0.tgz
tar -zxvf spark-2.0.0.tgz
sudo mv spark-2.0.0 /usr/local/spark
EOF
"""

def ssh_connect_with_retry(ssh, ip_address, retries):
    """
    This function connects via ssh on the instance.
    ssh : the id of the instance
    ip_address : the ip addres sof the instance
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

def get_id_ips():
    """
    This function ...
    """
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
            print(
                f"instance id :{instance_id}, instance type: {instance_type}, public ip:{public_ip}, private ip:{private_ip}")
    print("\n")
    return ids

def start_scripts(instanceID):
    """
    This function starts the scripts on the selected instance.
    instanceID : the id of the instance
    """
    return """
#!/bin/bash
sh start.sh
EOF
"""

def deploy_hadoop(id_ip, instance_nb):
    """
    This function ...
    """
    ip_address = id_ip[1]
    print(ip_address)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_connect_with_retry(ssh, ip_address, 0)
    stdin, stdout, stderr = ssh.exec_command(envsetup(id_ip[0]))
    old_stdout = sys.stdout
    log_file = open("logfile.log", "w")
    print('env setup done \n stdout:', stdout.read(), file=log_file)
    log_file.close()
    print('Sending files... \n')
    # Send the config.sh file to the instance
    scp = SCPClient(ssh.get_transport())
    scp.put(
        FILE1,
        remote_path=DESTINATION_PATH,
        recursive=True
    )
    scp.put(
        FILES,
        remote_path=DESTINATION_PATH,
        recursive=True
    )
    scp.put(
        DATASET,
        remote_path=DESTINATION_PATH,
        recursive=False
    )
    print('Deployment done for instance number ' + str(instance_nb) + '\n')
    
    # Running the script start.sh on the VM
    stdin, stdout, stderr = ssh.exec_command(start_scripts(id_ip[0]))
    old_stdout = sys.stdout
    #log_file = open("logfile.log", "w")
    print('Script done.', stdout.read())#, file=log_file)
    #log_file.close()
    print('Retrieving results file')
    scp.get('/home/ubuntu/results.tar.gz', 'results/')
    ssh.close()

def deploy_app():
    """
    This function deploys the applications, scripts on the instance.
    """
    running = False
    while (not running):
        try:
            instances_IDs_IPs = get_id_ips()
            id_ip = instances_IDs_IPs[0]
            running = True
        except:
            print("Waiting for the instance to be running .. (10s)")
            time.sleep(10)
    instance_count = 0
    deploy_hadoop(id_ip, instance_count)


print("\n############### Installing Hadoop ###############\n")

deploy_app()

print("Hadoop App Deployed On EC2 Instance!")
