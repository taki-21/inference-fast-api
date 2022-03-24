from lib.aws_resource import AwsResource
from lib.s3_client import S3Client


def test_put_object(test_pdf_data):
    s3 = AwsResource.s3()
    s3_client = S3Client(s3)
    rtn = s3_client.put_object('test.pdf', test_pdf_data)
    assert rtn is not None


def test_get_object(test_pdf_data):
    s3 = AwsResource.s3()
    s3_client = S3Client(s3)
    s3_client.put_object('test.pdf', test_pdf_data)
    rtn = s3_client.get_object('test.pdf')
    assert type(rtn) == bytes
    assert rtn is not None
