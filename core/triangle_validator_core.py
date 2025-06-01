import numpy as np
# import tensorflow as tf # 어댑터를 통해 사용
import os
import sys
import logging # 로깅 모듈 임포트
from models.adapters import get_adapter # 어댑터 임포트
import joblib # scaler 로드를 위해 추가

logger = logging.getLogger(__name__) # 모듈용 로거

# 기본 경로 설정 (애플리케이션 루트 기준)
# __file__은 현재 파일(triangle_validator_core.py)의 경로
# os.path.dirname(__file__)은 core 폴더
# os.path.dirname(os.path.dirname(__file__))은 프로젝트 루트 폴더 (AI_MVVM_Triangle_2025)
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MODEL_PATH = os.path.join(APP_ROOT, 'notebooks', 'model.h5')
DEFAULT_SCALER_PATH = os.path.join(APP_ROOT, 'notebooks', 'scaler.pkl')

# 실행 파일(exe) 환경 경로 설정
if getattr(sys, 'frozen', False):
    # PyInstaller 등으로 패키징된 경우, sys._MEIPASS는 임시 추출 폴더
    # 이 경우, 모델과 스케일러가 실행 파일과 동일한 위치에 있거나, 특정 하위 폴더에 있다고 가정
    # 예를 들어, main.py에서 패키징 시 datas에 추가했다면 해당 경로를 사용해야 함
    # 여기서는 MEIPASS를 기준으로 notebooks 폴더가 아닌, 루트에 있다고 가정하고 수정 (필요시 조정)
    # base_path = sys._MEIPASS
    # DEFAULT_MODEL_PATH = os.path.join(base_path, 'model.h5') 
    # DEFAULT_SCALER_PATH = os.path.join(base_path, 'scaler.pkl')
    # 만약 패키징 시 notebooks 폴더를 포함했다면 아래와 같이 사용 가능
    if hasattr(sys, '_MEIPASS'):
        notebooks_dir_frozen = os.path.join(sys._MEIPASS, 'notebooks')
        if os.path.exists(os.path.join(notebooks_dir_frozen, 'model.h5')):
            DEFAULT_MODEL_PATH = os.path.join(notebooks_dir_frozen, 'model.h5')
            DEFAULT_SCALER_PATH = os.path.join(notebooks_dir_frozen, 'scaler.pkl')
        else: # 루트에 있는 경우 (혹은 다른 상대경로)
            DEFAULT_MODEL_PATH = os.path.join(sys._MEIPASS, 'model.h5')
            DEFAULT_SCALER_PATH = os.path.join(sys._MEIPASS, 'scaler.pkl')

class TriangleValidatorCore:
    """삼각형 검증을 위한 핵심 로직을 제공하는 클래스"""
    
    def __init__(self, model_path=None, scaler_path=None, framework="tensorflow"):
        current_model_path = model_path if model_path else DEFAULT_MODEL_PATH
        current_scaler_path = scaler_path if scaler_path else DEFAULT_SCALER_PATH
        
        self.model = None
        self.scaler = None
        self.adapter = get_adapter(framework) # 어댑터 인스턴스 생성
        
        try:
            self.model = self.adapter.load_model(current_model_path)
            logger.info(f"AI 모델 로드 성공: {current_model_path}")
        except Exception as e:
            logger.error(f"AI 모델 로드 실패 ({current_model_path}): {e}")
            
        try:
            self.scaler = joblib.load(current_scaler_path)
            logger.info(f"Scaler 로드 성공: {current_scaler_path}")
        except Exception as e:
            logger.error(f"Scaler 로드 실패 ({current_scaler_path}): {e}")

    def validate_by_math(self, a, b, c):
        """수학적 방법으로 삼각형 가능 여부를 확인합니다."""
        # 0 이하의 값은 삼각형 변이 될 수 없음
        if a <= 0 or b <= 0 or c <= 0:
            logger.debug(f"수학적 검증 실패 (0 이하 변): a={a}, b={b}, c={c}")
            return False
        result = (a + b > c) and (a + c > b) and (b + c > a)
        logger.debug(f"수학적 검증: a={a}, b={b}, c={c} -> {result}")
        return result
    
    def validate_by_ai(self, a, b, c):
        """AI 모델로 삼각형 가능 여부를 예측합니다."""
        if self.model is None:
            logger.warning("AI 모델이 로드되지 않아 AI 검증을 건너뜁니다.")
            return None
        if self.scaler is None:
            logger.warning("Scaler가 로드되지 않아 AI 검증을 건너뜁니다.")
            return None
        
        try:
            sides_for_ai = np.array([[float(a), float(b), float(c)]]) 
            # scaled_data = self.scaler.transform(sides_for_ai) # 어댑터 내부에서 수행
            # prediction = self.adapter.predict(self.model, scaled_data)
            prediction = self.adapter.predict(self.model, sides_for_ai, scaler=self.scaler) # scaler 전달
            logger.debug(f"AI 예측 (Core): a={a}, b={b}, c={c} -> pred={prediction}") # 스케일된 데이터 로깅은 어댑터에서
            return prediction
        except Exception as e:
            logger.error(f"AI 예측 실패 (Core): a={a},b={b},c={c}): {e}", exc_info=True)
            return None
    
    def validate(self, a, b, c):
        """모든 방법으로 삼각형 가능 여부를 확인합니다."""
        math_result = self.validate_by_math(a, b, c)
        ai_prediction_value = self.validate_by_ai(a, b, c)
        
        # ai_prediction_value가 None이 아닐 경우에만 is_valid_by_ai 계산
        is_valid_by_ai = None
        if ai_prediction_value is not None:
            is_valid_by_ai = ai_prediction_value > 0.5
        
        return {
            "sides": [float(a), float(b), float(c)],
            "math_result": math_result,
            "ai_prediction_value": ai_prediction_value,
            "is_valid_by_ai": is_valid_by_ai,
            "is_consistent": math_result == is_valid_by_ai if is_valid_by_ai is not None else None
        }

# Test (선택적)
if __name__ == '__main__':
    # TriangleValidatorCore 테스트 코드 (필요시 작성)
    # 이 테스트는 models.adapters.tf_adapter에 있는 scaler.pkl이 notebooks 폴더에 존재한다고 가정
    
    # 기본 경로를 사용하는 경우 (상대 경로에 의존)
    logger.info("기본 경로로 Core 초기화 시도...")
    core_default = TriangleValidatorCore()

    logger.info("\n--- 유효한 삼각형 (3, 4, 5) ---")
    result1 = core_default.validate(3, 4, 5)
    if result1['ai_prediction_value'] is not None:
        logger.info(f"수학적 검증: {'가능' if result1['math_result'] else '불가능'}")
        logger.info(f"AI 예측 값: {result1['ai_prediction_value']:.4f} ({'가능' if result1['is_valid_by_ai'] else '불가능'})")
        logger.info(f"일치 여부: {result1['is_consistent']}")
    else:
        logger.warning("AI 예측을 수행할 수 없습니다 (모델 또는 스케일러 로드 실패).")

    logger.info("\n--- 유효하지 않은 삼각형 (1, 2, 10) ---")
    result3 = core_default.validate(1, 2, 10)
    if result3['ai_prediction_value'] is not None:
        logger.info(f"수학적 검증: {'가능' if result3['math_result'] else '불가능'}")
        logger.info(f"AI 예측 값: {result3['ai_prediction_value']:.4f} ({'가능' if result3['is_valid_by_ai'] else '불가능'})")
        logger.info(f"일치 여부: {result3['is_consistent']}")
    else:
        logger.warning("AI 예측을 수행할 수 없습니다.")

    # 특정 모델/스케일러 경로 지정 테스트
    # 예: custom_model_path = "path/to/your/model.h5"
    #     custom_scaler_path = "path/to/your/scaler.pkl"
    #     core_custom = TriangleValidatorCore(model_path=custom_model_path, scaler_path=custom_scaler_path)
    #     # ... 테스트 진행 ...
    logger.info("\n참고: 위 테스트는 'notebooks/model.h5'와 'notebooks/scaler.pkl'이 존재해야 정상 동작합니다.")