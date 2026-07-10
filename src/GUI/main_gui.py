import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout,
    QPushButton, QLabel, QMainWindow, QFileDialog, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt

import argparse

# GUI onglets
from GUI_Tab_File       import GUI_Tab_File
from GUI_Tab_Display    import GUI_Tab_Display
from GUI_Tab_Background import GUI_Tab_Background
from GUI_Tab_Centroid   import GUI_Tab_Centroid


class main_window(QMainWindow):

    def __init__(self):

        super().__init__()
        self.setWindowTitle("Interface FITS - PyQt6")
        self.resize(900, 600)
        self.move(0, 0)
        self.base_image = None
        self.image_data = None
        self.image_window = None
        
        self.display = GUI_Tab_Display(self)

        self.onglets = QTabWidget()
        self.onglets.addTab(GUI_Tab_File(self),       "File")
        self.onglets.addTab(self.display,             "Display")
        self.onglets.addTab(GUI_Tab_Background(self), "Background")
        self.onglets.addTab(GUI_Tab_Centroid(self),   "Centroid")

        widget_central = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.onglets)
        widget_central.setLayout(layout)
        self.setCentralWidget(widget_central)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = main_window()
    window.show()
    sys.exit(app.exec())
