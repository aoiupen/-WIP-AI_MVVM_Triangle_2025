import sys
import os
import numpy as np
import tensorflow as tf
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl, QTimer
from PySide6.QtQml import QQmlApplicationEngine

# 모델 파일 경로 설정
if getattr(sys, 'frozen', False):
    model_path = os.path.join(sys._MEIPASS, 'model.h5')
else:
    model_path = 'model.h5'

class TriangleModel:
    """TensorFlow 모델을 사용하여 삼각형 가능 여부를 예측하는 클래스"""
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)

    def predict(self, sides):
        data = np.array([sides]) / 255.0
        prediction = self.model.predict(data)
        return prediction.item()

def is_triangle_possible(sides):
    """삼각형 부등식을 사용하여 삼각형 가능 여부를 판단합니다."""
    a, b, c = sides
    return (a + b > c) and (a + c > b) and (b + c > a)

class TriangleVisualizer(QObject):
    """QML과 연동하여 삼각형을 시각화하는 클래스"""
    # 시그널 정의
    resultChanged = Signal(str)
    canvasDataChanged = Signal()
    
    def __init__(self):
        super().__init__()
        self.model = TriangleModel(model_path)
        self._sides = [3.0, 4.0, 5.0]  # 기본값 설정
        self._prediction = 0.99
        self._result = "결과"
        self._scale = 20.0
        self._is_possible = True
        print("TriangleVisualizer 초기화 완료")
        
        # 초기 상태 설정을 위한 타이머
        QTimer.singleShot(500, self.initialize_canvas)
    
    def initialize_canvas(self):
        """초기 캔버스 상태를 설정합니다."""
        print("초기 캔버스 상태 설정")
        self.canvasDataChanged.emit()
    
    # 프로퍼티 정의
    def get_sides(self):
        return self._sides
    
    def set_sides(self, sides):
        if self._sides != sides:
            self._sides = sides
            print(f"sides 변경됨: {sides}")
            self.canvasDataChanged.emit()
    
    def get_prediction(self):
        return self._prediction
    
    def set_prediction(self, prediction):
        if self._prediction != prediction:
            self._prediction = prediction
            print(f"prediction 변경됨: {prediction}")
            self.canvasDataChanged.emit()
    
    def get_result(self):
        return self._result
    
    def set_result(self, result):
        if self._result != result:
            self._result = result
            print(f"result 변경됨: {result}")
            self.resultChanged.emit(result)
    
    def get_scale(self):
        return self._scale
    
    def set_scale(self, scale):
        if self._scale != scale:
            self._scale = scale
            print(f"scale 변경됨: {scale}")
            self.canvasDataChanged.emit()
    
    def get_is_possible(self):
        return self._is_possible
    
    def set_is_possible(self, is_possible):
        if self._is_possible != is_possible:
            self._is_possible = is_possible
            print(f"is_possible 변경됨: {is_possible}")
            self.canvasDataChanged.emit()
    
    # 프로퍼티 등록
    sides = Property(list, get_sides, set_sides, notify=canvasDataChanged)
    prediction = Property(float, get_prediction, set_prediction, notify=canvasDataChanged)
    result = Property(str, get_result, set_result, notify=resultChanged)
    scale = Property(float, get_scale, set_scale, notify=canvasDataChanged)
    is_possible = Property(bool, get_is_possible, set_is_possible, notify=canvasDataChanged)
    
    @Slot(str, str, str)
    def predict(self, a_str, b_str, c_str):
        """세 변의 길이를 입력받아 삼각형 가능 여부를 예측하고 결과를 업데이트합니다."""
        try:
            print(f"입력값: {a_str}, {b_str}, {c_str}")
            a, b, c = float(a_str), float(b_str), float(c_str)
            sides = sorted([a, b, c])
            
            # 수학적으로 삼각형 가능 여부 판단
            math_possible = is_triangle_possible(sides)
            
            # AI 모델 예측
            prediction = self.model.predict(sides)
            
            # 결과 표시 (수학적 검증 결과와 AI 예측 결과 모두 표시)
            math_result = "가능" if math_possible else "불가능"
            ai_result = "가능" if prediction > 0.9 else "불가능"
            
            result_text = f"결과: 삼각형 {math_result} (수학적 검증), AI 예측: {ai_result} (확률: {prediction:.2f})"
            
            max_side = max(sides)
            scale = 100 / max_side if max_side > 0 else 1
            
            # 모든 속성을 한 번에 설정하기 전에 canvasDataChanged 시그널이 여러 번 발생하지 않도록 함
            self.set_sides(sides)
            self.set_prediction(prediction)
            self.set_is_possible(math_possible)
            self.set_scale(scale)
            self.set_result(result_text)
            
            print(f"삼각형 계산 완료: sides={sides}, prediction={prediction}, scale={scale}, math_possible={math_possible}")
            
            # 명시적으로 캔버스 업데이트 요청
            QTimer.singleShot(100, self.canvasDataChanged.emit)
            
        except ValueError:
            self.set_result("올바른 숫자를 입력하세요.")
        except Exception as e:
            self.set_result(f"예측 오류: {e}")
            print(f"예측 오류: {e}")

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
        print("QML 파일 로드 실패")
        sys.exit(-1)
    
    print("애플리케이션 실행 중...")
    sys.exit(app.exec())