import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    id: appWindow
    width: 320
    height: 400
    visible: true
    title: "Triangle Predictor & Visualizer"

    // 초기 상태 설정
    Component.onCompleted: {
        resultLabel.text = "세 변의 길이를 입력하고 판별하기 버튼을 누르세요.";
        console.log("애플리케이션 초기화 완료");
        // 초기 삼각형 그리기 테스트
        triangleVisualizer.predict("3", "4", "5");
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 10

        // 제목 레이블
        Label {
            text: "세 변의 길이를 입력하세요:"
            font.pixelSize: 14
            font.bold: true
        }

        // 입력 영역
        GridLayout {
            columns: 3
            rowSpacing: 5
            columnSpacing: 5

            TextField {
                id: input1
                Layout.columnSpan: 2
                Layout.fillWidth: true
                placeholderText: "첫 번째 변의 길이"
                text: "3"
                selectByMouse: true
            }

            TextField {
                id: input2
                Layout.columnSpan: 2
                Layout.fillWidth: true
                placeholderText: "두 번째 변의 길이"
                text: "4"
                selectByMouse: true
            }

            TextField {
                id: input3
                Layout.columnSpan: 2
                Layout.fillWidth: true
                placeholderText: "세 번째 변의 길이"
                text: "5"
                selectByMouse: true
            }

            Button {
                text: "판별하기"
                Layout.columnSpan: 1
                Layout.rowSpan: 3
                Layout.fillHeight: true
                onClicked: {
                    console.log("판별하기 버튼 클릭됨");
                    triangleVisualizer.predict(input1.text, input2.text, input3.text);
                }
            }
        }

        // 결과 표시 레이블
        Label {
            id: resultLabel
            text: "결과"
            font.pixelSize: 14
            Layout.fillWidth: true
            wrapMode: Text.WordWrap

            Connections {
                target: triangleVisualizer
                function onResultChanged(result) {
                    console.log("결과 변경됨: " + result);
                    resultLabel.text = result;
                }
            }
        }

        // 캔버스 영역 (삼각형 시각화)
        Rectangle {
            id: canvasContainer
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.minimumHeight: 200
            color: "lightgray"
            border.color: "darkgray"
            border.width: 1
            
            // 디버깅용 텍스트 - 항상 표시
            Text {
                id: debugText
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.margins: 5
                font.pixelSize: 10
                color: "black"
                text: "디버깅: 준비됨"
                z: 10
                visible: true // 디버깅 모드에서 표시
            }
            
            Canvas {
                id: canvas
                anchors.fill: parent
                anchors.margins: 5
                
                // 삼각형 데이터가 변경되면 캔버스 다시 그리기
                Connections {
                    target: triangleVisualizer
                    function onCanvasDataChanged() {
                        console.log("Canvas 데이터 변경됨");
                        debugText.text = "디버깅: sides=" + JSON.stringify(triangleVisualizer.sides) + 
                                        ", prediction=" + triangleVisualizer.prediction + 
                                        ", is_possible=" + triangleVisualizer.is_possible;
                        canvas.requestPaint();
                    }
                }
                
                // 캔버스 그리기 함수
                onPaint: {
                    console.log("Canvas onPaint 호출됨");
                    var ctx = getContext("2d");
                    ctx.reset();
                    
                    var width = canvas.width;
                    var height = canvas.height;
                    var centerX = width / 2;
                    var centerY = height / 2;
                    
                    // 기본 배경 그리기
                    ctx.fillStyle = "#f0f0f0";
                    ctx.fillRect(0, 0, width, height);
                    
                    // 삼각형 변의 길이 가져오기
                    var sides = triangleVisualizer.sides;
                    var scale = triangleVisualizer.scale;
                    var prediction = triangleVisualizer.prediction;
                    var isPossible = triangleVisualizer.is_possible;
                    
                    console.log("Canvas 그리기: sides=" + JSON.stringify(sides) + 
                               ", prediction=" + prediction + 
                               ", is_possible=" + isPossible);
                    
                    // 변의 길이가 유효한지 확인
                    if (sides.length !== 3 || sides[0] <= 0 || sides[1] <= 0 || sides[2] <= 0) {
                        console.log("유효하지 않은 변의 길이");
                        ctx.fillStyle = "black";
                        ctx.font = "14px sans-serif";
                        ctx.textAlign = "center";
                        ctx.fillText("유효한 변의 길이를 입력하세요", centerX, centerY);
                        return;
                    }
                    
                    var a = sides[0] * scale;
                    var b = sides[1] * scale;
                    var c = sides[2] * scale;
                    
                    // 스케일 조정 (너무 크거나 작지 않게)
                    // 삼각형이 캔버스 영역을 벗어나지 않도록 조정
                    var maxDimension = Math.min(width, height) * 0.6; // 0.8에서 0.6으로 줄임
                    var maxScaledSide = Math.max(a, b, c);
                    
                    // 삼각형의 높이 계산 (정확한 높이 계산을 위해)
                    var triangleHeight = 0;
                    if (isPossible) {
                        triangleHeight = Math.sqrt(Math.max(0, b*b - Math.pow((b*b - a*a + c*c) / (2*c), 2)));
                    }
                    
                    // 높이도 고려하여 스케일 조정
                    var adjustedScale = maxDimension / Math.max(maxScaledSide, triangleHeight);
                    
                    // 스케일 적용
                    a = sides[0] * scale * adjustedScale;
                    b = sides[1] * scale * adjustedScale;
                    c = sides[2] * scale * adjustedScale;
                    
                    console.log("스케일링된 변의 길이: a=" + a + ", b=" + b + ", c=" + c);
                    
                    // 바닥 선 그리기 (c 변)
                    ctx.strokeStyle = "black";
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.moveTo(centerX - c / 2, centerY);
                    ctx.lineTo(centerX + c / 2, centerY);
                    ctx.stroke();
                    
                    // c 변 길이 표시
                    ctx.fillStyle = "black";
                    ctx.font = "12px sans-serif";
                    ctx.textAlign = "center";
                    ctx.fillText(sides[2].toString(), centerX, centerY + 15);
                    
                    // a 변 원 그리기 (빨간색 점선)
                    ctx.strokeStyle = "red";
                    ctx.lineWidth = 1;
                    ctx.setLineDash([2, 2]);
                    ctx.beginPath();
                    ctx.arc(centerX - c / 2, centerY, a, 0, 2 * Math.PI);
                    ctx.stroke();
                    
                    // a 변 길이 표시
                    ctx.fillStyle = "red";
                    ctx.textAlign = "left";
                    ctx.fillText(sides[0].toString(), centerX - c / 2 - a / 2, centerY - a / 2);
                    
                    // b 변 원 그리기 (파란색 점선)
                    ctx.strokeStyle = "blue";
                    ctx.setLineDash([2, 2]);
                    ctx.beginPath();
                    ctx.arc(centerX + c / 2, centerY, b, 0, 2 * Math.PI);
                    ctx.stroke();
                    
                    // b 변 길이 표시
                    ctx.fillStyle = "blue";
                    ctx.textAlign = "right";
                    ctx.fillText(sides[1].toString(), centerX + c / 2 + b / 2, centerY - b / 2);
                    
                    // 삼각형 가능 여부에 따라 다르게 그리기
                    if (isPossible) {
                        console.log("삼각형 그리기 (가능)");
                        try {
                            // 삼각형 그리기
                            var h = Math.sqrt(Math.max(0, b*b - Math.pow((b*b - a*a + c*c) / (2*c), 2)));
                            var topX = centerX + c / 2 - ((b*b - a*a + c*c) / (2*c));
                            var topY = centerY - h;
                            
                            console.log("삼각형 좌표: topX=" + topX + ", topY=" + topY + ", h=" + h);
                            
                            ctx.strokeStyle = "black";
                            ctx.lineWidth = 2;
                            ctx.setLineDash([]);
                            
                            // 삼각형 그리기 (채우기 먼저)
                            ctx.fillStyle = "rgba(0, 255, 0, 0.2)";
                            ctx.beginPath();
                            ctx.moveTo(centerX - c / 2, centerY);
                            ctx.lineTo(topX, topY);
                            ctx.lineTo(centerX + c / 2, centerY);
                            ctx.closePath();
                            ctx.fill();
                            
                            // 왼쪽 변 그리기
                            ctx.beginPath();
                            ctx.moveTo(centerX - c / 2, centerY);
                            ctx.lineTo(topX, topY);
                            ctx.stroke();
                            
                            // 오른쪽 변 그리기
                            ctx.beginPath();
                            ctx.moveTo(centerX + c / 2, centerY);
                            ctx.lineTo(topX, topY);
                            ctx.stroke();
                            
                            // 변의 길이 표시
                            ctx.fillStyle = "black";
                            ctx.textAlign = "center";
                            ctx.fillText(sides[0].toString(), (centerX - c / 2 + topX) / 2 - 10, (centerY + topY) / 2);
                            ctx.fillText(sides[1].toString(), (centerX + c / 2 + topX) / 2 + 10, (centerY + topY) / 2);
                            
                            // AI 예측이 틀린 경우 경고 표시
                            if (prediction <= 0.9) {
                                ctx.fillStyle = "rgba(255, 255, 0, 0.3)";
                                ctx.beginPath();
                                ctx.moveTo(centerX - c / 2, centerY);
                                ctx.lineTo(topX, topY);
                                ctx.lineTo(centerX + c / 2, centerY);
                                ctx.closePath();
                                ctx.fill();
                                
                                // 경고 아이콘
                                ctx.fillStyle = "orange";
                                ctx.font = "16px sans-serif";
                                ctx.textAlign = "center";
                                ctx.fillText("⚠️ AI 예측 불일치", centerX, topY - 20);
                            }
                        } catch (e) {
                            console.error("삼각형 그리기 오류: " + e);
                            ctx.fillStyle = "red";
                            ctx.font = "14px sans-serif";
                            ctx.textAlign = "center";
                            ctx.fillText("그리기 오류: " + e, centerX, centerY);
                        }
                    } else {
                        console.log("삼각형 그리기 (불가능)");
                        // 삼각형이 불가능한 경우 시각화
                        ctx.setLineDash([]);
                        
                        // a 변 표시 (빨간색)
                        ctx.strokeStyle = "red";
                        ctx.lineWidth = 2;
                        ctx.beginPath();
                        ctx.moveTo(centerX - c / 2, centerY - 20);
                        ctx.lineTo(centerX - c / 2 + a, centerY - 20);
                        ctx.stroke();
                        
                        ctx.fillStyle = "red";
                        ctx.textAlign = "center";
                        ctx.fillText(sides[0].toString(), centerX - c / 2 + a / 2, centerY - 30);
                        
                        // b 변 표시 (파란색)
                        ctx.strokeStyle = "blue";
                        ctx.beginPath();
                        ctx.moveTo(centerX + c / 2 - b, centerY - 20);
                        ctx.lineTo(centerX + c / 2, centerY - 20);
                        ctx.stroke();
                        
                        ctx.fillStyle = "blue";
                        ctx.textAlign = "center";
                        ctx.fillText(sides[1].toString(), centerX + c / 2 - b / 2, centerY - 30);
                        
                        // 불가능 표시
                        ctx.strokeStyle = "red";
                        ctx.lineWidth = 3;
                        ctx.beginPath();
                        ctx.moveTo(centerX - 30, centerY - 30);
                        ctx.lineTo(centerX + 30, centerY + 30);
                        ctx.stroke();
                        
                        ctx.beginPath();
                        ctx.moveTo(centerX + 30, centerY - 30);
                        ctx.lineTo(centerX - 30, centerY + 30);
                        ctx.stroke();
                        
                        // 불가능 메시지
                        ctx.fillStyle = "red";
                        ctx.font = "14px sans-serif";
                        ctx.textAlign = "center";
                        ctx.fillText("삼각형 불가능", centerX, centerY + 50);
                        
                        // AI 예측이 틀린 경우 경고 표시
                        if (prediction > 0.9) {
                            ctx.fillStyle = "orange";
                            ctx.font = "16px sans-serif";
                            ctx.textAlign = "center";
                            ctx.fillText("⚠️ AI 예측 불일치", centerX, centerY - 60);
                        }
                    }
                }
            }
        }
    }
}