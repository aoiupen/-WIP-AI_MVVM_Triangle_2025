"""
ML 모델 어댑터 인터페이스

이 모듈은 다양한 ML 프레임워크를 추상화하는 기본 어댑터 인터페이스를 정의합니다.
새로운 ML 프레임워크 지원을 추가하려면 이 인터페이스를 구현하는 새 어댑터를 생성하세요.
"""

from abc import ABC, abstractmethod

class MLModelAdapter(ABC):
    """
    ML 모델 어댑터 인터페이스
    
    다양한 ML 프레임워크(TensorFlow, PyTorch, ONNX 등)에 대한 
    일관된 인터페이스를 제공하는 추상 기본 클래스입니다.
    """
    
    @abstractmethod
    def load_model(self, model_path):
        """
        모델 파일을 로드합니다.
        
        Args:
            model_path (str): 모델 파일 경로
            
        Returns:
            object: 로드된 모델 객체
        """
        pass
    
    @abstractmethod
    def predict(self, model, input_data):
        """
        입력 데이터에 대한 예측을 수행합니다.
        
        Args:
            model (object): load_model로 로드된 모델 객체
            input_data (list or numpy.ndarray): 입력 데이터
            
        Returns:
            float: 예측 결과 (0~1 사이 값)
        """
        pass
    
    @abstractmethod
    def get_framework_name(self):
        """
        사용 중인 ML 프레임워크 이름을 반환합니다.
        
        Returns:
            str: 프레임워크 이름 (예: "TensorFlow", "PyTorch")
        """
        pass