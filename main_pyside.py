import sys
import os
import numpy as np
import tensorflow as tf
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QFrame, QSizePolicy
from PySide6.QtGui import QPainter, QPen, QFont
from PySide6.QtCore import Qt

class Canvas(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sides = [0, 0, 0]
        self.prediction = 0
        self.setFixedSize(300, 300)  # 캔버스 크기를 정사각형으로 고정
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def set_sides_and_prediction(self, sides, prediction):
        self.sides = sides
        self.prediction = prediction
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width, height = self.width(), self.height()
        center_x, center_y = width // 2, height // 2  # 그림 영역을 중앙으로 조정
        scale = 100 / max(self.sides) if max(self.sides) > 0 else 1

        a, b, c = [side * scale for side in self.sides]

        # 긴 변(기준선) 그리기
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        painter.drawLine(center_x - c / 2, center_y, center_x + c / 2, center_y)
        self.drawText(painter, center_x, center_y - 10, str(self.sides[2]))

        # 원의 궤적 점선으로 그리기
        pen.setStyle(Qt.DotLine)
        pen.setColor(Qt.red)
        painter.setPen(pen)
        painter.drawEllipse(center_x - c / 2 - a, center_y - a, 2 * a, 2 * a)
        self.drawText(painter, center_x - c / 2 - a / 2, center_y - a / 2, str(self.sides[0]), align_left=True)

        pen.setColor(Qt.blue)
        painter.setPen(pen)
        painter.drawEllipse(center_x + c / 2 - b, center_y - b, 2 * b, 2 * b)
        self.drawText(painter, center_x + c / 2 - b / 2, center_y - b / 2, str(self.sides[1]), align_right=True)

        # 삼각형 가능하면 실선으로 꼭짓점 연결
        if self.prediction > 0.9:
            h = np.sqrt(b**2 - ((b**2 - a**2 + c**2) / (2 * c))**2)
            top_x = center_x + c / 2 - ((b**2 - a**2 + c**2) / (2 * c))
            top_y = center_y - h
            pen.setStyle(Qt.SolidLine)
            pen.setColor(Qt.black)
            painter.setPen(pen)
            painter.drawLine(center_x - c / 2, center_y, top_x, top_y)
            painter.drawLine(center_x + c / 2, center_y, top_x, top_y)
        else:
            # 삼각형 불가능할 때 수평으로 변을 배치
            pen.setStyle(Qt.SolidLine)
            pen.setColor(Qt.red)
            painter.setPen(pen)
            painter.drawLine(center_x - c / 2, center_y - 20, center_x - c / 2 + a, center_y - 20)
            self.drawText(painter, center_x - c / 2 + a / 2, center_y - 30, str(self.sides[0]))

            pen.setColor(Qt.blue)
            painter.setPen(pen)
            painter.drawLine(center_x + c / 2 - b, center_y - 20, center_x + c / 2, center_y - 20)
            self.drawText(painter, center_x + c / 2 - b / 2, center_y - 30, str(self.sides[1]))

        painter.end()  # QPainter 객체 명시적으로 종료

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

class TriangleVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        try:
            # model.h5 파일 경로 설정
            if hasattr(sys, '_MEIPASS'):
                model_path = os.path.join(sys._MEIPASS, 'model.h5')
            else:
                model_path = 'model.h5'
            self.model = tf.keras.models.load_model(model_path)  # 모델 로드
        except Exception as e:
            self.result_label.setText(f"모델 로드 실패: {e}")
            self.model = None
        self.sides = [0, 0, 0]  # 입력된 변의 길이
        self.prediction = 0  # 예측 결과

    def initUI(self):
        self.setWindowTitle("Triangle Predictor & Visualizer")
        self.setFixedSize(320, 400)  # 윈도우 크기 고정 (300 + 좌우 패딩 10 * 2)

        self.layout = QVBoxLayout()
        self.label = QLabel("세 변의 길이를 입력하세요:")
        self.layout.addWidget(self.label)

        input_layout = QGridLayout()

        self.input1 = QLineEdit()
        self.input2 = QLineEdit()
        self.input3 = QLineEdit()
        self.button = QPushButton("판별하기")
        self.button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.button.clicked.connect(self.predict)

        input_layout.addWidget(self.input1, 0, 0, 1, 2)  # 행 0, 열 0, 행 스팬 1, 열 스팬 2
        input_layout.addWidget(self.input2, 1, 0, 1, 2)  # 행 1, 열 0, 행 스팬 1, 열 스팬 2
        input_layout.addWidget(self.input3, 2, 0, 1, 2)  # 행 2, 열 0, 행 스팬 1, 열 스팬 2
        input_layout.addWidget(self.button, 0, 2, 3, 1)  # 행 0, 열 2, 행 스팬 3, 열 스팬 1

        self.up_layout = QHBoxLayout()
        self.dw_layout = QVBoxLayout()

        self.up_layout.addLayout(input_layout)

        self.result_label = QLabel("결과")
        self.dw_layout.addWidget(self.result_label)

        self.canvas = Canvas(self)
        self.canvas.setStyleSheet("background-color: lightgray; padding-bottom: 20px;")
        self.dw_layout.addWidget(self.canvas)

        self.layout.addLayout(self.up_layout)
        self.layout.addLayout(self.dw_layout)

        self.layout.setContentsMargins(10, 10, 10, 10)  # 전체 레이아웃에 패딩 추가
        self.dw_layout.setContentsMargins(0, 0, 0, 10)  # 캔버스 아래에 약간의 여백 추가

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
            result = "삼각형 가능" if self.prediction > 0.9 else "삼각형 불가능"
            self.result_label.setText(f"결과: {result} (확률: {self.prediction:.2f})")
            self.canvas.set_sides_and_prediction(self.sides, self.prediction)
        except ValueError:
            self.result_label.setText("올바른 숫자를 입력하세요.")
        except Exception as e:
            self.result_label.setText(f"예측 오류: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TriangleVisualizer()
    window.show()
    sys.exit(app.exec())