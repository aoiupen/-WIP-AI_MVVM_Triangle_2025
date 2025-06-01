"""
삼각형 검증 모델

이 모듈은 삼각형의 세 변 길이를 입력받아 삼각형 형성 가능성을 예측하는
ML 모델을 관리합니다. 어댑터 패턴을 사용하여 ML 프레임워크 의존성을 관리합니다.
"""

import os
from models.adapters import get_adapter

class TriangleModel:
    """
    삼각형 검증을 위한 ML 모델 클래스
    
    이 클래스는 ML 모델을 로드하고 삼각형의 세 변 길이를 입력받아
    삼각형 가능성을 예측합니다. 어댑터 패턴을 사용하여 특정 ML 프레임워크에
    직접 의존하지 않습니다.
    """
    
    def __init__(self, model_path=None, framework="tensorflow"):
        """
        TriangleModel 초기화
        
        Args:
            model_path (str, optional): 모델 파일 경로. 기본값은 None으로,
                                       이 경우 기본 모델 경로가 사용됩니다.
            framework (str, optional): 사용할 ML 프레임워크. 기본값은 "tensorflow"
        """
        if model_path is None:
            # 기본 모델 경로 설정
            current_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(current_dir, "data", "triangle_model.h5")
        
        self.model_path = model_path
        self.adapter = get_adapter(framework)
        # self.model = None # 모델 인스턴스는 Core에서 관리
        
        # # 모델 로드 # Core에서 담당
        # self.load_model()
    
    # def load_model(self): # Core에서 담당
    #     """
    #     ML 모델을 로드합니다.
        
    #     Raises:
    #         Exception: 모델 로드 실패 시
    #     """
    #     try:
    #         self.model = self.adapter.load_model(self.model_path)
    #         print(f"{self.adapter.get_framework_name()} 모델 로드 성공")
    #     except Exception as e:
    #         print(f"모델 로드 실패: {str(e)}")
    #         raise
    
    # def predict(self, sides): # Core에서 담당
    #     """
    #     삼각형 가능성 예측
        
    #     Args:
    #         sides (list): 삼각형 세 변의 길이 [a, b, c]
            
    #     Returns:
    #         float: 삼각형 가능성 (0~1 사이 값, 1에 가까울수록 가능성 높음)
            
    #     Raises:
    #         Exception: 예측 실패 시
    #     """
    #     if self.model is None:
    #         raise Exception("모델이 로드되지 않았습니다.")
        
    #     try:
    #         result = self.adapter.predict(self.model, sides)
    #         return result
    #     except Exception as e:
    #         print(f"예측 실패: {str(e)}")
    #         raise

    # def validate(self, a, b, c): # Core에서 담당
    #     """
    #     세 변의 길이를 받아 예측 결과와 수학적 검증 결과를 모두 반환합니다.
    #     """
    #     sides = [a, b, c]
    #     ai_prediction_value = self.predict(sides)
    #     math_result = (a + b > c) and (a + c > b) and (b + c > a)
    #     is_valid_by_ai = ai_prediction_value > 0.5 if ai_prediction_value is not None else None

    #     # 인스턴스 변수로도 저장 (ViewModel에서 사용)
    #     self.sides = sides
    #     self.ai_prediction_value = ai_prediction_value
    #     self.math_result = math_result
    #     self.is_valid_by_ai = is_valid_by_ai

    #     return {
    #         "sides": sides,
    #         "math_result": math_result,
    #         "ai_prediction_value": ai_prediction_value,
    #         "is_valid_by_ai": is_valid_by_ai,
    #         "is_consistent": math_result == is_valid_by_ai if is_valid_by_ai is not None else None
    #     }

# Test
if __name__ == '__main__':
    # 모델 경로를 애플리케이션 루트 기준으로 수정
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    test_model_path = os.path.join(project_root, 'notebooks', 'model.h5')
    
    print(f"테스트 모델 경로: {test_model_path}")
    pass # 테스트 코드는 Core에서 수행