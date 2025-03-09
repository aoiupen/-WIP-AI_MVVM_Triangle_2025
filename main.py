import sys
import traceback
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlApplicationEngine
from core.triangle_validator_core import TriangleValidatorCore
from models.triangle_model import TriangleModel
from viewmodels.triangle_viewmodel import TriangleViewModel

def main():
    try:
        app = QApplication(sys.argv)
        
        print("의존성 설정 중...")
        validator = TriangleValidatorCore()
        print("TriangleValidatorCore 생성 완료")
        
        # QML 엔진 생성
        print("QML 엔진 생성 중...")
        engine = QQmlApplicationEngine()
        
        # Python 객체를 QML에 노출
        print("ViewModel 생성 중...")
        triangle_viewmodel = TriangleViewModel(validator)
        print("ViewModel을 QML에 노출 중...")
        engine.rootContext().setContextProperty("triangleVisualizer", triangle_viewmodel)
        
        # QML 파일 로드
        print("QML 파일 로드 중...")
        qml_path = "views/triangle_view.qml"
        print(f"QML 파일 경로: {qml_path}")
        engine.load(QUrl.fromLocalFile(qml_path))
        
        if not engine.rootObjects():
            print("QML 파일 로드 실패")
            sys.exit(-1)
        
        print("애플리케이션 실행 중...")
        sys.exit(app.exec())
    except Exception as e:
        print(f"오류 발생: {e}")
        traceback.print_exc()
        sys.exit(-1)

if __name__ == "__main__":
    main()