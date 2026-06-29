import boto3
from config import AWS_REGION

# create Lambda client
lambda_client = boto3.client(
    "lambda",
    region_name=AWS_REGION
)

# get the list of Lambda functions and their runtimes
def get_lambda_functions():

    response = lambda_client.list_functions()

    functions = []

    for function in response["Functions"]:

        functions.append({
            "function_name": function["FunctionName"],
            "runtime": function["Runtime"]
        })

    return functions