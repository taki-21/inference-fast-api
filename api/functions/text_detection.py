import json
import typing as t

from lib.aws_resource import AwsResource
from lib.binary_data import BinaryData
from lib.object_key import ObjectKey
from lib.s3_client import S3Client
from lib.sqs_client import SqsClient
from schemas.api_model import ApiModel
from schemas.api_response import ApiResponse, ApiResponseError
from schemas.sqs_message import SqsMessage


def lambda_handler(event, context):
    api_model = ApiModel.parse_raw(event['body'])
    message_id = execute(api_model)
    if message_id:
        api_response = ApiResponse(message='Accepted', request_id=message_id)
        return {"statusCode": 200, "body": json.dumps(api_response.dict())}
    else:
        api_response = ApiResponseError(
            message='Failed to register for data analysis')
        return {"statusCode": 500, "body": json.dumps(api_response.dict())}


def execute(target_data: ApiModel) -> t.Union[str, None]:
    try:
        binary_data = BinaryData.decode_from_str(
            target_data.drawing_pdf_data)
        object_key = ObjectKey.make_object_key('pdf')

        s3_client = S3Client(AwsResource.s3())
        s3_put_object = s3_client.put_object(object_key, binary_data)
        print(f's3 put object : {object_key}')

        if not s3_put_object:
            print('Failed to save the data to S3')
            return None

        sqs_message = SqsMessage(image_key=object_key,
                                 webhook_url=target_data.webhook_url,
                                 metadata=target_data.metadata)
        sqs_client = SqsClient(AwsResource.sqs())
        message_id = sqs_client.set_messages(sqs_message.dict())
        if message_id is None:
            print('Failed to send a message to SQS')
            return None

        print(f'sqs msgid : {message_id}')
        return message_id

    except Exception as e:
        print(e)
        return None
