import time
import numpy as np

from astropy.io import fits

with fits.open(r'./src/image/IM_20250912_192447_1818_Brahms_Rp_CDL.fits.gz', memmap=False) as hdul:
    data = np.array(hdul[0].data, dtype=float)

import matplotlib.pyplot as plt
from astropy.visualization import simple_norm

fig, axs = plt.subplots()

from astropy.stats import sigma_clipped_stats, SigmaClip
from photutils.segmentation import detect_threshold, detect_sources
from photutils.utils import circular_footprint
sigma_clip = SigmaClip(sigma=100.0, maxiters=10)
threshold = detect_threshold(data, n_sigma=2.0, sigma_clip=sigma_clip)

segment_img = detect_sources(data, threshold, n_pixels=10)

footprint = circular_footprint(radius=5)
mask = segment_img.make_source_mask(footprint=footprint)

img_masked = []
for y in range(len(data)):
    temp = []
    for x in range(len(data[y])):
        if mask[y][x]:
            temp.append(data[y][x])
        else:
            temp.append(0)

    img_masked.append(temp)

mean, median, std = sigma_clipped_stats(data, sigma=100.0, mask=mask)
print(np.array((mean, median, std)))

from astropy.stats import SigmaClip
from photutils.background import Background2D, MedianBackground

sigma_clip = SigmaClip(sigma=100.0)
bkg_estimator = MedianBackground()
bkg = Background2D(data, (15, 15), filter_size=(3, 3), sigma_clip=sigma_clip, bkg_estimator=bkg_estimator)

data2_sub = data - bkg.background

data = data2_sub

mean, median, std = sigma_clipped_stats(data, sigma=100.0)
print(np.array((mean, median, std)))



#######################################################################################################################
#########################################CENTROID######################################################################
#######################################################################################################################

from photutils.detection import DAOStarFinder

threshold = 5.0 * std
daofind = DAOStarFinder(threshold, fwhm=2.5, sharpness_range=(0.2, 1.5))

sources = daofind(data - median)
for col in sources.colnames:
    if col not in ('id', 'n_pixels'):
        sources[col].info.format = '%.2f'
sources.pprint(max_lines=12, max_width=76)

from photutils.centroids import centroid_sources, centroid_2dg
    
x, y = centroid_sources(data, sources['x_centroid'], sources['y_centroid'], box_size=25, centroid_func=centroid_2dg)

norm = simple_norm(data, 'sqrt', percent=99.5)
axs.imshow(data, norm=norm, origin='lower')

for i in range(len(x)):
    axs.plot([x[i] - 5, x[i] + 5], [y[i] - 5, y[i] + 5], color="blue", linewidth=1.5)
    
    axs.plot([sources['x_centroid'][i] - 5, sources['x_centroid'][i] + 5], [sources['y_centroid'][i] - 5, sources['y_centroid'][i] + 5], color="red", linewidth=1.5)
    axs.plot([sources['x_centroid'][i] - 5, sources['x_centroid'][i] + 5], [sources['y_centroid'][i] + 5, sources['y_centroid'][i] - 5], color="red", linewidth=1.5)
    
    axs.plot([x[i] - 5, x[i] + 5], [y[i] + 5, y[i] - 5], color="blue", linewidth=1.5)


plt.show()