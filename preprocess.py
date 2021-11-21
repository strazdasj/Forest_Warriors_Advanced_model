from scipy.ndimage.filters import uniform_filter
from scipy.ndimage.measurements import variance
import numpy as np
import tifffile
from matplotlib import pyplot as plt

def lee_filter(img):
    size = 224
    sizex = 221
    sizey = 222
    
    img_mean = uniform_filter(img, (sizex, sizey))
    img_sqr_mean = uniform_filter(img**2, (sizex, sizey))
    img_variance = img_sqr_mean - img_mean**2

    overall_variance = variance(img)

    img_weights = img_variance / (img_variance + 0.25)
    img_output = img_mean + img_weights * (img - img_mean)
    return img_output



#how to use
im = tifffile.imread('Sentinel1_img_before.tif')
f, axarr = plt.subplots(2)
imarray = np.array(im)
before = imarray
print(np.shape(imarray))
col_mean = np.nanmean(imarray, axis=0)
inds = np.where(np.isnan(imarray))
imarray[inds] = np.take(col_mean, inds[1])
after = lee_filter(imarray)
axarr[0].imshow(before)
axarr[1].imshow(after)
plt.show()




