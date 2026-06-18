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
                "cpu_utilization": cpu_value,
                "state": instance["State"]["Name"]
            })
    

    return metrics

def get_instance_status():

    response = ec2_client.describe_instances()

    instances = []

    for reservation in response["Reservations"]:

        for instance in reservation["Instances"]:

            instance_name = "Unknown"

            for tag in instance.get("Tags", []):

                if tag["Key"] == "Name":

                    instance_name = tag["Value"]

            instances.append({

                "instance_id": instance["InstanceId"],

                "instance_name": instance_name,

                "state": instance["State"]["Name"],

                "public_ip": instance.get(
                    "PublicIpAddress",
                    "N/A"
                ),

                "availability_zone":
                    instance["Placement"]["AvailabilityZone"]

            })

    return instances

def get_cloudwatch_alarms():

    response = cloudwatch_client.describe_alarms()

    alarm_data = []

    for alarm in response["MetricAlarms"]:

        alarm_data.append({

            "alarm_name": alarm["AlarmName"],

            "state": alarm["StateValue"],

            "reason": alarm["StateReason"],

            "metric": alarm["MetricName"],

            "updated": str(
                alarm["StateUpdatedTimestamp"]
            )
        })

    return alarm_data

def determine_health(cpu, state):

    if state == "stopped":
        return "Offline"

    if cpu < 70:
        return "Healthy"

    elif cpu < 90:
        return "Warning"

    return "Critical"
		

def get_system_health():

    cpu_metrics = get_ec2_cpu_metrics()

    health_data = []

    for metric in cpu_metrics:

        cpu = metric["cpu_utilization"]

        state = metric["state"]

        health_data.append({

            "instance_id": metric["instance_id"],

            "cpu_utilization": cpu,

            "cpu_health": determine_health(cpu, state)

        })

    return health_data
