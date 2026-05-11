import boto3
import logging
import os
from datetime import datetime, timedelta, UTC
from decimal import Decimal

#AWS services
cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

#Environmental varaibles for EC2 instances and table
INSTANCE_IDS = os.environ['INSTANCE_ID'].split(',')
TABLE_NAME = os.environ['TABLE_NAME']
table = dynamodb.Table(TABLE_NAME)

#Set up logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#use CloudWatch to pull the EC2 data
def get_metric(instance_id, metric_name, start_time, end_time):

    logger.info(f"Collecting metric: {metric_name}")

    #Get EC2 metrics using CloudWatch
    response = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName=metric_name,
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average']
    )

    datapoints = response['Datapoints']

    #Error handling if no datapoint found
    if not datapoints:
        logger.warning(f"No datapoints found for {metric_name}")
        return Decimal("0")

    sorted_points = sorted(
        datapoints,
        key=lambda x: x['Timestamp']
    )

    latest_value = sorted_points[-1]['Average']

    logger.info(f"{metric_name}: {latest_value}")

    return Decimal(str(latest_value))
    
#Store metrics into DynamoDB table
def store_metric(instance_id, metric_name, value, timestamp):

    try:
        table.put_item(
            Item={
                'ResourceId': instance_id,
                'Timestamp': f"{timestamp.isoformat()}#{metric_name}",
                'MetricName': metric_name,
                'Value': value
            }
        )

        logger.info(f"Stored {metric_name}")

    except Exception as e:
        logger.error(f"Failed storing {metric_name}: {str(e)}")

#Lambda handler function
def lambda_handler(event, context):

    try:

        logger.info("Lambda execution started")

        end_time = datetime.now(UTC)
        start_time = end_time - timedelta(minutes=15)

        metrics = [
            "CPUUtilization",
            "NetworkIn",
            "NetworkOut",
            "DiskReadOps",
            "DiskWriteOps",
            "StatusCheckFailed"
        ]

        timestamp = datetime.now(UTC)

        #Loop throuh EC2 instances
        for instance_id in INSTANCE_IDS:

            logger.info(f"Processing instance: {instance_id}")

            for metric_name in metrics:

                value = get_metric(
                    instance_id,
                    metric_name,
                    start_time,
                    end_time
                )

                store_metric(
                    instance_id,
                    metric_name,
                    value,
                    timestamp
                )

        logger.info("Lambda execution completed")

        return {
            "statusCode": 200,
            "body": "Metrics stored successfully"
        }

    except Exception as e:

        logger.error(f"Lambda failed: {str(e)}")

        return {
            "statusCode": 500,
            "body": str(e)
        }