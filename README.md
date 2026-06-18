# The goal of this project is to create an AWS monitoring dashboard using Python and AWS services

# This is the initial project setup
-Created an EC2 instance
-Deploy Nginx web server on the instance.
-Connected to server and generated CPU spike.
-Verified that metric is being tracked in CloudWatch.

# Services used
-EC2
-CloudWatch

# Added Backend infrastructure
-Created Python script that uses CloudWatch to gather EC2 data.
-Imported script in Lambda
-Stored data into DynamoDB table.
-Set up EventBridge to run the fuction automatically.

# Services used
-Lambda
-DynamoDB
-EventBridge
-CloudWatch

# Started setting up the Flask frontend
-Created Flask app to display dashboard metrics.
-Set up main page, Metrics page, and health check
-Created functions to query metrics from the DynamoDB Table

# Services used
-Flask
-Python
-DynamoDB

# Set up API Routes
-Created Flask API architecture
-Set up resuable AWS service modules.
-Added logging.
-Created API endpoints for:
	- EC2
	- Lambda
	- DynamoDB
	- Dashboard

# Set up charts to display metrics
-Used JavaScript to set up charts
-Set up chart to display EC2 instances and CPU usage
-Set up chart to display DynamoDB tables and ite count
-Added chart to show the number of Lambda functions
-Set up auto-refresh to provide real time monitoring of metrics

# Services used
-JavaScript
-HTML

# Added dashboard enhancements to improve monitoring
-Added widgets to display device health status
-Added device status to display if EC2 is on or stopped

# Services used
-JavaScript
-HTML/CSS

# Added Auto-Remediation 
-Set up auto-remediation using CloudWatch and EventBridge.
-Added EC2 to Systems Manager.
-Created Lambda function to automatically remediate alert.
-Saved remediation history to DynamoDB.
-Used SNS to sent notification to emal.
-Added widgets to dashboard to display statistics and alert history.

# Services used
-CloudWatch
-EventBridge
-Lambda
-DynamoDB
-SNS
-JavaScript, HTML