import sys
from PyQt6.QtWidgets import QApplication, QLabel

app = QApplication(sys.argv)
label = QLabel("Test PyQt6 OK")
label.show()
sys.exit(app.exec())
