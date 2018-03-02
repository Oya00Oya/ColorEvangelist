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
from models.standard import NetG

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("[%(levelname)s][%(asctime)s] - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


def denoise(img):
    return img# Image.fromarray(cv2.fastNlMeansDenoising(np.asarray(img), None, 10, 7, 21))).enhance(1.5)


web = socket.socket()
web.bind(('127.0.0.1', 1230))
web.listen(5)

desire_min = 512.0
args = sys.argv

netG = torch.nn.DataParallel(NetG(ngf=64))
netG.load_state_dict(torch.load('/home/orashi/magics/monitors/VANBCE2.1/netG_epoch_only.pth'))
netG.cuda().eval()
to_tensor, to_pil = transforms.ToTensor(), transforms.ToPILImage()
ts = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

ts2 = transforms.Compose([
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

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
            Variable((to_tensor(np.array(colormap.convert('RGB')))).cuda().unsqueeze(0)) * -1, 4, 4) * -1

        # retrieve down valid mask
        valid_mask = F.max_pool2d(Variable(
            (torch.FloatTensor(np.array(back)[:, :, 3].astype('float'))).gt(254).float().cuda().unsqueeze(0).unsqueeze(
                0)), 4, 4)

        sketch, colormap = Variable(ts(sketch)).unsqueeze(0).cuda(), Variable(ts2(colormap.squeeze().data).unsqueeze(0))

        h, w = colormap.shape[2] // 2, colormap.shape[3] // 2
        mask = Variable(
            torch.FloatTensor(([1, 0] * h + [0, 1] * h) * w).view(colormap.shape[2], colormap.shape[3]).cuda())
        mask = mask * valid_mask
        noise = torch.Tensor(1, 64, 1, 1).normal_(0, 1).cuda()

        hint = torch.cat((colormap * mask, mask), 1)

        with torch.no_grad():
            out = netG(sketch,
                       hint,
                       Variable(noise),
                       ).data
        to_pil(out.mul(0.5).add(0.5).squeeze().cpu()).resize(ori_size, Image.BICUBIC).save(msg["out"])

        sent = conn.send('Success\r\n'.encode('utf-8'))
        print("sent {}".format(sent))
        print("Success")
    except Exception as e:
        logger.exception(e)
    finally:
        conn.close()
        print("conn closed")
