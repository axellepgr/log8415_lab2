import boto3
import time


AWS_REGION = 'us-east-1'
AVAILABILITY_ZONE = ['us-east-1a']
INSTANCE_TYPE = ["m4.large"]
NB_INSTANCES = 1
KEY_PAIR_NAME = "vockey"
AMI_ID = "ami-08c40ec9ead489470"


ec2_client = boto3.client("ec2", region_name=AWS_REGION)
ec2_resource = boto3.resource('ec2', region_name=AWS_REGION)
vpcID = 'vpc-087ef03df262abb66'
subnet_id = 'subnet-066c5c280a820dc2d'
def create_sg(vpcID):
    """
    This function creates a new security group for the VPC.
    vpcID : is the ID of the concerned VPC.
    Returns the security group ID.
    """
    response = ec2_client.create_security_group(GroupName="LAB2",
                                                Description='SG_basic',
                                                VpcId=vpcID)
    security_group_id = response['GroupId']
    ec2_client.authorize_security_group_ingress(
        GroupId=security_group_id,
        IpPermissions=[
            {'IpProtocol': 'tcp',
             'FromPort': 80,
             'ToPort': 80,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 22,
             'ToPort': 22,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp',
             'FromPort': 443,
             'ToPort': 443,
             'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ])
    print('Ingress rules successfully set!')
    return security_group_id

def create_ec2_instances(nbr, type, sg_id, subnet_id):
    """
    This function creates EC2 instances.
    nbr : is the desired number of instances to be created.
    type : is either 0 for m4.large instances ot 1 for t2.large instances.
    sg_id : is the ID of the security group that you wish your instaces to follow.
    subnet_id : is the subnet where you instances will reside.
    """
    ec2_client.run_instances(
        MinCount=nbr,
        MaxCount=nbr,
        ImageId=AMI_ID,
        InstanceType=INSTANCE_TYPE[type],
        KeyName=KEY_PAIR_NAME,
        NetworkInterfaces=[{
            "DeviceIndex": 0,
            "Groups": [sg_id],
            "AssociatePublicIpAddress": True,
            "SubnetId": subnet_id
        }]
    )

# Start


print("\n############### SETTING UP THE SYSTEM ###############\n")

print("Security group created!\n")

print("Creating the EC2 instances...")
sg_id = create_sg(vpcID)
create_ec2_instances(1, 0, sg_id, subnet_id)
print("EC2 instances created!\n")

time.sleep(20)
print("Finished waiting.\n")
print("\n############### DONE SETTING UP THE SYSTEM ###############\n")
