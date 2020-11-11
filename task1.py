import os
from time import sleep
import getpass as g
import pyfiglet as py


def getFileContent(folder,node):
    return f"<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>\n\n<!-- Put site-specific property overrides in this file. -->\n\n<configuration>\n<property>\n<name>dfs.{node}.dir</name>\n<value>{folder}</value>\n</property>\n</configuration>"

def getFileContentCore(ip):
    return f"<?xml version=\"1.0\"?>\n<?xml-stylesheet type=\"text/xsl\" href=\"configuration.xsl\"?>\n\n<!-- Put site-specific property overrides in this file. -->\n\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://{ip}:9001</value>\n</property>\n</configuration>"

def configureNameNode(option):
    node = "name"
    if(option == "1"):
        ip = input("Enter your local IP: ")
        folder = input("Enter the folder name: ")
        if(not os.path.isdir(folder)):
            os.mkdir(folder)
        print("Configuring ...........")
        os.system("rm -f /etc/hadoop/hdfs-site.xml")
        os.system(f"echo -e \'{getFileContent(folder,node)}\' > /etc/hadoop/hdfs-site.xml")
        os.system("rm -f /etc/hadoop/core-site.xml")
        os.system(f"echo -e \'{getFileContentCore(ip)}\' > /etc/hadoop/core-site.xml")
        os.system("hadoop namenode -format")
        os.system("setenforce 0")
        os.system("systemctl disable firewalld")
        os.system("hadoop-daemon.sh start namenode")
        print("Configured NameNode")
    elif(option == "2"):
        ip = input("Enter the remote IP: ")
        folder = input("Enter the folder name: ")
        if(not os.path.isdir(folder)):
            os.mkdir(folder)
        password = g.getpass("Please enter the password: ")
        print("Configuring ...........")
        os.system(f"sshpass -p {password} ssh root@{ip} rm -f /etc/hadoop/hdfs-site.xml")
        os.system(f"echo -e \'{getFileContent(folder,node)}\' > /root/send.txt")
        os.system(f"sshpass -p {password} scp /root/send.txt root@{ip}:/")
        os.system(f"sshpass -p {password} ssh root@{ip} mv /send.txt /etc/hadoop/hdfs-site.xml -f")
        os.system(f"sshpass -p {password} ssh root@{ip} rm -f /etc/hadoop/core-site.xml")
        os.system(f"echo -e \'{getFileContentCore(ip)}\' > /root/send.txt")
        os.system(f"sshpass -p {password} scp /root/send.txt root@{ip}:/")
        os.system(f"sshpass -p {password} ssh root@{ip} mv /send.txt /etc/hadoop/core-site.xml -f")
        os.system(f"sshpass -p {password} ssh root@{ip} hadoop namenode -format")
        os.system(f"sshpass -p {password} ssh root@{ip} setenforce 0")
        os.system(f"sshpass -p {password} ssh root@{ip} systemctl disable firewalld")
        os.system(f"sshpass -p {password} ssh root@{ip} hadoop-daemon.sh start namenode")
        print("Configured NameNode")

def configureDataNode(option):
    node = "data"
    if(option == "1"):
        ip = input("Enter the master IP: ")
        folder = input("Enter the folder name: ")
        if(not os.path.isdir(folder)):
            os.mkdir(folder)
        print("Configuring ...........")
        os.system("rm -f /etc/hadoop/hdfs-site.xml")
        os.system(f"echo -e \'{getFileContent(folder,node)}\' > /etc/hadoop/hdfs-site.xml")
        os.system("rm -f /etc/hadoop/core-site.xml")
        os.system(f"echo -e \'{getFileContentCore(ip)}\' > /etc/hadoop/core-site.xml")
        os.system("hadoop namenode -format")
        os.system("setenforce 0")
        os.system("systemctl disable firewalld")
        os.system("hadoop-daemon.sh start namenode")
        print("Configured DataNode")
    elif(option == "2"):
        ip = input("Enter the remote IP: ")
        masterIp = input("Enter the master IP: ")
        folder = input("Enter the folder name: ")
        if(not os.path.isdir(folder)):
            os.mkdir(folder)
        password = g.getpass("Please enter the password: ")
        print("Configuring ...........")
        os.system(f"sshpass -p {password} ssh root@{ip} rm -f /etc/hadoop/hdfs-site.xml")
        os.system(f"echo -e \'{getFileContent(folder,node)}\' > /root/send.txt")
        os.system(f"sshpass -p {password} scp /root/send.txt root@{ip}:/")
        os.system(f"sshpass -p {password} ssh root@{ip} mv /send.txt /etc/hadoop/hdfs-site.xml -f")
        os.system(f"sshpass -p {password} ssh root@{ip} rm -f /etc/hadoop/core-site.xml")
        os.system(f"echo -e \'{getFileContentCore(masterIp)}\' > /root/send.txt")
        os.system(f"sshpass -p {password} scp /root/send.txt root@{ip}:/")
        os.system(f"sshpass -p {password} ssh root@{ip} mv /send.txt /etc/hadoop/core-site.xml -f")
        os.system(f"sshpass -p {password} ssh root@{ip} setenforce 0")
        os.system(f"sshpass -p {password} ssh root@{ip} systemctl disable firewalld")
        os.system(f"sshpass -p {password} ssh root@{ip} hadoop-daemon.sh start datanode")
        print("Configured DataNode")

def HadoopMenu():
    while(1):
        os.system("clear")
        print()
        print()
        os.system("tput setaf 2")
        py.print_figlet("Welcome to Hadoop Configuration:",font="slant") 
        os.system("tput setaf 3")
        print("1] Configure NameNode")
        print("2] Configure DataNode")
        print("3] Check Report")
        print("4] Check NameNode Status")
        print("5] Check DataNode status")
        print("6] Stop NameNode")
        print("7] Stop Datanode")
        print("8] Exit\n\n")
        os.system("tput setaf 7")
        option = input("Select your option: ")
        if(option=="1"):
            print("Choose an option: \n1] Local\n2] Remote\n")
            lor = input("Select an option: \n")
            configureNameNode(lor)
        elif(option=="2"):
            print("Choose an option: \n1] Local\n2] Remote\n")
            lor = input("Select an option: ")
            configureDataNode(lor)
        elif(option=="3"):
            print("Getting Data.............")
            os.system("hadoop dfsadmin -report")
        elif(option=="4" or option=="5"):
            print("Choose an option: \n1] Local\n2] Remote\n")
            lor = input("Select an option: \n")
            if(lor=="1"):
                os.system("jps")
            elif(lor=="2"):
                ip = input("Enter the remote IP: ")
                password = g.getpass("Please enter the password: \n")
                os.system(f"sshpass -p {password} ssh root@{ip} jps")
        elif(option=="6"):
            print("Choose an option: \n1] Local\n2] Remote\n")
            lor = input("Select an option: \n")
            if(lor=="1"):
                os.system("hadoop-daemon.sh stop namenode")
                print("Stopped local NameNode")
            elif(lor=="2"):
                ip = input("Enter the remote IP: ")
                password = g.getpass("Please enter the password: \n")
                os.system(f"sshpass -p {password} ssh root@{ip} hadoop-daemon.sh stop namenode")
                print("Stopped remote NameNode")
        elif(option=="7"):
            print("Choose an option: \n1] Local\n2] Remote\n")
            lor = input("Select an option: \n")
            if(lor=="1"):
                os.system("hadoop-daemon.sh stop datanode")
                print("Stopped local DataNode")
            elif(lor=="2"):
                ip = input("Enter the remote IP: ")
                password = g.getpass("Enter the password: ")
                os.system(f"sshpass -p {password} ssh root@{ip} hadoop-daemon.sh stop datanode")
                print("Stopped remote DataNode")
        elif(option=="8"):
            print("Exiting Hadoop Menu  .......Please Wait..............")
            break
    input("Hit Enter to continue...")

def LVMMenu():
    print("Choose an option: \n1] Local\n2] Remote\n")
    lor = input("Select an option: \n")
    if(lor=="1"):
        while(1):
            os.system("clear")
            print()
            print()
            os.system("tput setaf 2")
            py.print_figlet("Welcome to LVM Configuration:",font="slant") 
            os.system("tput setaf 3")    
            print("1] Check Disk Information")
            print("2] Create a Physical Volume")
            print("3] Create a Volume Group")
            print("4] Create, Format, Mount LVM")
            print("5] Extend LVM")
            print("6] Exit")
            os.system("tput setaf 7")
            print()
            option = input("Select an option: ")
            if(option == "1"):
                os.system("fdisk -l")
            elif(option == "2"):
                disk_name = input("Please spcify the disk name: ")
                os.system(f"pvcreate {disk_name}")
            elif(option == "3"):
                vgname = input("Name of the Volume Group: ")
                disks = input("Please specify all the DiskNames ( with spaces ): ")
                os.system(f"vgcreate {vgname} {disks}")
            elif(option == "4"):
                vgname = input("Name of the Volume Group: ")
                lvmname = input("Name of the LVM: ")
                size = input("Enter the size: ")
                mount_point = input("Specify the Mount Point: ")
                os.system(f"lvcreate --size {size} --name {lvmname} {vgname}")
                os.system(f"mkfs.ext4 /dev/{vgname}/{lvmname}")
                os.system(f"mount /dev/{vgname}/{lvmname} {mount_point}")
            elif(option == "5"):
                vgname = input("Specify the name of the Volume Group: ")
                lvmname = input("Specify the name of the LVM: ")
                size = input("Size to be increased: ")
                os.system(f"lvextend --size +{size} /dev/{vgname}/{lvmname}")
                os.system(f"resize2fs /dev/{vgname}/{lvmname}")
            elif(option == "6"):
                print("Exiting LVM Menu  .......Please Wait..............")
                break
            input("Hit Enter to continue")
    elif(lor=="2"):
        ip = input("Enter the remote IP: ")
        password = g.getpass("Enter the password: ")
        while(1):
            os.system("clear")
            print()
            print()
            os.system("tput setaf 2")
            py.print_figlet("Welcome to LVM Configuration:",font="slant") 
            os.system("tput setaf 3")    
            print("1] Check Disk Information")
            print("2] Create a Physical Volume")
            print("3] Create a Volume Group")
            print("4] Create, Format, Mount LVM")
            print("5] Extend LVM")
            print("6] Exit")
            os.system("tput setaf 7")
            print()
            option = input("Select an option: ")
            if(option == "1"):
                os.system("fdisk -l")
            elif(option == "2"):
                disk_name = input("Please spcify the disk name: ")
                os.system(f"sshpass -p {password} ssh root@{ip} pvcreate {disk_name}")
            elif(option == "3"):
                vgname = input("Name of the Volume Group: ")
                disks = input("Please specify all the DiskNames ( with spaces ): ")
                os.system(f"sshpass -p {password} ssh root@{ip} vgcreate {vgname} {disks}")
            elif(option == "4"):
                vgname = input("Name of the Volume Group: ")
                lvmname = input("Name of the LVM: ")
                size = input("Enter the size: ")
                mount_point = input("Specify the Mount Point: ")
                os.system(f"sshpass -p {password} ssh root@{ip} lvcreate --size {size} --name {lvmname} {vgname}")
                os.system(f"sshpass -p {password} ssh root@{ip} mkfs.ext4 /dev/{vgname}/{lvmname}")
                os.system(f"sshpass -p {password} ssh root@{ip} mount /dev/{vgname}/{lvmname} {mount_point}")
            elif(option == "5"):
                vgname = input("Specify the name of the Volume Group: ")
                lvmname = input("Specify the name of the LVM: ")
                size = input("Size to be increased: ")
                os.system(f"sshpass -p {password} ssh root@{ip} lvextend --size +{size} /dev/{vgname}/{lvmname}")
                os.system(f"sshpass -p {password} ssh root@{ip} resize2fs /dev/{vgname}/{lvmname}")
            elif(option == "6"):
                print("Exiting LVM Menu  .......Please Wait..............")
                break
            input("Hit Enter to continue")
        

def AWSMenu():
    print("Choose an option: \n1] Local\n2] Remote\n")
    lor = input("Select an option: \n")
    if(lor=="1"):
        while(1):
            os.system("clear")
            print()
            print()
            os.system("tput setaf 2")
            py.print_figlet("Welcome to AWS Configuration:",font="slant")        
            os.system("tput setaf 3")            
            print("1]  Set a User Profile")
            print("2]  Create a KeyPair")
            print("3]  List of VPC-ids")
            print("4]  List of Subnet-ids")
            print("5]  Create a Security Group")
            print("6]  List of all Security Group IDs")
            print("7]  Add Inbound Rules to Security Group")
            print("8]  Launch Instance")
            print("9]  List of all Instances")
            print("10] Connect to an Instance")
            print("11] Stop Instances")
            print("12] Terminate Instances")
            print("13] Create an EBS Volume")
            print("14] List of all EBS Volumes")
            print("15] Attach Volume")
            print("16] Create an S3 Bucket")
            print("17] Upload File to S3 Bucket")
            print("18] Create a CloudFront Distribution")
            print("19] Exit\n\n")
            os.system("tput setaf 7")
            option = input("Select an option: ")
            if(option=="1"):
                os.system("aws configure")
            elif(option=="2"):
                keyName = input("Enter the KeyName: ")
                os.system(f"aws ec2 create-key-pair --key-name {keyName} --query \"KeyMaterial\" --output text > {keyName}.pem")
                print("Key has been downloaded to your current directory.")
            elif(option=="3"):
                print("VPC-ID\t\t\tDefault_VPC")
                os.system("aws ec2 describe-vpcs --query \"Vpcs[*].[VpcId,IsDefault]\" --output=text")
            elif(option=="4"):
                print("Availability Zone\t\tSubnetID\t\tVpcID")
                os.system("aws ec2 describe-subnets --query \"Subnets[*].[AvailabilityZone,SubnetId,VpcId]\" --output=text")
            elif(option=="5"):
                gname = input("Enter group_name: ")
                des = input("Enter description: ")
                os.system(f"aws ec2 create-security-group --description \"{des}\" --group-name {gname}")
            elif(option=="6"):
                os.system("aws ec2 describe-security-groups --query \"SecurityGroups[*].[GroupName,GroupId]\" --output=json")
            elif(option=="7"):
                groupID = input("Please enter the Security Group ID: ")
                protocol = input("Which protocol? ")
                port = input("Enter the port number: ")
                cidr = input("Enter the IP range to be allowed ( in CIDR notation ): ")
                os.system(f"aws ec2 authorize-security-group-ingress --group-id {groupID} --protocol {protocol} --port {port} --cidr {cidr}")
                print(f"Added {protocol} to the Inbound Rules")
            elif(option=="8"):
                imageId = input("Enter the AMI ID: ")
                instanceType = input("Enter the Instance Type: ")
                subnetId = input("Enter the Subnet-ID: ")
                sg = input("Enter the Security Group ID: ")
                keyname = input("Enter the KeyName: ")
                count = input("How many instances you want? ")
                os.system(f"aws ec2 run-instances --image-id {imageId} --count {count} --instance-type {instanceType} --key-name {keyname} --security-group-ids {sg} --subnet-id {subnetId}")
            elif(option=="9"):
                print("Instance-ID\t\tPublicIP")
                os.system("aws ec2 describe-instances --query \"Reservations[*].Instances[*].[InstanceId,PublicIpAddress]\" --output=text")
            elif(option=="10"):
                ip = input("Enter the PublicIP: ")
                keyName = input("Enter the KeyName: ")
                os.system(f"ssh -i {keyName}.pem ec2-user@{ip}")
            elif(option=="11"):
                instanceIDs = input("Enter the Instance IDs ( with space in between ): ")
                os.system(f"aws ec2 stop-instances --instance-ids {instanceIDs}")
            elif(option=="12"):
                instanceIDs = input("Enter the Instance IDs ( with space in between ): ")
                os.system(f"aws ec2 terminate-instances --instance-ids {instanceIDs}")
            elif(option=="13"):
                size = input("Enter the size: ")
                az = input("Enter the Availability Zone: ")
                name = input("Enter Tag Name: ")
                tag = "ResourceType=volume,Tags=[{Key=Name,Value="+name+"}]"
                os.system(f"aws ec2 create-volume --availability-zone {az} --size {size} --tag-specifications \"{tag}\"")
            elif(option=="14"):
                print("Displaying VolumeID,Availability Zone,Size,Tag\n")
                os.system("aws ec2 describe-volumes --query \"Volumes[*].[VolumeId,AvailabilityZone,Size,Tags[*].Value]\"")
            elif(option=="15"):
                volId = input("Enter the Volume ID: ")
                instanceID = input("Enter the Instance ID: ")
                device = input("Enter Disk Name: ")
                os.system(f"aws ec2 attach-volume --device {device} --instance-id {instanceID} --volume-id {volId}")
            elif(option=="16"):
                bucketName = input("Enter the Bucket Name: ")
                region = input("Enter the Region: ")
                os.system(f"aws s3api create-bucket --bucket {bucketName} --region {region} --create-bucket-configuration LocationConstraint={region}")
                opt= input("Do you want to make the bucket public? y or n: ")
                if(opt=="y"):
                    os.system(f"aws s3api put-bucket-acl --acl public-read --bucket {bucketName}")
            elif(option=="17"):
                bucketname = input("Enter the Bucket Name: ")
                filePath = input("FileName: ")
                os.system(f"aws s3api put-object --bucket {bucketname} --body {filePath} --key {filePath}")
            elif(option=="18"):
                bn = input("Enter Bucket Name: ")
                os.system(f"aws cloudfront create-distribution --origin-domain-name {bn}.s3.amazonaws.com")
            elif(option=="19"):
                print("Exiting AWS Menu  .......Please Wait..............")
                break
            else:
                print("Invalid input ")
            input("Hit Enter To continue...")
    elif(lor=="2"):
        ip = input("Enter the remote IP: ")
        password = g.getpass("Enter the password: ")
        while(1):
            os.system("clear")
            print()
            print()
            os.system("tput setaf 2")
            py.print_figlet("Welcome to AWS Configuration:",font="slant")
            os.system("tput setaf 3")            
            print("1]  Set a User Profile")
            print("2]  Create a KeyPair")
            print("3]  List of VPC-ids")
            print("4]  List of Subnet-ids")
            print("5]  Create a Security Group")
            print("6]  List of all Security Group IDs")
            print("7]  Add Inbound Rules to Security Group")
            print("8]  Launch Instance")
            print("9]  List of all Instances")
            print("10] Connect to an Instance")
            print("11] Stop Instances")
            print("12] Terminate Instances")
            print("13] Create an EBS Volume")
            print("14] List of all EBS Volumes")
            print("15] Attach Volume")
            print("16] Create an S3 Bucket")
            print("17] Upload File to S3 Bucket")
            print("18] Create a CloudFront Distribution")
            print("19] Exit\n\n")
            os.system("tput setaf 7")
            option = input("Select an option: ")
            if(option=="1"):
                os.system(f"sshpass -p {password} ssh root@{ip} aws configure")
            elif(option=="2"):
                keyName = input("Enter the KeyName: ")
                os.system(f"sshpass -p {password} ssh root@{ip} aws ec2 create-key-pair --key-name {keyName} --query \"KeyMaterial\" --output text > {keyName}.pem")
                print("Key has been downloaded to your current directory.")
            elif(option=="3"):
                print("VPC-ID\t\t\tDefault_VPC")
                os.system(f"sshpass -p {password} ssh root@{ip} aws ec2 describe-vpcs --query \"Vpcs[*].[VpcId,IsDefault]\" --output=text")
            elif(option=="4"):
                print("Availability Zone\t\tSubnetID\t\tVpcID")
                os.system(f"sshpass -p {password} ssh root@{ip} aws ec2 describe-subnets --query \"Subnets[*].[AvailabilityZone,SubnetId,VpcId]\" --output=text")
            elif(option=="5"):
                gname = input("Enter group_name: ")
                des = input("Enter description: ")
                os.system(f"sshpass -p {password} ssh root@{ip} aws ec2 create-security-group --description \"{des}\" --group-name {gname}")
            elif(option=="6"):
                os.system(f"sshpass -p {password} ssh root@{ip} aws ec2 describe-security-groups --query \"SecurityGroups[*].[GroupName,GroupId]\" --output=json")
            elif(option=="7"):
                groupID = input("Please enter the Security Group ID: ")
                protocol = input("Which protocol? ")
                port = input("Enter the port number: ")
                cidr = input("Enter the IP range to be allowed ( in CIDR notation ): ")
                os.system(f"sshpass -p {password} ssh root@{ip} aws ec2 authorize-security-group-ingress --group-id {groupID} --protocol {protocol} --port {port} --cidr {cidr}")
                print(f"Added {protocol} to the Inbound Rules")
            elif(option=="8"):
                imageId = input("Enter the AMI ID: ")
                instanceType = input("Enter the Instance Type: ")
                subnetId = input("Enter the Subnet-ID: ")
                sg = input("Enter the Security Group ID: ")
                keyname = input("Enter the KeyName: ")
                count = input("How many instances you want? ")
                os.system(f"sshpass -p {password} ssh root@{ip} aws ec2 run-instances --image-id {imageId} --count {count} --instance-type {instanceType} --key-name {keyname} --security-group-ids {sg} --subnet-id {subnetId}")
            elif(option=="9"):
                print("Instance-ID\t\tPublicIP")
                os.system(f"sshpass -p {password} ssh root@{ip} aws ec2 describe-instances --query \"Reservations[*].Instances[*].[InstanceId,PublicIpAddress]\" --output=text")
            elif(option=="10"):
                ip = input("Enter the PublicIP: ")
                keyName = input("Enter the KeyName: ")
                os.system(f"sshpass -p {password} ssh root@{ip} ssh -i {keyName}.pem ec2-user@{ip}")
            elif(option=="11"):
                instanceIDs = input("Enter the Instance IDs ( with space in between ): ")
                os.system(f"sshpass -p {password} ssh root@{ip} aws ec2 stop-instances --instance-ids {instanceIDs}")
            elif(option=="12"):
                instanceIDs = input("Enter the Instance IDs ( with space in between ): ")
                os.system(f"sshpass -p {password} ssh root@{ip} aws ec2 terminate-instances --instance-ids {instanceIDs}")
            elif(option=="13"):
                size = input("Enter the size: ")
                az = input("Enter the Availability Zone: ")
                name = input("Enter Tag Name: ")
                tag = "ResourceType=volume,Tags=[{Key=Name,Value="+name+"}]"
                os.system(f"sshpass -p {password} ssh root@{ip} aws ec2 create-volume --availability-zone {az} --size {size} --tag-specifications \"{tag}\"")
            elif(option=="14"):
                print("Displaying VolumeID,Availability Zone,Size,Tag\n")
                os.system(f"sshpass -p {password} ssh root@{ip} aws ec2 describe-volumes --query \"Volumes[*].[VolumeId,AvailabilityZone,Size,Tags[*].Value]\"")
            elif(option=="15"):
                volId = input("Enter the Volume ID: ")
                instanceID = input("Enter the Instance ID: ")
                device = input("Enter Disk Name: ")
                os.system(f"sshpass -p {password} ssh root@{ip} aws ec2 attach-volume --device {device} --instance-id {instanceID} --volume-id {volId}")
            elif(option=="16"):
                bucketName = input("Enter the Bucket Name: ")
                region = input("Enter the Region: ")
                os.system(f"sshpass -p {password} ssh root@{ip} aws s3api create-bucket --bucket {bucketName} --region {region} --create-bucket-configuration LocationConstraint={region}")
                opt= input("Do you want to make the bucket public? y or n: ")
                if(opt=="y"):
                    os.system(f"sshpass -p {password} ssh root@{ip} aws s3api put-bucket-acl --acl public-read --bucket {bucketName}")
            elif(option=="17"):
                bucketname = input("Enter the Bucket Name: ")
                filePath = input("FileName: ")
                os.system(f"sshpass -p {password} ssh root@{ip} aws s3api put-object --bucket {bucketname} --body {filePath} --key {filePath}")
            elif(option=="18"):
                bn = input("Enter Bucket Name: ")
                os.system(f"sshpass -p {password} ssh root@{ip} aws cloudfront create-distribution --origin-domain-name {bn}.s3.amazonaws.com")
            elif(option=="19"):
                print("Exiting AWS Menu  .......Please Wait..............")
                break
            else:
                print("Invalid input ")
            input("Hit Enter To continue...")

def dockerMenu():
    print("Choose an option: \n1] Local\n2] Remote\n")
    lor = input("Select an option: \n")
    if(lor=="1"):
        while(1):
            os.system("clear")
            print()
            print()
            os.system("tput setaf 2")
            py.print_figlet("Welcome to Docker Configuration:",font="slant")
            os.system("tput setaf 3")
            print("1]  Start Docker service")
            print("2]  See Downloaded Images")
            print("3]  Launch a Container")
            print("4]  Start Container")
            print("5]  Stop Container")
            print("6]  Terminate a Container")
            print("7]  Pull Image")
            print("8]  Attach a Container")
            print("9]  Configure a WebServer")
            print("10] Add new files to the active webserver")
            print("11] See Information of running/stoped container")
            print("12] Terminate all containers")
            print("13] Exit")
            os.system("tput setaf 7")
            option = input("\nSelect an option: ")
            if(option=="1"):
                print("Starting Docker........")
                os.system("systemctl start docker")
                print("Started Docker service")
            elif(option=="2"):
                os.system("docker images")
            elif(option=="3"):
                osName = input("Enter an OS image name: ")
                tag = input("Enter the version (By Default latest): ")
                name = input("Enter the Container name: ")
                os.system(f"docker run -dit --name {name} {osName}:{tag}")
                print(f"Launched {name}")
            elif(option=="4"):
                cname = input("Enter the container Name/ID: ")
                os.system(f"docker start {cname}")
                print(f"Started {cname}")
            elif(option=="5"):
                cname = input("Enter the container Name/ID: ")
                os.system(f"docker stop {cname}")
                print(f"Stopped {cname}")
            elif(option=="6"):
                cname = input("Enter the container Name/ID: ")
                os.system(f"docker rm -f {cname}")
            elif(option=="7"):
                osname = input("Enter the OS image name: ")
                tag = input("Enter the version (By Default latest): ")
                os.system(f"docker pull {osname}:{tag}")
                print(f"Successfully downloaded {osname}:{tag}")
            elif(option=="8"):
                id = input("Enter the container Name/ID: ")
                os.system(f"docker attach {id}")
            elif(option=="9"):
                ip = input("Enter your current ip: ")
                name = input("Enter a Container name: ")
                port = input("Enter the Port Number: ")
                files = input("Enter the path of the files to be served by the webserver: ")
                os.system(f"docker run -dit -p {port}:80 --name {name} vimal13/apache-webserver-php:latest")
                print("\nYour container is launched")
                print("Transfering your files..........")
                os.system(f"docker cp {files} {name}:/var/www/html/")
                print(f"You can now access the webpage at {ip}:{port}/{files}")
            elif(option=="10"):
                name = input("Enter the Container Name: ")
                files = input("Enter the path of the files to be added: ")
                os.system(f"docker cp {files} {name}:/var/www/html/")
            elif(option=="11"):
                print()
                os.system(f"docker ps -a")
            elif(option=="12"):
                print()
                verify=input("!! You are about to terminate all the running and stoped containers !!\nDo you want to continue\n1] Yes\n2]No\n")
                if(verify=="1"):
                    print("Cleaning environment ...")
                    os.system(f"docker rm -f $(docker ps -a -q)")
                else:
                    print("Task Terminated")
            elif(option=="13"):
                print("Exiting Docker Menu  .......Please Wait..............")
                break
            else:
                print("Invalid Input")
            input("Hit Enter to continue...")
    elif(lor=="2"):
        ip = input("Enter the remote IP: ")
        password = g.getpass("Enter the password: ")
        while(1):
            os.system("clear")
            print()
            print()
            os.system("tput setaf 2")
            py.print_figlet("Welcome to Docker Configuration:",font="slant")
            os.system("tput setaf 3")           
            print("1]  Start Docker service")
            print("2]  See Downloaded Images")
            print("3]  Launch a Container")
            print("4]  Start Container")
            print("5]  Stop Container")
            print("6]  Terminate a Container")
            print("7]  Pull Image")
            print("8]  Attach a Container")
            print("9]  Configure a WebServer")
            print("10] Add new files to the active webserver")
            print("11] See Information of running/stoped container")
            print("12] Terminate all containers")
            print("13] Exit")
            os.system("tput setaf 7")
            option = input("\nSelect an option: ")
            if(option=="1"):
                print("Starting Docker........")
                os.system(f"sshpass -p {password} ssh root@{ip} systemctl start docker")
                print("Started Docker service")
            elif(option=="2"):
                os.system(f"sshpass -p {password} ssh root@{ip} docker images")
            elif(option=="3"):
                osName = input("Enter an OS image name: ")
                tag = input("Enter the version: ")
                name = input("Enter the Container name: ")
                os.system(f"sshpass -p {password} ssh root@{ip} docker run -dit --name {name} {osName}:{tag}")
                print(f"Launched {name}")
            elif(option=="4"):
                cname = input("Enter the container Name/ID: ")
                os.system(f"sshpass -p {password} ssh root@{ip} docker start {cname}")
                print(f"Started {cname}")
            elif(option=="5"):
                cname = input("Enter the container Name/ID: ")
                os.system(f"sshpass -p {password} ssh root@{ip} docker stop {cname}")
                print(f"Stopped {cname}")
            elif(option=="6"):
                cname = input("Enter the container Name/ID: ")
                os.system(f"sshpass -p {password} ssh root@{ip} docker rm -f {cname}")
            elif(option=="7"):
                osname = input("Enter the OS image name: ")
                tag = input("Enter the version: ")
                os.system(f"sshpass -p {password} ssh root@{ip} docker pull {osname}:{tag}")
                print(f"Successfully downloaded {osname}:{tag}")
            elif(option=="8"):
                id = input("Enter the container Name/ID: ")
                os.system(f"sshpass -p {password} ssh root@{ip} docker attach {id}")
            elif(option=="9"):
                ip = input("Enter your current ip: ")
                name = input("Enter a Container Name: ")
                port = input("Enter the Port Number: ")
                files = input("Enter the path of the files to be served by the webserver: ")
                os.system(f"sshpass -p {password} ssh root@{ip} docker run -dit -p {port}:80 --name {name} vimal13/apache-webserver-php:latest")
                print("\nYour container is launched")
                print("Transfering your files..........")
                os.system(f"sshpass -p {password} ssh root@{ip} docker cp {files} {name}:/var/www/html/")
                print(f"You can now access the webpage at {ip}:{port}/{files}")
            elif(option=="10"):
                name = input("Enter the Container Name: ")
                files = input("Enter the path of the files to be added: ")
                os.system(f"sshpass -p {password} ssh root@{ip} docker cp {files} {name}:/var/www/html/")
            elif(option=="11"):
                print()
                os.system(f"sshpass -p {password} ssh root@{ip} docker ps -a")
            elif(option=="12"):
                print()
                verify=input("!! You are about to terminate all the running and stoped containers !!\nDo you want to continue\n1] Yes\n2] No\n")
                if(verify=="1"):
                    print("Cleaning environment ...")
                    os.system(f"sshpass -p {password} ssh root@{ip} docker rm -f $(docker ps -a -q)")
                else:
                    print("Task Terminated")
            elif(option=="13"):
                print("Exiting Docker Menu  .......Please Wait..............")
                break
            else:
                print("Invalid Input")
            input("Hit Enter to continue ...")

def LinuxCmd():
    print("Choose an option: \n1] Local\n2] Remote\n")
    lor = input("Select an option: \n")
    if(lor=="1"):
        while(1):
            os.system("clear")
            os.system("tput setaf 2")
            py.print_figlet("Run Basic System Commands",font="slant")
            os.system("tput setaf 3")
            print("1] Run System Commands")
            print("2] Exit")
            os.system("tput setaf 7")
            option = input("\n\nSelect an option: ")
            if(option=="1"):
                cmd=input("Enter the Command to run: ")
                os.system(cmd)
            elif(option=="2"):
                print("Exiting Program ......Please Wait............")
                break                               
            input("Hit Enter to Continue...")
    elif(lor=="2"):
        ip = input("Enter the remote IP: ")
        password = g.getpass("Enter the password: ")
        while(1):    
            os.system("clear")
            os.system("tput setaf 2")
            py.print_figlet("Run Basic System Commands",font="slant")
            os.system("tput setaf 3")
            print("1] Run System Commands")
            print("2] Exit")
            os.system("tput setaf 7")
            option = input("\n\nSelect an option: ")
            if(option=="1"):
                cmd=input("Enter the Command to run: ")
                os.system(f"sshpass -p {password} ssh root@{ip} {cmd}")
            elif(option=="2"):
                print("Exiting Program ......Please Wait............")
                break      
            input("Hit Enter to Continue...")


while(1):
    os.system("clear")
    print()
    print()
    os.system("tput setaf 2")
    py.print_figlet("Welcome to Automation with Python",font="slant")
    os.system("tput setaf 3")
    print("1] Hadoop Configuration")
    print("2] LVM Configuration")
    print("3] AWS Configuration")
    print("4] Docker Configuration")
    print("5] Run Basic linux Command")
    print("6] Exit")
    os.system("tput setaf 6")
    option = input("\n\nSelect an option: ")
    os.system("tput setaf 7")
    if(option=="1"):
        HadoopMenu()
    elif(option=="2"):
        LVMMenu()
    elif(option=="3"):
        AWSMenu()
    elif(option=="4"):
        dockerMenu()
    elif(option=="5"):
        LinuxCmd()
    elif(option=="6"):
        print("Exiting Program ......Please Wait............")
        sleep(2)
        exit()
    else:
        print("Invalid Input")
