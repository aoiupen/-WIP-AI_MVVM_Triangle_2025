"""
ML 모델 어댑터 팩토리

이 모듈은 적절한 ML 모델 어댑터를 생성하는 팩토리 함수를 제공합니다.
"""

# 절대 경로 임포트 대신 상대 경로 임포트 사용
from .tf_adapter import TensorFlowAdapter

def get_adapter(framework="tensorflow"):
    """
    지정된 프레임워크에 대한 어댑터를 반환합니다.
    
    Args:
        framework (str): ML 프레임워크 이름 (기본값: "tensorflow")
        
    Returns:
        MLModelAdapter: 요청된 프레임워크에 대한 어댑터 인스턴스
        
    Raises:
        ValueError: 지원되지 않는 프레임워크가 요청된 경우
    """
    framework = framework.lower()
    
    if framework == "tensorflow":
        return TensorFlowAdapter()
    # 향후 다른 프레임워크 지원 추가
    # elif framework == "pytorch":
    #     return PyTorchAdapter()
    # elif framework == "onnx":
    #     return ONNXAdapter()
    else:
        raise ValueError(f"지원되지 않는 프레임워크: {framework}")