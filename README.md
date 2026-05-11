# The goal of this project is to create an AWS monitoring dashboard using Python

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