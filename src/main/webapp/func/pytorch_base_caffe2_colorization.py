import logging
import torch.utils.data
import torch.nn as nn
import torchvision.transforms as transforms
from torch.autograd import Variable
import torch.nn.functional as F
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

desire_min = 512.0
args = sys.argv

model = onnx.load("../webapps/ROOT/func/VBD.proto")
netG = backend.prepare(model, device="CUDA:0")
netG.predict_net.type = 'prof_dag'
model = onnx.load("../webapps/ROOT/func/i2v.proto")
netI = backend.prepare(model, device="CUDA:0")
netI.predict_net.type = 'prof_dag'

to_tensor, to_pil = transforms.ToTensor(), transforms.ToPILImage()
ts = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

ts2 = transforms.Compose([
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

rmean = Variable(torch.FloatTensor([164.76139251, 167.47864617, 181.13838569]).view(1, 3, 1, 1))

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
        colormap = F.max_pool2d(
            Variable((to_tensor(np.array(colormap.convert('RGB')))).unsqueeze(0)) * -1, 4, 4) * -1

        # retrieve down valid mask
        valid_mask = F.max_pool2d(Variable(
            (torch.FloatTensor(np.array(back)[:, :, 3].astype('float'))).gt(254).float().unsqueeze(0).unsqueeze(
                0)), 4, 4)

        sketch, colormap = Variable(ts(sketch)).unsqueeze(0), Variable(ts2(colormap.squeeze().data).unsqueeze(0))

        h, w = colormap.shape[2] // 2, colormap.shape[3] // 2
        mask = Variable(
            torch.FloatTensor(([1, 0] * h + [0, 1] * h) * w).view(colormap.shape[2], colormap.shape[3]))
        mask = mask * valid_mask
        noise = torch.Tensor(1, 64, 1, 1).normal_(0, 1)

        hint = torch.cat((colormap * mask, mask), 1)

        ske_feat = netI.run(sketch.data.numpy())
        ske_feat = F.avg_pool2d(Variable(torch.FloatTensor(ske_feat)), 2, 2).mul(0.5).add(0.5).mul(255) - rmean
        out = torch.FloatTensor(netG.run([sketch.data.numpy(),
                                          hint.data.numpy(),
                                          netI.run(sketch.data.numpy())
                                          ]))

        to_pil(out.mul(0.5).add(0.5).squeeze()).resize(ori_size, Image.BICUBIC).save(msg["out"])

        sent = conn.send('Success\r\n'.encode('utf-8'))
        print("sent {}".format(sent))
        print("Success")
    except Exception as e:
        logger.exception(e)
    finally:
        conn.close()
        print("conn closed")
