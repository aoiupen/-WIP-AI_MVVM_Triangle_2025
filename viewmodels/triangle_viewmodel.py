from PySide6.QtCore import QObject, Signal, Slot, Property, QTimer
import logging # 로깅 모듈 임포트
# from models.triangle_model import TriangleModel # 더 이상 직접 사용 안 함
from core.triangle_validator_core import TriangleValidatorCore #, model_path as core_model_path # model_path 직접 사용 안함

logger = logging.getLogger(__name__) # 모듈용 로거

class TriangleViewModel(QObject):
    """QML과 연동하여 삼각형을 시각화하는 ViewModel 클래스"""
    # 시그널 정의
    resultChanged = Signal(str)
    canvasDataChanged = Signal()
    predictionChanged = Signal() # prediction 값 변경 시그널 추가
    
    def __init__(self, validator=None):
        super().__init__()
        # 의존성 주입 또는 기본값 생성
        self.validator = validator if validator else TriangleValidatorCore()
        # self.triangle_model = TriangleModel(model_path=core_model_path) # Core를 통해 접근하므로 제거
        
        # UI 상태
        self._sides = [3.0, 4.0, 5.0]  # 기본값 설정
        self._prediction = None # 초기값 None으로 변경 (QML에서 "---" 표시 위함)
        self._result = "결과를 보려면 값을 입력하고 Check 버튼을 누르세요." # 초기 메시지 변경
        self._scale = 20.0
        self._is_possible = True # 수학적 가능 여부
        
        logger.info("TriangleViewModel 초기화 완료")
        
        # 초기 상태 설정을 위한 타이머
        QTimer.singleShot(0, self.initialize_canvas) # 지연을 0ms로 변경하여 즉시 실행에 가깝게
    
    def initialize_canvas(self):
        """초기 캔버스 상태를 설정합니다."""
        logger.info("초기 캔버스 상태 설정")
        # 초기 prediction 값도 반영되도록 emit
        self.predictionChanged.emit()
        self.canvasDataChanged.emit()
    
    # 프로퍼티 정의
    def get_sides(self):
        return self._sides
    
    def set_sides(self, sides):
        if self._sides != sides:
            self._sides = sides
            logger.debug(f"ViewModel sides 변경됨: {sides}")
            self.canvasDataChanged.emit()
    
    def get_prediction(self):
        return self._prediction
    
    def set_prediction(self, prediction):
        # None 값도 허용하도록 조건 변경
        if self._prediction != prediction or prediction is None:
            self._prediction = prediction
            logger.debug(f"ViewModel prediction 변경됨: {prediction}")
            self.predictionChanged.emit() # prediction 값 변경 시그널 발생
            # self.canvasDataChanged.emit() # prediction은 canvas 모양에 직접 영향 안 줄 수 있음
    
    def get_result(self):
        return self._result
    
    def set_result(self, result):
        if self._result != result:
            self._result = result
            logger.info(f"ViewModel result 변경됨: {result}")
            self.resultChanged.emit(result)
    
    def get_scale(self):
        return self._scale
    
    def set_scale(self, scale):
        if self._scale != scale:
            self._scale = scale
            logger.debug(f"ViewModel scale 변경됨: {scale}")
            self.canvasDataChanged.emit()
    
    def get_is_possible(self):
        return self._is_possible
    
    def set_is_possible(self, is_possible):
        if self._is_possible != is_possible:
            self._is_possible = is_possible
            logger.debug(f"ViewModel is_possible 변경됨: {is_possible}")
            self.canvasDataChanged.emit()
    
    # 프로퍼티 등록
    sides = Property(list, get_sides, set_sides, notify=canvasDataChanged)
    # prediction 프로퍼티의 notify 시그널 변경
    prediction = Property(float, get_prediction, set_prediction, notify=predictionChanged)
    result = Property(str, get_result, set_result, notify=resultChanged)
    scale = Property(float, get_scale, set_scale, notify=canvasDataChanged)
    is_possible = Property(bool, get_is_possible, set_is_possible, notify=canvasDataChanged)
    
    @Slot(str, str, str)
    def predict(self, a_str, b_str, c_str):
        """세 변의 길이를 입력받아 삼각형 가능 여부를 예측하고 결과를 업데이트합니다."""
        try:
            logger.info(f"ViewModel predict 호출됨. 입력값: a='{a_str}', b='{b_str}', c='{c_str}'")
            a, b, c = float(a_str), float(b_str), float(c_str)
            
            if a <= 0 or b <= 0 or c <= 0:
                logger.warning(f"잘못된 변 길이 입력: a={a}, b={b}, c={c}")
                self.set_result("변의 길이는 0보다 커야 합니다.")
                self.set_prediction(None) # 유효하지 않은 입력 시 예측값 초기화
                self.set_is_possible(False)
                self.set_sides([0,0,0]) # 시각화 초기화 또는 에러 상태 표시
                self.canvasDataChanged.emit()
                self.predictionChanged.emit() # QML 업데이트
                return

            # TriangleValidatorCore를 사용하여 검증
            validation_results = self.validator.validate(a, b, c)
            
            # UI 상태 업데이트
            self.set_sides(validation_results["sides"]) # validator가 반환한 값 사용
            self.set_prediction(validation_results["ai_prediction_value"]) # validator가 반환한 값 사용
            self.set_is_possible(validation_results["math_result"]) # validator가 반환한 값 사용
            
            # 유효한 변들이 있을 때만 스케일 계산
            if max(validation_results["sides"]) > 0:
                self.set_scale(100 / max(validation_results["sides"])) 
            else:
                self.set_scale(1) # 기본 스케일
            
            # 결과 텍스트 생성
            math_result_text = "가능" if validation_results["math_result"] else "불가능"
            
            ai_prediction_value = validation_results["ai_prediction_value"]
            if ai_prediction_value is None:
                ai_result_text = "N/A"
                ai_prob_text = "N/A"
            else:
                ai_result_text = "가능" if validation_results["is_valid_by_ai"] else "불가능"
                ai_prob_text = f"{ai_prediction_value:.4f}"
                
            result_text = f"수학: {math_result_text}, AI: {ai_result_text} (값: {ai_prob_text})"
            self.set_result(result_text)
            
            logger.info(f"ViewModel 검증 완료: sides={validation_results['sides']}, ai_pred={ai_prediction_value}, math_result={validation_results['math_result']}")
            
            # UI 업데이트 요청 (canvasDataChanged는 sides, scale, is_possible 변경 시 이미 발생)
            # predictionChanged는 set_prediction에서 이미 발생
            # resultChanged는 set_result에서 이미 발생
            # QTimer.singleShot(100, self.canvasDataChanged.emit) # 중복 호출일 수 있으므로 필요성 검토
            
        except ValueError:
            logger.warning(f"잘못된 숫자 형식 입력: a='{a_str}', b='{b_str}', c='{c_str}'", exc_info=True)
            self.set_result("올바른 숫자를 입력하세요.")
            self.set_prediction(None) # 오류 시 예측값 초기화
            self.set_is_possible(False)
            self.predictionChanged.emit() # QML 업데이트
        except Exception as e:
            logger.error(f"ViewModel predict 슬롯 오류: {e}", exc_info=True)
            self.set_result(f"오류: {e}")
            self.set_prediction(None) # 오류 시 예측값 초기화
            self.set_is_possible(False)
            self.predictionChanged.emit() # QML 업데이트

    # ViewModel 내의 중복 validate 메소드 제거
    # def validate(self, a, b, c):
    #     ...