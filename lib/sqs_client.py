import json
import os
import typing as t

QUEUE_NAME = os.environ['QUEUE_NAME']
MESSAGE_GROUP_ID = os.getenv('MESSAGE_GROUP_ID', 'analysis-message')


class SqsClient():
    def __init__(self, sqs_resource, queue: str = None):
        self._sqs_resource = sqs_resource
        queue_name = queue if queue is not None else QUEUE_NAME
        self._queue = self._sqs_resource.get_queue_by_name(
            QueueName=queue_name)

    def get_messages(self):
        return self._queue.receive_messages(VisibilityTimeout=60 * 10)

    def set_messages(self, message_dict: dict) -> t.Union[str, None]:
        rtn = self._queue.send_message(MessageBody=json.dumps(message_dict),
                                       MessageGroupId=MESSAGE_GROUP_ID)

        if rtn['ResponseMetadata']['HTTPStatusCode'] == 200:
            return rtn['MessageId']
        else:
            return None
