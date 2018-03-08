import torch.utils.data as data
import torch
import cv2
import lime
import numpy as np
import os
import os.path
import sys
from PIL import Image

IMG_EXTENSIONS = [
    '.jpg', '.JPG', '.jpeg', '.JPEG',
    '.png', '.PNG', '.ppm', '.PPM', '.bmp', '.BMP',
]

args = sys.argv

def small_component_removal(img):
    """
    remove small chokes
    :param imgs: 1 channel opencv np array 0-255
    :return: 1 channel opencv np array 0-255
    """
    thresh = 127
    im_bw = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]
    im_bw = im_bw * -1 + 255
    # find connected black components
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(im_bw.astype(np.uint8), connectivity=8)

    sizes = stats[1:, -1]
    nb_components = nb_components - 1

    min_size = 10

    # answer image
    img2 = np.zeros(output.shape)
    for i in range(0, nb_components):
        if sizes[i] >= min_size:
            img2[output == i + 1] = 255
    return img2.astype(np.float32) * -1 + 255


def XDoG_S(img, sig):
    gray = np.array(img.convert('L')) / 255
    xdog_params = {
        'kappa': 1.0001, 'sigma': sig, 'tau': 0.999997, 'phi': 1e20,
        'edgeType': lime.NPR_EDGE_XDOG
    }
    edge = small_component_removal(lime.edgeDoG(gray.astype(np.float32), xdog_params) * 255)
    return Image.fromarray(edge, mode='I').convert('RGB')


def resize_by(img, side_min):
    return img.resize((int(img.size[0] / min(img.size) * side_min), int(img.size[1] / min(img.size) * side_min)),
                      Image.BICUBIC)


def is_image_file(filename):
    return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)


def default_loader(path):  # fixed
    return Image.open(path).convert('RGB')


image = default_loader(args[1])
image = resize_by(image, 750)
edge = XDoG_S(image, sig=0.7)
edge.save(args[2])
print('Success')
