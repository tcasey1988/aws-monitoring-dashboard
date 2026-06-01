from flask import Blueprint, jsonify
from datetime import datetime
from services.ec2_service import get_ec2_instances
from services.lambda_service import get_lambda_functions
from services.dynamodb_service import get_tables
from utils.logger import logger

api = Blueprint("api", __name__)

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

@api.route("/api/health")
def health_check():

    logger.info("Health endpoint called")

    return jsonify({
        "status": "success",
        "timestamp": datetime.utcnow().isoformat(),
        "message": "API is healthy"
    })
	
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