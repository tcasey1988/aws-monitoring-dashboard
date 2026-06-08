import boto3
from config import AWS_REGION

dynamodb = boto3.client(
    "dynamodb",
    region_name=AWS_REGION
)

def get_tables():

    dynamodb = boto3.client('dynamodb')

    response = dynamodb.list_tables()

    table_data = []

    for table_name in response['TableNames']:

        table_details = dynamodb.describe_table(
            TableName=table_name
        )

        table_data.append({
            "table_name": table_name,
            "item_count": table_details['Table']['ItemCount']
        })

    return table_data