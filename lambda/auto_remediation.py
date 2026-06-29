import boto3
import uuid
import os
from datetime import datetime

# Set up AWS clients
ssm = boto3.client("ssm")
dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")

# Get environment variables
INSTANCE_ID = os.environ.get("INSTANCE_ID")
TABLE_NAME = os.environ.get("TABLE_NAME")
SNS_TOPIC_ARN = os.environ.get("SNS_TOPIC_ARN")

# Lambda function handler
def lambda_handler(event, context):

    table = dynamodb.Table(TABLE_NAME)

    try:

        # Execute the SSM command to restart nginx
        event_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        response = ssm.send_command(
            InstanceIds=[INSTANCE_ID],
            DocumentName="AWS-RunShellScript",
            Parameters={
                "commands": [
                    "sudo systemctl restart nginx"
                ]
            }
        )

        command_id = response["Command"]["CommandId"]

        table.put_item(
            Item={
                "event_id": event_id,
                "timestamp": timestamp,
                "instance_id": INSTANCE_ID,
                "action": "Restart nginx",
                "command_id": command_id,
                "status": "SUCCESS"
            }
        )

        message = f"""
        Auto Remediation Executed

        Instance:
        {INSTANCE_ID}

        Action:
        Restart nginx

        Command ID:
        {command_id}

        Timestamp:
        {timestamp}
        """

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="Auto Remediation SUCCESS",
            Message=message
        )

        return {
            "statusCode": 200,
            "body": {
                "event_id": event_id,
                "command_id": command_id,
                "status": "SUCCESS"
            }
        }

    except Exception as e:

        try:

            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="Auto Remediation FAILURE",
                Message=str(e)
            )

        except Exception:
            pass

        raise e