# AWS Monitoring Dashboard Project

# Overview

The AWS Monitoring Dasbhoard is a cloud monitoring
solution built using EC2, CloudWatch, Lambda, DynamoDB,
EventBridge, SNS, and Flask.

This Dashboard collects infrastructure metrics, stores them to DynamoDB,
displays metrics in a web Dashboard, and performs auto-remediatino when CloudWatch alarms are triggered.

# Architecture
<img width="321" height="761" alt="dashboard_diagram drawio" src="https://github.com/user-attachments/assets/1f97d710-9baa-4f20-90aa-92e7a7d21096" />

# AWS Services Used
-EC2
-CloudWatch
-Lambda
-DynamoDB
-EventBridge
-SNS
-Systems Manager

# Features
-Real-time metric monitoring
-CloudWatch alarm visibility
-Auto-refresh dashboard
-Automated remediation
-Email notification
-Remediation tracking

# Screenshots:
Auto-Remediation working:
<img width="606" height="742" alt="auto-remediation" src="https://github.com/user-attachments/assets/f0d2effe-c0aa-4c9a-8cbb-23fb670c323b" />

Lambda monitoring chart:
<img width="1031" height="627" alt="lambda_chart" src="https://github.com/user-attachments/assets/829f6eb7-4074-4de4-8fc9-d4c310bd7ace" />
DynamoDB monitoring chart:
<img width="1017" height="612" alt="dynamodb_chart" src="https://github.com/user-attachments/assets/0df15a6c-1717-4dd2-89db-115528ac2b79" />
EC2 CPU monitoring chart:
<img width="1092" height="682" alt="cpu_chart" src="https://github.com/user-attachments/assets/be9c5376-d027-4895-8067-4cb6b5209cd3" />
EventBridge schedule:
<img width="1912" height="882" alt="eventbridge_schedule" src="https://github.com/user-attachments/assets/ab7f0dff-8d22-44c0-98dc-8980c62b82f0" />
EC2 instance running:
<img width="1875" height="862" alt="ec2_instance" src="https://github.com/user-attachments/assets/dc0dd1f0-33b1-42a6-bfb1-bfb93538ba37" />
DynamoDB table:
<img width="1917" height="870" alt="dynamodb_table" src="https://github.com/user-attachments/assets/81a6ebea-ddef-4442-ad64-dc8385a547c8" />
Lambda function:
<img width="1851" height="835" alt="lamba_function" src="https://github.com/user-attachments/assets/87d70531-ad1f-4b8e-8278-3731e7f82e21" />
Flask terminal running and site working:
<img width="1092" height="317" alt="flask_terminal" src="https://github.com/user-attachments/assets/60c0c809-44b4-4ac1-8250-cbd615a88068" />
API metrics running:
<img width="790" height="927" alt="api_metrics" src="https://github.com/user-attachments/assets/0aad232d-7899-405c-9448-ccfe276c6aa3" />

# Future Enhancements
-ECS deployment
-Docker containers
-Terraform deployment
-CloudWatch dashboards
-RDS integratin
-Multi-account monitoring
