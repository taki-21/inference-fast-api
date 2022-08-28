# import inspect
import os
import traceback
import typing as t

import sampledetection.output_result as op
import sampledetection.text_recognition as tr
from loguru import logger
from schemas.webhook_response import ImageSize, Result
from sampledetection.preprocessing import Preprocessing
from sampledetection.text_detection import Detector

MODEL_PATH = os.getenv(
    'MODEL_PATH', './weights/XXX.pt')
PRETRAINED_WEIGHT_PATH = os.getenv('PRETRAINED_WEIGHT_PATH', 'weights')
OCR_KEY_PATH = os.getenv(
    'OCR_KEY_PATH', './ocr_key/XXX.json')


class SampleDetectionAnalysis():
    def __init__(self) -> None:
        try:
            logger.debug('model file read!')
            with open(MODEL_PATH, "rb") as f:
                weight_file = f.read()
            self._detector = Detector(
                weight_file=weight_file,
                pretrained_weight_path=PRETRAINED_WEIGHT_PATH)

        except Exception as e:
            logger.info('Analysis model initialization error.')
            logger.info(e)
            logger.info(traceback.format_exc())
            raise SampleDetectionAnalysisError()

    def execute(self, target_data: bytes, dsize=(
            2339, 1654)) -> t.Union[Result, None]:
        try:
            logger.debug('execute!!')
            preprocessing = Preprocessing(target_data)
            original_drawing_area = preprocessing.img
            origin_image_size = preprocessing.img_size
            resized_drawing_area = preprocessing.resized_img
            detected_box_list = self._detector.detect_text_area(
                resized_drawing_area)
            fitted_detected_box_list = self._detector.fit_to_img_size(
                origin_image_size, dsize, detected_box_list)
            text_list = tr.recognize_texts(
                original_drawing_area, fitted_detected_box_list, OCR_KEY_PATH)
            is_str = False
            for text in text_list:
                if len(text[0]) != 0:
                    is_str = True
            if not is_str:
                raise SampleDetectionAnalysisError()
            output_result = op.output_result(text_list, origin_image_size)
            img_size = ImageSize(width=output_result['img_size']['width'],
                                 height=output_result['img_size']['height'])
            text_result = output_result['text']
            return Result(img_size=img_size, text=text_result)
        except Exception as e:
            logger.info('Execution error.')
            logger.info(e)
            logger.info(traceback.format_exc())
            raise SampleDetectionAnalysisError()


class SampleDetectionAnalysisError(Exception):
    def __str__(self):
        return "Sample-Detection analysis Error"


sample_detection_analysis_obj = SampleDetectionAnalysis()
