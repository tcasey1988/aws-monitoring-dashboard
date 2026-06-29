import boto3
from config import AWS_REGION

# create DynamoDB client
dynamodb = boto3.client(
    "dynamodb",
    region_name=AWS_REGION
)

# get the list of DynamoDB tables and their item counts
def get_tables():

    dynamodb = boto3.client('dynamodb')

    response = dynamodb.list_tables()

    table_data = []

    # iterate through the list of table names and get their item counts
    for table_name in response['TableNames']:

        table_details = dynamodb.describe_table(
            TableName=table_name
        )

        table_data.append({
            "table_name": table_name,
            "item_count": table_details['Table']['ItemCount']
        })

    return table_data

# get the remediation history from the AutoRemediationHistory DynamoDB table
def get_remediation_history():

    resource = boto3.resource(
        "dynamodb",
        region_name=AWS_REGION
    )

    table = resource.Table(
        "AutoRemediationHistory"
    )

    response = table.scan()

    items = response.get(
        "Items",
        []
    )

    items = sorted(
        items,
        key=lambda x: x.get(
            "timestamp",
            ""
        ),
        reverse=True
    )

    return items[:20]