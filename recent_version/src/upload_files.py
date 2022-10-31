from os.path import isfile, join
from os import listdir
import paramiko
import time
import json
import sys
from scp import SCPClient

DESTINATION_PATH = '~'

files_list = [f for f in listdir("upload/") if isfile(join("upload/", f))]
FILES = [f'upload/{f}' for f in files_list]

with open('collected_data.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)
    openfile.close()

ip = json_object["ip"]


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


def upload_files(ip):

    # Setting Up SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_connect_with_retry(ssh, ip, 0)
    print("Connected through SSH!")

    print("Sending the necessary files...")
    scp = SCPClient(ssh.get_transport())
    scp.put(
        FILES,
        remote_path=DESTINATION_PATH,
        recursive=True
    )

    time.sleep(20)

    print("Files sent!")

    print("preparing .sh files for execution...")
    stdin, stdout, stderr = ssh.exec_command("python3 prepare_sh_files.py")
    old_stdout = sys.stdout
    log_file = open("logfile.log", "w")
    print('env setup done \n stdout:', stdout.read(), file=log_file)
    log_file.close()

    ssh.close()


print("\n############### Sending the necessary files ###############\n")

upload_files(ip)

print("\n############### Done sending the files ###############\n")
