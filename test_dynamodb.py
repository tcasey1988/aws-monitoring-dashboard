from services.dynamodb_service import get_metrics

metrics = get_metrics()

print(metrics)