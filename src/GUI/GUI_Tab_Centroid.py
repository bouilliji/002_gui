# QT
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout,
    QPushButton, QLabel, QMainWindow, QFileDialog, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt








class GUI_Tab_Centroid(QWidget):

    def __init__(self, parent):

        super().__init__()
        self.parent = parent

        layout = QHBoxLayout()

        boutons_layout = QVBoxLayout()
        boutons_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        btn1 = QPushButton("Bouton1")
        btn2 = QPushButton("Bouton2")
        boutons_layout.addWidget(btn1)
        boutons_layout.addWidget(btn2)

        label = QLabel("Onglet Centroid")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(boutons_layout, 1)
        layout.addWidget(label, 3)
        self.setLayout(layout)

