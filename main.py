import sys
import os
import numpy as np
import tensorflow as tf
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QFrame, QSizePolicy
from PySide6.QtGui import QPainter, QPen, QFont
from PySide6.QtCore import Qt

# 모델 파일 경로 설정
if getattr(sys, 'frozen', False):
    model_path = os.path.join(sys._MEIPASS, 'model.h5')
else:
    model_path = 'model.h5'

class TriangleModel:
    def __init__(self, model_path):
        self.model = tf.keras.models.load_model(model_path)

    def predict(self, sides):
        data = np.array([sides]) / 255.0
        prediction = self.model.predict(data)
        return prediction.item()

class Canvas(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sides = [0, 0, 0]
        self.prediction = 0
        self.setFixedSize(300, 300)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def set_sides_and_prediction(self, sides, prediction):
        self.sides = sides
        self.prediction = prediction
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        width, height = self.width(), self.height()
        center_x, center_y = width // 2, height // 2
        scale = 100 / max(self.sides) if max(self.sides) > 0 else 1

        a, b, c = [side * scale for side in self.sides]

        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        painter.drawLine(center_x - c / 2, center_y, center_x + c / 2, center_y)
        self.drawText(painter, center_x, center_y - 10, str(self.sides[2]))

        pen.setStyle(Qt.DotLine)
        pen.setColor(Qt.red)
        painter.setPen(pen)
        painter.drawEllipse(center_x - c / 2 - a, center_y - a, 2 * a, 2 * a)
        self.drawText(painter, center_x - c / 2 - a / 2, center_y - a / 2, str(self.sides[0]), align_left=True)

        pen.setColor(Qt.blue)
        painter.setPen(pen)
        painter.drawEllipse(center_x + c / 2 - b, center_y - b, 2 * b, 2 * b)
        self.drawText(painter, center_x + c / 2 - b / 2, center_y - b / 2, str(self.sides[1]), align_right=True)

        if self.prediction > 0.9:
            h = np.sqrt(b**2 - ((b**2 - a**2 + c**2) / (2 * c))**2) * self.prediction
            top_x = center_x + c / 2 - ((b**2 - a**2 + c**2) / (2 * c))
            top_y = center_y - h
            pen.setStyle(Qt.SolidLine)
            pen.setColor(Qt.black)
            painter.setPen(pen)
            painter.drawLine(center_x - c / 2, center_y, top_x, top_y)
            painter.drawLine(center_x + c / 2, center_y, top_x, top_y)
        else:
            pen.setStyle(Qt.SolidLine)
            pen.setColor(Qt.red)
            painter.setPen(pen)
            painter.drawLine(center_x - c / 2, center_y - 20, center_x - c / 2 + a, center_y - 20)
            self.drawText(painter, center_x - c / 2 + a / 2, center_y - 30, str(self.sides[0]))

            pen.setColor(Qt.blue)
            painter.setPen(pen)
            painter.drawLine(center_x + c / 2 - b, center_y - 20, center_x + c / 2, center_y - 20)
            self.drawText(painter, center_x + c / 2 - b / 2, center_y - 30, str(self.sides[1]))

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

class TriangleView(QWidget):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Triangle Predictor & Visualizer")
        self.setFixedSize(320, 400)

        self.layout = QVBoxLayout()
        self.label = QLabel("세 변의 길이를 입력하세요:")
        self.layout.addWidget(self.label)

        input_layout = QGridLayout()

        self.input1 = QLineEdit()
        self.input2 = QLineEdit()
        self.input3 = QLineEdit()
        self.button = QPushButton("판별하기")
        self.button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.button.clicked.connect(self.view_model.predict)

        input_layout.addWidget(self.input1, 0, 0, 1, 2)
        input_layout.addWidget(self.input2, 1, 0, 1, 2)
        input_layout.addWidget(self.input3, 2, 0, 1, 2)
        input_layout.addWidget(self.button, 0, 2, 3, 1)

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

        self.layout.setContentsMargins(10, 10, 10, 10)
        self.dw_layout.setContentsMargins(0, 0, 0, 10)

        self.setLayout(self.layout)

    def set_result_label(self, text):
        self.result_label.setText(text)

    def set_canvas_data(self, sides, prediction):
        self.canvas.set_sides_and_prediction(sides, prediction)

class TriangleVisualizer:
    def __init__(self):
        self.model = TriangleModel(model_path)
        self.view = TriangleView(self)
        self.view.show()

    def predict(self):
        try:
            a, b, c = float(self.view.input1.text()), float(self.view.input2.text()), float(self.view.input3.text())
            self.sides = sorted([a, b, c])
            prediction = self.model.predict(self.sides)
            result = "삼각형 가능" if prediction > 0.9 else "삼각형 불가능"
            self.view.set_result_label(f"결과: {result} (확률: {prediction:.2f})")
            self.view.set_canvas_data(self.sides, prediction)
            self.view.set_canvas_data(self.sides, prediction)
        except ValueError:
            self.view.set_result_label("올바른 숫자를 입력하세요.")
        except Exception as e:
            self.view.set_result_label(f"예측 오류: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TriangleVisualizer()
    sys.exit(app.exec())