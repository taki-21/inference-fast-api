import os

import boto3


class AwsResource():

    @classmethod
    def s3(cls):
        params = cls.__set_base_resource()
        if 'AWS_S3_ENDPOINT' in os.environ:
            params['endpoint_url'] = os.environ['AWS_S3_ENDPOINT']

        return boto3.resource('s3', **params)

    @classmethod
    def sqs(cls):
        params = cls.__set_base_resource()
        if 'AWS_SQS_ENDPOINT' in os.environ:
            params['endpoint_url'] = os.environ['AWS_SQS_ENDPOINT']

        return boto3.resource('sqs', **params)

    @classmethod
    def __set_base_resource(cls):
        params = {}
        if 'AWS_DEFAULT_REGION' in os.environ:
            params['region_name'] = os.environ['AWS_DEFAULT_REGION']
        else:
            params['region_name'] = 'ap-northeast-1'

        return params
