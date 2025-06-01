"""
TensorFlow 모델 어댑터

이 모듈은 TensorFlow 모델을 로드하고 예측을 수행하는 어댑터를 제공합니다.
MLModelAdapter 인터페이스를 구현하여 TensorFlow 의존성을 캡슐화합니다.
"""

import numpy as np
from models.adapters.base_adapter import MLModelAdapter
import os
import logging

logger = logging.getLogger(__name__)

class TensorFlowAdapter(MLModelAdapter):
    """
    TensorFlow 모델을 위한 어댑터 구현
    
    TensorFlow 의존성을 이 클래스 내부로 제한하여
    애플리케이션의 다른 부분이 TensorFlow에 직접 의존하지 않도록 합니다.
    """
    
    def load_model(self, model_path):
        """
        TensorFlow 모델을 로드합니다.
        
        Args:
            model_path (str): 모델 파일 경로
            
        Returns:
            object: 로드된 TensorFlow 모델
        
        Raises:
            FileNotFoundError: 모델 파일이 존재하지 않을 경우
            Exception: 기타 모델 로드 실패 시 발생
        """
        import tensorflow as tf
        
        if not os.path.exists(model_path):
            logger.error(f"모델 파일을 찾을 수 없습니다: {model_path}")
            raise FileNotFoundError(f"모델 파일 '{model_path}'이 존재하지 않습니다.")
        
        try:
            model = tf.keras.models.load_model(model_path)
            logger.info(f"모델 파일 '{model_path}'을 성공적으로 로드했습니다.")
            return model
        except Exception as e:
            logger.error(f"TensorFlow 모델 로드 중 오류 발생 ({model_path}): {e}", exc_info=True)
            raise Exception(f"TensorFlow 모델 로드 실패 ({model_path}): {str(e)}")
    
    def predict(self, model, input_data, scaler=None):
        """
        TensorFlow 모델을 사용하여 예측을 수행합니다.
        
        Args:
            model (tf.keras.Model): 로드된 TensorFlow 모델
            input_data (list or numpy.ndarray): 입력 데이터
            scaler (sklearn.preprocessing.StandardScaler, optional): 학습된 스케일러 객체. Defaults to None.
            
        Returns:
            float: 예측 결과 (0~1 사이 값)
        """
        if scaler is None:
            logger.error("예측을 위한 스케일러(scaler) 객체가 제공되지 않았습니다.")
            raise ValueError("스케일러 객체가 필요합니다.")

        try:
            # 입력 데이터 전처리 (numpy array로 변환)
            if isinstance(input_data, list):
                processed_input_data = np.array(input_data)
            elif isinstance(input_data, np.ndarray):
                processed_input_data = input_data
            else:
                logger.error(f"잘못된 input_data 타입: {type(input_data)}")
                raise ValueError("input_data는 list 또는 numpy.ndarray 여야 합니다.")

            if len(processed_input_data.shape) == 1:
                processed_input_data = processed_input_data.reshape(1, -1)
            
            # 제공된 스케일러로 변환
            scaled_data = scaler.transform(processed_input_data)
            logger.debug(f"스케일링된 데이터: {scaled_data.tolist()}")

            # 예측 수행
            prediction = model.predict(scaled_data)
            result = float(prediction[0][0])
            logger.debug(f"모델 예측 결과 (raw): {prediction.tolist()}, 최종 반환 값: {result}")
            return result
        except Exception as e:
            logger.error(f"TensorFlow 예측 실패: {e}", exc_info=True)
            raise Exception(f"TensorFlow 예측 실패: {str(e)}")
    
    def get_framework_name(self):
        """
        프레임워크 이름 반환
        
        Returns:
            str: "TensorFlow"
        """
        return "TensorFlow"