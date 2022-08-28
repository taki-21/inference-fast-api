#!/bin/bash -eu

deploy_key=$(aws secretsmanager get-secret-value --secret-id sample-detection-deploy-key --region ap-northeast-1 |  jq '.SecretString' | jq -r . | jq -r '.["deploy-key"]')
bucket_name=$(/opt/elasticbeanstalk/bin/get-config environment | jq -r .BUCKET_NAME)
queue_name=$(/opt/elasticbeanstalk/bin/get-config environment | jq -r .QUEUE_NAME)

aws s3 sync s3://${bucket_name}/weights /var/app/weights --quiet

echo "DEPLOY_KEY=${deploy_key}" > .env
echo "BUCKET_NAME=${bucket_name}" >> .env
echo "QUEUE_NAME=${queue_name}" >> .env
