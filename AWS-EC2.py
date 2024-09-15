import boto3

# AWS EC2 client
ec2 = boto3.client('ec2')

# Define instance ID
instance_id = 'i-0123456789abcdef0'

# Function to start the EC2 instance
def start_instance():
    response = ec2.start_instances(InstanceIds=[instance_id])
    print(f"Starting instance {instance_id}. Current state: {response['StartingInstances'][0]['CurrentState']['Name']}")

# Function to stop the EC2 instance
def stop_instance():
    response = ec2.stop_instances(InstanceIds=[instance_id])
    print(f"Stopping instance {instance_id}. Current state: {response['StoppingInstances'][0]['CurrentState']['Name']}")

# Start the instance
start_instance()

# Stop the instance
stop_instance()
