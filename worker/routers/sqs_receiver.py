import json
import sys
import traceback

import requests
from fastapi import APIRouter, Depends, Response, status
from loguru import logger
from models.analysis_result import AnalysisResult
from models.sample_detection_analysis import SampleDetectionAnalysisError
from schemas.sqs_message import SqsMessage
from schemas.sqs_receiver import SqsReceiverOut
from schemas.webhook_response import (ResponseStatus, SavedResult,
                                      WebHookResponse)

from routers import dependencies

logger.remove()
logger.add(sys.stdout, format="{time} - {level} - {message}", level="DEBUG")

sqs_receiver_router = r = APIRouter()


@r.post("/sqs_receiver",
        response_model=SqsReceiverOut,
        status_code=status.HTTP_200_OK)
async def sqs_receive(sqs_message: SqsMessage,
                      response: Response,
                      msgid=Depends(dependencies.get_msgid_from_header),
                      analysis_instance=Depends(dependencies.get_analysis_instance)):

    web_hook_response_status = ResponseStatus.success
    message = 'OK'
    result = None
    try:
        logger.info(f'Start of worker execution. message-iD : {msgid}')
        logger.debug('Start of worker execution')
        analysis_target_data = dependencies.get_analysis_target_data(
            sqs_message)
        result = analysis_instance.execute(analysis_target_data)
        logger.info(f'result : {result}')

        if result is None:
            logger.error(f'Error. message-iD : {msgid}')
            logger.debug('Error1')

            web_hook_response_status = ResponseStatus.error
            message = 'Analysis error'
        else:
            analysis_result_data = AnalysisResult(
                SavedResult(
                    id=msgid,
                    result=result,
                    target_data_s3path=sqs_message.image_key
                )
            )
            analysis_result_data.save()

    except SampleDetectionAnalysisError as e:
        logger.error(f'Error. message-iD : {msgid}')
        logger.debug('Error2')
        logger.error(e)
        logger.error(traceback.format_exc())
        web_hook_response_status = ResponseStatus.error
        message = 'Analysis error'

    except Exception as e:
        logger.error(f'Error. message-iD : {msgid}')
        logger.debug('Error3')
        logger.error(e)
        logger.error(traceback.format_exc())
        web_hook_response_status = ResponseStatus.error
        message = 'Server Error'

    finally:
        web_hook_response = WebHookResponse(id=msgid,
                                            status=web_hook_response_status,
                                            result=result,
                                            message=message,
                                            metadata=sqs_message.metadata)
        web_hook_post_response = requests.post(
            sqs_message.webhook_url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(web_hook_response.dict()),
        )
        web_hook_post_status_code = web_hook_post_response.status_code
        logger.info(f'Webhook post status : {web_hook_post_status_code}')

        if (web_hook_post_status_code != status.HTTP_200_OK) and (
                web_hook_post_status_code != status.HTTP_201_CREATED):
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return SqsReceiverOut(status='ok')
