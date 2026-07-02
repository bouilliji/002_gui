# outils systemes
import sys

# QT
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout,
    QPushButton, QLabel, QMainWindow, QFileDialog, QMessageBox, QHBoxLayout
)
from PyQt6.QtCore import Qt

# Utilitaires
from tools.Tools_File import Tools_File



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
            self.parent.image_data = Tools_File.load_fits_image(filename)
            QMessageBox.information(self, "Chargement", f"Image chargee : {filename}")

    def afficher_image(self):
        if self.parent.image_data is None:
            QMessageBox.warning(self, "Erreur", "Aucune image chargee.")
            return
        self.parent.image_window = Tools_File(self.parent.image_data)
        self.parent.image_window.show()

    def quitter(self):
        sys.exit() 
