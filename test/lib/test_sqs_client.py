import json

from lib.aws_resource import AwsResource
from lib.sqs_client import SqsClient


def test_set_and_get_messages():
    sqs = AwsResource.sqs()
    sqs_client = SqsClient(sqs, 'test_queue')
    rtn = sqs_client.set_messages({'message': 'test'})
    assert rtn is not None
    assert type(rtn) == str

    rtn = sqs_client.get_messages()
    body = json.loads(rtn[0].body)
    assert body['message'] == 'test'
