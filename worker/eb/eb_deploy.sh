#!/usr/bin/env bash

set -e

env_name=$1

if [ "$env_name" == "" ]
then
    echo "Usage: $0 <eb environment name>"
    exit 1
fi

cat $(pwd)/.ebextensions/option_settings.config.tmp | \
    sed -e "s/<%AccountId%>/${ACCOUNT_ID}/g" \
        -e "s/<%BucketName%>/${BUCKET_NAME}/g" > \
        $(pwd)/.ebextensions/option_settings.config

eb deploy ${env_name} \
   --profile default
