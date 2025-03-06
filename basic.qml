import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 300
    height: 200
    title: "Basic QML Test"
    
    Column {
        anchors.centerIn: parent
        spacing: 10
        
        Label {
            text: "Hello QML World!"
        }
        
        Button {
            text: "Click Me"
            onClicked: {
                console.log("Button clicked")
            }
        }
    }
} 