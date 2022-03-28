import os

BUCKET_NAME = os.environ['BUCKET_NAME']


class S3Client():
    def __init__(self, s3_resource, bucket: str = None):
        self._s3_resource = s3_resource
        self._s3_bucket = bucket if bucket is not None else BUCKET_NAME

    def put_object(self, name: str, data):
        return self._s3_resource.Bucket(self._s3_bucket).put_object(Key=name, Body=data)

    def get_object(self, name: str) -> bytes:
        s3_obj = self._s3_resource.Object(self._s3_bucket, name)
        return s3_obj.get()["Body"].read()

    def delete_object(self, name: str) -> dict:
        s3_obj = self._s3_resource.Object(self._s3_bucket, name)
        return s3_obj.delete()
