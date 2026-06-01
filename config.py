import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

DYNAMODB_TABLE = os.getenv("DYNAMO_TABLE", "MonitoringDashboard")

