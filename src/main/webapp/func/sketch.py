import torch.utils.data as data
import torch
import cv2
import lime
import numpy as np
import os
import os.path
import sys

IMG_EXTENSIONS = [
    '.jpg', '.JPG', '.jpeg', '.JPEG',
    '.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP',
]


args = sys.argv

def demoDoG(img, sig=0.55, tau=0.975, phi=10000):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    xdog_params = {
        'kappa': 4.5, 'sigma': sig, 'tau': tau, 'phi': phi,
        'edgeType': lime.NPR_EDGE_XDOG
    }
    xdog = lime.edgeDoG(gray, xdog_params)
    return xdog


def is_image_file(filename):
    return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)


def default_loader(path):  # fixed
    return cv2.imread(path, cv2.IMREAD_COLOR)


img = cv2.imread(args[1], cv2.IMREAD_COLOR)
img = demoDoG((img / 255.0).astype(np.float32), sig=0.5) * 255.0
cv2.imwrite('../webapps/ROOT/output_sketch/'+args[2]+'_out.png', img)
print('Success')
