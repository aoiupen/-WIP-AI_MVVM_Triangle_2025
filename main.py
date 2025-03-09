import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QUrl
from PySide6.QtQml import QQmlApplicationEngine

# 모듈 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 분리된 모듈 임포트
from viewmodels.triangle_visualizer import TriangleVisualizer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # QML 엔진 생성
    engine = QQmlApplicationEngine()
    
    # Python 객체를 QML에 노출
    triangle_visualizer = TriangleVisualizer()
    engine.rootContext().setContextProperty("triangleVisualizer", triangle_visualizer)
    
    # QML 파일 로드 (경로 수정)
    engine.load(QUrl.fromLocalFile("views/triangle_visualizer.qml"))
    
    if not engine.rootObjects():
        print("QML 파일 로드 실패")
        sys.exit(-1)
    
    print("애플리케이션 실행 중...")
    sys.exit(app.exec())