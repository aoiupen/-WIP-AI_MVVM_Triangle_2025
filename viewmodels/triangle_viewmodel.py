from PySide6.QtCore import QObject, Signal, Slot, Property, QTimer
from models.triangle_model import TriangleModel
from core.triangle_validator_core import TriangleValidatorCore

class TriangleViewModel(QObject):
    """QML과 연동하여 삼각형을 시각화하는 ViewModel 클래스"""
    # 시그널 정의
    resultChanged = Signal(str)
    canvasDataChanged = Signal()
    
    def __init__(self, validator=None):
        super().__init__()
        # 의존성 주입 또는 기본값 생성
        self.validator = validator if validator else TriangleValidatorCore()
        self.triangle_model = TriangleModel(self.validator)
        
        # UI 상태
        self._sides = [3.0, 4.0, 5.0]  # 기본값 설정
        self._prediction = 0.99
        self._result = "결과"
        self._scale = 20.0
        self._is_possible = True
        
        print("TriangleViewModel 초기화 완료")
        
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
            
            # 삼각형 검증 (단일 호출로 모든 결과 얻기)
            result = self.triangle_model.validate(a, b, c)
            
            # UI 상태 업데이트
            self.set_sides(self.triangle_model.sides)
            self.set_prediction(self.triangle_model.ai_prediction_value)
            self.set_is_possible(self.triangle_model.math_result)
            self.set_scale(100 / max(self._sides) if max(self._sides) > 0 else 1)
            
            # 결과 텍스트 생성
            math_result_text = "가능" if self.triangle_model.math_result else "불가능"
            ai_result_text = "가능" if self.triangle_model.is_valid_by_ai else "불가능"
            result_text = f"결과: 삼각형 {math_result_text} (수학적 검증), AI 예측: {ai_result_text} (확률: {self.triangle_model.ai_prediction_value:.2f})"
            self.set_result(result_text)
            
            print(f"삼각형 계산 완료: sides={self._sides}, prediction={self.triangle_model.ai_prediction_value}, math_result={self.triangle_model.math_result}")
            
            # UI 업데이트 요청
            QTimer.singleShot(100, self.canvasDataChanged.emit)
            
        except ValueError:
            self.set_result("올바른 숫자를 입력하세요.")
        except Exception as e:
            self.set_result(f"예측 오류: {e}")
            print(f"예측 오류: {e}")