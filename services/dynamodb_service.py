import boto3
from config import AWS_REGION

dynamodb = boto3.client(
    "dynamodb",
    region_name=AWS_REGION
)

def get_tables():

    response = dynamodb.list_tables()

    return response["TableNames"]