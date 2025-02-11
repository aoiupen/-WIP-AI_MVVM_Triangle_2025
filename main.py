import sys
import numpy as np
import tensorflow as tf
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtGui import QPainter, QPen, QFont
from PySide6.QtCore import Qt
import math

class TriangleVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        try:
            self.model = tf.keras.models.load_model("model.h5")  # 모델 로드
        except Exception as e:
            self.result_label.setText(f"모델 로드 실패: {e}")
            self.model = None
        self.sides = [0, 0, 0]  # 입력된 변의 길이
        self.prediction = 0  # 예측 결과

    def initUI(self):
        self.setWindowTitle("Triangle Predictor & Visualizer")
        self.setGeometry(100, 100, 400, 400)
        
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
            self.sides = sorted([a, b, c])  # 정렬하여 가장 긴 변을 마지막에 둠
            data = np.array([[a, b, c]]) / 255.0  # 정규화
            self.prediction = self.model.predict(data)[0][0]
            result = "삼각형 가능" if self.prediction > 0.5 else "삼각형 불가능"
            self.result_label.setText(f"결과: {result} (확률: {self.prediction:.2f})")
            self.update()
        except ValueError:
            self.result_label.setText("올바른 숫자를 입력하세요.")
        except Exception as e:
            self.result_label.setText(f"예측 오류: {e}")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        width, height = self.width(), self.height()
        center_x, base_y = width // 2, height - 50
        scale = 100 / max(self.sides) if max(self.sides) > 0 else 1
        
        a, b, c = [side * scale for side in self.sides]
        
        # 긴 변(기준선) 그리기
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        painter.drawLine(center_x - c / 2, base_y, center_x + c / 2, base_y)
        self.drawText(painter, center_x, base_y - 10, str(self.sides[2]))
        
        # 원의 궤적 점선으로 그리기
        pen.setStyle(Qt.DotLine)
        pen.setColor(Qt.red)
        painter.setPen(pen)
        painter.drawEllipse(center_x - c / 2 - a, base_y - a, 2 * a, 2 * a)
        self.drawText(painter, center_x - c / 2 - a / 2, base_y - a / 2, str(self.sides[0]), align_left=True)
        
        pen.setColor(Qt.blue)
        painter.setPen(pen)
        painter.drawEllipse(center_x + c / 2 - b, base_y - b, 2 * b, 2 * b)
        self.drawText(painter, center_x + c / 2 - b / 2, base_y - b / 2, str(self.sides[1]), align_right=True)
        
        # 삼각형 가능하면 실선으로 꼭짓점 연결
        if self.prediction > 0.5:
            h = math.sqrt(b**2 - ((b**2 - a**2 + c**2) / (2 * c))**2)
            top_x = center_x - c / 2 + ((b**2 - a**2 + c**2) / (2 * c))
            top_y = base_y - h
            pen.setStyle(Qt.SolidLine)
            pen.setColor(Qt.black)
            painter.setPen(pen)
            painter.drawLine(center_x - c / 2, base_y, top_x, top_y)
            painter.drawLine(center_x + c / 2, base_y, top_x, top_y)
        else:
            # 삼각형 불가능할 때 수평으로 변을 배치
            pen.setStyle(Qt.SolidLine)
            pen.setColor(Qt.red)
            painter.setPen(pen)
            painter.drawLine(center_x - c / 2, base_y - 20, center_x - c / 2 + a, base_y - 20)
            self.drawText(painter, center_x - c / 2 + a / 2, base_y - 30, str(self.sides[0]))
            
            pen.setColor(Qt.blue)
            painter.setPen(pen)
            painter.drawLine(center_x + c / 2 - b, base_y - 20, center_x + c / 2, base_y - 20)
            self.drawText(painter, center_x + c / 2 - b / 2, base_y - 30, str(self.sides[1]))
        
        painter.end()
    
    def drawText(self, painter, x, y, text, align_left=False, align_right=False):
        font = QFont()
        font.setPointSize(10)
        painter.setFont(font)
        if align_left:
            painter.drawText(x - 10, y, text)
        elif align_right:
            painter.drawText(x + 10, y, text)
        else:
            painter.drawText(x - 10, y, text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TriangleVisualizer()
    window.show()
    sys.exit(app.exec())
