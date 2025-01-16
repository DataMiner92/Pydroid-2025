import sys
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication
from PySide6.QtQuick import QQuickView

app = QApplication(sys.argv)
view = QQuickView()
view.setResizeMode(QQuickView.SizeRootObjectToView)

view.engine().quit.connect(app.quit)
view.setSource(QUrl('declarative-camera.qml'))
view.show()
sys.exit(app.exec())
