"""
TensorFlow 모델 어댑터

이 모듈은 TensorFlow 모델을 로드하고 예측을 수행하는 어댑터를 제공합니다.
MLModelAdapter 인터페이스를 구현하여 TensorFlow 의존성을 캡슐화합니다.
"""

import numpy as np
from models.adapters.base_adapter import MLModelAdapter
import os

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
            Exception: 모델 로드 실패 시 발생
        """
        import tensorflow as tf
        
        try:
            if os.path.exists(model_path):
                # 실제 모델 파일이 존재하는 경우
                model = tf.keras.models.load_model(model_path)
                print(f"모델 파일 '{model_path}'을 성공적으로 로드했습니다.")
            else:
                # 모델 파일이 없는 경우 경고 로그 출력
                print(f"모델 파일 '{model_path}'이 존재하지 않습니다. 기본 모델을 생성합니다.")
                
                # 기본 모델 생성
                model = tf.keras.Sequential([
                    tf.keras.layers.Dense(64, activation='relu', input_shape=(3,)),
                    tf.keras.layers.Dense(1, activation='sigmoid')
                ])
                model.compile(optimizer='adam', loss='binary_crossentropy')
                
                # 모델 저장 디렉토리 생성 (선택사항)
                try:
                    os.makedirs(os.path.dirname(model_path), exist_ok=True)
                    model.save(model_path)
                    print(f"기본 모델을 '{model_path}'에 저장했습니다.")
                except Exception as save_error:
                    print(f"기본 모델 저장 실패: {str(save_error)}")
            
            return model
        except Exception as e:
            raise Exception(f"TensorFlow 모델 로드 실패: {str(e)}")
    
    def predict(self, model, input_data):
        """
        TensorFlow 모델을 사용하여 예측을 수행합니다.
        
        Args:
            model (tf.keras.Model): 로드된 TensorFlow 모델
            input_data (list or numpy.ndarray): 입력 데이터
            
        Returns:
            float: 예측 결과 (0~1 사이 값)
        """
        import tensorflow as tf
        import numpy as np
        
        try:
            # 입력 데이터 전처리
            if isinstance(input_data, list):
                input_data = np.array(input_data)
            
            # 입력 형태 조정 (모델에 맞게)
            if len(input_data.shape) == 1:
                input_data = input_data.reshape(1, -1)
            
            # 정규화 (필요한 경우)
            input_data = input_data / 255.0  # 예시: 0-255 값을 0-1로 정규화
            
            # 예측 수행
            prediction = model.predict(input_data)
            
            # 결과 처리 (예: 첫 번째 출력값 반환)
            return float(prediction[0][0])
        except Exception as e:
            raise Exception(f"TensorFlow 예측 실패: {str(e)}")
    
    def get_framework_name(self):
        """
        프레임워크 이름 반환
        
        Returns:
            str: "TensorFlow"
        """
        return "TensorFlow"