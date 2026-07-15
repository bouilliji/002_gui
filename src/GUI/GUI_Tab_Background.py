# QT
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QLineEdit, QGroupBox, QSpinBox, QSizePolicy, QStackedWidget
from PyQt6.QtCore import Qt

# Utilitaires
from tools.Tools_Background import Tools_Background

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np

class GUI_Tab_Background(QWidget):

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
        layout = QVBoxLayout(self.page_pleine)
        
        self.stack.addWidget(self.page_pleine)

        # ---------------- Barre du haut : median / bi-weight ----------------
        top_bar = QHBoxLayout()
        top_bar.addWidget(QLabel("median :"))
        self.median_edit = QLineEdit()
        self.median_edit.setFixedWidth(100)
        self.median_edit.setReadOnly(True)
        top_bar.addWidget(self.median_edit)

        top_bar.addSpacing(30)

        top_bar.addWidget(QLabel("bi-weight :"))
        self.biweight_edit = QLineEdit()
        self.biweight_edit.setFixedWidth(120)
        self.biweight_edit.setReadOnly(True)
        top_bar.addWidget(self.biweight_edit)

        top_bar.addStretch()
        layout.addLayout(top_bar)

        # ---------------- Corps : panneau gauche + zone matplotlib ----------------
        body_layout = QHBoxLayout()
        layout.addLayout(body_layout)

        # ---- Panneau gauche ----
        
        # ---- Boutton methode ----
        left_panel = QGroupBox("Methode")
        left_layout = QVBoxLayout(left_panel)

        self.method_median_button = QPushButton("median noise\nestimation")
        self.method_2d_button = QPushButton("2d background\nnoise estimation")

        left_layout.addWidget(self.method_median_button)
        left_layout.addWidget(self.method_2d_button)
        left_layout.addSpacing(15)

        # ---- Zone de texte ----
        
        # ---- Sigma ----
        
        row_sigma = QHBoxLayout()
        row_sigma.addWidget(QLabel("Sigma :"))
        row_sigma.addStretch()
        
        self.spin_sigma = QSpinBox()
        self.spin_sigma.setSingleStep(int(1))

        self.spin_sigma.setMinimum(1)
        self.spin_sigma.setMaximum(2147483647)
        self.spin_sigma.setValue(1)
        self.spin_sigma.setFixedWidth(120)
        
        row_sigma.addWidget(self.spin_sigma)
        left_layout.addLayout(row_sigma)
        
        left_layout.addSpacing(10)
        
        # ---- Box Size ----
        
        row_box_size = QHBoxLayout()
        row_box_size.addWidget(QLabel("Box Size :"))
        row_box_size.addStretch()
        
        self.spin_box_size = QSpinBox()
        self.spin_box_size.setSingleStep(int(1))

        self.spin_box_size.setMinimum(1)
        self.spin_box_size.setMaximum(2147483647)
        self.spin_box_size.setValue(1)
        self.spin_box_size.setFixedWidth(120)
        
        row_box_size.addWidget(self.spin_box_size)
        left_layout.addLayout(row_box_size)
        
        left_layout.addSpacing(10)
        
        # ---- Filter Size ----
        
        row_filter_size = QHBoxLayout()
        row_filter_size.addWidget(QLabel("Filter Size :"))
        row_filter_size.addStretch()
        
        self.spin_filter_size = QSpinBox()
        self.spin_filter_size.setSingleStep(int(1))

        self.spin_filter_size.setMinimum(1)
        self.spin_filter_size.setMaximum(2147483647)
        self.spin_filter_size.setValue(1)
        self.spin_filter_size.setFixedWidth(120)
        
        row_filter_size.addWidget(self.spin_filter_size)
        left_layout.addLayout(row_filter_size)

        left_layout.addStretch()
        left_panel.setFixedWidth(280)
        body_layout.addWidget(left_panel)

        # ---- Zone droite : matplotlib + boutons ----
        right_layout = QVBoxLayout()

        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        right_layout.addWidget(self.canvas, stretch=1)

        # Boutons Reset / Apply (alignés à droite comme sur le croquis)
        button_row = QHBoxLayout()
        button_row.addStretch()
        self.reset_button = QPushButton("Reset")
        self.apply_button = QPushButton("Apply")
        self.reset_button.setFixedWidth(100)
        self.apply_button.setFixedWidth(100)
        button_row.addWidget(self.reset_button)
        button_row.addWidget(self.apply_button)
        right_layout.addLayout(button_row)

        body_layout.addLayout(right_layout, stretch=1)
        
        self.update()
        
    def update(self):
        if self.parent.image_data is not None:
            
            self.minval = float(np.nanmin(self.parent.image_data))
            self.maxval = float(np.nanmax(self.parent.image_data))
            
            self.stack.setCurrentWidget(self.page_pleine)
            self.ax.clear()   # <-- vider les axes avant de redessiner
            self.im = self.ax.imshow(self.parent.image_data, cmap="gray", origin="lower",
                                    vmin=self.minval, vmax=self.maxval)
            median, biweight = Tools_Background.compute_background_stats(self.parent.image_data)
            self.median_edit.setText(str(median))
            self.biweight_edit.setText(str(biweight))
        else:
            self.stack.setCurrentWidget(self.page_vide)
            