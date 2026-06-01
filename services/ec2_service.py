import boto3
from config import AWS_REGION

ec2_client = boto3.client(
    "ec2",
    region_name=AWS_REGION
)

def get_ec2_instances():

    response = ec2_client.describe_instances()

    instances = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:

            instances.append({
                "instance_id": instance["InstanceId"],
                "state": instance["State"]["Name"]
            })

    return instances