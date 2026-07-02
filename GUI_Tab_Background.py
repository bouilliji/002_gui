# QT
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout,
    QPushButton, QLabel, QMainWindow, QFileDialog, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt

# Utilitaires
from Tools_Background import Tools_Background





class GUI_Tab_Background(QWidget):

    def __init__(self, parent):

        super().__init__()
        self.parent = parent

        layout = QHBoxLayout()

        boutons_layout = QVBoxLayout()
        boutons_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        btn_median = QPushButton("Median")
        btn_b2     = QPushButton("Bouton2")
        btn_b3     = QPushButton("Bouton3")

        boutons_layout.addWidget(btn_median)
        boutons_layout.addWidget(btn_b2)
        boutons_layout.addWidget(btn_b3)

        label = QLabel("Onglet Background")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(boutons_layout, 1)
        layout.addWidget(label, 3)
        self.setLayout(layout)

        btn_median.clicked.connect(self.compute_median)

    def compute_median(self):

        if self.parent.image_data is None:
            QMessageBox.warning(self, "Erreur", "Aucune image chargee.")
            return

        median, biweight = Tools_Background.compute_background_stats(self.parent.image_data)
        QMessageBox.information(self,"Resultat Background",f"Median = {median:.3f}\nBiweight = {biweight:.3f}"
        )
