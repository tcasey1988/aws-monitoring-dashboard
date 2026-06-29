from flask import Blueprint, jsonify
from datetime import datetime

# import AWS services
from services.ec2_service import get_ec2_instances, get_ec2_cpu_metrics, get_instance_status, get_cloudwatch_alarms, get_system_health
from services.lambda_service import get_lambda_functions
from services.dynamodb_service import get_tables, get_remediation_history
from utils.logger import logger

api = Blueprint("api", __name__)

# returns Lambda information
@api.route("/api/lambda")
def lambda_data():

    logger.info("Fetching Lambda functions")

    try:

        functions = get_lambda_functions()

        return jsonify({
            "status": "success",
            "data": functions
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# return endpoint Health
@api.route("/api/health")
def health_check():

    logger.info("Health endpoint called")

    return jsonify({
        "status": "success",
        "timestamp": datetime.utcnow().isoformat(),
        "message": "API is healthy"
    })
	
# return EC2 information
@api.route("/api/ec2")
def ec2_data():

    logger.info("Fetching EC2 data")

    try:

        instances = get_ec2_instances()

        return jsonify({
            "status": "success",
            "data": instances
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
		
# returns DynamoDB table information
@api.route("/api/dynamodb")
def dynamodb_data():

    logger.info("Fetching DynamoDB tables")

    try:

        tables = get_tables()

        return jsonify({
            "status": "success",
            "data": tables
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# returns the Dashboard		
@api.route("/api/dashboard")
def dashboard_data():

    logger.info("Dashboard endpoint requested")

    try:

        ec2_instances = get_ec2_instances()

        lambda_functions = get_lambda_functions()

        dynamodb_tables = get_tables()

        return jsonify({
            "status": "success",
            "data": {
                "ec2": ec2_instances,
                "lambda": lambda_functions,
                "dynamodb": dynamodb_tables
            }
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
# return EC2 cpu information
@api.route("/api/ec2/cpu")
def ec2_cpu_data():

    logger.info("Fetching EC2 CPU metrics")

    try:

        metrics = get_ec2_cpu_metrics()

        return jsonify({
            "status": "success",
            "data": metrics
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
# returns EC2 status information
@api.route('/api/status')
def api_status():

    logger.info("Fetching EC2 status")

    try:

        status = get_instance_status()

        return jsonify({
            "status": "success",
            "data": status
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
# returns CloudWatch alarms
@api.route('/api/alarms')
def alarms_data():

    logger.info("Fetching CloudWatch alarms")

    try:

        alarms = get_cloudwatch_alarms()

        return jsonify({
            "status": "success",
            "data": alarms
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# returns system health
@api.route('/api/system-health')
def system_health():

    logger.info("Fetching system health")

    try:

        health = get_system_health()

        return jsonify({
            "status": "success",
            "data": health
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
# returns the remediation history
@api.route("/api/remediation-history")
def remediation_history():

    try:

        history = get_remediation_history()

        return jsonify({
            "status": "success",
            "data": history
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500