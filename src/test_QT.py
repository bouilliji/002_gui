"""
Layout PyQt6 reproduisant le second croquis (UI pure, sans logique).
Aucune connexion fonctionnelle n'est faite sur les widgets.
A toi de brancher ta propre logique derriere chaque widget.

Installation nécessaire :
    pip install PyQt6 matplotlib

Lancement :
    python calcul_ui.py
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QGroupBox, QFrame,
    QSizePolicy
)

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class CalculWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calcul")
        self.resize(1000, 650)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        # ---------------- Cadre principal (rectangle englobant sur le croquis) ----------------
        main_frame = QFrame()
        main_frame.setFrameShape(QFrame.Shape.Box)
        frame_layout = QHBoxLayout(main_frame)
        main_layout.addWidget(main_frame)

        # ---- Panneau gauche : Methode / Calcule / Info ----
        left_layout = QVBoxLayout()

        left_layout.addWidget(QLabel("Methode"))

        self.methode_combo = QComboBox()
        left_layout.addWidget(self.methode_combo)

        self.calcule_button = QPushButton("Calcule")
        left_layout.addWidget(self.calcule_button)

        self.info_box = QGroupBox("Info")
        self.info_box.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.info_layout = QVBoxLayout(self.info_box)
        left_layout.addWidget(self.info_box, stretch=1)

        frame_layout.addLayout(left_layout, stretch=1)

        # ---- Panneau droite : display matplotlib + bouton Save ----
        right_layout = QVBoxLayout()

        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        right_layout.addWidget(self.canvas, stretch=1)

        save_row = QHBoxLayout()
        save_row.addStretch()
        self.save_button = QPushButton("Save")
        self.save_button.setFixedWidth(100)
        save_row.addWidget(self.save_button)
        right_layout.addLayout(save_row)

        frame_layout.addLayout(right_layout)


def main():
    app = QApplication(sys.argv)
    window = CalculWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()