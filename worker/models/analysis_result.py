import json
import os

from lib.aws_resource import AwsResource
from lib.object_key import ObjectKey
from lib.s3_client import S3Client
from schemas.webhook_response import SavedResult

SAVE_RESULT_DIR = os.getenv('SAVE_RESULT_DIR', 'analysis_result/')


class AnalysisResult():
    def __init__(self, saved_result: SavedResult):
        self.saved_result = saved_result

    def save(self) -> bool:
        file_name = os.path.splitext(os.path.basename(
            self.saved_result.target_data_s3path))[0]
        s3_client = S3Client(AwsResource.s3())
        object_key = ObjectKey.make_object_key('json', file_name)
        rtn = s3_client.put_object(SAVE_RESULT_DIR + object_key,
                                   json.dumps(self.saved_result.dict()))

        return bool(rtn)
