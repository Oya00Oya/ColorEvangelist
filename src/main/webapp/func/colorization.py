import logging
import torch.utils.data
import torchvision.transforms as transforms
from torch.autograd import Variable
from PIL import Image
import cv2
import sys
import json
import numpy as np
import socket
from models.pro_model import def_netG

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("[%(levelname)s][%(asctime)s] - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)


def denoise(img):
    return Image.fromarray(cv2.fastNlMeansDenoising(np.asarray(img), None, 10, 7, 21))


web = socket.socket()
web.bind(('127.0.0.1', 1230))
web.listen(5)

desire_min = 512.0
args = sys.argv

netG = def_netG(ngf=64)
netG.load_state_dict(torch.load('../webapps/ROOT/func/netG_epoch_only_CP5.5_0.00001.pth'))
netG.cuda().eval()
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

        desire_size, ori_size = (int(desire_min / min(sketch.size) * sketch.size[0]),
                                 int(desire_min / min(sketch.size) * sketch.size[1])), sketch.size
        sketch, back = sketch.resize(desire_size, Image.BICUBIC), back.resize(desire_size, Image.BICUBIC)

        colormap = Image.new('RGBA', desire_size, (255, 255, 255))

        target_size = (sketch.size[0] // 16 * 16, sketch.size[1] // 16 * 16)  # make fully convolutional
        valid_mask = (torch.FloatTensor(
            np.array(back.resize((target_size[0] // 4, target_size[1] // 4), Image.NEAREST))[:, :, 3].astype(
                'float'))).gt(
            254).float().cuda().unsqueeze(0).unsqueeze(0)

        colormap.paste(back, (0, 0, desire_size[0], desire_size[1]), back)
        colormap = colormap.convert('RGB')

        ts = transforms.Compose([
            transforms.Scale((target_size[1], target_size[0]), Image.BICUBIC),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

        ts2 = transforms.Compose([
            transforms.Scale((target_size[1] // 4, target_size[0] // 4), Image.NEAREST),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

        sketch, colormap = ts(sketch), ts2(colormap)
        sketch, colormap = sketch.unsqueeze(0).cuda(), colormap.unsqueeze(0).cuda()

        # mask = torch.rand(1, 1, colormap.shape[2], colormap.shape[3]).ge(0.85).float().cuda()
        h, w = colormap.shape[2] // 2, colormap.shape[3] // 2
        mask = torch.FloatTensor(([1, 0] * h + [0, 1] * h) * w).view(colormap.shape[2], colormap.shape[3]).cuda()
        mask = mask * valid_mask

        hint = torch.cat((colormap * mask, mask), 1)

        out = netG(Variable(sketch, volatile=True), Variable(hint, volatile=True)).data
        transforms.ToPILImage()(out.mul(0.5).add(0.5).squeeze().cpu()).resize(ori_size, Image.BICUBIC).save(msg["out"])

        sent = conn.send('Success\r\n'.encode('utf-8'))
        print("sent {}".format(sent))
        print("Success")
    except Exception as e:
        logger.exception(e)
    finally:
        conn.close()
        print("conn closed")
