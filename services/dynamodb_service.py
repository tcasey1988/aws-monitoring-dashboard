import boto3
import logging
from decimal import Decimal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MonitoringMetrics')

def convert_decimals(obj):

    if isinstance(obj, list):
        return [convert_decimals(i) for i in obj]

    elif isinstance(obj, dict):
        return {k: convert_decimals(v) for k, v in obj.items()}

    elif isinstance(obj, Decimal):
        return float(obj)

    return obj
	
def get_metrics():

    try:

        response = table.scan()

        items = response.get('Items', [])

        cleaned_items = convert_decimals(items)

        return cleaned_items

    except Exception as e:

        logger.exception(f"Error retrieving metrics: {str(e)}")

        return []