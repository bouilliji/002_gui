from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSlider, QLabel, QPushButton, QLineEdit, QSizePolicy
from PyQt6.QtCore import Qt

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.widgets import RectangleSelector

import numpy as np
from astropy.io import fits
from astropy.visualization import ZScaleInterval, ImageNormalize, AsymmetricPercentileInterval


class Tools_File(QWidget):

    def __init__(self, image_data):
        super().__init__()
        self.setWindowTitle("FITS Viewer (PyQt6)")
        self.resize(1200, 800)
        self.move(0, 0)

        # donnees image (float, NaN possibles)
        self.image = np.asarray(image_data, dtype=float)

        # valeurs min/max initiales (ignorer NaN)
        self.minval = float(np.nanmin(self.image))
        self.maxval = float(np.nanmax(self.image))

        # protection si image constante / non-finite
        if not np.isfinite(self.minval):
            self.minval = 0.0
        if not np.isfinite(self.maxval):
            self.maxval = 1.0
        if self.maxval == self.minval:
            self.maxval = self.minval + 1.0

        # Layout principal sans marges ni espacement entre lignes
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
    
        # Figure
        fig = Figure()
        self.canvas = FigureCanvas(fig)
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.canvas)
        self.ax = fig.add_subplot(111)
    
        # afficher l'image et garder la reference a l'Image
        self.im = self.ax.imshow(self.image, cmap="gray", origin="lower",
                                 vmin=self.minval, vmax=self.maxval)
        self.ax.set_title("Image FITS")
        fig.tight_layout()
        self.canvas.draw()
    
        # Helper pour layouts horizontaux sans espaces
        def make_row():
            row = QHBoxLayout()
            row.setContentsMargins(0, 0, 0, 0)
            row.setSpacing(0)
            layout.addLayout(row)
            return row
    
        # --- Coordonnees: X, Y, ADU ---
        row_coords = make_row()
        row_coords.addWidget(QLabel("Coordonnees :   "))
        row_coords.addWidget(QLabel("X:"))
        self.edit_x = QLineEdit()
        self.edit_x.setReadOnly(True)
        self.edit_x.setFixedWidth(80)
        row_coords.addWidget(self.edit_x)
        row_coords.addWidget(QLabel("Y:"))
        self.edit_y = QLineEdit()
        self.edit_y.setReadOnly(True)
        self.edit_y.setFixedWidth(80)
        row_coords.addWidget(self.edit_y)
        row_coords.addWidget(QLabel("ADU:"))
        self.edit_adu = QLineEdit()
        self.edit_adu.setReadOnly(True)
        self.edit_adu.setFixedWidth(140)
        row_coords.addWidget(self.edit_adu)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        row_coords.addWidget(spacer)
    
        # --- Visu label ---
        row_visu_label = make_row()
        row_visu_label.addWidget(QLabel("Visu :"))
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        row_visu_label.addWidget(spacer)
    
        # Slider min
        row_slider_min = make_row()
        row_slider_min.addWidget(QLabel("Min"))
        self.slider_min = QSlider(Qt.Orientation.Horizontal)
        self.slider_min.setMinimum(0)
        self.slider_min.setMaximum(1000)
        self.slider_min.setValue(0)
        self.slider_min.setFixedHeight(20)
        row_slider_min.addWidget(self.slider_min)

        # Slider max
        row_slider_max = make_row()
        row_slider_max.addWidget(QLabel("Max"))
        self.slider_max = QSlider(Qt.Orientation.Horizontal)
        self.slider_max.setMinimum(0)
        self.slider_max.setMaximum(1000)
        self.slider_max.setValue(1000)
        self.slider_max.setFixedHeight(20)
        row_slider_max.addWidget(self.slider_max)
    
        # Connexions sliders
        self.slider_min.valueChanged.connect(self._on_threshold_changed)
        self.slider_max.valueChanged.connect(self._on_threshold_changed)
    
        # Auto: Iris Percentile Zscale Vmin Vmax
        row_auto = make_row()
        row_auto.addWidget(QLabel("Auto :"))
        self.btn_iris = QPushButton("Iris")
        row_auto.addWidget(self.btn_iris)
        self.btn_iris.clicked.connect(self._apply_iris)
        self.btn_percentile = QPushButton("Percentile")
        row_auto.addWidget(self.btn_percentile)
        self.btn_percentile.clicked.connect(self._apply_percentile)
        self.btn_zscale = QPushButton("Zscale")
        row_auto.addWidget(self.btn_zscale)
        self.btn_zscale.clicked.connect(self._apply_zscale)
        row_auto.addWidget(QLabel("Vmin:"))
        self.edit_vmin = QLineEdit()
        self.edit_vmin.setFixedWidth(140)
        row_auto.addWidget(self.edit_vmin)
        row_auto.addWidget(QLabel("Vmax:"))
        self.edit_vmax = QLineEdit()
        self.edit_vmax.setFixedWidth(140)
        row_auto.addWidget(self.edit_vmax)
    
        # Connexions pour appliquer la valeur quand l'utilisateur appuie sur Enter ou quitte le champ
        self.edit_vmin.returnPressed.connect(self._on_text_values_changed)
        self.edit_vmax.returnPressed.connect(self._on_text_values_changed)
        self.edit_vmin.editingFinished.connect(self._on_text_values_changed)
        self.edit_vmax.editingFinished.connect(self._on_text_values_changed)

        # Initialiser les champs avec les valeurs actuelles
        vmin0 = self._slider_to_value(self.slider_min.value())
        vmax0 = self._slider_to_value(self.slider_max.value())
        self._update_value_fields(vmin0, vmax0)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        row_auto.addWidget(spacer)

        # Zoom: Zoom and Reset buttons
        row_zoom = make_row()
        row_zoom.addWidget(QLabel("Zoom:"))
        self.btn_zoom = QPushButton("Zoom")
        row_zoom.addWidget(self.btn_zoom)
        self.btn_zoom.clicked.connect(self._zoom_to_rectangle)
        self.btn_reset = QPushButton("Reset")
        row_zoom.addWidget(self.btn_reset)
        self.btn_reset.clicked.connect(self._reset_zoom)
        self.btn_half = QPushButton("Half")
        row_zoom.addWidget(self.btn_half)
        self.btn_half.clicked.connect(self._reset_zoom_half)
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        row_zoom.addWidget(spacer)

        # Connecter l'event motion_notify_event de matplotlib
        self.canvas.mpl_connect("motion_notify_event", self._on_mouse_move)
    
        # RectangleSelector for interactive rectangle selection (no drawtype arg)
        self._rect = None
        rectprops = dict(facecolor="none", edgecolor="red", linestyle="-",
                         linewidth=1, alpha=0.8)
        self._rect_selector = RectangleSelector(
            self.ax, self._on_select,
            useblit=True,
            button=[1],
            minspanx=1, minspany=1,
            spancoords="pixels",
            interactive=True
        )

        # store last rectangle coords in image pixel space (x0,y0,x1,y1) or None
        self.last_rect = None



    def _on_mouse_move(self, event):
        """Met a jour X, Y, ADU selon la position de la souris sur l'image."""
        # Si souris hors axes ou pas sur image, vider les champs
        if event.inaxes is None:
            self.edit_x.clear()
            self.edit_y.clear()
            self.edit_adu.clear()
            return

        # Obtenir coordonnees dans l'image (float); convertir en indices entiers
        xdata = event.xdata
        ydata = event.ydata
        if xdata is None or ydata is None:
            self.edit_x.clear()
            self.edit_y.clear()
            self.edit_adu.clear()
            return

        # Les images sont affichees avec origin='lower', coordonnees y commencent a 0 en bas
        # Convertir en indices int en tenant compte des limites
        ix = int(np.floor(xdata + 0.5))
        iy = int(np.floor(ydata + 0.5))

        ny, nx = self.image.shape
        if ix < 0 or ix >= nx or iy < 0 or iy >= ny:
            # hors image
            self.edit_x.clear()
            self.edit_y.clear()
            self.edit_adu.clear()
            return

        # Recuperer valeur ADU du pixel
        val = self.image[iy, ix]

        # Mettre a jour champs (format compact)
        self.edit_x.setText(str(ix))
        self.edit_y.setText(str(iy))
        # formater ADU avec precision raisonnable
        if np.isfinite(val):
            self.edit_adu.setText("{:.6g}".format(float(val)))
        else:
            self.edit_adu.setText("")

    @staticmethod
    def load_fits_image(filename):
        """Charge un fichier FITS (supporte .gz) et retourne les donnees numpy."""
        with fits.open(filename, memmap=False) as hdul:
            return np.array(hdul[0].data, dtype=float)

    def _slider_to_value(self, slider_value):
        """Mappe la position du slider (0..1000) a l'echelle lineaire des donnees."""
        frac = slider_value / 1000.0
        return self.minval + frac * (self.maxval - self.minval)

    def _update_value_fields(self, vmin, vmax):
        """Met a jour les champs texte sans ecraser si l'utilisateur edite."""
        fmt = "{:.6g}"
        if not self.edit_vmin.hasFocus():
            self.edit_vmin.setText(fmt.format(vmin))
        if not self.edit_vmax.hasFocus():
            self.edit_vmax.setText(fmt.format(vmax))

    def _apply_iris(self):

        imin = np.min(self.image)
        imax = np.max(self.image)
        median = np.median(self.image)
        vmin = median - 200
        vmax = median + 1000
        if vmin<imin:
            vmin = imin
        if vmax > imax:
            vmax = imax    

        self.im.set_clim(vmin, vmax)
        self.canvas.draw_idle()

        def value_to_slider(val):
            range_ = (self.maxval - self.minval) or 1.0
            frac = (val - self.minval) / range_
            return int(max(0, min(1000, round(frac * 1000))))

        self.slider_min.blockSignals(True)
        self.slider_max.blockSignals(True)
        self.slider_min.setValue(value_to_slider(vmin))
        self.slider_max.setValue(value_to_slider(vmax))
        self.slider_min.blockSignals(False)
        self.slider_max.blockSignals(False)

        self._update_value_fields(vmin, vmax)

    def _apply_percentile(self, lowpct=3, highpct=98):
        """Calcule les percentiles lowpct-highpct en ignorant NaN et applique."""
        data = self.image
        # extraire valeurs finies
        vals = data[np.isfinite(data)].ravel()
        if vals.size == 0:
            vmin = self.minval
            vmax = self.maxval
        else:
            vmin = float(np.percentile(vals, lowpct))
            vmax = float(np.percentile(vals, highpct))

        vmin, vmax = AsymmetricPercentileInterval(3, 98).get_limits(data)

        if vmin >= vmax:
            vmax = vmin + max(1e-6, 0.001 * abs(self.maxval - self.minval))

        try:
            self.im.set_norm(None)
        except Exception:
            pass
        self.im.set_clim(vmin, vmax)
        self.canvas.draw_idle()

        def value_to_slider(val):
            range_ = (self.maxval - self.minval) or 1.0
            frac = (val - self.minval) / range_
            return int(max(0, min(1000, round(frac * 1000))))

        self.slider_min.blockSignals(True)
        self.slider_max.blockSignals(True)
        self.slider_min.setValue(value_to_slider(vmin))
        self.slider_max.setValue(value_to_slider(vmax))
        self.slider_min.blockSignals(False)
        self.slider_max.blockSignals(False)

        self._update_value_fields(vmin, vmax)


    def _apply_zscale(self):
        try:
            interval = ZScaleInterval()
            # preferer get_limits quand disponible
            if hasattr(interval, "get_limits"):
                vmin, vmax = interval.get_limits(self.image)
            else:
                # fallback: appeler interval puis deduire echelle depuis resultat si possible
                res = interval(self.image)
                if isinstance(res, (tuple, list, np.ndarray)):
                    # si c'est un tableau (image normalisee), prendre min/max et denormaliser
                    arr = np.asarray(res)
                    if arr.size > 1 and np.isfinite(arr).any():
                        rmin, rmax = float(np.nanmin(arr)), float(np.nanmax(arr))
                        # denormaliser par minval/maxval de l'image retourne si besoin
                        # ici mieux prendre percentiles sur image d'origine comme fallback
                        vmin = float(np.nanpercentile(self.image, 0.5))
                        vmax = float(np.nanpercentile(self.image, 99.5))
                    else:
                        raise ValueError
                else:
                    raise ValueError
            if not (np.isfinite(vmin) and np.isfinite(vmax)):
                raise ValueError
        except Exception:
            # fallback simple: percentiles robustes
            vals = self.image[np.isfinite(self.image)].ravel()
            if vals.size:
                vmin = float(np.percentile(vals, 0.5))
                vmax = float(np.percentile(vals, 99.5))
            else:
                vmin, vmax = self.minval, self.maxval

        if vmin >= vmax:
            vmax = vmin + max(1e-6, 0.001 * abs(self.maxval - self.minval))

        try:
            self.im.set_norm(None)
        except Exception:
            pass
        self.im.set_clim(vmin, vmax)
        self.canvas.draw_idle()

        def value_to_slider(val):
            range_ = (self.maxval - self.minval) or 1.0
            frac = (val - self.minval) / range_
            return int(max(0, min(1000, round(frac * 1000))))

        self.slider_min.blockSignals(True)
        self.slider_max.blockSignals(True)
        self.slider_min.setValue(value_to_slider(vmin))
        self.slider_max.setValue(value_to_slider(vmax))
        self.slider_min.blockSignals(False)
        self.slider_max.blockSignals(False)

        self._update_value_fields(vmin, vmax)




    def _on_text_values_changed(self):
        # Lire les valeurs texte, convertir en float si possible
        try:
            vmin = float(self.edit_vmin.text())
        except Exception:
            vmin = self._slider_to_value(self.slider_min.value())

        try:
            vmax = float(self.edit_vmax.text())
        except Exception:
            vmax = self._slider_to_value(self.slider_max.value())

        # S'assurer ordre correct
        if vmin >= vmax:
            delta = max(1e-6, 0.001 * abs(self.maxval - self.minval))
            if self.sender() is self.edit_vmin:
                vmin = vmax - delta
            else:
                vmax = vmin + delta

        try:
            self.im.set_norm(None)
        except Exception:
            pass
        self.im.set_clim(vmin, vmax)
        self.canvas.draw_idle()

        def value_to_slider(val):
            range_ = (self.maxval - self.minval) or 1.0
            frac = (val - self.minval) / range_
            return int(max(0, min(1000, round(frac * 1000))))

        self.slider_min.blockSignals(True)
        self.slider_max.blockSignals(True)
        self.slider_min.setValue(value_to_slider(vmin))
        self.slider_max.setValue(value_to_slider(vmax))
        self.slider_min.blockSignals(False)
        self.slider_max.blockSignals(False)

        self._update_value_fields(vmin, vmax)

    def _on_threshold_changed(self, _=None):
        # Obtenir vmin/vmax depuis les sliders
        vmin = self._slider_to_value(self.slider_min.value())
        vmax = self._slider_to_value(self.slider_max.value())

        # S'assurer vmin < vmax
        if vmin >= vmax:
            if self.sender() is self.slider_min:
                vmin = vmax - max(1e-6, 0.001 * abs(self.maxval - self.minval))
            else:
                vmax = vmin + max(1e-6, 0.001 * abs(self.maxval - self.minval))

        try:
            self.im.set_norm(None)
        except Exception:
            pass
        self.im.set_clim(vmin, vmax)
        self.canvas.draw_idle()

        self._update_value_fields(vmin, vmax)


    # Rectangle selector callback: store rectangle in image pixel coords
    def _on_select(self, eclick, erelease):
        # eclick and erelease are matplotlib events with xdata,ydata in data coords
        x0, y0 = eclick.xdata, eclick.ydata
        x1, y1 = erelease.xdata, erelease.ydata
        if x0 is None or y0 is None or x1 is None or y1 is None:
            self.last_rect = None
            return
        # convert to integer pixel indices (round)
        ix0 = int(np.floor(min(x0, x1) + 0.5))
        ix1 = int(np.floor(max(x0, x1) + 0.5))
        iy0 = int(np.floor(min(y0, y1) + 0.5))
        iy1 = int(np.floor(max(y0, y1) + 0.5))
        ny, nx = self.image.shape
        # clamp to image bounds
        ix0 = max(0, min(ix0, nx-1))
        ix1 = max(0, min(ix1, nx-1))
        iy0 = max(0, min(iy0, ny-1))
        iy1 = max(0, min(iy1, ny-1))
        if ix1 <= ix0 or iy1 <= iy0:
            self.last_rect = None
        else:
            self.last_rect = (ix0, iy0, ix1, iy1)
        # draw rectangle overlay: RectangleSelector already draws it interactively

    def _zoom_to_rectangle(self):
        """Zoom to last selected rectangle."""
        if self.last_rect is None:
            return
        ix0, iy0, ix1, iy1 = self.last_rect
        # set axis limits correctly for origin='lower'
        # x corresponds to columns [ix0..ix1], y to rows [iy0..iy1]
        self.ax.set_xlim(ix0 - 0.5, ix1 + 0.5)
        self.ax.set_ylim(iy0 - 0.5, iy1 + 0.5)
        self.canvas.draw_idle()

    def _reset_zoom(self):
        """Reset axes to show full image."""
        ny, nx = self.image.shape
        self.ax.set_xlim(-0.5, nx - 0.5)
        self.ax.set_ylim(-0.5, ny - 0.5)
        self.canvas.draw_idle()

    def _reset_zoom_half(self):
        """
        Dezoom by factor 2 around current view center.
        Keeps axes limits within image extents.
        """
        # image extents in data coords
        ny, nx = self.image.shape
        x_min_img, x_max_img = 0.0, float(nx)
        y_min_img, y_max_img = 0.0, float(ny)

        # current view limits
        x0, x1 = self.ax.get_xlim()
        y0, y1 = self.ax.get_ylim()

        # center and current half-sizes
        cx = 0.5 * (x0 + x1)
        cy = 0.5 * (y0 + y1)
        half_w = 0.5 * (x1 - x0)
        half_h = 0.5 * (y1 - y0)

        # new half-sizes (multiply by 2 to dezoom by 2)
        new_half_w = half_w * 2.0
        new_half_h = half_h * 2.0

        # compute new limits
        new_x0 = cx - new_half_w
        new_x1 = cx + new_half_w
        new_y0 = cy - new_half_h
        new_y1 = cy + new_half_h

        # clamp to image extents
        width = new_x1 - new_x0
        height = new_y1 - new_y0

        if width >= (x_max_img - x_min_img):
            new_x0, new_x1 = x_min_img, x_max_img
        else:
            if new_x0 < x_min_img:
                new_x1 = x_min_img + width
                new_x0 = x_min_img
            if new_x1 > x_max_img:
                new_x0 = x_max_img - width
                new_x1 = x_max_img

        if height >= (y_max_img - y_min_img):
            new_y0, new_y1 = y_min_img, y_max_img
        else:
            if new_y0 < y_min_img:
                new_y1 = y_min_img + height
                new_y0 = y_min_img
            if new_y1 > y_max_img:
                new_y0 = y_max_img - height
                new_y1 = y_max_img

        # apply limits and redraw
        self.ax.set_xlim(new_x0, new_x1)
        self.ax.set_ylim(new_y0, new_y1)
        self.canvas.draw_idle()




    def _on_mouse_move(self, event):
        if event.inaxes is None:
            self.edit_x.clear()
            self.edit_y.clear()
            self.edit_adu.clear()
            return
        xdata = event.xdata
        ydata = event.ydata
        if xdata is None or ydata is None:
            self.edit_x.clear()
            self.edit_y.clear()
            self.edit_adu.clear()
            return
        ix = int(np.floor(xdata + 0.5))
        iy = int(np.floor(ydata + 0.5))
        ny, nx = self.image.shape
        if ix < 0 or ix >= nx or iy < 0 or iy >= ny:
            self.edit_x.clear()
            self.edit_y.clear()
            self.edit_adu.clear()
            return
        val = self.image[iy, ix]
        self.edit_x.setText(str(ix))
        self.edit_y.setText(str(iy))
        if np.isfinite(val):
            self.edit_adu.setText("{:.6g}".format(float(val)))
        else:
            self.edit_adu.clear()
