import logging
import chainer
import chainer.functions as F
from chainer import Variable
from PIL import Image, ImageEnhance
import cv2
import sys
import os
import json
import numpy as np
import socket
import onnx
import caffe2.python.onnx.backend as backend

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

RMEAN = np.array([164.76139251, 167.47864617, 181.13838569])
desire_min = 512.0
args = sys.argv

model = onnx.load("../webapps/ROOT/func/models/VBD.proto")
netG = backend.prepare(model, device="CUDA:0")
netG.predict_net.type = 'prof_dag'
model = onnx.load("../webapps/ROOT/func/models/i2v.proto")
netI = backend.prepare(model, device="CUDA:0")
netI.predict_net.type = 'prof_dag'

to_pil = lambda x: Image.fromarray(((x.array.astype('float') / 2 + 0.5) * 255).transpose(1, 2, 0))
ts = lambda x: F.expand_dims(Variable((np.asarray(x).astype('float') / 255) * 2 - 1), 0)

ts2 = lambda x: x * 2 - 1

print("model loaded")
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
            F.expand_dims(
                Variable((np.array(colormap.convert('RGB')).astype('float') / 255) * 2 - 1).transpose(2, 0, 1), 0) * -1,
            4,
            4) * -1

        # retrieve down valid mask
        valid_mask = F.max_pooling_2d(
            F.expand_dims(F.expand_dims(Variable((np.array(back)[:, :, 3].astype('float') > 254).astype('float')), 0),
                          0), 4, 4)

        sketch, colormap = F.expand_dims(ts(sketch), 0), ts2(colormap)

        h, w = colormap.shape[2] // 2, colormap.shape[3] // 2
        mask = Variable(
            np.array(([1, 0] * h + [0, 1] * h) * w).reshape(colormap.shape[2], colormap.shape[3]).astype('float'))
        mask = F.expand_dims(F.expand_dims(mask, 0), 0) * valid_mask

        hint = F.concat((colormap * F.broadcast_to(mask, (1, 3, colormap.shape[2], colormap.shape[3])), mask), 1)

        ske_feat = netI.run(sketch.data.numpy())
        ske_feat = (F.average_pooling_2d(Variable(ske_feat), 2, 2) / 2 + 0.5) * 255
        ske_feat = (
            F.broadcast_to(ske_feat, (1, 3, ske_feat.shape[2], ske_feat.shape[3])).transpose(
                (0, 2, 3, 1)) - RMEAN).transpose((0, 3, 1, 2))
        out = Variable(netG.run([sketch.data.numpy(),
                                 hint.data.numpy(),
                                 netI.run(sketch.data.numpy())
                                 ]))

        to_pil(F.squeeze(out * 0.5 + 0.5)).resize(ori_size, Image.BICUBIC).save(msg["out"])

        sent = conn.send('Success\r\n'.encode('utf-8'))
        print("sent {}".format(sent))
        print("Success")
    except Exception as e:
        logger.exception(e)
    finally:
        conn.close()
        print("conn closed")
