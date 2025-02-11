import sys
import numpy as np
import tensorflow as tf
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class TrianglePredictor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        try:
            self.model = tf.keras.models.load_model("model.h5")  # 모델을 model.h5 파일로 불러오기
        except Exception as e:
            self.result_label.setText(f"모델 로드 실패: {e}")
            self.model = None

    def initUI(self):
        self.setWindowTitle("Triangle Predictor")
        self.setGeometry(100, 100, 250, 150)  # 콤팩트한 창 크기
        
        self.layout = QVBoxLayout()
        
        self.label = QLabel("세 변의 길이를 입력하세요:")
        self.layout.addWidget(self.label)
        
        self.input1 = QLineEdit()
        self.input2 = QLineEdit()
        self.input3 = QLineEdit()
        self.layout.addWidget(self.input1)
        self.layout.addWidget(self.input2)
        self.layout.addWidget(self.input3)
        
        self.button = QPushButton("판별하기")
        self.button.clicked.connect(self.predict)
        self.layout.addWidget(self.button)
        
        self.result_label = QLabel("결과: ")
        self.layout.addWidget(self.result_label)
        
        self.setLayout(self.layout)
    
    def predict(self):
        if self.model is None:
            self.result_label.setText("모델이 로드되지 않았습니다.")
            return
        
        try:
            a, b, c = float(self.input1.text()), float(self.input2.text()), float(self.input3.text())
            data = np.array([[a, b, c]]) / 255.0  # 모델에 맞게 정규화
            prediction = self.model.predict(data)[0][0]
            result = "삼각형 가능" if prediction > 0.5 else "삼각형 불가능"
            self.result_label.setText(f"결과: {result} (확률: {prediction:.2f})")
        except ValueError:
            self.result_label.setText("올바른 숫자를 입력하세요.")
        except Exception as e:
            self.result_label.setText(f"예측 오류: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrianglePredictor()
    window.show()
    sys.exit(app.exec())
