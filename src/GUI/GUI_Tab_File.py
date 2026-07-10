# outils systemes
import sys

# QT
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout,
    QPushButton, QLabel, QMainWindow, QFileDialog, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt


import numpy as np

from astropy.io import fits



class GUI_Tab_File(QWidget):

    def __init__(self, parent):

        super().__init__()
        self.parent = parent

        layout = QHBoxLayout()

        boutons_layout = QVBoxLayout()
        boutons_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.btn_charger  = QPushButton("Charger")
        self.btn_afficher = QPushButton("Afficher")
        self.btn_quitter  = QPushButton("Quitter")

        boutons_layout.addWidget(self.btn_charger)
        boutons_layout.addWidget(self.btn_afficher)
        boutons_layout.addWidget(self.btn_quitter)

        label = QLabel("Onglet Fichiers")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(boutons_layout, 1)
        layout.addWidget(label, 3)
        self.setLayout(layout)

        self.btn_charger.clicked.connect(self.charger_image)
        self.btn_afficher.clicked.connect(self.afficher_image)
        self.btn_quitter.clicked.connect(self.quitter)

    def charger_image(self):
        
        # introspection des classes Python
        #print(f"methode classes QWidget = {dir(QWidget)}")
        #print(f"methode classes QWidget = {QWidget.parent.__doc__}")
        
        filename, _ = QFileDialog.getOpenFileName(
            self, "Choisir un fichier FITS", "", "FITS Files (*.fits *.fits.gz)"
        )
        if filename:
            with fits.open(filename, memmap=False) as hdul:
                self.parent.base_image = np.array(hdul[0].data, dtype=float)
                self.parent.image_data = self.parent.base_image.copy()
            QMessageBox.information(self, "Chargement", f"Image chargee : {filename}")
            self.parent.display.update_display()

    def afficher_image(self):
        self.parent.onglets.setCurrentIndex(1)
        
        
    def quitter(self):
        sys.exit() 
