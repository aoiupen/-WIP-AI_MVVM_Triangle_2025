import sys
import traceback
import os # os 모듈 임포트
import logging # 로깅 모듈 임포트
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlApplicationEngine
from core.triangle_validator_core import TriangleValidatorCore
# from models.triangle_model import TriangleModel # 더 이상 직접 사용하지 않으므로 제거
from viewmodels.triangle_viewmodel import TriangleViewModel

# 애플리케이션 루트 경로 설정
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def setup_logging():
    """기본 로깅 설정을 수행합니다."""
    logging.basicConfig(
        level=logging.INFO,  # 기본 로그 레벨 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout)  # 콘솔 출력 핸들러
            # logging.FileHandler("app.log") # 파일 출력 핸들러 (필요시 추가)
        ]
    )
    # 특정 라이브러리의 로그 레벨 조정 (예: 너무 많은 로그를 출력하는 라이브러리)
    # logging.getLogger("some_library").setLevel(logging.WARNING)

logger = logging.getLogger(__name__) # main 모듈용 로거

def main():
    try:
        setup_logging() # 로깅 설정 함수 호출
        logger.info("애플리케이션 시작 중...")
        app = QApplication(sys.argv)
        
        logger.info("의존성 설정 중...")
        validator = TriangleValidatorCore()
        logger.info("TriangleValidatorCore 생성 완료")
        
        # QML 엔진 생성
        logger.info("QML 엔진 생성 중...")
        engine = QQmlApplicationEngine()
        
        # Python 객체를 QML에 노출
        logger.info("ViewModel 생성 중...")
        triangle_viewmodel = TriangleViewModel(validator)
        logger.info("ViewModel을 QML에 노출 중...")
        engine.rootContext().setContextProperty("triangleVisualizer", triangle_viewmodel)
        
        # QML 파일 로드 (애플리케이션 루트 기준 상대 경로)
        logger.info("QML 파일 로드 중...")
        qml_file_name = "triangle_view.qml"
        qml_path = os.path.join(APP_ROOT, "views", qml_file_name) # APP_ROOT 기준
        
        # PyInstaller 환경에서 QML 경로 처리 (만약 views 폴더가 MEIPASS에 포함된다면)
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            frozen_qml_path = os.path.join(sys._MEIPASS, "views", qml_file_name)
            if os.path.exists(frozen_qml_path):
                qml_path = frozen_qml_path
            else: # 루트에 있는 경우 (또는 다른 상대경로)
                frozen_qml_path_root = os.path.join(sys._MEIPASS, qml_file_name)
                if os.path.exists(frozen_qml_path_root):
                    qml_path = frozen_qml_path_root

        logger.info(f"QML 파일 경로: {qml_path}")
        if not os.path.exists(qml_path):
            logger.error(f"QML 파일을 찾을 수 없습니다: {qml_path}")
            # 대체 경로 시도 (예: 현재 작업 디렉토리 기준)
            fallback_qml_path = os.path.join("views", qml_file_name)
            if os.path.exists(fallback_qml_path):
                logger.info(f"대체 QML 경로 사용: {fallback_qml_path}")
                qml_path = fallback_qml_path
            else:
                logger.critical(f"QML 파일 완전 실패: {fallback_qml_path}")
                sys.exit(-1)
        
        engine.load(QUrl.fromLocalFile(qml_path))
        
        if not engine.rootObjects():
            logger.critical("QML 파일 로드 실패 또는 루트 객체 없음")
            sys.exit(-1)
        
        logger.info("애플리케이션 실행 준비 완료.")
        sys.exit(app.exec())
    except Exception as e:
        logger.exception(f"애플리케이션 실행 중 심각한 오류 발생: {e}") # traceback 포함 로깅
        # traceback.print_exc() # logger.exception이 대신함
        sys.exit(-1)

if __name__ == "__main__":
    main()