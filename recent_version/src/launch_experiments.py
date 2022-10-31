import paramiko
import json
import time
import scp
from scp import SCPClient

with open('collected_data.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)
    openfile.close()

ip = json_object["ip"]


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


def launch_experiments(ip):
    """
    This function runs the scripts on the instance.
    ip : the ip of the instances
    """
    # Setting Up SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_connect_with_retry(ssh, ip, 0)
    print("Connected through SSH!")

    ssh.exec_command("bash pg4300_hadoop.sh")
    print("hadoop pg4300 done.")

    ssh.exec_command("bash pg4300_linux.sh")
    print("linux pg4300 done.")

    ssh.exec_command("bash experiment_spark.sh")
    print("spark job on the 9 files done.")

    ssh.exec_command("bash experiment_hadoop.sh")
    print("hadoop job on the 9 files done.")

    ssh.exec_command("bash generate_times_file.sh")
    print("\"~/times.txt\": a file that contains the running time of hadoop for each file was created")

    ssh.exec_command("bash run_hadoop_friends.sh")
    print("hadoop job friends recommendations done.")
    
    print('Retrieving results files')
    scp = SCPClient(ssh.get_transport())
    scp.get('/home/ubuntu/pg4300_linux_time.txt', 'results/')
    scp.get('/home/ubuntu/pg4300_hadoop_time.txt', 'results/')
    scp.get('/home/ubuntu/experiment_spark_time.txt', 'results/')
    scp.get('/home/ubuntu/times.txt', 'results/')

    scp.close()
    ssh.close()


print("\n############### Launching experiments ###############\n")

launch_experiments(ip)

print("Done!")
