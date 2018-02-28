import logging
import chainer
import chainer.functions as F
from chainer import Variable
import chainercv
from PIL import Image, ImageEnhance
import cv2
import sys
import os
import json
import numpy as np
import socket
from models.model import NetG

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("[%(levelname)s][%(asctime)s] - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


def denoise(img):
    return ImageEnhance.Contrast(img).enhance(
        1.0)  # Image.fromarray(cv2.fastNlMeansDenoising(np.asarray(img), None, 10, 7, 21))).enhance(1.5)


web = socket.socket()
web.bind(('127.0.0.1', 1230))
web.listen(5)

desire_min = 512.0
args = sys.argv

netG = NetG(ngf=64)
to_pil = lambda x: Image.fromarray(((x.array / 2 + 0.5) * 255).transpose(1, 2, 0))
ts = lambda x: F.expand_dims(Variable((np.asarray(x).astype('float') / 255) * 2 - 1), 0)

ts2 = lambda x: x * 2 - 1

print("model loaded")
chainercv.transforms.resize
while True:
    try:
        conn, addr = web.accept()
        data = conn.recv(1024)
        print("data received")
        print(data)
        if data == -1:
            continue
        msg = json.loads(data)
        sketch = denoise(Image.open(msg["sketch"]).convert('L'))
        back = Image.open(msg["hint"]).convert('RGBA')

        # desire fully convolutional
        desire_size, ori_size = (int(desire_min / min(sketch.size) * sketch.size[0]) // 16 * 16,
                                 int(desire_min / min(sketch.size) * sketch.size[1]) // 16 * 16), sketch.size
        sketch, back = sketch.resize(desire_size, Image.BICUBIC), back.resize(desire_size, Image.BICUBIC)

        # retrieve down color map
        colormap = Image.new('RGBA', desire_size, (255, 255, 255))
        colormap.paste(back, (0, 0, desire_size[0], desire_size[1]), back)
        colormap = F.max_pooling_2d(
            F.expand_dims(Variable(np.array(colormap.convert('RGB')).astype('float')).transpose(2, 0, 1), 0) * -1, 4,
            4) * -1

        # retrieve down valid mask
        valid_mask = F.max_pooling_2d(
            F.expand_dims(F.expand_dims(Variable((np.array(back)[:, :, 3].astype('float') > 254).astype('float')), 0),
                          0),
            4, 4)

        sketch, colormap = F.expand_dims(ts(sketch), 0), ts2(colormap)

        h, w = colormap.shape[2] // 2, colormap.shape[3] // 2
        mask = Variable(
            np.array(([1, 0] * h + [0, 1] * h) * w).reshape(colormap.shape[2], colormap.shape[3]).astype('float'))
        mask = F.expand_dims(F.expand_dims(mask, 0), 0) * valid_mask

        hint = F.concat((colormap * F.broadcast_to(mask, (1, 3, colormap.shape[2], colormap.shape[3])), mask), 1)

        with chainer.using_config('train', False):
            out = netG(F.cast(sketch, np.float32),
                       F.cast(hint, np.float32),
                       )
        to_pil(F.squeeze(out * 0.5 + 0.5)).resize(ori_size, Image.BICUBIC).save(msg["out"])

        sent = conn.send('Success\r\n'.encode('utf-8'))
        print("sent {}".format(sent))
        print("Success")
    except Exception as e:
        logger.exception(e)
    finally:
        conn.close()
        print("conn closed")
