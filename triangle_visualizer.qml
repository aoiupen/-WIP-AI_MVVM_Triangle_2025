import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    id: appWindow
    width: 360
    height: 720  // 윈도우 세로 길이 증가
    visible: true
    title: "Triangle Predictor & Visualizer"
    
    // 다크모드 상태 관리
    property bool isDarkMode: false
    
    // 테마 색상 정의
    property color backgroundColor: isDarkMode ? "#1c1c1e" : "#f5f5f7"
    property color cardColor: isDarkMode ? "#2c2c2e" : "#ffffff"
    property color textColor: isDarkMode ? "#ffffff" : "#1c1c1e"
    property color borderColor: isDarkMode ? "#3c3c3e" : "#e0e0e0"
    property color inputBgColor: isDarkMode ? "#3c3c3e" : "#f2f2f7"
    property color primaryColor: "#007aff"  // iOS 블루 컬러
    property color successColor: "#34c759"  // iOS 그린 컬러
    property color errorColor: "#ff3b30"    // iOS 레드 컬러
    property color warningColor: "#ff9500"  // iOS 오렌지 컬러
    property color lightColor: "#8e8e93"    // iOS 회색 컬러
    
    color: backgroundColor

    // 초기 상태 설정
    Component.onCompleted: {
        resultLabel.text = "세 변의 길이를 입력하고 판별하기 버튼을 누르세요.";
        console.log("애플리케이션 초기화 완료");
        // 초기 삼각형 그리기 테스트
        triangleVisualizer.predict("3", "4", "5");
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16  // 화면 여백 조정 (12~16pt)
        spacing: 20

        // 앱 타이틀과 다크모드 토글
        Rectangle {
            Layout.fillWidth: true
            height: 60
            color: "transparent"
            
            RowLayout {
                anchors.fill: parent
                spacing: 10
                
                Text {
                    Layout.fillWidth: true
                    text: "Triangle Validator"
                    font.pixelSize: 36  // 텍스트 크기 조정 (36pt)
                    font.weight: Font.DemiBold
                    font.letterSpacing: -0.72  // 자간 조정 (-2%)
                    color: textColor
                }
                
                // 다크모드 토글 버튼
                Rectangle {
                    width: 50
                    height: 30
                    radius: 15
                    color: isDarkMode ? primaryColor : inputBgColor
                    border.color: borderColor
                    border.width: 1
                    
                    Rectangle {
                        width: 26
                        height: 26
                        radius: 13
                        color: isDarkMode ? "#ffffff" : "#8e8e93"
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.left: parent.left
                        anchors.leftMargin: isDarkMode ? 20 : 4
                        
                        Behavior on anchors.leftMargin {
                            NumberAnimation { duration: 200 }
                        }
                    }
                    
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            isDarkMode = !isDarkMode;
                        }
                    }
                }
            }
        }

        // 입력 영역
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 220
            radius: 8
            color: cardColor
            border.color: borderColor
            border.width: 1
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 16  // 내부 여백 조정
                spacing: 15

                // 제목 레이블
                Text {
                    text: "Input"
                    font.pixelSize: 24  // 텍스트 크기 조정 (18pt에서 더 크게)
                    font.weight: Font.Medium
                    font.letterSpacing: -0.48  // 자간 조정 (-2%)
                    color: textColor
                }

                // 입력 필드들과 버튼을 포함하는 레이아웃
                GridLayout {
                    Layout.fillWidth: true
                    columns: 2
                    columnSpacing: 10
                    rowSpacing: 10
                    
                    // 첫 번째 입력 필드
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 50
                        radius: 8
                        color: inputBgColor
                        
                        TextInput {
                            id: input1
                            anchors.fill: parent
                            anchors.margins: 2
                            verticalAlignment: TextInput.AlignVCenter
                            horizontalAlignment: TextInput.AlignLeft
                            text: "3"
                            color: textColor
                            font.pixelSize: 18  // 텍스트 크기 조정 (18pt)
                            leftPadding: 15
                            selectByMouse: true
                            clip: true
                            
                            Text {
                                anchors.fill: parent
                                leftPadding: 15
                                verticalAlignment: Text.AlignVCenter
                                text: "첫 번째 변의 길이"
                                font.pixelSize: 18  // 텍스트 크기 조정 (18pt)
                                color: textColor
                                opacity: 0.5
                                visible: input1.text === ""
                            }
                        }
                    }
                    
                    // 판별하기 버튼 (세로로 확장)
                    Rectangle {
                        id: predictButton
                        Layout.rowSpan: 3
                        Layout.preferredWidth: 80
                        Layout.fillHeight: true
                        radius: 8
                        color: primaryColor
                        
                        MouseArea {
                            anchors.fill: parent
                            onClicked: {
                                console.log("판별하기 버튼 클릭됨");
                                triangleVisualizer.predict(input1.text, input2.text, input3.text);
                                parent.color = "#0066d6"  // 클릭 효과
                                clickTimer.start()
                            }
                        }
                        
                        Text {
                            anchors.centerIn: parent
                            text: "판별하기"
                            font.pixelSize: 18  // 텍스트 크기 조정 (18pt)
                            font.weight: Font.Medium
                            color: "white"
                        }
                        
                        Timer {
                            id: clickTimer
                            interval: 150
                            onTriggered: predictButton.color = primaryColor
                        }
                    }

                    // 두 번째 입력 필드
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 50
                        radius: 8
                        color: inputBgColor
                        
                        TextInput {
                            id: input2
                            anchors.fill: parent
                            anchors.margins: 2
                            verticalAlignment: TextInput.AlignVCenter
                            horizontalAlignment: TextInput.AlignLeft
                            text: "4"
                            color: textColor
                            font.pixelSize: 18  // 텍스트 크기 조정 (18pt)
                            leftPadding: 15
                            selectByMouse: true
                            clip: true
                            
                            Text {
                                anchors.fill: parent
                                leftPadding: 15
                                verticalAlignment: Text.AlignVCenter
                                text: "두 번째 변의 길이"
                                font.pixelSize: 18  // 텍스트 크기 조정 (18pt)
                                color: textColor
                                opacity: 0.5
                                visible: input2.text === ""
                            }
                        }
                    }

                    // 세 번째 입력 필드
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 50
                        radius: 8
                        color: inputBgColor
                        
                        TextInput {
                            id: input3
                            anchors.fill: parent
                            anchors.margins: 2
                            verticalAlignment: TextInput.AlignVCenter
                            horizontalAlignment: TextInput.AlignLeft
                            text: "5"
                            color: textColor
                            font.pixelSize: 18  // 텍스트 크기 조정 (18pt)
                            leftPadding: 15
                            selectByMouse: true
                            clip: true
                            
                            Text {
                                anchors.fill: parent
                                leftPadding: 15
                                verticalAlignment: Text.AlignVCenter
                                text: "세 번째 변의 길이"
                                font.pixelSize: 18  // 텍스트 크기 조정 (18pt)
                                color: textColor
                                opacity: 0.5
                                visible: input3.text === ""
                            }
                        }
                    }
                }
            }
        }

        // 결과 표시 영역
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 120
            radius: 8
            color: cardColor
            border.color: borderColor
            border.width: 1
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 16 
                spacing: 10
                
                // 결과 제목
                Text {
                    text: "Result"
                    font.pixelSize: 24 
                    font.weight: Font.Medium
                    font.letterSpacing: -0.48
                    color: textColor
                }
                
                // 결과 테이블
                Rectangle {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    color: "transparent"
                    
                    // 테이블 헤더
                    Row {
                        id: tableHeader
                        anchors.top: parent.top
                        anchors.left: parent.left
                        anchors.right: parent.right
                        height: 30
                        
                        Rectangle {
                            width: parent.width / 2
                            height: parent.height
                            color: "transparent"
                            border.color: borderColor
                            border.width: 1
                            
                            Text {
                                anchors.centerIn: parent
                                text: "AI 예측"
                                font.pixelSize: 14
                                font.weight: Font.Medium
                                color: textColor
                            }
                        }
                        
                        Rectangle {
                            width: parent.width / 2
                            height: parent.height
                            color: "transparent"
                            border.color: borderColor
                            border.width: 1
                            
                            Text {
                                anchors.centerIn: parent
                                text: "수학적 검증"
                                font.pixelSize: 14 
                                font.weight: Font.Medium
                                color: textColor
                            }
                        }
                    }
                    
                    // 테이블 내용
                    Row {
                        id: tableContent
                        anchors.top: tableHeader.bottom
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        
                        Rectangle {
                            id: aiResultCell
                            width: parent.width / 2
                            height: parent.height
                            color: "transparent"
                            border.color: borderColor
                            border.width: 1
                            
                            Text {
                                id: aiResultText
                                anchors.centerIn: parent
                                text: "O"
                                font.pixelSize: 24
                                font.weight: Font.Bold
                                color: successColor
                            }
                        }
                        
                        Rectangle {
                            id: mathResultCell
                            width: parent.width / 2
                            height: parent.height
                            color: "transparent"
                            border.color: borderColor
                            border.width: 1
                            
                            Text {
                                id: mathResultText
                                anchors.centerIn: parent
                                text: "O"
                                font.pixelSize: 24
                                font.weight: Font.Bold
                                color: successColor
                            }
                        }
                    }
                }
            }
            
            // 결과 변경 연결
            Connections {
                target: triangleVisualizer
                function onResultChanged(result) {
                    console.log("결과 변경됨: " + result);
                    resultLabel.text = result;
                    
                    // 결과 파싱하여 테이블 업데이트
                    if (result.includes("가능 (수학적 검증)")) {
                        mathResultText.text = "O";
                        mathResultText.color = successColor;
                    } else if (result.includes("불가능 (수학적 검증)")) {
                        mathResultText.text = "X";
                        mathResultText.color = errorColor;
                    }
                    
                    if (result.includes("AI 예측: 가능")) {
                        aiResultText.text = "O";
                        aiResultText.color = successColor;
                    } else if (result.includes("AI 예측: 불가능")) {
                        aiResultText.text = "X";
                        aiResultText.color = errorColor;
                    }
                }
            }
            
            // 원래 결과 텍스트 (숨김)
            Text {
                id: resultLabel
                visible: false
                text: "결과"
            }
        }

        // 캔버스 영역 (삼각형 시각화)
        Rectangle {
            id: canvasContainer
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.minimumHeight: 280  // 캔버스 최소 높이 증가
            radius: 8
            color: cardColor
            border.color: borderColor
            border.width: 1
            
            // 디버깅용 텍스트 - 숨김 처리
            Text {
                id: debugText
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.margins: 5
                font.pixelSize: 10
                color: "black"
                text: "디버깅: 준비됨"
                z: 10
                visible: false  // 디버깅 정보 숨김
            }
            
            Canvas {
                id: canvas
                anchors.fill: parent
                anchors.margins: 16  // 내부 여백 조정
                
                // 삼각형 데이터가 변경되면 캔버스 다시 그리기
                Connections {
                    target: triangleVisualizer
                    function onCanvasDataChanged() {
                        console.log("Canvas 데이터 변경됨");
                        // 디버깅 정보 업데이트 (표시는 안 함)
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
                    ctx.fillStyle = isDarkMode ? "#2c2c2e" : "#ffffff";
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
                        ctx.fillStyle = textColor;
                        ctx.font = "16px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto";
                        ctx.textAlign = "center";
                        ctx.fillText("유효한 변의 길이를 입력하세요", centerX, centerY);
                        return;
                    }
                    
                    var a = sides[0] * scale;
                    var b = sides[1] * scale;
                    var c = sides[2] * scale;
                    
                    // 스케일 조정 (너무 크거나 작지 않게)
                    // 삼각형이 캔버스 영역을 벗어나지 않도록 조정
                    var maxDimension = Math.min(width, height) * 0.4; // 더 작게 조정
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
                    ctx.strokeStyle = isDarkMode ? "#8e8e93" : "#8e8e93";
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.moveTo(centerX - c / 2, centerY);
                    ctx.lineTo(centerX + c / 2, centerY);
                    ctx.stroke();
                    
                    // c 변 길이 표시
                    ctx.fillStyle = isDarkMode ? "#8e8e93" : "#8e8e93";
                    ctx.font = "14px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto";
                    ctx.textAlign = "center";
                    ctx.fillText(sides[2].toString(), centerX, centerY + 20);
                    
                    // a 변 원 그리기 (빨간색 점선)
                    ctx.strokeStyle = "#ff2d55";  // iOS 핑크 컬러
                    ctx.lineWidth = 1.5;
                    ctx.setLineDash([3, 3]);
                    ctx.beginPath();
                    ctx.arc(centerX - c / 2, centerY, a, 0, 2 * Math.PI);
                    ctx.stroke();
                    
                    // a 변 길이 표시
                    ctx.fillStyle = "#ff2d55";
                    ctx.textAlign = "left";
                    ctx.fillText(sides[0].toString(), centerX - c / 2 - a / 2, centerY - a / 2);
                    
                    // b 변 원 그리기 (파란색 점선)
                    ctx.strokeStyle = "#5ac8fa";  // iOS 라이트 블루 컬러
                    ctx.setLineDash([3, 3]);
                    ctx.beginPath();
                    ctx.arc(centerX + c / 2, centerY, b, 0, 2 * Math.PI);
                    ctx.stroke();
                    
                    // b 변 길이 표시
                    ctx.fillStyle = "#5ac8fa";
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
                            
                            ctx.strokeStyle = primaryColor;
                            ctx.lineWidth = 2.5;
                            ctx.setLineDash([]);
                            
                            // 삼각형 그리기 (채우기 먼저)
                            ctx.fillStyle = isDarkMode ? "rgba(0, 122, 255, 0.25)" : "rgba(0, 122, 255, 0.15)";
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
                            
                        } catch (e) {
                            console.error("삼각형 그리기 오류: " + e);
                            ctx.fillStyle = errorColor;
                            ctx.font = "16px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto";
                            ctx.textAlign = "center";
                            ctx.fillText("그리기 오류가 발생했습니다", centerX, centerY);
                        }
                    } else {
                        console.log("삼각형 그리기 (불가능)");
                        // 삼각형이 불가능한 경우 시각화
                        ctx.setLineDash([]);
                        
                        // 변 표시 위치 조정 (더 가깝게)
                        var offsetY = 20;  // 위쪽으로 이동
                        var lineSpacing = 40;  // 두 선 사이의 간격
                        
                        // a 변 표시 (빨간색) - 위치 조정
                        ctx.strokeStyle = "#ff2d55";
                        ctx.lineWidth = 2.5;
                        ctx.beginPath();
                        ctx.moveTo(centerX - c / 4, centerY - offsetY);  // 시작점 조정
                        ctx.lineTo(centerX - c / 4 + a, centerY - offsetY);
                        ctx.stroke();
                        
                        ctx.fillStyle = "#ff2d55";
                        ctx.textAlign = "center";
                        ctx.fillText(sides[0].toString(), centerX - c / 4 + a / 2, centerY - offsetY - 10);
                        
                        // b 변 표시 (파란색) - 위치 조정
                        ctx.strokeStyle = "#5ac8fa";
                        ctx.beginPath();
                        ctx.moveTo(centerX + c / 4 - b, centerY - offsetY - lineSpacing);  // 시작점 조정
                        ctx.lineTo(centerX + c / 4, centerY - offsetY - lineSpacing);
                        ctx.stroke();
                        
                        ctx.fillStyle = "#5ac8fa";
                        ctx.textAlign = "center";
                        ctx.fillText(sides[1].toString(), centerX + c / 4 - b / 2, centerY - offsetY - lineSpacing - 10);
                        
                        ctx.fillStyle = errorColor;
                        ctx.font = "18px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto";
                        ctx.textAlign = "center";
                        ctx.fillText("삼각형 불가능", centerX, centerY + 50);
                        
                    }
                }
            }
        }
    }
}