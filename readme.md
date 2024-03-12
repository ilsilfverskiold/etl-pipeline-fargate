# ETL Pipeline for BigQuery on AWS ECS with Fargate

This repository contains a template for setting up a serverless long-running ETL pipeline that extracts data from Google BigQuery, transforms it, and loads it back. This README guides you through setting up and deploying the ETL pipeline on AWS ECS with AWS Fargate.

Follow the tutorial [here](https://medium.com/towards-data-science/deploy-long-running-etl-pipelines-to-ecs-with-fargate-01ab19c6d2a8) if you need help setting this up. 

## Prerequisites

- Python 3.8+
- Docker
- AWS CLI configured with appropriate permissions
- Google Cloud account with BigQuery access

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/ilsilfverskiold/etl-pipeline-fargate.git
cd etl-pipeline-fargate
```

### 2. BigQuery Configuration

- Create a BigQuery table with a name field as a string and insert some rows with the name "Doe".
- Create a service account in Google Cloud IAM with BigQuery User access.
- Add the service account to your dataset in BigQuery with appropriate permissions.
- Download the service account key as a JSON file and place it in the root directory of this project.
- Make sure you change the table_id in the main.py file.

### 3. Run Locally

#### Create and activate a Python virtual environment:

```bash
python -m venv etl-env
source etl-env/bin/activate  # On Windows use `venv\Scripts\activate`
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the script:

```bash
python main.py
```

Successful execution will log "New rows have been added"

### Docker Image

Build the Docker image:

```bash
docker buildx build --platform=linux/amd64 -t bigquery-etl-pipeline .
```

Run the Docker container locally (optional):

```bash
docker run bigquery-etl-pipeline
```

### AWS Deployment

Create an ECR repository:

```bash
aws ecr create-repository --repository-name bigquery-etl-pipeline
```

Authenticate Docker to AWS ECR and push the image:

```bash
aws ecr get-login-password --region YOUR_REGION | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com
docker tag bigquery-etl-pipeline:latest YOUR_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com/bigquery-etl-pipeline:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.YOUR_REGION.amazonaws.com/bigquery-etl-pipeline:latest
```

### Create Task and Execution Roles

Refer to the provided JSON files in the repository to create the necessary IAM roles for task execution and logging.

### Create Log Group

```bash
aws logs create-log-group --log-group-name /ecs/etl-pipeline-logs
```

### Register Task Definition

Update task-definition.json with your AWS account ID, region, and ECR image URI. Make sure you've created the task and execution roles that are in the task definition. Then, register the task definition:

```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

### Schedule the Task to run with EventBridge

#### Create a scheduled rule:

```bash
aws events put-rule --name "ETLPipelineDailyRun" --schedule-expression "cron(0 5 * * ? *)" --state ENABLED
```

#### Attach the ECS task as a target:

```bash
aws events put-targets --rule "ETLPipelineDailyRun" --targets "[{\"Id\":\"1\",\"Arn\":\"arn:aws:ecs:REGION:ACCOUNT_NUMBER:cluster/etl-pipeline-cluster\",\"RoleArn\":\"arn:aws:iam::ACCOUNT_NUMBER:role/ecsEventsRole\",\"EcsParameters\":{\"TaskDefinitionArn\":\"arn:aws:ecs:REGION:ACCOUNT_NUMBER:task-definition/my-etl-task\",\"TaskCount\":1,\"LaunchType\":\"FARGATE\",\"NetworkConfiguration\":{\"awsvpcConfiguration\":{\"Subnets\":[\"SUBNET_ID\"],\"SecurityGroups\":[\"SECURITY_GROUP_ID\"],\"AssignPublicIp\":\"ENABLED\"}}}}]"
```

Replace placeholders with your actual AWS region, account number, subnet IDs, and security group IDs. To get subnet and security group ids run

```bash
aws ec2 describe-subnets
```

And for security groups.

```bash
aws ec2 describe-security-groups
```