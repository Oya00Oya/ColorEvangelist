import torch.utils.data
import torchvision.transforms as transforms
from torch.autograd import Variable
from PIL import Image
import sys
from models.CascaderNextLite import Pyramid

args = sys.argv

netG = Pyramid()
netG.load_state_dict(torch.load('../webapps/ROOT/func/netG_deblur.pth'))
netG.cuda().eval()

Trans = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

blurry = Trans(Image.open(args[1]).convert('RGB')).unsqueeze(0).cuda()

out = netG(Variable(blurry, volatile=True)).data
transforms.ToPILImage()(out.mul(0.5).add(0.5).squeeze().clamp(0, 1).cpu()).save(args[2])
print('Success')
