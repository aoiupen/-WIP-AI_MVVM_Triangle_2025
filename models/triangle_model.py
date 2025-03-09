import numpy as np
import tensorflow as tf
import os
import sys

# 모델 파일 경로 설정
if getattr(sys, 'frozen', False):
    model_path = os.path.join(sys._MEIPASS, 'model.h5')
else:
    # 모델 파일이 notebooks 폴더로 이동했으므로 경로 수정
    model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'notebooks', 'model.h5')

class TriangleModel:
    """TensorFlow 모델을 사용하여 삼각형 가능 여부를 예측하는 클래스"""
    def __init__(self, model_path=model_path):
        self.model = tf.keras.models.load_model(model_path)

    def predict(self, sides):
        data = np.array([sides]) / 255.0
        prediction = self.model.predict(data)
        return prediction.item()

def is_triangle_possible(sides):
    """삼각형 부등식을 사용하여 삼각형 가능 여부를 판단합니다."""
    a, b, c = sides
    return (a + b > c) and (a + c > b) and (b + c > a) 