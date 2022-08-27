from fastapi import Header, HTTPException, status
from lib.aws_resource import AwsResource
from lib.s3_client import S3Client
from models.sample_detector_analysis import (
    SampleDetectionAnalysis, sample_detector_analysis_obj)
from schemas.sqs_message import SqsMessage


def get_analysis_target_data(sqs_message: SqsMessage) -> bytes:
    s3_client = S3Client(AwsResource.s3())
    s3_object = s3_client.get_object(sqs_message.object_key)
    return s3_object


def get_msgid_from_header(x_aws_sqsd_msgid: str = Header(None)) -> str:
    if not x_aws_sqsd_msgid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Sqsd-Msgid header invalid")
    return x_aws_sqsd_msgid


def get_analysis_instance() -> SampleDetectionAnalysis:
    return sample_detector_analysis_obj
