import sys
import os
import numpy as np
import tensorflow as tf
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl
from PySide6.QtQml import QQmlApplicationEngine

# 모델 파일 경로 설정
if getattr(sys, 'frozen', False):
    model_path = os.path.join(sys._MEIPASS, 'model.h5')
else:
    model_path = 'model.h5'

class TriangleModel:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)

    def predict(self, sides):
        data = np.array([sides]) / 255.0
        prediction = self.model.predict(data)
        return prediction.item()

class TriangleVisualizer(QObject):
    # 시그널 정의
    resultChanged = Signal(str)
    canvasDataChanged = Signal()
    
    def __init__(self):
        super().__init__()
        self.model = TriangleModel(model_path)
        self._sides = [0, 0, 0]
        self._prediction = 0
        self._result = "결과"
        self._scale = 1
    
    # 프로퍼티 정의
    def get_sides(self):
        return self._sides
    
    def set_sides(self, sides):
        if self._sides != sides:
            self._sides = sides
            self.canvasDataChanged.emit()
    
    def get_prediction(self):
        return self._prediction
    
    def set_prediction(self, prediction):
        if self._prediction != prediction:
            self._prediction = prediction
            self.canvasDataChanged.emit()
    
    def get_result(self):
        return self._result
    
    def set_result(self, result):
        if self._result != result:
            self._result = result
            self.resultChanged.emit(result)
    
    def get_scale(self):
        return self._scale
    
    def set_scale(self, scale):
        if self._scale != scale:
            self._scale = scale
            self.canvasDataChanged.emit()
    
    # 프로퍼티 등록
    sides = Property(list, get_sides, set_sides, notify=canvasDataChanged)
    prediction = Property(float, get_prediction, set_prediction, notify=canvasDataChanged)
    result = Property(str, get_result, set_result, notify=resultChanged)
    scale = Property(float, get_scale, set_scale, notify=canvasDataChanged)
    
    @Slot(str, str, str)
    def predict(self, a_str, b_str, c_str):
        try:
            a, b, c = float(a_str), float(b_str), float(c_str)
            sides = sorted([a, b, c])
            self.set_sides(sides)
            
            prediction = self.model.predict(sides)
            self.set_prediction(prediction)
            
            result_text = "삼각형 가능" if prediction > 0.9 else "삼각형 불가능"
            self.set_result(f"결과: {result_text} (확률: {prediction:.2f})")
            
            max_side = max(sides)
            self.set_scale(100 / max_side if max_side > 0 else 1)
        except ValueError:
            self.set_result("올바른 숫자를 입력하세요.")
        except Exception as e:
            self.set_result(f"예측 오류: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # QML 엔진 생성
    engine = QQmlApplicationEngine()
    
    # Python 객체를 QML에 노출
    triangle_visualizer = TriangleVisualizer()
    engine.rootContext().setContextProperty("triangleVisualizer", triangle_visualizer)
    
    # QML 파일 로드
    engine.load(QUrl.fromLocalFile("triangle_visualizer.qml"))
    
    if not engine.rootObjects():
        sys.exit(-1)
    
    sys.exit(app.exec()) 