from functions.sample_detection import execute, lambda_handler
from lib.s3_client import S3Client
from lib.sqs_client import SqsClient
from schemas.api_response import ApiResponse, ApiResponseError


def put_object_mock(self, name: str, data):
    return None


def set_messages_mock(messages: dict):
    return None


def test_execute(test_api_model):
    message_id = execute(test_api_model)
    assert message_id is not None
    assert isinstance(message_id, str)


def test_execute_s3_error(test_api_model, monkeypatch):
    monkeypatch.setattr(S3Client, "put_object", put_object_mock)
    message_id = execute(test_api_model)
    assert message_id is None


def test_execute_sqs_error(test_api_model, monkeypatch):
    monkeypatch.setattr(SqsClient, "set_messages", set_messages_mock)
    message_id = execute(test_api_model)
    assert message_id is None


def test_lambda_handler(test_api_model):
    event = {}
    event['body'] = test_api_model.json()
    rtn = lambda_handler(event, None)

    assert rtn['statusCode'] == 200
    response = ApiResponse.parse_raw(rtn['body'])
    assert response.message == 'Accepted'
    assert isinstance(response.request_id, str)


def test_lambda_handler_error(test_api_model, monkeypatch):
    monkeypatch.setattr(S3Client, "put_object", put_object_mock)
    event = {}
    event['body'] = test_api_model.json()
    rtn = lambda_handler(event, None)
    assert rtn['statusCode'] == 500
    response = ApiResponseError.parse_raw(rtn['body'])
    assert response.message == 'Failed to register for data analysis'
