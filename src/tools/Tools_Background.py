import numpy as np
from astropy.stats import biweight_location


class Tools_Background():

    def __init__(self, parent):
        self.parent = parent

    @staticmethod
    def compute_background_stats(image_data):
        """Calcule la mediane et la biweight_location d'une image."""
        if image_data is None:
            raise ValueError("image_data is None")
        arr = np.asarray(image_data).ravel()
        arr = arr[np.isfinite(arr)]
        if arr.size == 0:
            raise ValueError("Aucune donnee numerique dans l image")
        median = np.median(arr)
        biweight = biweight_location(arr)
        return float(median), float(biweight)
