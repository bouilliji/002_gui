import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout,
    QPushButton, QLabel, QMainWindow, QFileDialog, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt

import argparse

# GUI onglets
from GUI.GUI_Tab_File       import GUI_Tab_File
from GUI.GUI_Tab_Background import GUI_Tab_Background
from GUI.GUI_Tab_Centroid   import GUI_Tab_Centroid


class main_window(QMainWindow):

    def __init__(self):

        super().__init__()
        self.setWindowTitle("Interface FITS - PyQt6")
        self.resize(900, 600)
        self.move(0, 0)
        self.image_data = None
        self.image_window = None

        onglets = QTabWidget()
        onglets.addTab(GUI_Tab_File(self),       "File")
        onglets.addTab(GUI_Tab_Background(self), "Background")
        onglets.addTab(GUI_Tab_Centroid(self),   "Centroid")

        widget_central = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(onglets)
        widget_central.setLayout(layout)
        self.setCentralWidget(widget_central)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main_window()
    window.show()
    sys.exit(app.exec())
