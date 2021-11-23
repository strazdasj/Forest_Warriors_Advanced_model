from scipy.ndimage.filters import uniform_filter
from scipy.ndimage.measurements import variance
import numpy as np
import tifffile
from matplotlib import pyplot as plt
import os
from tqdm import tqdm

#lee filter on a single image
def lee_filter(img):
    size = 224
    img_mean = uniform_filter(img, (size, size))
    img_sqr_mean = uniform_filter(img**2, (size, size))
    img_variance = img_sqr_mean - img_mean**2

    overall_variance = variance(img)

    img_weights = img_variance / (img_variance + 0.25)
    img_output = img_mean + img_weights * (img - img_mean)
    return img_output


#lee filter on a directory:
# src should be the path to the source directory containing the sar images
# out should be the path to where you want to store the despeckled images
def lee_filter_on_dir(src, out):

    if not os.path.exists(out):
            os.makedirs(out)

    for filename in tqdm(os.listdir(src)):
        srctemp = src + "/" + filename
        im = tifffile.imread(srctemp)
        if("target" in filename):
            tifffile.imsave(out + "/" + filename, im)
        else:
            im = tifffile.imread(srctemp)
            im = np.array(im)
            col_mean = np.nanmean(im, axis=0)
            inds = np.where(np.isnan(im))
            im[inds] = np.take(col_mean, inds[1])  
            im = lee_filter(im)
            tifffile.imsave(out + "/" + filename, im)



lee_filter_on_dir('C://Users/justa/Downloads/SAR_Input_mapbiomas-20211123T125601Z-001/SAR_Input_mapbiomas', 'C://Users/justa/Downloads/SAR_Input_mapbiomas-20211123T125601Z-001/Despeckled_SAR_Input_mapbiomas')
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



