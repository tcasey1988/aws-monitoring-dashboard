import boto3
from datetime import datetime, timedelta
from config import AWS_REGION

ec2_client = boto3.client(
    "ec2",
    region_name='us-east-1'
)

cloudwatch_client = boto3.client(
    "cloudwatch",
    region_name='us-east-1'
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


def get_ec2_cpu_metrics():

    response = ec2_client.describe_instances()

    metrics = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:

            instance_id = instance["InstanceId"]

            cpu_response = cloudwatch_client.get_metric_statistics(

                Namespace="AWS/EC2",

                MetricName="CPUUtilization",

                Dimensions=[
                {
            "Name": "InstanceId",
            "Value": instance_id
             }
        ],

    StartTime=datetime.utcnow() - timedelta(hours=1),

    EndTime=datetime.utcnow(),

    Period=300,

    Statistics=["Average"]
            )

            datapoints = cpu_response.get("Datapoints", [])

            cpu_value = 0

            if datapoints:

                latest = sorted(
                    datapoints,
                    key=lambda x: x["Timestamp"]
                )[-1]

                cpu_value = round(
                    latest["Average"],
                    2
                )

            metrics.append({
                "instance_id": instance_id,
                "cpu_utilization": cpu_value
            })
    

    return metrics

