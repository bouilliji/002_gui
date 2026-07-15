# QT
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QComboBox, QGroupBox, QSizePolicy, QStackedWidget
from PyQt6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


import numpy as np




class GUI_Tab_Centroid(QWidget):

    def __init__(self, parent):

        super().__init__()
        self.parent = parent

        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        self.setLayout(outer_layout)

        self.stack = QStackedWidget()
        outer_layout.addWidget(self.stack)
        
        # --- Page vide (aucune image) ---
        self.page_vide = QWidget()
        layout_vide = QVBoxLayout(self.page_vide)
        label_vide = QLabel("Vous n'avez pas selctione l'image a utilise aller dan image et choisiser votre preset")
        label_vide.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_vide.addWidget(label_vide)
        self.stack.addWidget(self.page_vide)
        
        
        self.page_pleine = QWidget()
        layout = QHBoxLayout(self.page_pleine)
        
        self.stack.addWidget(self.page_pleine)

        # ---- Panneau gauche : Methode / Calcule / Info ----
        left_layout = QVBoxLayout()

        left_layout.addWidget(QLabel("Methode"))

        self.methode_combo = QComboBox()
        left_layout.addWidget(self.methode_combo)
        
        self.methode_combo.addItems(['Centroïde with flux-weighted', 'Centroid with 2d quadratique', 'centroid with 1d Gaussians', 'centroid with 2d Gaussians', "-- chose a methode --"])
        self.methode_combo.setCurrentIndex(4)
        
        self.calcule_button = QPushButton("Calcule")
        left_layout.addWidget(self.calcule_button)

        self.info_box = QGroupBox("Info")
        self.info_box.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        self.info_layout = QVBoxLayout(self.info_box)
        left_layout.addWidget(self.info_box, stretch=1)
        
        layout.addLayout(left_layout, stretch=2)

        # ---- Panneau droite : display matplotlib + bouton Save ----
        right_layout = QVBoxLayout()

        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        right_layout.addWidget(self.canvas, stretch=1)

        save_row = QHBoxLayout()
        save_row.addStretch()
        self.save_button = QPushButton("Save")
        self.save_button.setFixedWidth(100)
        save_row.addWidget(self.save_button)
        right_layout.addLayout(save_row)
        
        layout.addLayout(right_layout, stretch=3)
        
        self.update()
        
    def update(self):
        if self.parent.image_data is not None:
            
            self.minval = float(np.nanmin(self.parent.image_data))
            self.maxval = float(np.nanmax(self.parent.image_data))
            
            self.stack.setCurrentWidget(self.page_pleine)
            self.ax.clear()   # <-- vider les axes avant de redessiner
            self.im = self.ax.imshow(self.parent.image_data, cmap="gray", origin="lower",
                                    vmin=self.minval, vmax=self.maxval)
        else:
            self.stack.setCurrentWidget(self.page_vide)

