import torch.utils.data
import torchvision.transforms as transforms
from torch.autograd import Variable
from PIL import Image
import sys
import numpy as np
from models.naive_model import def_netG

desire_min = 512.0
args = sys.argv

netG = def_netG(ngf=64)
netG.load_state_dict(torch.load('../webapps/ROOT/func/netG_epoch_only512_0.005_0.00001.pth'))
netG.cuda().eval()

sketch = Image.open(args[2]).convert('L')
back = Image.open(args[1]).convert('RGBA')

desire_size, ori_size = (int(desire_min / min(sketch.size) * sketch.size[0]),
                         int(desire_min / min(sketch.size) * sketch.size[1])), sketch.size
sketch, back = sketch.resize(desire_size, Image.BICUBIC), back.resize(desire_size, Image.BICUBIC)

colormap = Image.new('RGBA', desire_size, (255, 255, 255))

target_size = (sketch.size[0] // 16 * 16, sketch.size[1] // 16 * 16)  # TODO: test the influence of this part
valid_mask = (torch.FloatTensor(
    np.array(back.resize((target_size[0] // 4, target_size[1] // 4), Image.NEAREST))[:, :, 3].astype('float'))).gt(
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

mask = torch.rand(1, 1, colormap.shape[2], colormap.shape[3]).ge(0.2).float().cuda()
mask = mask * valid_mask

hint = torch.cat((colormap * mask, mask), 1)

out = netG(Variable(sketch, volatile=True), Variable(hint, volatile=True)).data
transforms.ToPILImage()(out.mul(0.5).add(0.5).squeeze().cpu()).resize(ori_size, Image.BICUBIC).save(args[3])
print('Success')
