<div align="center">

  **AWS CLoud Deployment Task**
</div>


### Installing
A step by step series of examples that tell you how to get a development env running

Cloning the repo
```
$ git clone https://github.com/gauravmandal27/AWS-Boto-Task
```
Installing the dependencies
```
https://aws.amazon.com/cli/
$ pip install awscli
$ aws configure
```
Run Any Python IDE

## Deployment <a name="deployment"></a>
**1. Create VPC and Subnets**
```
#1) Create an ec2 resource object
ec2 = boto3.resource('ec2', region_name='us-east-1')

# Create a VPC with CIDR block 192.168.10.8/24
vpc = ec2.create_vpc(CidrBlock='192.168.10.8/24')

# Enable public DNS hostname for the VPC
ec2Client = boto3.client('ec2')
ec2Client.modify_vpc_attribute(VpcId=vpc.id, EnableDnsSupport={'Value': True})
ec2Client.modify_vpc_attribute(VpcId=vpc.id, EnableDnsHostnames={'Value': True})

# Create a subnet with CIDR block 192.168.10.8/28 within the VPC
subnet = vpc.create_subnet(CidrBlock='192.168.10.8/28')

# Create a security group that allows SSH and HTTP access from anywhere
security_group = ec2.create_security_group(GroupName='my-sg', Description='My security group', VpcId=vpc.id)
security_group.authorize_ingress(IpProtocol='tcp', FromPort=22, ToPort=22, CidrIp='0.0.0.0/0')
security_group.authorize_ingress(IpProtocol='tcp', FromPort=80, ToPort=80, CidrIp='0.0.0.0/0')
```

**2. Deploy EC2 instance and attach it to the Subnet.**

+ Networkid helps ensure the privacy of your network. You can use any number here (where we used “1114”), but other peers joining your network must use the same one.
```
#2) Launch an EC2 instance using an AMI image, specifying the subnet, security group, and key pair
ec2resource = boto3.resource('ec2')
instance = ec2resource.create_instances(ImageId='ami-0ffac3e16de16665e', InstanceType='t2.micro', KeyName='my-key1', SubnetId=subnet,MinCount=1, MaxCount=1, TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'test-instance-2'}]}])
print(instance)
```
+ Output should look like this:
```
Welcome to the Geth JavaScript console!

instance: Geth/v1.7.3-stable-4bb3c89d/darwin-amd64/go1.8.3
coinbase: 0xae13d41d66af28380c7af6d825ab557eb271ffff
at block: 5 (Thu, 07 Dec 2017 17:08:48 PST)
datadir: /Users/test/my-eth-chain/myDataDir
modules: admin:1.0 clique:1.0 debug:1.0 eth:1.0 miner:1.0 net:1.0 personal:1.0 rpc:1.0 txpool:1.0 web3:1.0

>
```
This is the geth JavaScript console. Any command with the symbol > should be typed here.

**3. Create S3 bucket and deploy static website (hello world) using python**

+ Open another terminal window
+ ```#3)Creation of an S3 Bucket
s3 = boto3.client('s3')
bucketName='sample-bucket-for-cloud-deployment-test'
response = s3.create_bucket(Bucket=bucketName, CreateBucketConfiguration={'LocationConstraint': 'us-east-1'})
print(response)

#Storing of the website conetent index.html into the S3 bucket
s3.put_object(Body='<html><body><h1>Hello World</h1></body></html>', Bucket=bucketName, Key='index.html', ContentType='text/html')
bucket = s3.Bucket(bucketName)
url=s3.get_bucket_website(Bucket=bucketName)
#Storing of the URL website conetent index.html into the S3 bucket
print(url)
```
+ Type ```tail -f myEth.log```

**4. Install Nginx in the EC2 instance (using remote execution)**

+ If you allocated ETH in the Genesis file, import the corresponding account by dragging the UTC file into the ```myDataDir/keystoredirectory``` and skip to step 5.
+ In the geth JavaScript console, create an account:
```

## Authors <a name="authors"></a>
+ [Gaurav Mandal](https://github.com/gauravmandal27) <br>
