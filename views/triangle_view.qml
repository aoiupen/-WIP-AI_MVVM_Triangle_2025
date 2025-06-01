import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Window 2.15

ApplicationWindow {
    id: appWindow
    
    // 화면 크기에 맞게 비율 유지하면서 크기 조정
    property real scaleFactor: 0.25  // 모니터에 꽉 차지 않도록 작은 값 사용
    width: 1440 * scaleFactor
    height: 3200 * scaleFactor
    
    visible: true
    title: "Triangle Validator"
    color: "#FFFFFF"
    
    // 창 크기 고정
    minimumWidth: width
    minimumHeight: height
    maximumWidth: width
    maximumHeight: height

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 30  // 여백 증가
        spacing: 50  // 간격 증가

        // 제목 부분 - 가운데 정렬
        Item {
            Layout.fillWidth: true
            Layout.topMargin: 40  // 상단 여백 추가
            height: 50
            
            RowLayout {
                anchors.centerIn: parent  // 가운데 정렬
                spacing: 10
                
                Text {
                    text: "Can this be a"
                    font.pixelSize: 24
                    font.bold: true
                }
                
                // 빨간 삼각형 아이콘 - 테두리 추가 및 모서리 둥글게
                Item {
                    width: 30
                    height: 30
                    
                    Canvas {
                        id: triangleCanvas
                        anchors.fill: parent
                        onPaint: {
                            var ctx = getContext("2d");
                            
                            // 삼각형 좌표
                            var topX = width/2;
                            var topY = 0;
                            var leftX = 0;
                            var leftY = height;
                            var rightX = width;
                            var rightY = height;
                            
                            // 검은색 테두리 그리기
                            ctx.lineWidth = 3;
                            ctx.strokeStyle = "black";
                            ctx.fillStyle = "red";
                            
                            ctx.beginPath();
                            
                            // 상단 꼭지점에서 시작
                            ctx.moveTo(topX, topY);
                            
                            // 우측 하단으로 선 그리기
                            ctx.lineTo(rightX, rightY);
                            
                            // 좌측 하단으로 선 그리기
                            ctx.lineTo(leftX, leftY);
                            
                            // 상단 꼭지점으로 선 그리기
                            ctx.lineTo(topX, topY);
                            
                            ctx.closePath();
                            ctx.fill();
                            ctx.stroke();
                        }
                    }
                }
            }
        }

        // 삼각형 시각화 영역
        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.minimumHeight: 300

            // 첫 번째 변 (파란색 선)
            Rectangle {
                width: 150
                height: 3
                color: "#6AABFF"  // 파란색
                rotation: -55
                anchors.left: parent.left
                anchors.leftMargin: 20
                anchors.top: parent.top
                anchors.topMargin: 120
            }

            // 두 번째 변 (청록색 선)
            Rectangle {
                width: 150
                height: 3
                color: "#55FFF1"  // 청록색
                rotation: 50
                anchors.right: parent.right
                anchors.rightMargin: 20
                anchors.top: parent.top
                anchors.topMargin: 120
            }

            // 세 번째 변 (노란색 선)
            Rectangle {
                width: 150
                height: 3
                color: "#FFCB21"  // 노란색
                rotation: -5
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.top
                anchors.topMargin: 200
            }

            // 첫 번째 입력 필드
            Rectangle {
                width: 80
                height: 40
                radius: 5
                color: "#F5F5F5"
                border.color: "#E0E0E0"
                border.width: 1
                anchors.left: parent.left
                anchors.leftMargin: 30
                anchors.top: parent.top
                anchors.topMargin: 30

                TextInput {
                    id: input1
                    anchors.fill: parent
                    anchors.margins: 5
                    horizontalAlignment: TextInput.AlignLeft
                    verticalAlignment: TextInput.AlignVCenter
                    text: "0"
                    font.pixelSize: 18
                    font.bold: true
                    font.weight: Font.ExtraBold
                    inputMethodHints: Qt.ImhDigitsOnly
                }
            }

            // 두 번째 입력 필드
            Rectangle {
                width: 80
                height: 40
                radius: 5
                color: "#F5F5F5"
                border.color: "#E0E0E0"
                border.width: 1
                anchors.right: parent.right
                anchors.rightMargin: 30
                anchors.top: parent.top
                anchors.topMargin: 30

                TextInput {
                    id: input2
                    anchors.fill: parent
                    anchors.margins: 5
                    horizontalAlignment: TextInput.AlignLeft
                    verticalAlignment: TextInput.AlignVCenter
                    text: "0"
                    font.pixelSize: 18
                    font.bold: true
                    font.weight: Font.ExtraBold
                    inputMethodHints: Qt.ImhDigitsOnly
                }
            }

            // 세 번째 입력 필드
            Rectangle {
                width: 80
                height: 40
                radius: 5
                color: "#F5F5F5"
                border.color: "#E0E0E0"
                border.width: 1
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.top
                anchors.topMargin: 220

                TextInput {
                    id: input3
                    anchors.fill: parent
                    anchors.margins: 5
                    horizontalAlignment: TextInput.AlignLeft
                    verticalAlignment: TextInput.AlignVCenter
                    text: "0"
                    font.pixelSize: 18
                    font.bold: true
                    font.weight: Font.ExtraBold
                    inputMethodHints: Qt.ImhDigitsOnly
                }
            }
        }

        // 결과 표시 영역
        Item {
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            
            Text {
                id: resultText
                anchors.centerIn: parent
                font.pixelSize: 18
                color: "#333333"
                text: ""
                visible: false  // 결과 텍스트 숨김 (이미지에는 없음)
            }
        }

        // AI 예측 결과 표시 Label (OK/NG)
        Text {
            id: predictionResultLabel
            Layout.alignment: Qt.AlignHCenter
            Layout.bottomMargin: 5 // 버튼과의 간격
            font.pixelSize: 20
            font.bold: true
            // triangleVisualizer.prediction 값이 0.0에서 1.0 사이의 float이라고 가정
            // ViewModel에 prediction Property가 있어야 함
            text: {
                if (typeof triangleVisualizer.prediction === 'undefined' || triangleVisualizer.prediction === null) {
                    "---"; // 초기값
                } else if (triangleVisualizer.prediction >= 0.5) {
                    "OK";
                } else {
                    "NG";
                }
            }
            color: {
                if (typeof triangleVisualizer.prediction === 'undefined' || triangleVisualizer.prediction === null) {
                    "black"; // 초기 색상
                } else if (triangleVisualizer.prediction >= 0.5) {
                    "green";
                } else {
                    "red";
                }
            }
            // 초기에는 보이지 않게 하거나, ViewModel의 상태에 따라 visible 제어 가능
            // visible: triangleVisualizer.prediction !== null 
        }

        // Check 버튼 - 위치 조정
        Rectangle {
            Layout.alignment: Qt.AlignHCenter
            Layout.topMargin: -30  // 위로 올리기
            Layout.bottomMargin: 80  // 아래 여백 추가
            width: 200
            height: 50
            radius: 25
            color: "#6750A4"  // 보라색

            Text {
                anchors.centerIn: parent
                text: "Check!"
                font.pixelSize: 18
                font.bold: true
                color: "white"
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    triangleVisualizer.predict(input1.text, input2.text, input3.text)
                }
            }
        }
    }

    // 결과 변경 연결
    Connections {
        target: triangleVisualizer
        function onResultChanged(result) {
            resultText.text = result
            // 결과 텍스트 대신 시각적 피드백 제공 (이미지에는 결과 텍스트가 없음)
        }
    }
}