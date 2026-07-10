from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMenu, QLabel,QApplication
import sys

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox

class MonWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        self.combo = QComboBox()
        self.combo.currentTextChanged.connect(self._on_option_choisie)
        layout.addWidget(self.combo)

        # boutons dont le nom alimente le combo
        self.combo.addItems(["Rouge", "Vert", "Bleu"])

    def _on_button_clicked(self):
        bouton = self.sender()
        self.ajouter_option(bouton.text())

    def ajouter_option(self, nom):
        if self.combo.findText(nom) == -1:
            self.combo.addItem(nom)
        self.combo.setCurrentText(nom)

    def _on_option_choisie(self, nom):
        print("Selection actuelle :", nom)
        
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MonWidget()
    window.show()
    sys.exit(app.exec())