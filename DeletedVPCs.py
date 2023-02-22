import boto3
#code to delete multiple Vpc's if the limit is exhausted
def stop_instance(instance_id):
    ec2_client = boto3.client("ec2", region_name="us-west-2")
    response = ec2_client.stop_instances(InstanceIds=[instance_id])
    print(response)


def terminate_instance(instance_id):
    ec2_client = boto3.client("ec2", region_name="us-west-2")
    response = ec2_client.terminate_instances(InstanceIds=[instance_id])
    print(response)

ec2client = boto3.client('ec2')
response = ec2client.describe_instances()
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        print(instance['InstanceId'])
        ins=instance['InstanceId']
        stop_instance(ins)
        terminate_instance(ins)


client = boto3.client('ec2',region_name='us-east-1')
response = client.describe_vpcs()
vpcs = response['Vpcs']
for vpc in vpcs:
    print(vpc['VpcId'])
    vp=vpc['VpcId']
    ec2 = boto3.resource('ec2')
    ec2client = ec2.meta.client
    ec2client.delete_vpc(VpcId=vp)
    try:
        print("Delete Sucess",vp)
    except:
        print("failed")