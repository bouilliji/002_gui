import time
import numpy as np

from photutils.datasets import make_100gaussians_image
data = make_100gaussians_image()

import matplotlib.pyplot as plt
from astropy.visualization import simple_norm
norm = simple_norm(data, 'sqrt', percent=99.5)
fig, axs = plt.subplots(3,4)
axs[0, 0].imshow(data, norm=norm, origin='lower')

from astropy.stats import sigma_clipped_stats, SigmaClip
from photutils.segmentation import detect_threshold, detect_sources
from photutils.utils import circular_footprint
sigma_clip = SigmaClip(sigma=3.0, maxiters=10)
threshold = detect_threshold(data, n_sigma=2.0, sigma_clip=sigma_clip)

norm = simple_norm(threshold, 'sqrt', percent=99.5)
axs[0, 1].imshow(threshold, norm=norm, origin='lower')

segment_img = detect_sources(data, threshold, n_pixels=10)

norm = simple_norm(segment_img, 'sqrt', percent=99.5)
axs[0, 2].imshow(segment_img, norm=norm, origin='lower')

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


norm = simple_norm(img_masked, 'sqrt', percent=99.5)
axs[1, 0].imshow(img_masked, norm=norm, origin='lower')

mean, median, std = sigma_clipped_stats(data, sigma=3.0, mask=mask)
print(np.array((mean, median, std)))

ny, nx = data.shape
y, x = np.mgrid[:ny, :nx]
gradient = x * y / 5000.0
data2 = data + gradient

norm = simple_norm(data2, 'sqrt', percent=99.5)
axs[1,1].imshow(data2, norm=norm, origin='lower')

from astropy.stats import SigmaClip
from photutils.background import Background2D, MedianBackground
sigma_clip = SigmaClip(sigma=3.0)
bkg_estimator = MedianBackground()
bkg = Background2D(data2, (15, 15), filter_size=(3, 3), sigma_clip=sigma_clip, bkg_estimator=bkg_estimator)

norm = simple_norm(bkg.background, 'sqrt', percent=99.5)
axs[1,2].imshow(bkg.background, origin='lower')

data2_sub = data2 - bkg.background

norm = simple_norm(data2_sub, 'sqrt', percent=99.5)
axs[2, 0].imshow(data2_sub, norm=norm, origin='lower')


from astropy.stats import sigma_clipped_stats
from photutils.datasets import load_simulated_hst_star_image, make_noise_image

hdu = load_simulated_hst_star_image()
data = hdu.data + make_noise_image(hdu.data.shape, distribution='gaussian', mean=10.0, stddev=5.0, seed=0)
mean, median, std = sigma_clipped_stats(data, sigma=3.0)
print(np.array((mean, median, std)))

norm = simple_norm(data, 'sqrt', percent=99.5)
axs[2, 1].imshow(data, norm=norm, origin='lower')

from photutils.detection import DAOStarFinder
threshold = 5.0 * std
daofind = DAOStarFinder(threshold, fwhm=2.5, sharpness_range=(0.2, 1.5))

sources = daofind(data - median)
for col in sources.colnames:
    if col not in ('id', 'n_pixels'):
        sources[col].info.format = '%.2f'
sources.pprint(max_lines=12, max_width=76)

norm = simple_norm(data, 'sqrt', percent=99.5)
axs[2, 2].imshow(data, norm=norm, origin='lower')

from matplotlib.patches import Circle

for i in range(len(sources['x_centroid'])):
    circ = Circle((sources['x_centroid'][i], sources['y_centroid'][i]), radius=10, edgecolor="red", facecolor="none", linewidth=1.5)
    axs[2,2].add_patch(circ)
    
from photutils.centroids import centroid_sources, centroid_2dg
    
x, y = centroid_sources(data, sources['x_centroid'], sources['y_centroid'], box_size=25, centroid_func=centroid_2dg)

norm = simple_norm(data, 'sqrt', percent=99.5)
axs[0, 3].imshow(data, norm=norm, origin='lower')

for i in range(len(x)):
    circ = Circle((x[i], y[i]), radius=10, edgecolor="blue", facecolor="none", linewidth=1.5)
    axs[0,3].add_patch(circ)

norm = simple_norm(data, 'sqrt', percent=99.5)
axs[1, 3].imshow(data, norm=norm, origin='lower')

for i in range(len(x)):
    axs[1, 3].plot([x[i] - 5, x[i] + 5], [y[i] - 5, y[i] + 5], color="blue", linewidth=1.5)
    
    axs[1, 3].plot([sources['x_centroid'][i] - 5, sources['x_centroid'][i] + 5], [sources['y_centroid'][i] - 5, sources['y_centroid'][i] + 5], color="red", linewidth=1.5)
    axs[1, 3].plot([sources['x_centroid'][i] - 5, sources['x_centroid'][i] + 5], [sources['y_centroid'][i] + 5, sources['y_centroid'][i] - 5], color="red", linewidth=1.5)
    
    axs[1, 3].plot([x[i] - 5, x[i] + 5], [y[i] + 5, y[i] - 5], color="blue", linewidth=1.5)


plt.show()