import numpy as np
import tensorflow as tf
import os
import sys

# 모델 파일 경로 설정
if getattr(sys, 'frozen', False):
    model_path = os.path.join(sys._MEIPASS, 'model.h5')
else:
    model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'notebooks', 'model.h5')

class TriangleValidatorCore:
    """삼각형 검증을 위한 핵심 로직을 제공하는 클래스"""
    
    def __init__(self, model_path=model_path):
        self.model = None
        try:
            self.model = tf.keras.models.load_model(model_path)
        except Exception as e:
            print(f"AI 모델 로드 실패: {e}")
    
    def validate_by_math(self, a, b, c):
        """수학적 방법으로 삼각형 가능 여부를 확인합니다."""
        return (a + b > c) and (a + c > b) and (b + c > a)
    
    def validate_by_ai(self, a, b, c):
        """AI 모델로 삼각형 가능 여부를 예측합니다."""
        if self.model is None:
            return None
        
        try:
            sides = [a, b, c]
            data = np.array([sides]) / 255.0
            prediction = self.model.predict(data)
            return prediction.item()
        except Exception as e:
            print(f"AI 예측 실패: {e}")
            return None
    
    def validate(self, a, b, c):
        """모든 방법으로 삼각형 가능 여부를 확인합니다."""
        math_result = self.validate_by_math(a, b, c)
        ai_prediction_value = self.validate_by_ai(a, b, c)
        is_valid_by_ai = ai_prediction_value > 0.5 if ai_prediction_value is not None else None
        
        return {
            "sides": [a, b, c],
            "math_result": math_result,
            "ai_prediction_value": ai_prediction_value,
            "is_valid_by_ai": is_valid_by_ai,
            "is_consistent": math_result == is_valid_by_ai if is_valid_by_ai is not None else None
        }